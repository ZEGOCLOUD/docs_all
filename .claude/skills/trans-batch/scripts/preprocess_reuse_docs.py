#!/usr/bin/env python3
"""
预处理全复用文档，尝试替换引用路径

全复用文档特征：
- 除了 frontmatter 外只有两行非空内容
- 一行以 import Content from 开头
- 另一行以 <Content 开头

处理逻辑：
1. 提取 import 路径
2. 将路径中的 /zh/ 替换为 /en/
3. 检查对应的英文文档是否存在
4. 如果存在：替换路径并保存，标记为"已解决"
5. 如果不存在：标记为"需要翻译"

IMPORTANT: 此脚本必须在 workspace 根目录下运行。
"""

import sys
import json
import re
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional


def get_workspace_root() -> Path:
    """
    Find the workspace root directory by looking for marker files.

    Marker files (in order of priority):
    - docuo.config.json or docuo.config.en.json (DOCUO project)
    - .git (Git repository)
    - package.json (Node.js project)

    Returns:
        Path: workspace root directory

    Note:
        Falls back to current directory if no markers found.
    """
    current = Path.cwd().resolve()

    # Search up to 10 levels up
    for _ in range(10):
        markers = [
            'docuo.config.json',
            'docuo.config.en.json',
            '.git',
            'package.json'
        ]

        for marker in markers:
            if (current / marker).exists():
                return current

        parent = current.parent
        if parent == current:  # Reached root
            break
        current = parent

    # Fallback to current directory if no markers found
    return Path.cwd()


def extract_import_path(content: str) -> str:
    """
    提取 import 路径

    Args:
        content: 文件内容

    Returns:
        str: import 路径，如果未找到则返回 None
    """
    # 匹配 import Content from "..."; 或 import Content from '...';
    match = re.search(r'import Content from ["\'](.+?)["\']', content)
    if match:
        return match.group(1)
    return None


def replace_import_path(content: str, old_path: str, new_path: str) -> str:
    """
    替换 import 路径

    Args:
        content: 文件内容
        old_path: 原始路径
        new_path: 新路径

    Returns:
        str: 替换后的内容
    """
    return content.replace(old_path, new_path)


def process_reuse_doc(file_path: Path, target_path: Path) -> Dict[str, Any]:
    """
    处理单个全复用文档

    Args:
        file_path: 源文件路径
        target_path: 目标文件路径

    Returns:
        dict: 处理结果
    """
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取 import 路径
        import_path = extract_import_path(content)
        if not import_path:
            return {
                'source': str(file_path),
                'target': str(target_path),
                'status': 'failed',
                'reason': 'no_import_found',
                'line_count': len(content.splitlines())
            }

        # 替换路径中的 /zh/ 为 /en/
        new_import_path = import_path.replace('/zh/', '/en/')

        # 计算英文文档的绝对路径
        # import 路径是绝对路径（以 / 开头），需要相对于项目根目录解析
        if import_path.startswith('/'):
            # 绝对路径：相对于工作目录（项目根目录）
            project_root = get_workspace_root()
            new_import_path_abs = project_root / new_import_path.lstrip('/')
        else:
            # 相对路径：相对于文件所在目录
            source_dir = file_path.parent
            new_import_path_abs = (source_dir / new_import_path).resolve()

        # 检查英文文档是否存在
        if not new_import_path_abs.exists():
            return {
                'source': str(file_path),
                'target': str(target_path),
                'status': 'need_translate',
                'original_import_path': import_path,
                'new_import_path': new_import_path,
                'reason': 'en_doc_not_found',
                'line_count': len(content.splitlines())
            }

        # 替换路径并保存
        new_content = replace_import_path(content, import_path, new_import_path)

        # 确保目标目录存在
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # 写入目标文件
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return {
            'source': str(file_path),
            'target': str(target_path),
            'status': 'resolved',
            'original_import_path': import_path,
            'new_import_path': new_import_path,
            'resolved_to': str(new_import_path_abs),
            'line_count': len(content.splitlines())
        }

    except Exception as e:
        return {
            'source': str(file_path),
            'target': str(target_path),
            'status': 'failed',
            'reason': str(e),
            'line_count': 0
        }


def preprocess_reuse_docs(reuse_docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    批量预处理全复用文档

    Args:
        reuse_docs: 全复用文档列表

    Returns:
        list: 处理结果列表
    """
    results = []

    for file_info in reuse_docs:
        file_path = Path(file_info['path'])
        target_path = Path(file_info['target_path'])

        result = process_reuse_doc(file_path, target_path)
        results.append(result)

    return results


def main():
    parser = argparse.ArgumentParser(
        description='预处理全复用文档，尝试替换引用路径',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例：
  %(prog)s scan_result.json
  %(prog)s scan_result.json --output-dir core_products/real-time-voice-video/en/flutter
  %(prog)s scan_result.json --output-file custom/path/preprocess.json
        '''
    )

    parser.add_argument('scan_result', help='扫描结果文件路径（scan_result.json）')
    parser.add_argument('--output-dir', help='输出目录路径（默认从 scan_result.json 的 target_directory 字段读取）')
    parser.add_argument('--output-file', default='preprocess_result.json', help='输出文件名（默认：preprocess_result.json）')
    parser.add_argument('--stdout', action='store_true', help='输出到 stdout 而不是文件（兼容旧版本）')

    args = parser.parse_args()

    scan_result_file = args.scan_result

    # 读取扫描结果
    try:
        with open(scan_result_file, 'r', encoding='utf-8') as f:
            scan_result = json.load(f)
    except Exception as e:
        print(f"Error: Failed to read scan result file: {e}", file=sys.stderr)
        sys.exit(1)

    # 计算输出目录
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        # 从 scan_result.json 中读取 target_directory
        target_directory = scan_result.get('target_directory')
        if target_directory:
            output_dir = Path(target_directory)
        else:
            # 兼容旧版本：如果没有 target_directory 字段，使用 scan_result 文件所在目录
            output_dir = Path(scan_result_file).parent

    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"📂 输入文件：{scan_result_file}")
    print(f"📁 输出目录：{output_dir}")

    # 提取全复用文档
    reuse_docs = [f for f in scan_result.get('files', []) if f.get('is_reuse_doc', False)]

    if not reuse_docs:
        print("\n⚠️  未找到全复用文档")
        results = []
    else:
        print(f"🔄 找到 {len(reuse_docs)} 个全复用文档，开始预处理...")

        # 预处理全复用文档
        results = preprocess_reuse_docs(reuse_docs)

        # 统计结果
        resolved_count = sum(1 for r in results if r['status'] == 'resolved')
        need_translate_count = sum(1 for r in results if r['status'] == 'need_translate')
        failed_count = sum(1 for r in results if r['status'] == 'failed')

        print(f"\n📊 预处理结果：")
        print(f"   ✅ 已解决：{resolved_count} 个")
        print(f"   🔀 需翻译：{need_translate_count} 个")
        print(f"   ❌ 失败：{failed_count} 个")

    # 输出结果
    if args.stdout:
        # 兼容旧版本：输出到 stdout
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        # 新版本：保存到文件
        output_file = output_dir / args.output_file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"\n✅ 预处理结果已保存：{output_file}")


if __name__ == '__main__':
    main()
