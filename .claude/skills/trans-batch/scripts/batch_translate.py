#!/usr/bin/env python3
"""
批量翻译新产品文档的主编排脚本

整合所有步骤：
1. 扫描和分类文档
2. 准备目标目录
3. 预处理全复用文档
4. 生成翻译批次计划
5. 输出进度记录文件模板
"""

import sys
import json
from pathlib import Path
from datetime import datetime


def calculate_target_directory(source_dir: str) -> str:
    """
    计算目标目录路径（将 /zh/ 替换为 /en/）

    Args:
        source_dir: 源目录路径

    Returns:
        str: 目标目录路径
    """
    return source_dir.replace('/zh/', '/en/')


def prepare_target_directory(source_dir: str, target_dir: str) -> dict:
    """
    准备目标目录

    如果目标目录不存在，则拷贝源目录到目标目录
    如果目标目录已存在，则直接使用

    Args:
        source_dir: 源目录路径
        target_dir: 目标目录路径

    Returns:
        dict: 准备结果
    """
    source_path = Path(source_dir)
    target_path = Path(target_dir)

    result = {
        'source_dir': source_dir,
        'target_dir': target_dir,
        'existed': target_path.exists(),
        'copied': False
    }

    if target_path.exists():
        print(f"✅ 目标目录已存在：{target_dir}")
    else:
        print(f"\n📁 目标目录不存在，开始拷贝...")
        print(f"   源目录：{source_dir}")
        print(f"   目标目录：{target_dir}")

        # 这里只是生成命令，实际拷贝由用户执行
        copy_command = f"cp -r '{source_dir}' '{target_dir}'"
        print(f"\n💡 请执行以下命令拷贝目录：")
        print(f"   {copy_command}")
        print(f"\n⚠️  拷贝完成后请重新运行此脚本")
        sys.exit(0)

    return result


def create_progress_file(scan_result: dict, prep_result: dict, preprocess_results: list = None) -> dict:
    """
    创建进度记录文件

    Args:
        scan_result: 扫描结果
        prep_result: 准备结果
        preprocess_results: 预处理结果（可选）

    Returns:
        dict: 进度记录
    """
    now = datetime.utcnow().isoformat() + 'Z'

    # 提取批次信息
    batches = scan_result.get('batches', [])

    # 构建跳过的文件列表
    skipped_files = []

    # API 文档
    for file_info in scan_result.get('files', []):
        if file_info.get('has_doctype_api', False):
            skipped_files.append({
                'path': file_info['path'],
                'reason': 'docType: API',
                'line_count': file_info['line_count']
            })

    # YAML 生成的 MDX
    # 这些信息在 scan_result 中没有直接标记，需要从 yaml_pairs 中提取
    # 这里简化处理，实际使用时可以从 scan_result 中提取

    # 全复用文档（已解决的）
    if preprocess_results:
        for result in preprocess_results:
            if result['status'] == 'resolved':
                skipped_files.append({
                    'path': result['source'],
                    'reason': 'reuse_doc_resolved',
                    'line_count': result.get('line_count', 0),
                    'resolved_to': result.get('resolved_to')
                })

    progress = {
        'source_directory': scan_result['directory'],
        'target_directory': prep_result['target_dir'],
        'started_at': now,
        'last_updated': now,
        'status': 'in_progress',
        'total_files': scan_result['summary']['total_files'],
        'completed_files': 0,
        'skipped_files': len(skipped_files),
        'total_lines': scan_result['summary']['total_lines'],
        'translated_lines': 0,
        'current_batch': 1,
        'total_batches': len(batches),
        'scan_summary': scan_result['summary'],
        'batches': [],
        'skipped_files': skipped_files,
        'failed_files': []
    }

    # 添加批次信息
    for batch in batches:
        progress['batches'].append({
            'batch_number': batch['batch_number'],
            'status': 'pending',
            'file_count': batch['file_count'],
            'total_lines': batch['total_lines'],
            'files': [
                {
                    'source': f['path'],
                    'target': f['target_path'],
                    'lines': f['line_count'],
                    'status': 'pending'
                }
                for f in batch['files']
            ]
        })

    return progress


def save_progress_file(progress: dict, target_dir: str):
    """
    保存进度文件到目标目录

    Args:
        progress: 进度记录
        target_dir: 目标目录
    """
    progress_file_path = Path(target_dir) / '.translation-progress.json'

    with open(progress_file_path, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

    print(f"\n✅ 进度文件已创建：{progress_file_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: batch_translate.py <source_directory>", file=sys.stderr)
        print("Example: batch_translate.py core_products/real-time-voice-video/zh/flutter", file=sys.stderr)
        sys.exit(1)

    source_dir = sys.argv[1]
    target_dir = calculate_target_directory(source_dir)

    print("="*70)
    print("🚀 批量翻译新产品文档")
    print("="*70)

    # 第一步：准备目标目录
    print("\n📁 第一步：准备目标目录")
    prep_result = prepare_target_directory(source_dir, target_dir)

    # 第二步：扫描文档（需要调用 scan_batch_translation.py）
    print("\n🔍 第二步：扫描文档")
    print("💡 请先运行扫描脚本生成扫描结果：")
    print(f"   python3 .claude/skills/trans-batch/scripts/scan_batch_translation.py {source_dir}")
    print(f"   将输出保存为 scan_result.json")
    print("\n⚠️  扫描完成后请重新运行此脚本，并指定扫描结果文件：")
    print(f"   python3 .claude/skills/trans-batch/scripts/batch_translate.py {source_dir} scan_result.json")

    if len(sys.argv) < 3:
        sys.exit(0)

    # 如果提供了扫描结果文件，继续处理
    scan_result_file = sys.argv[2]

    try:
        with open(scan_result_file, 'r', encoding='utf-8') as f:
            scan_result = json.load(f)
    except Exception as e:
        print(f"❌ 错误：无法读取扫描结果文件：{e}", file=sys.stderr)
        sys.exit(1)

    print(f"✅ 已加载扫描结果：{scan_result_file}")

    # 第三步：预处理全复用文档
    print("\n🔄 第三步：预处理全复用文档")
    reuse_docs = [f for f in scan_result.get('files', []) if f.get('is_reuse_doc', False)]

    if reuse_docs:
        print(f"发现 {len(reuse_docs)} 个全复用文档")
        print("💡 请运行预处理脚本：")
        print(f"   python3 .claude/skills/trans-batch/scripts/preprocess_reuse_docs.py {scan_result_file}")
        print(f"   将输出保存为 preprocess_result.json")
        print("\n⚠️  预处理完成后请重新运行此脚本，并指定预处理结果文件：")
        print(f"   python3 .claude/skills/trans-batch/scripts/batch_translate.py {source_dir} {scan_result_file} preprocess_result.json")

        if len(sys.argv) < 4:
            sys.exit(0)

        preprocess_result_file = sys.argv[3]

        try:
            with open(preprocess_result_file, 'r', encoding='utf-8') as f:
                preprocess_results = json.load(f)
        except Exception as e:
            print(f"❌ 错误：无法读取预处理结果文件：{e}", file=sys.stderr)
            sys.exit(1)

        print(f"✅ 已加载预处理结果：{preprocess_result_file}")
    else:
        print("✅ 没有需要预处理的全复用文档")
        preprocess_results = None

    # 第四步：创建进度文件
    print("\n📊 第四步：创建进度记录文件")
    progress = create_progress_file(scan_result, prep_result, preprocess_results)
    save_progress_file(progress, target_dir)

    # 第五步：输出翻译计划
    print("\n📋 第五步：翻译批次计划")
    print("="*70)

    batches = scan_result.get('batches', [])
    for i, batch in enumerate(batches, 1):
        print(f"\n批次 {batch['batch_number']}/{len(batches)} ({batch['total_lines']} 行, {batch['file_count']} 个文件)")
        for j, file_info in enumerate(batch['files'], 1):
            size_flag = ""
            if file_info.get('size_category') == 'large':
                size_flag = " [大文件]"
            elif file_info.get('size_category') == 'medium':
                size_flag = " [中等]"

            print(f"  {j}. {file_info['relative_path']}{size_flag}")
            print(f"     → {file_info['target_path']}")
            print(f"     {file_info['line_count']} 行")

        if batch.get('needs_segmentation'):
            print(f"  ⚠️  此批次包含超大文件，翻译时需要分段处理（每段不超过 2000 行）")

    # 输出总结
    print("\n" + "="*70)
    print("📊 准备工作完成")
    print("="*70)
    print(f"源目录：{source_dir}")
    print(f"目标目录：{target_dir}")
    print(f"总文件数：{scan_result['summary']['total_files']}")
    print(f"总行数：{scan_result['summary']['total_lines']}")
    print(f"总批次数：{len(batches)}")
    print(f"\n跳过文件数：{progress['skipped_files']}")
    print(f"   - API 文档：{scan_result['summary']['skipped_api_files']}")
    print(f"   - YAML 生成 MDX：{scan_result['summary']['skipped_mdx_files']}")
    if preprocess_results:
        resolved_count = sum(1 for r in preprocess_results if r['status'] == 'resolved')
        print(f"   - 全复用文档（已解决）：{resolved_count}")

    print(f"\n✅ 准备工作完成！可以开始逐批翻译了")
    print(f"📝 进度文件：{Path(target_dir) / '.translation-progress.json'}")
    print(f"\n💡 提示：")
    print(f"   1. 加载术语对照表：.translate/common-terminology.csv")
    print(f"   2. 开始翻译第一批，每批完成后更新进度文件")
    print(f"   3. 大文件需要分段翻译（每段不超过 2000 行）")


if __name__ == '__main__':
    main()
