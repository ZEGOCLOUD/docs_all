#!/usr/bin/env python3
"""
查漏补缺：扫描英文实例的 sidebars.json，找出所有未翻译的文档

功能：
1. 读取英文实例目录下的 sidebars.json
2. 遍历所有 type="doc" 的节点
3. 检查节点的 label 是否包含中文字符
4. 如果包含中文，说明该文档未翻译
5. 根据 DOCUO 文档 ID 规则计算对应的 MDX 文件路径
6. 输出待翻译文件列表

使用场景：
- 批量翻译时某些文件被遗漏
- 部分文档翻译失败需要重试
- 检查翻译完成度

输出格式：
- 默认：完整的 scan_result.json 格式（用于翻译流程）
- --text：人类可读的文本格式（调试用）
- --json：简化的 JSON 格式（只包含基本信息）
"""

import sys
import json
import re
import argparse
from pathlib import Path
from typing import List, Dict, Any


def has_chinese(text: str) -> bool:
    """检查字符串是否包含中文字符"""
    return any('\u4e00' <= ch <= '\u9fff' for ch in text)


def convert_doc_id_to_path(doc_id: str, instance_dir: Path) -> Path:
    """
    根据 DOCUO 文档 ID 规则转换为 MDX 文件路径

    转换规则（从 DOCUO_CONFIG_GUIDE.md）：
    1. 文档 ID 相对于实例目录
    2. 无扩展名（.mdx）
    3. 小写 + 连字符（空格、下划线转连字符）
    4. 移除数字前缀（01-、02-）

    注意：这里的转换是反向的，从 doc_id 找到可能的文件名
    由于 doc_id 已经是转换后的格式（小写、连字符、无数字前缀），
    我们需要找到原始文件名

    策略：直接使用 doc_id + .mdx 作为文件名，因为 DOCUO 已经做了规范化
    """
    # doc_id 已经是小写、连字符的格式
    # 直接添加 .mdx 扩展名
    return instance_dir / f"{doc_id}.mdx"


def find_mdx_file(doc_id: str, instance_dir: Path) -> Path:
    """
    在实例目录中查找 doc_id 对应的 MDX 文件

    由于 doc_id 是经过规范化的（小写、连字符、无数字前缀），
    而实际文件名可能有数字前缀或不同的命名，我们需要智能匹配

    策略：
    1. 先尝试直接匹配（doc_id.mdx）
    2. 如果不存在，尝试带数字前缀的版本（01-doc_id.mdx, 02-doc_id.mdx）
    3. 如果还不存在，尝试在子目录中查找（doc_id 拆分为路径）
    """
    # 策略 1: 直接匹配
    direct_path = instance_dir / f"{doc_id}.mdx"
    if direct_path.exists():
        return direct_path

    # 策略 2: 尝试带数字前缀的文件
    for prefix_num in range(1, 100):  # 尝试 01- 到 99-
        prefixed_path = instance_dir / f"{prefix_num:02d}-{doc_id}.mdx"
        if prefixed_path.exists():
            return prefixed_path

    # 策略 3: doc_id 可能包含路径分隔符，拆分并查找
    if '/' in doc_id:
        # 例如：introduction/overview
        path_parts = doc_id.split('/')
        target_dir = instance_dir
        for i, part in enumerate(path_parts[:-1]):
            # 尝试在子目录中查找
            candidate_dir = target_dir / part
            if candidate_dir.is_dir():
                target_dir = candidate_dir
            else:
                # 尝试带数字前缀的目录名
                found = False
                for prefix_num in range(1, 100):
                    if (target_dir / f"{prefix_num:02d}-{part}").is_dir():
                        target_dir = target_dir / f"{prefix_num:02d}-{part}"
                        found = True
                        break
                if not found:
                    return None  # 找不到

        # 现在查找最后的文件
        filename = path_parts[-1]

        # 尝试直接文件名
        file_path = target_dir / f"{filename}.mdx"
        if file_path.exists():
            return file_path

        # 尝试带数字前缀的文件名
        for prefix_num in range(1, 100):
            prefixed_file = target_dir / f"{prefix_num:02d}-{filename}.mdx"
            if prefixed_file.exists():
                return prefixed_file

    # 所有策略都失败
    return None


def scan_sidebar_for_untranslated(sidebars_path: Path) -> List[Dict[str, Any]]:
    """
    扫描 sidebars.json 文件，找出所有未翻译的文档

    Args:
        sidebars_path: sidebars.json 文件路径

    Returns:
        未翻译文档列表，每个元素包含：
        {
            "doc_id": "文档ID",
            "label": "当前标签（中文）",
            "mdx_path": "MDX 文件路径",
            "sidebar_path": "sidebars.json 路径",
            "exists": "MDX 文件是否存在"
        }
    """
    if not sidebars_path.exists():
        print(f"Error: sidebars.json not found at {sidebars_path}", file=sys.stderr)
        return []

    # 读取 sidebars.json
    with open(sidebars_path, 'r', encoding='utf-8') as f:
        sidebars = json.load(f)

    # 获取实例目录（sidebars.json 所在目录）
    instance_dir = sidebars_path.parent

    untranslated = []

    def process_sidebar_item(item: Any, path: str = ""):
        """递归处理侧边栏项"""
        if not isinstance(item, dict):
            return

        item_type = item.get('type')

        if item_type == 'doc' and 'id' in item:
            doc_id = item['id']
            label = item.get('label', '')

            # 检查 label 是否包含中文
            if has_chinese(label):
                # 查找对应的 MDX 文件
                mdx_path = find_mdx_file(doc_id, instance_dir)

                untranslated.append({
                    'doc_id': doc_id,
                    'label': label,
                    'mdx_path': str(mdx_path) if mdx_path else None,
                    'sidebar_path': str(sidebars_path),
                    'exists': mdx_path is not None and mdx_path.exists(),
                    'path_in_sidebar': path
                })

        # 递归处理分类和子项
        if 'items' in item and isinstance(item['items'], list):
            category_label = item.get('label', '')
            current_path = f"{path} > {category_label}" if path else category_label
            for sub_item in item['items']:
                process_sidebar_item(sub_item, current_path)

    # 遍历所有侧边栏
    for sidebar_name, items in sidebars.items():
        if isinstance(items, list):
            for item in items:
                process_sidebar_item(item, sidebar_name)

    return untranslated


def check_instance_directory(instance_dir: Path) -> List[Dict[str, Any]]:
    """
    检查单个实例目录

    Args:
        instance_dir: 实例目录路径（包含 sidebars.json）

    Returns:
        未翻译文档列表
    """
    sidebars_path = instance_dir / 'sidebars.json'

    if not sidebars_path.exists():
        print(f"Warning: No sidebars.json found in {instance_dir}", file=sys.stderr)
        return []

    return scan_sidebar_for_untranslated(sidebars_path)


def convert_to_scan_result_format(
    missing_data: List[Dict[str, Any]],
    en_instance_dir: Path
) -> Dict[str, Any]:
    """
    将查漏补缺结果转换为 scan_result.json 格式

    Args:
        missing_data: 从 scan_sidebar_for_untranslated 获取的数据
        en_instance_dir: 英文实例目录路径

    Returns:
        scan_result.json 格式的数据
    """
    # 推断中文源目录
    instance_path_str = str(en_instance_dir)
    if '/en/' in instance_path_str:
        zh_source_str = instance_path_str.replace('/en/', '/zh/')
    elif instance_path_str.endswith('/en'):
        zh_source_str = instance_path_str[:-3] + '/zh'
    else:
        print(f"Warning: Cannot infer Chinese source directory from {en_instance_dir}", file=sys.stderr)
        zh_source_str = instance_path_str.replace('/en/', '/zh/')

    zh_source = Path(zh_source_str)

    converted_files = []

    for file_info in missing_data:
        mdx_path = Path(file_info['mdx_path']) if file_info.get('mdx_path') else None
        doc_id = file_info['doc_id']

        if not mdx_path:
            continue

        # 计算对应的中文源文件路径
        path_str = str(mdx_path)
        if '/en/' in path_str:
            zh_path_str = path_str.replace('/en/', '/zh/')
        else:
            print(f"Warning: Cannot determine Chinese source path for {mdx_path}", file=sys.stderr)
            continue

        zh_path = Path(zh_path_str)

        # 读取文件行数
        line_count = 0
        try:
            with open(mdx_path, 'r', encoding='utf-8') as f:
                line_count = len(f.readlines())
        except Exception as e:
            print(f"Warning: Cannot read {mdx_path}: {e}", file=sys.stderr)
            line_count = 0

        # 判断文档类型
        doc_type = 'normal'  # 默认

        # 检查是否是 API 文档
        if 'api-reference' in doc_id:
            doc_type = 'API'

        # 检查是否是复用文档（import Content）
        try:
            with open(mdx_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if "import Content from" in content and "import" in content.split("import Content")[1][:200]:
                    doc_type = 'reuse'
        except:
            pass

        # 创建 scan_result 格式条目
        entry = {
            'source': str(zh_path),
            'target': str(mdx_path),
            'relative_path': doc_id,
            'line_count': line_count,
            'docType': doc_type,
            'missing_translation': True,
            'sidebar_label': file_info.get('label', ''),
        }

        converted_files.append(entry)

    # 创建统计摘要
    summary = {
        'total_files': len(converted_files),
        'total_lines': sum(f.get('line_count', 0) for f in converted_files),
        'api_docs': len([f for f in converted_files if f.get('docType') == 'API']),
        'yaml_mdx_pairs': 0,
        'reuse_docs': len([f for f in converted_files if f.get('docType') == 'reuse']),
        'normal_docs': len([f for f in converted_files if f.get('docType') == 'normal']),
        'missing_translations': len(converted_files),
    }

    return {
        'files': converted_files,
        'summary': summary
    }


def main():
    parser = argparse.ArgumentParser(
        description='查漏补缺：扫描英文实例的 sidebars.json，找出所有未翻译的文档',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例：
  %(prog)s core_products/real-time-voice-video/en/android-java
  %(prog)s core_products/real-time-voice-video/en/android-java --output-dir custom/path
  %(prog)s core_products/real-time-voice-video/en/android-java --text
  %(prog)s core_products/real-time-voice-video/en/android-java --stdout > scan_result.json
        '''
    )

    parser.add_argument('instance_dir', help='英文实例目录路径（包含 sidebars.json）')
    parser.add_argument('--output-dir', help='输出目录路径（默认使用实例目录）')
    parser.add_argument('--output-file', default='scan_result.json', help='输出文件名（默认：scan_result.json）')
    parser.add_argument('--stdout', action='store_true', help='输出到 stdout 而不是文件（兼容旧版本）')
    parser.add_argument('--text', action='store_true', help='人类可读的文本格式（调试用）')
    parser.add_argument('--json', action='store_true', help='简化的 JSON 格式（只包含基本信息）')

    args = parser.parse_args()

    # 确定输出格式
    if args.text:
        output_format = 'text'
    elif args.json:
        output_format = 'json'
    else:
        output_format = 'scan'  # 默认 scan_result.json 格式

    instance_dir = Path(args.instance_dir)

    if not instance_dir.exists():
        print(f"Error: Directory '{instance_dir}' does not exist", file=sys.stderr)
        sys.exit(1)

    # 计算输出目录
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        # 默认使用实例目录
        output_dir = instance_dir

    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)

    # 判断是单个实例目录还是包含多个实例的目录
    sidebars_path = instance_dir / 'sidebars.json'

    results = []

    if sidebars_path.exists():
        # 单个实例目录
        results = check_instance_directory(instance_dir)
    else:
        # 可能是包含多个实例的目录（如 /en/）
        # 查找所有子目录中的 sidebars.json
        for sidebars_file in sorted(instance_dir.rglob('sidebars.json')):
            instance_path = sidebars_file.parent
            instance_results = check_instance_directory(instance_path)
            results.extend(instance_results)

    # 统计信息
    existing_files = [r for r in results if r['exists']]
    missing_files = [r for r in results if not r['exists']]

    # 输出结果
    if output_format == 'scan':
        # 完整的 scan_result.json 格式输出（默认，用于翻译流程）
        scan_result = convert_to_scan_result_format(results, instance_dir)
        scan_result['directory'] = str(instance_dir)
        scan_result['target_directory'] = str(output_dir)

        if args.stdout:
            # 兼容旧版本：输出到 stdout
            print(json.dumps(scan_result, ensure_ascii=False, indent=2))
        else:
            # 新版本：保存到文件
            output_file = output_dir / args.output_file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(scan_result, f, indent=2, ensure_ascii=False)

            print(f"🔍 扫描完成：找到 {len(results)} 个未翻译文档")
            print(f"📁 输出目录：{output_dir}")
            print(f"✅ 扫描结果已保存：{output_file}")

    elif output_format == 'text':
        # 文本格式输出（用于人类阅读，调试用）
        if not results:
            print("✅ All documents are translated! No missing translations found.")
            return 0

        print(f"Found {len(results)} untranslated documents:\n")

        print("Summary:")
        print(f"  - Total untranslated: {len(results)}")
        print(f"  - Files exist (can be translated): {len(existing_files)}")
        print(f"  - Files missing (need investigation): {len(missing_files)}")

        print("\n" + "=" * 80)
        print("Untranslated documents:")
        print("=" * 80)

        for i, doc in enumerate(results, 1):
            status = "✓" if doc['exists'] else "✗"
            print(f"\n{i}. [{status}] {doc['label']}")
            print(f"   Doc ID: {doc['doc_id']}")
            print(f"   MDX Path: {doc['mdx_path'] or 'Not found'}")
            if doc.get('path_in_sidebar'):
                print(f"   Sidebar Path: {doc['path_in_sidebar']}")

        print("\n" + "=" * 80)
        print(f"\nLegend: [✓] File exists, [✗] File missing")

    elif output_format == 'json':
        # 简化的 JSON 格式输出（只包含基本信息）
        output_data = {
            'summary': {
                'total': len(results),
                'existing': len(existing_files),
                'missing': len(missing_files)
            },
            'files': results
        }

        if args.stdout:
            print(json.dumps(output_data, ensure_ascii=False, indent=2))
        else:
            output_file = output_dir / args.output_file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            print(f"✅ 结果已保存：{output_file}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
