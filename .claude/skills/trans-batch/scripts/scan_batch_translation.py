#!/usr/bin/env python3
"""
扫描待翻译的中文目录，智能分类文档并生成翻译计划

分类规则：
1. API 文档：docType 为 API 的 MD 文档（自动跳过）
2. YAML 生成的 MDX：同一目录下存在同名 mdx 和 yaml 文件（只翻译 yaml）
3. 全复用文档：除了 frontmatter 外只有两行非空内容（一行 import Content，一行 <Content）
4. 普通文档：按行数分类（<50行小文件，50-300行中等文件，>300行大文件）
"""

import sys
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple
from collections import defaultdict


def is_reuse_doc(file_path: Path) -> bool:
    """
    判断是否为全复用文档

    全复用文档特征：
    - 除了 frontmatter 外只有两行非空内容
    - 一行以 import Content from 开头
    - 另一行以 <Content 开头
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 跳过 frontmatter（在 --- 之间的内容）
        frontmatter_end = -1
        if lines[0].strip() == '---':
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    frontmatter_end = i
                    break

        # 提取 frontmatter 之后的内容
        content_lines = lines[frontmatter_end + 1:] if frontmatter_end > 0 else lines

        # 过滤空行和纯空格行
        non_empty_lines = [line for line in content_lines if line.strip()]

        # 检查是否只有两行非空内容
        if len(non_empty_lines) != 2:
            return False

        # 检查第一行是否包含 import Content from
        line1 = non_empty_lines[0].strip()
        line2 = non_empty_lines[1].strip()

        has_import = 'import Content from' in line1
        has_content_tag = line2.startswith('<Content')

        return has_import and has_content_tag

    except Exception as e:
        print(f"Warning: Failed to check file {file_path}: {e}", file=sys.stderr)
        return False


def has_doctype_api(file_path: Path) -> bool:
    """检查文件 frontmatter 中是否包含 docType: API"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 只检查前 20 行
        for line in lines[:20]:
            if line.strip() == 'docType: API':
                return True

        return False

    except Exception:
        return False


def scan_directory(directory: str) -> List[Dict[str, Any]]:
    """
    递归扫描目录下所有 .md 和 .mdx 文件

    Args:
        directory: 要扫描的目录路径

    Returns:
        list: 文件信息列表
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        print(f"Error: Directory '{directory}' does not exist", file=sys.stderr)
        return []

    files = []
    for file_path in dir_path.rglob('*'):
        # 只处理 .md 和 .mdx 文件
        if file_path.is_file() and file_path.suffix in ['.md', '.mdx']:
            # 计算文件行数
            line_count = 0
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    line_count = len(lines)
            except Exception:
                line_count = 0

            files.append({
                'path': str(file_path),
                'relative_path': str(file_path.relative_to(dir_path)),
                'suffix': file_path.suffix,
                'line_count': line_count,
                'size_kb': file_path.stat().st_size / 1024,
                'has_doctype_api': has_doctype_api(file_path),
                'is_reuse_doc': is_reuse_doc(file_path)
            })

    return files


def categorize_files(files: List[Dict[str, Any]], base_dir: Path) -> Dict[str, Any]:
    """
    分类文件

    分类规则：
    1. API 文档：has_doctype_api = True（自动跳过）
    2. YAML 生成的 MDX：同一目录下存在同名 mdx 和 yaml 文件
    3. 全复用文档：is_reuse_doc = True
    4. 普通文档：按行数分类

    Returns:
        dict: 分类结果
    """
    result = {
        'api_docs': [],           # API 文档（跳过）
        'yaml_pairs': {           # YAML+MDX 对
            'yaml_files': [],     # 需要翻译的 yaml
            'mdx_files': []       # 跳过的 mdx
        },
        'reuse_docs': [],         # 全复用文档（需要预处理）
        'regular_docs': {         # 普通文档
            'small': [],          # < 50 行
            'medium': [],         # 50-300 行
            'large': []           # > 300 行
        }
    }

    # 第一步：分离 API 文档和非 API 文档
    non_api_files = []
    for file_info in files:
        if file_info.get('has_doctype_api', False):
            result['api_docs'].append(file_info)
        else:
            non_api_files.append(file_info)

    # 第二步：检查 YAML+MDX 文件对
    file_map = defaultdict(lambda: {'.mdx': None, '.md': None, '.yaml': None})

    for file_info in non_api_files:
        file_path_obj = Path(file_info['path'])
        parent_dir = file_path_obj.parent
        basename = file_path_obj.stem  # 不带扩展名的文件名
        suffix = file_info['suffix']

        if suffix in ['.md', '.mdx', '.yaml']:
            key = (parent_dir, basename)
            file_map[key][suffix] = file_info

    # 第三步：分类文件
    for (parent_dir, basename), file_dict in file_map.items():
        md_file = file_dict['.md']
        mdx_file = file_dict['.mdx']
        yaml_file = file_dict['.yaml']

        # 优先处理 YAML+MDX 对
        if yaml_file and (md_file or mdx_file):
            # 这是一个 YAML 生成的 MDX 文件对
            result['yaml_pairs']['yaml_files'].append(yaml_file)
            if mdx_file:
                result['yaml_pairs']['mdx_files'].append(mdx_file)
            if md_file:
                result['yaml_pairs']['mdx_files'].append(md_file)
            continue

        # 处理全复用文档
        if mdx_file and mdx_file.get('is_reuse_doc', False):
            result['reuse_docs'].append(mdx_file)
            continue

        if md_file and md_file.get('is_reuse_doc', False):
            result['reuse_docs'].append(md_file)
            continue

        # 处理普通文档
        regular_files = [f for f in [md_file, mdx_file, yaml_file] if f]
        for file_info in regular_files:
            line_count = file_info['line_count']
            if line_count < 50:
                file_info['size_category'] = 'small'
                result['regular_docs']['small'].append(file_info)
            elif line_count <= 300:
                file_info['size_category'] = 'medium'
                result['regular_docs']['medium'].append(file_info)
            else:
                file_info['size_category'] = 'large'
                result['regular_docs']['large'].append(file_info)

    return result


def calculate_target_path(source_path: str, base_dir: Path) -> str:
    """
    计算目标文件路径（将 /zh/ 替换为 /en/）
    """
    path_obj = Path(source_path)
    parts = path_obj.parts

    # 找到 /zh/ 的位置并替换为 /en/
    new_parts = []
    for part in parts:
        if part == 'zh':
            new_parts.append('en')
        else:
            new_parts.append(part)

    return str(Path(*new_parts))


def create_batches(categorized: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    创建翻译批次

    批次策略：
    - 小文件（< 50 行）：每批 10-20 个文件，总行数控制在 1000 行以内
    - 中等文件（50-300 行）：每批 2-5 个文件，总行数控制在 1500 行以内
    - 大文件（> 300 行）：单独成批

    Args:
        categorized: 分类后的文件信息

    Returns:
        list: 批次列表
    """
    batches = []
    batch_number = 1

    # 处理小文件
    small_files = categorized['regular_docs']['small']
    if small_files:
        current_batch = {
            'batch_number': batch_number,
            'files': [],
            'total_lines': 0,
            'file_count': 0
        }

        for file_info in small_files:
            if current_batch['file_count'] >= 20 or current_batch['total_lines'] + file_info['line_count'] > 1000:
                batches.append(current_batch)
                batch_number += 1
                current_batch = {
                    'batch_number': batch_number,
                    'files': [],
                    'total_lines': 0,
                    'file_count': 0
                }

            current_batch['files'].append(file_info)
            current_batch['total_lines'] += file_info['line_count']
            current_batch['file_count'] += 1

        if current_batch['files']:
            batches.append(current_batch)
            batch_number += 1

    # 处理中等文件
    medium_files = categorized['regular_docs']['medium']
    if medium_files:
        for file_info in medium_files:
            # 每 2-5 个文件一批，或总行数超过 1500
            batch = {
                'batch_number': batch_number,
                'files': [file_info],
                'total_lines': file_info['line_count'],
                'file_count': 1
            }

            # 尝试添加更多文件
            for other_file in medium_files[medium_files.index(file_info) + 1:]:
                if batch['file_count'] >= 5 or batch['total_lines'] + other_file['line_count'] > 1500:
                    break
                batch['files'].append(other_file)
                batch['total_lines'] += other_file['line_count']
                batch['file_count'] += 1

            batches.append(batch)
            batch_number += 1

    # 处理大文件
    large_files = categorized['regular_docs']['large']
    for file_info in large_files:
        batches.append({
            'batch_number': batch_number,
            'files': [file_info],
            'total_lines': file_info['line_count'],
            'file_count': 1,
            'needs_segmentation': file_info['line_count'] > 2000
        })
        batch_number += 1

    return batches


def print_summary(categorized: Dict[str, Any], base_dir: Path):
    """打印扫描结果摘要"""
    print("\n" + "="*70)
    print("📊 批量翻译扫描结果")
    print("="*70)

    # API 文档统计
    api_docs = categorized['api_docs']
    print(f"\n⏭️  API 文档（docType: API，自动跳过）：{len(api_docs)} 个")
    if api_docs:
        api_lines = sum(f['line_count'] for f in api_docs)
        print(f"   总行数：{api_lines} 行")
        for f in api_docs[:3]:
            print(f"   - {f['relative_path']} ({f['line_count']} 行)")
        if len(api_docs) > 3:
            print(f"   ... 还有 {len(api_docs) - 3} 个文件")

    # YAML+MDX 文件对统计
    yaml_pairs = categorized['yaml_pairs']
    yaml_files = yaml_pairs['yaml_files']
    mdx_files = yaml_pairs['mdx_files']

    if yaml_files:
        print(f"\n🔗 YAML+MDX 文件对：{len(yaml_files)} 对")
        yaml_lines = sum(f['line_count'] for f in yaml_files)
        mdx_lines = sum(f['line_count'] for f in mdx_files)
        print(f"   ✅ 需翻译 YAML：{len(yaml_files)} 个 ({yaml_lines} 行)")
        print(f"   ⏭️  跳过 MDX/MD（自动生成）：{len(mdx_files)} 个 ({mdx_lines} 行)")
        for i, (yaml_file, mdx_file) in enumerate(zip(yaml_files[:3], mdx_files[:3])):
            print(f"   {i+1}. {yaml_file['relative_path']} → {yaml_file['line_count']} 行")
            print(f"      {mdx_file['relative_path']} → 跳过")
        if len(yaml_files) > 3:
            print(f"   ... 还有 {len(yaml_files) - 3} 对文件")

    # 全复用文档统计
    reuse_docs = categorized['reuse_docs']
    print(f"\n🔄 全复用文档（需要预处理）：{len(reuse_docs)} 个")
    if reuse_docs:
        reuse_lines = sum(f['line_count'] for f in reuse_docs)
        print(f"   总行数：{reuse_lines} 行")
        for f in reuse_docs[:3]:
            print(f"   - {f['relative_path']} ({f['line_count']} 行)")
        if len(reuse_docs) > 3:
            print(f"   ... 还有 {len(reuse_docs) - 3} 个文件")

    # 普通文档统计
    regular_docs = categorized['regular_docs']
    small_files = regular_docs['small']
    medium_files = regular_docs['medium']
    large_files = regular_docs['large']

    print(f"\n📄 普通文档分类：")
    print(f"   小文件（< 50 行）：{len(small_files)} 个")
    if small_files:
        small_lines = sum(f['line_count'] for f in small_files)
        print(f"      总行数：{small_lines} 行")

    print(f"   中等文件（50-300 行）：{len(medium_files)} 个")
    if medium_files:
        medium_lines = sum(f['line_count'] for f in medium_files)
        print(f"      总行数：{medium_lines} 行")

    print(f"   大文件（> 300 行）：{len(large_files)} 个")
    if large_files:
        large_lines = sum(f['line_count'] for f in large_files)
        print(f"      总行数：{large_lines} 行")
        print(f"   ⚠️  大文件列表：")
        for f in large_files[:5]:
            print(f"      - {f['relative_path']} ({f['line_count']} 行)")
        if len(large_files) > 5:
            print(f"      ... 还有 {len(large_files) - 5} 个大文件")


def print_batch_plan(batches: List[Dict[str, Any]]):
    """打印翻译批次计划"""
    print("\n" + "="*70)
    print("📋 翻译批次计划")
    print("="*70)

    for i, batch in enumerate(batches, 1):
        print(f"\n批次 {batch['batch_number']} ({batch['total_lines']} 行, {batch['file_count']} 个文件)")

        for j, file_info in enumerate(batch['files'], 1):
            size_flag = ""
            if file_info.get('size_category') == 'large':
                size_flag = " [大文件]"
            elif file_info.get('size_category') == 'medium':
                size_flag = " [中等]"

            print(f"  {j}. {file_info['relative_path']}{size_flag}")
            print(f"     → {file_info['line_count']} 行")

        if batch.get('needs_segmentation'):
            print(f"  ⚠️  此批次包含超大文件，翻译时需要分段处理（每段不超过 2000 行）")


def main():
    if len(sys.argv) < 2:
        print("Usage: scan_batch_translation.py <directory>", file=sys.stderr)
        print("Example: scan_batch_translation.py core_products/real-time-voice-video/zh/flutter", file=sys.stderr)
        sys.exit(1)

    directory = sys.argv[1]
    base_dir = Path(directory)

    print(f"🔍 扫描目录：{directory}")

    # 扫描文件
    files = scan_directory(directory)

    if not files:
        print("\n❌ 未找到任何文件")
        sys.exit(0)

    # 分类文件
    categorized = categorize_files(files, base_dir)

    # 计算目标路径并添加到文件信息中
    all_files = (
        categorized['api_docs'] +
        categorized['yaml_pairs']['yaml_files'] +
        categorized['yaml_pairs']['mdx_files'] +
        categorized['reuse_docs'] +
        categorized['regular_docs']['small'] +
        categorized['regular_docs']['medium'] +
        categorized['regular_docs']['large']
    )

    for file_info in all_files:
        file_info['target_path'] = calculate_target_path(file_info['path'], base_dir)

    # 创建翻译批次（只包含需要翻译的文件）
    files_to_translate = (
        categorized['yaml_pairs']['yaml_files'] +
        categorized['reuse_docs'] +
        categorized['regular_docs']['small'] +
        categorized['regular_docs']['medium'] +
        categorized['regular_docs']['large']
    )

    batches = create_batches(categorized)

    # 计算统计信息
    total_files = len(files_to_translate)
    total_lines = sum(f['line_count'] for f in files_to_translate)

    # 打印结果
    print_summary(categorized, base_dir)
    print_batch_plan(batches)

    print(f"\n📊 翻译任务统计：")
    print(f"   需翻译文件数：{total_files}")
    print(f"   需翻译总行数：{total_lines}")
    print(f"   翻译批次数：{len(batches)}")

    # 输出 JSON 格式供后续处理
    print("\n" + "="*70)
    print("📄 JSON 输出")
    print("="*70)

    result = {
        'directory': directory,
        'summary': {
            'total_files': total_files,
            'total_lines': total_lines,
            'skipped_api_files': len(categorized['api_docs']),
            'skipped_mdx_files': len(categorized['yaml_pairs']['mdx_files']),
            'yaml_files_to_translate': len(categorized['yaml_pairs']['yaml_files']),
            'reuse_docs': len(categorized['reuse_docs']),
            'small_files': len(categorized['regular_docs']['small']),
            'medium_files': len(categorized['regular_docs']['medium']),
            'large_files': len(categorized['regular_docs']['large'])
        },
        'files': all_files,
        'batches': batches
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
