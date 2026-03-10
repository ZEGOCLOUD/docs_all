#!/usr/bin/env python3
"""
进度报告管理脚本

功能：
1. 创建进度报告文件
2. 更新文件翻译状态
3. 更新批次进度
4. 添加跳过的文件
5. 添加失败的文件
6. 读取和恢复进度
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional


PROGRESS_FILE_NAME = '.translation-progress.json'


def create_batches_from_files(files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    从文件列表自动创建批次

    批次策略（与 scan_batch_translation.py 保持一致）：
    - 小文件（< 50 行）：每批 10-20 个文件，总行数控制在 1000 行以内
    - 中等文件（50-300 行）：每批 2-5 个文件，总行数控制在 1500 行以内
    - 大文件（> 300 行）：单独成批

    Args:
        files: 文件信息列表，每个文件包含 line_count 等字段

    Returns:
        list: 批次列表
    """
    # 按文件大小分类
    small_files = [f for f in files if f.get('line_count', 0) < 50]
    medium_files = [f for f in files if 50 <= f.get('line_count', 0) <= 300]
    large_files = [f for f in files if f.get('line_count', 0) > 300]

    batches = []
    batch_number = 1

    # 处理小文件
    if small_files:
        current_batch = {
            'batch_number': batch_number,
            'files': [],
            'total_lines': 0,
            'file_count': 0
        }

        for file_info in small_files:
            # 为每个文件添加必需的字段
            file_entry = {
                'path': file_info.get('source', file_info.get('target', '')),
                'target_path': file_info.get('target', ''),
                'relative_path': file_info.get('relative_path', ''),
                'line_count': file_info.get('line_count', 0)
            }

            if current_batch['file_count'] >= 20 or current_batch['total_lines'] + file_info.get('line_count', 0) > 1000:
                batches.append(current_batch)
                batch_number += 1
                current_batch = {
                    'batch_number': batch_number,
                    'files': [],
                    'total_lines': 0,
                    'file_count': 0
                }

            current_batch['files'].append(file_entry)
            current_batch['total_lines'] += file_info.get('line_count', 0)
            current_batch['file_count'] += 1

        if current_batch['files']:
            batches.append(current_batch)
            batch_number += 1

    # 处理中等文件
    if medium_files:
        i = 0
        while i < len(medium_files):
            file_info = medium_files[i]
            file_entry = {
                'path': file_info.get('source', file_info.get('target', '')),
                'target_path': file_info.get('target', ''),
                'relative_path': file_info.get('relative_path', ''),
                'line_count': file_info.get('line_count', 0)
            }

            batch = {
                'batch_number': batch_number,
                'files': [file_entry],
                'total_lines': file_info.get('line_count', 0),
                'file_count': 1
            }

            # 尝试添加更多文件
            i += 1
            while i < len(medium_files):
                other_file = medium_files[i]
                if batch['file_count'] >= 5 or batch['total_lines'] + other_file.get('line_count', 0) > 1500:
                    break

                other_entry = {
                    'path': other_file.get('source', other_file.get('target', '')),
                    'target_path': other_file.get('target', ''),
                    'relative_path': other_file.get('relative_path', ''),
                    'line_count': other_file.get('line_count', 0)
                }

                batch['files'].append(other_entry)
                batch['total_lines'] += other_file.get('line_count', 0)
                batch['file_count'] += 1
                i += 1

            batches.append(batch)
            batch_number += 1

    # 处理大文件
    for file_info in large_files:
        file_entry = {
            'path': file_info.get('source', file_info.get('target', '')),
            'target_path': file_info.get('target', ''),
            'relative_path': file_info.get('relative_path', ''),
            'line_count': file_info.get('line_count', 0)
        }

        batches.append({
            'batch_number': batch_number,
            'files': [file_entry],
            'total_lines': file_info.get('line_count', 0),
            'file_count': 1,
            'needs_segmentation': file_info.get('line_count', 0) > 2000
        })
        batch_number += 1

    return batches


def create_progress(
    target_directory: str,
    source_directory: str,
    scan_result: Dict[str, Any],
    preprocess_result: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    创建进度报告文件

    Args:
        target_directory: 目标目录路径
        source_directory: 源目录路径
        scan_result: 扫描结果
        preprocess_result: 预处理结果（可选）

    Returns:
        dict: 进度报告对象
    """
    now = datetime.utcnow().isoformat() + 'Z'

    # 提取批次信息，如果不存在则自动生成
    batches = scan_result.get('batches', [])
    if not batches and 'files' in scan_result:
        # 如果 scan_result 中没有 batches，自动从 files 生成
        print("⚠️  scan_result.json 中没有批次信息，正在自动生成批次...")
        batches = create_batches_from_files(scan_result['files'])
        print(f"✅ 已生成 {len(batches)} 个批次")

    # 构建跳过的文件列表
    skipped_files = []

    # 1. API 文档
    for file_info in scan_result.get('files', []):
        if file_info.get('has_doctype_api', False):
            skipped_files.append({
                'path': file_info['path'],
                'relative_path': file_info.get('relative_path', ''),
                'reason': 'docType: API',
                'reason_code': 'api_doc',
                'line_count': file_info['line_count']
            })

    # 2. YAML 生成的 MDX
    # 从扫描结果中提取 YAML+MDX 对的信息
    yaml_pairs = scan_result.get('yaml_pairs', {})
    if yaml_pairs:
        for mdx_file in yaml_pairs.get('mdx_files', []):
            skipped_files.append({
                'path': mdx_file['path'],
                'relative_path': mdx_file.get('relative_path', ''),
                'reason': 'YAML generated MDX',
                'reason_code': 'yaml_generated',
                'line_count': mdx_file['line_count']
            })

    # 3. 全复用文档（已解决的）
    if preprocess_result:
        for result in preprocess_result:
            if result['status'] == 'resolved':
                skipped_files.append({
                    'path': result['source'],
                    'relative_path': result.get('relative_path', ''),
                    'reason': 'Reuse doc resolved',
                    'reason_code': 'reuse_doc_resolved',
                    'line_count': result.get('line_count', 0),
                    'resolved_to': result.get('resolved_to')
                })

    # 4. 全复用文档（跳过的，因为没有对应的英文文档）
    if preprocess_result:
        for result in preprocess_result:
            if result['status'] == 'need_translate':
                # 这些不是跳过，而是需要翻译的全复用文档
                pass

    # 构建批次详情
    batch_details = []
    for batch in batches:
        batch_info = {
            'batch_number': batch['batch_number'],
            'status': 'pending',
            'file_count': batch['file_count'],
            'lines': batch['total_lines'],
            'files': []
        }

        for file_info in batch['files']:
            batch_info['files'].append({
                'source': file_info['path'],
                'target': file_info.get('target_path', file_info['path'].replace('/zh/', '/en/')),
                'relative_path': file_info.get('relative_path', ''),
                'lines': file_info['line_count'],
                'status': 'pending'
            })

        batch_details.append(batch_info)

    # 计算总行数（如果 summary 中没有 total_lines）
    total_lines = scan_result['summary'].get('total_lines')
    if total_lines is None:
        total_lines = sum(f.get('line_count', 0) for f in scan_result.get('files', []))

    # 构建完整进度报告
    progress = {
        'directory': source_directory,
        'target_directory': target_directory,
        'started_at': now,
        'last_updated': now,
        'total_batches': len(batches),
        'completed_batches': 0,
        'total_files': scan_result['summary']['total_files'],
        'translated_files': 0,
        'total_lines': total_lines,
        'translated_lines': 0,
        'current_batch': 1,
        'status': 'in_progress',
        'scan_summary': scan_result['summary'],
        'completed_files': [],
        'skipped_files': skipped_files,
        'failed_files': [],
        'batches': batch_details
    }

    # 保存进度文件
    save_progress(target_directory, progress)

    return progress


def save_progress(target_directory: str, progress: Dict[str, Any]):
    """
    保存进度文件到目标目录

    Args:
        target_directory: 目标目录
        progress: 进度报告对象
    """
    progress_file_path = Path(target_directory) / PROGRESS_FILE_NAME

    with open(progress_file_path, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

    print(f"✅ 进度文件已保存：{progress_file_path}")


def load_progress(target_directory: str) -> Optional[Dict[str, Any]]:
    """
    从目标目录加载进度文件

    Args:
        target_directory: 目标目录

    Returns:
        dict: 进度报告对象，如果文件不存在则返回 None
    """
    progress_file_path = Path(target_directory) / PROGRESS_FILE_NAME

    if not progress_file_path.exists():
        return None

    try:
        with open(progress_file_path, 'r', encoding='utf-8') as f:
            progress = json.load(f)
        return progress
    except Exception as e:
        print(f"❌ 错误：无法加载进度文件：{e}", file=sys.stderr)
        return None


def update_file_completed(
    target_directory: str,
    source_path: str,
    target_path: str,
    batch_number: int
) -> Dict[str, Any]:
    """
    标记文件翻译完成

    Args:
        target_directory: 目标目录
        source_path: 源文件路径
        target_path: 目标文件路径
        batch_number: 批次号

    Returns:
        dict: 更新后的进度报告
    """
    progress = load_progress(target_directory)
    if not progress:
        raise ValueError(f"进度文件不存在：{target_directory}")

    now = datetime.utcnow().isoformat() + 'Z'

    # 查找文件并更新状态
    file_found = False
    for batch in progress['batches']:
        if batch['batch_number'] == batch_number:
            for file_info in batch['files']:
                if file_info['source'] == source_path:
                    file_info['status'] = 'completed'
                    file_info['completed_at'] = now
                    file_found = True
                    break

    if not file_found:
        print(f"⚠️  警告：未找到文件 {source_path}，可能已在之前完成", file=sys.stderr)
        return progress

    # 添加到已完成文件列表
    completed_file = {
        'source': source_path,
        'target': target_path,
        'batch': batch_number,
        'completed_at': now
    }

    # 检查是否已在列表中
    already_exists = any(f['source'] == source_path for f in progress['completed_files'])
    if not already_exists:
        progress['completed_files'].append(completed_file)
        progress['translated_files'] += 1

        # 更新已翻译行数
        file_lines = 0
        for batch in progress['batches']:
            if batch['batch_number'] == batch_number:
                for file_info in batch['files']:
                    if file_info['source'] == source_path:
                        file_lines = file_info['lines']
                        break
                break

        progress['translated_lines'] += file_lines

    # 更新时间戳
    progress['last_updated'] = now

    # 保存
    save_progress(target_directory, progress)

    return progress


def update_batch_completed(target_directory: str, batch_number: int) -> Dict[str, Any]:
    """
    标记批次翻译完成

    Args:
        target_directory: 目标目录
        batch_number: 批次号

    Returns:
        dict: 更新后的进度报告
    """
    progress = load_progress(target_directory)
    if not progress:
        raise ValueError(f"进度文件不存在：{target_directory}")

    now = datetime.utcnow().isoformat() + 'Z'

    # 查找批次并更新状态
    batch_found = False
    for batch in progress['batches']:
        if batch['batch_number'] == batch_number:
            batch['status'] = 'completed'
            batch['completed_at'] = now
            batch_found = True

            # 如果没有设置开始时间，设置开始时间
            if 'started_at' not in batch:
                batch['started_at'] = now

            break

    if not batch_found:
        print(f"⚠️  警告：未找到批次 {batch_number}", file=sys.stderr)
        return progress

    # 更新已完成批次数量
    if batch_number == progress['current_batch']:
        progress['completed_batches'] += 1
        progress['current_batch'] = batch_number + 1

    # 更新时间戳
    progress['last_updated'] = now

    # 检查是否全部完成
    if progress['completed_batches'] >= progress['total_batches']:
        progress['status'] = 'completed'
        print(f"\n🎉 所有批次翻译完成！")

    # 保存
    save_progress(target_directory, progress)

    return progress


def add_failed_file(
    target_directory: str,
    source_path: str,
    error_message: str,
    batch_number: int
) -> Dict[str, Any]:
    """
    添加失败的文件

    Args:
        target_directory: 目标目录
        source_path: 源文件路径
        error_message: 错误信息
        batch_number: 批次号

    Returns:
        dict: 更新后的进度报告
    """
    progress = load_progress(target_directory)
    if not progress:
        raise ValueError(f"进度文件不存在：{target_directory}")

    now = datetime.utcnow().isoformat() + 'Z'

    # 添加到失败文件列表
    failed_file = {
        'source': source_path,
        'batch': batch_number,
        'error': error_message,
        'failed_at': now
    }

    progress['failed_files'].append(failed_file)

    # 更新时间戳
    progress['last_updated'] = now

    # 保存
    save_progress(target_directory, progress)

    return progress


def print_progress_summary(progress: Dict[str, Any]):
    """
    打印进度摘要

    Args:
        progress: 进度报告对象
    """
    print("\n" + "="*70)
    print("📊 翻译进度摘要")
    print("="*70)

    print(f"\n源目录：{progress['directory']}")
    print(f"目标目录：{progress['target_directory']}")
    print(f"状态：{progress['status']}")
    print(f"开始时间：{progress['started_at']}")
    print(f"最后更新：{progress['last_updated']}")

    print(f"\n批次进度：{progress['completed_batches']}/{progress['total_batches']}")
    print(f"文件进度：{progress['translated_files']}/{progress['total_files']}")
    print(f"行数进度：{progress['translated_lines']}/{progress['total_lines']}")
    print(f"当前批次：{progress['current_batch']}")

    # 跳过的文件
    if progress['skipped_files']:
        print(f"\n⏭️  跳过的文件：{len(progress['skipped_files'])} 个")
        for reason in ['api_doc', 'yaml_generated', 'reuse_doc_resolved']:
            files_by_reason = [f for f in progress['skipped_files'] if f.get('reason_code') == reason]
            if files_by_reason:
                reason_text = {
                    'api_doc': 'API 文档',
                    'yaml_generated': 'YAML 生成',
                    'reuse_doc_resolved': '全复用文档已解决'
                }.get(reason, reason)
                lines = sum(f.get('line_count', 0) for f in files_by_reason)
                print(f"   - {reason_text}：{len(files_by_reason)} 个 ({lines} 行)")

    # 失败的文件
    if progress['failed_files']:
        print(f"\n❌ 失败的文件：{len(progress['failed_files'])} 个")
        for failed_file in progress['failed_files'][-5:]:  # 只显示最后 5 个
            print(f"   - {failed_file['source']}")
            print(f"     错误：{failed_file['error']}")
        if len(progress['failed_files']) > 5:
            print(f"   ... 还有 {len(progress['failed_files']) - 5} 个失败文件")

    # 批次详情
    print(f"\n📦 批次详情：")
    for batch in progress['batches']:
        status_icon = {
            'pending': '⏳',
            'in_progress': '🔄',
            'completed': '✅'
        }.get(batch['status'], '❓')

        completed_files = sum(1 for f in batch['files'] if f['status'] == 'completed')

        print(f"   {status_icon} 批次 {batch['batch_number']}/{progress['total_batches']} "
              f"({batch['lines']} 行, {completed_files}/{batch['file_count']} 文件)")


def print_current_batch(progress: Dict[str, Any]):
    """
    打印当前批次信息

    Args:
        progress: 进度报告对象
    """
    current_batch_num = progress['current_batch']

    # 查找当前批次
    current_batch = None
    for batch in progress['batches']:
        if batch['batch_number'] == current_batch_num:
            current_batch = batch
            break

    if not current_batch:
        # 如果没有找到当前批次，尝试找到第一个未完成的批次
        for batch in progress['batches']:
            if batch['status'] == 'pending':
                current_batch = batch
                current_batch_num = batch['batch_number']
                break

    if not current_batch:
        print("\n✅ 所有批次已完成！")
        return

    print("\n" + "="*70)
    print(f"🔄 当前批次：{current_batch_num}/{progress['total_batches']}")
    print("="*70)
    print(f"批次信息：{current_batch['lines']} 行, {current_batch['file_count']} 个文件")

    # 显示待翻译文件
    pending_files = [f for f in current_batch['files'] if f['status'] == 'pending']
    if pending_files:
        print(f"\n待翻译文件：{len(pending_files)} 个")
        for i, file_info in enumerate(pending_files, 1):
            print(f"  {i}. {file_info['relative_path']} ({file_info['lines']} 行)")
    else:
        print(f"\n✅ 当前批次所有文件已完成")

    # 显示已完成文件
    completed_files = [f for f in current_batch['files'] if f['status'] == 'completed']
    if completed_files:
        print(f"\n已完成文件：{len(completed_files)} 个")
        for i, file_info in enumerate(completed_files, 1):
            print(f"  {i}. {file_info['relative_path']} ({file_info['lines']} 行)")


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("Usage: progress_manager.py <command> [args...]", file=sys.stderr)
        print("", file=sys.stderr)
        print("Commands:", file=sys.stderr)
        print("  create <target_dir> <source_dir> <scan_result.json> [preprocess_result.json]", file=sys.stderr)
        print("  update-file <target_dir> <source_path> <target_path> <batch_number>", file=sys.stderr)
        print("  update-batch <target_dir> <batch_number>", file=sys.stderr)
        print("  fail-file <target_dir> <source_path> <error_message> <batch_number>", file=sys.stderr)
        print("  show <target_dir>", file=sys.stderr)
        print("  current <target_dir>", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    if command == 'create':
        if len(sys.argv) < 5:
            print("Usage: progress_manager.py create <target_dir> <source_dir> <scan_result.json> [preprocess_result.json]", file=sys.stderr)
            sys.exit(1)

        target_dir = sys.argv[2]
        source_dir = sys.argv[3]
        scan_result_file = sys.argv[4]
        preprocess_result_file = sys.argv[5] if len(sys.argv) > 5 else None

        # 加载扫描结果
        with open(scan_result_file, 'r', encoding='utf-8') as f:
            scan_result = json.load(f)

        # 加载预处理结果（可选）
        preprocess_result = None
        if preprocess_result_file:
            with open(preprocess_result_file, 'r', encoding='utf-8') as f:
                preprocess_result = json.load(f)

        # 创建进度报告
        progress = create_progress(target_dir, source_dir, scan_result, preprocess_result)
        print_progress_summary(progress)

    elif command == 'update-file':
        if len(sys.argv) < 6:
            print("Usage: progress_manager.py update-file <target_dir> <source_path> <target_path> <batch_number>", file=sys.stderr)
            sys.exit(1)

        target_dir = sys.argv[2]
        source_path = sys.argv[3]
        target_path = sys.argv[4]
        batch_number = int(sys.argv[5])

        progress = update_file_completed(target_dir, source_path, target_path, batch_number)
        print(f"✅ 文件已标记为完成：{source_path}")

    elif command == 'update-batch':
        if len(sys.argv) < 4:
            print("Usage: progress_manager.py update-batch <target_dir> <batch_number>", file=sys.stderr)
            sys.exit(1)

        target_dir = sys.argv[2]
        batch_number = int(sys.argv[3])

        progress = update_batch_completed(target_dir, batch_number)
        print(f"✅ 批次 {batch_number} 已标记为完成")

    elif command == 'fail-file':
        if len(sys.argv) < 6:
            print("Usage: progress_manager.py fail-file <target_dir> <source_path> <error_message> <batch_number>", file=sys.stderr)
            sys.exit(1)

        target_dir = sys.argv[2]
        source_path = sys.argv[3]
        error_message = sys.argv[4]
        batch_number = int(sys.argv[5])

        progress = add_failed_file(target_dir, source_path, error_message, batch_number)
        print(f"⚠️  文件已标记为失败：{source_path}")

    elif command == 'show':
        if len(sys.argv) < 3:
            print("Usage: progress_manager.py show <target_dir>", file=sys.stderr)
            sys.exit(1)

        target_dir = sys.argv[2]
        progress = load_progress(target_dir)

        if not progress:
            print(f"❌ 未找到进度文件：{target_dir}")
            sys.exit(1)

        print_progress_summary(progress)

    elif command == 'current':
        if len(sys.argv) < 3:
            print("Usage: progress_manager.py current <target_dir>", file=sys.stderr)
            sys.exit(1)

        target_dir = sys.argv[2]
        progress = load_progress(target_dir)

        if not progress:
            print(f"❌ 未找到进度文件：{target_dir}")
            sys.exit(1)

        print_current_batch(progress)

    else:
        print(f"❌ 未知命令：{command}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
