#!/usr/bin/env python3
"""
扫描指定目录下所有需要翻译的文件，并生成翻译计划
支持 Markdown 和 YAML 文件，自动识别 API 文件（mdx + yaml 对）
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict


def scan_directory(directory: str, file_types: List[str] = None) -> List[Dict[str, Any]]:
    """
    递归扫描目录下所有指定类型的文件

    Args:
        directory: 要扫描的目录路径
        file_types: 要包含的文件扩展名列表，如 ['.md', '.yaml', '.mdx']

    Returns:
        list: 文件信息列表
    """
    if file_types is None:
        file_types = ['.md', '.yaml', '.mdx']

    dir_path = Path(directory)
    if not dir_path.exists():
        print(f"Error: Directory '{directory}' does not exist", file=sys.stderr)
        return []

    files = []
    for file_path in dir_path.rglob('*'):
        if file_path.is_file() and file_path.suffix in file_types:
            # 只处理中文文档（路径中包含 /zh/ 的）
            if '/zh/' in str(file_path):
                # 计算文件行数
                line_count = 0
                has_doctype_api = False

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        line_count = len(lines)

                        # 检查是否包含 docType: API
                        for line in lines[:20]:  # 只检查前 20 行
                            if line.strip() == 'docType: API':
                                has_doctype_api = True
                                break
                except Exception:
                    line_count = 0

                files.append({
                    'path': str(file_path),
                    'relative_path': str(file_path.relative_to(dir_path)),
                    'suffix': file_path.suffix,
                    'line_count': line_count,
                    'size_kb': file_path.stat().st_size / 1024,
                    'has_doctype_api': has_doctype_api  # 新增字段标识是否为 API 文件
                })

    return files


def identify_api_files(files: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    识别 API 文件对（同名 mdx 和 yaml）以及 docType: API 文件

    规则：
    - 包含 docType: API 的文件自动跳过
    - 在任意目录下存在同名的 .mdx 和 .yaml 文件
    - 这类文件只需要翻译 .yaml，.mdx 是自动生成的

    Returns:
        dict: {
            'doctype_api_files': [...],      # docType: API 文件（自动跳过）
            'mdx_yaml_pairs': {              # 同名 mdx+yaml 文件对
                'yaml_files': [...],         # 需要翻译的 yaml
                'mdx_files': [...]           # 跳过的 mdx（自动生成）
            },
            'regular_files': [...]           # 普通文件
        }
    """
    result = {
        'doctype_api_files': [],  # docType: API 文件
        'mdx_yaml_pairs': {
            'yaml_files': [],  # 需要翻译的 yaml
            'mdx_files': []    # 跳过的 mdx
        },
        'regular_files': []
    }

    # 第一步：分离 docType: API 文件
    non_doctype_files = []
    for file_info in files:
        if file_info.get('has_doctype_api', False):
            result['doctype_api_files'].append(file_info)
        else:
            non_doctype_files.append(file_info)

    # 第二步：在所有文件中查找同名的 mdx 和 yaml 对（不限于 api-reference 目录）
    file_map = defaultdict(lambda: {'.mdx': None, '.yaml': None})

    for file_info in non_doctype_files:
        file_path_obj = Path(file_info['path'])
        basename = file_path_obj.stem  # 不带扩展名的文件名
        suffix = file_info['suffix']

        if suffix in ['.mdx', '.yaml']:
            file_map[basename][suffix] = file_info

    # 第三步：分类文件
    for basename, file_dict in file_map.items():
        mdx_file = file_dict['.mdx']
        yaml_file = file_dict['.yaml']

        if mdx_file and yaml_file:
            # 有成对的 mdx 和 yaml 文件
            result['mdx_yaml_pairs']['yaml_files'].append(yaml_file)
            result['mdx_yaml_pairs']['mdx_files'].append(mdx_file)
        elif yaml_file:
            # 只有 yaml，按普通文件处理
            result['regular_files'].append(yaml_file)
        elif mdx_file:
            # 只有 mdx，按普通文件处理
            result['regular_files'].append(mdx_file)

    return result


def create_translation_batches(files: List[Dict[str, Any]], lines_per_batch: int = 5000) -> List[Dict[str, Any]]:
    """
    将文件组织成翻译批次

    策略：
    - 小文件（< 100 行）：按文件分组，每批多个文件
    - 中等文件（100-500 行）：每批 1-2 个文件
    - 大文件（> 500 行）：单独成批，可能需要分段翻译

    Args:
        files: 文件列表
        lines_per_batch: 每批大致的目标行数

    Returns:
        list: 批次列表
    """
    # 按文件大小排序（小文件优先）
    sorted_files = sorted(files, key=lambda x: x['line_count'])

    batches = []
    current_batch = {
        'files': [],
        'total_lines': 0,
        'file_count': 0
    }

    for file_info in sorted_files:
        line_count = file_info['line_count']
        file_size_category = 'small' if line_count < 100 else 'medium' if line_count < 500 else 'large'

        file_info['size_category'] = file_size_category

        # 大文件（> 500 行）单独成批
        if file_size_category == 'large':
            # 保存当前批次
            if current_batch['files']:
                batches.append(current_batch)
                current_batch = {'files': [], 'total_lines': 0, 'file_count': 0}

            # 大文件单独成批
            batches.append({
                'files': [file_info],
                'total_lines': line_count,
                'file_count': 1,
                'needs_segmentation': True
            })
        elif file_size_category == 'medium':
            # 中等文件，检查当前批次
            if current_batch['file_count'] >= 2 or current_batch['total_lines'] + line_count > lines_per_batch:
                batches.append(current_batch)
                current_batch = {'files': [], 'total_lines': 0, 'file_count': 0}

            current_batch['files'].append(file_info)
            current_batch['total_lines'] += line_count
            current_batch['file_count'] += 1
        else:
            # 小文件，可以多个一批
            if current_batch['total_lines'] + line_count > lines_per_batch * 1.5:
                batches.append(current_batch)
                current_batch = {'files': [], 'total_lines': 0, 'file_count': 0}

            current_batch['files'].append(file_info)
            current_batch['total_lines'] += line_count
            current_batch['file_count'] += 1

    # 保存最后一个批次
    if current_batch['files']:
        batches.append(current_batch)

    return batches


def print_summary(result: Dict[str, Any]):
    """打印扫描结果摘要"""
    print("\n" + "="*70)
    print("📊 翻译扫描结果")
    print("="*70)

    # docType: API 文件统计
    doctype_api_files = result.get('doctype_api_files', [])
    print(f"\n⏭️  docType: API 文件（自动跳过）：{len(doctype_api_files)} 个")
    if doctype_api_files:
        doctype_lines = sum(f['line_count'] for f in doctype_api_files)
        print(f"   总行数：{doctype_lines} 行")
        # 显示前 5 个文件
        for f in doctype_api_files[:5]:
            print(f"   - {f['relative_path']} ({f['line_count']} 行)")
        if len(doctype_api_files) > 5:
            print(f"   ... 还有 {len(doctype_api_files) - 5} 个文件")

    # 同名 mdx+yaml 文件对统计
    mdx_yaml_pairs = result.get('mdx_yaml_pairs', {})
    yaml_to_translate = mdx_yaml_pairs.get('yaml_files', [])
    mdx_to_skip = mdx_yaml_pairs.get('mdx_files', [])

    if yaml_to_translate:
        print(f"\n🔗 同名 MDX+YAML 文件对：{len(yaml_to_translate)} 对")
        yaml_lines = sum(f['line_count'] for f in yaml_to_translate)
        mdx_lines = sum(f['line_count'] for f in mdx_to_skip)
        print(f"   ✅ 需翻译 YAML：{len(yaml_to_translate)} 个 ({yaml_lines} 行)")
        print(f"   ⏭️  跳过 MDX（自动生成）：{len(mdx_to_skip)} 个 ({mdx_lines} 行)")
        # 显示前 5 对文件
        for i, (yaml_file, mdx_file) in enumerate(zip(yaml_to_translate[:5], mdx_to_skip[:5])):
            print(f"   {i+1}. {yaml_file['relative_path']} → {yaml_file['line_count']} 行")
            print(f"      {mdx_file['relative_path']} → 跳过")
        if len(yaml_to_translate) > 5:
            print(f"   ... 还有 {len(yaml_to_translate) - 5} 对文件")

    # 普通文件统计
    regular_files = result['regular_files']
    md_files = [f for f in regular_files if f['suffix'] == '.md' or f['suffix'] == '.mdx']
    yaml_files = [f for f in regular_files if f['suffix'] == '.yaml']

    if md_files:
        print(f"\n📄 Markdown/MDX 文件：{len(md_files)} 个")
        md_lines = sum(f['line_count'] for f in md_files)
        print(f"   总行数：{md_lines} 行")

    if yaml_files:
        print(f"\n📋 YAML 文件：{len(yaml_files)} 个")
        yaml_lines = sum(f['line_count'] for f in yaml_files)
        print(f"   总行数：{yaml_lines} 行")

    # 批次统计
    batches = result['batches']
    print(f"\n📦 翻译批次：{len(batches)} 批")
    print(f"   总文件数：{result['total_files']}")
    print(f"   总行数：{result['total_lines']}")
    print(f"   平均每批：{result['total_lines'] // len(batches) if batches else 0} 行")

    # 大文件提示
    large_files = [f for f in result['all_files'] if f.get('size_category') == 'large']
    if large_files:
        print(f"\n⚠️  大文件（>500 行）：{len(large_files)} 个")
        for f in large_files[:5]:  # 只显示前 5 个
            print(f"   - {f['relative_path']} ({f['line_count']} 行)")
        if len(large_files) > 5:
            print(f"   ... 还有 {len(large_files) - 5} 个大文件")


def print_batch_plan(batches: List[Dict[str, Any]], show_details: bool = True):
    """打印翻译批次计划"""
    print("\n" + "="*70)
    print("📋 翻译批次计划")
    print("="*70)

    for i, batch in enumerate(batches, 1):
        print(f"\n批次 {i}/{len(batches)} ({batch['total_lines']} 行, {batch['file_count']} 个文件)")

        if show_details or batch.get('needs_segmentation'):
            for j, file_info in enumerate(batch['files'], 1):
                flag = ""
                if file_info.get('size_category') == 'large':
                    flag = " [大文件-需分段]"
                elif file_info.get('size_category') == 'medium':
                    flag = " [中文件]"

                print(f"  {j}. {file_info['relative_path']}{flag}")
                print(f"     → {file_info['line_count']} 行, {file_info['size_kb']:.1f} KB")
        else:
            # 简略显示
            file_names = [f['relative_path'].split('/')[-1] for f in batch['files']]
            print(f"  文件：{', '.join(file_names)}")

        if batch.get('needs_segmentation'):
            print(f"  ⚠️  此批次包含大文件，翻译时可能需要分段处理")


def main():
    if len(sys.argv) < 2:
        print("Usage: scan_translation_files.py <directory> [lines_per_batch]", file=sys.stderr)
        print("Example: scan_translation_files.py docs/zh/product 500", file=sys.stderr)
        print("Example: scan_translation_files.py docs/zh/server/api-reference", file=sys.stderr)
        sys.exit(1)

    directory = sys.argv[1]
    lines_per_batch = int(sys.argv[2]) if len(sys.argv) > 2 else 5000

    print(f"🔍 扫描目录：{directory}")
    print(f"⚙️  每批目标行数：{lines_per_batch}")

    # 扫描文件
    files = scan_directory(directory)

    if not files:
        print("\n❌ 未找到任何需要翻译的文件")
        print("提示：确保目录路径正确，且包含 /zh/ 子目录的文件")
        sys.exit(0)

    # 识别 API 文件
    categorized = identify_api_files(files)

    # 合并所有需要翻译的文件
    mdx_yaml_pairs = categorized.get('mdx_yaml_pairs', {})
    yaml_files = mdx_yaml_pairs.get('yaml_files', [])
    regular_files = categorized['regular_files']

    files_to_translate = yaml_files + regular_files
    all_files = (
        categorized.get('doctype_api_files', []) +
        mdx_yaml_pairs.get('yaml_files', []) +
        mdx_yaml_pairs.get('mdx_files', []) +
        regular_files
    )

    # 创建翻译批次（只翻译非 docType: API 的文件）
    batches = create_translation_batches(files_to_translate, lines_per_batch)

    # 计算统计信息
    total_lines = sum(f['line_count'] for f in files_to_translate)

    # 构建结果
    result = {
        'directory': directory,
        'total_files': len(files_to_translate),
        'total_lines': total_lines,
        'doctype_api_files': categorized.get('doctype_api_files', []),
        'mdx_yaml_pairs': categorized.get('mdx_yaml_pairs', {}),
        'regular_files': regular_files,
        'all_files': all_files,
        'files_to_translate': files_to_translate,
        'batches': batches,
        'lines_per_batch': lines_per_batch
    }

    # 打印结果
    print_summary(result)
    print_batch_plan(batches, show_details=True)

    # 输出 JSON 格式供脚本使用
    print("\n" + "="*70)
    print("📄 JSON 输出（供后续处理）")
    print("="*70)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
