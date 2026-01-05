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
"""

import sys
import json
import re
from pathlib import Path
from typing import List, Dict, Any


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
            project_root = Path.cwd()
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
    if len(sys.argv) < 2:
        print("Usage: preprocess_reuse_docs.py <scan_result.json>", file=sys.stderr)
        print("Example: preprocess_reuse_docs.py scan_result.json", file=sys.stderr)
        sys.exit(1)

    scan_result_file = sys.argv[1]

    # 读取扫描结果
    try:
        with open(scan_result_file, 'r', encoding='utf-8') as f:
            scan_result = json.load(f)
    except Exception as e:
        print(f"Error: Failed to read scan result file: {e}", file=sys.stderr)
        sys.exit(1)

    # 提取全复用文档
    reuse_docs = [f for f in scan_result.get('files', []) if f.get('is_reuse_doc', False)]

    if not reuse_docs:
        print(json.dumps([], ensure_ascii=False))
        sys.exit(0)

    # 预处理全复用文档
    results = preprocess_reuse_docs(reuse_docs)

    # 输出结果（纯 JSON）
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
