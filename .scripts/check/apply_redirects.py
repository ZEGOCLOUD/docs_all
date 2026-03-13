#!/usr/bin/env python3
"""
根据 check_redirect_result.json 的重定向结果，自动替换文档中的旧链接。

将 redirected: true 且 status_code: 200 的 original_url 替换为 url_path。
"""

import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple


def load_redirect_results(result_file: str) -> List[Dict]:
    """
    加载重定向检查结果，过滤出需要替换的条目。

    Args:
        result_file: check_redirect_result.json 文件路径

    Returns:
        需要替换的条目列表
    """
    with open(result_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 过滤：redirected=true 且 status_code=200
    replacements = []
    for item in data.get("urls", []):
        if item.get("redirected") and item.get("status_code") == 200:
            replacements.append({
                "original_url": item["original_url"],
                "url_path": item["url_path"],
                "count": item.get("count", 0)
            })

    return replacements


def find_mdx_files(root_dir: Path) -> List[Path]:
    """
    递归查找所有 MDX 文件。

    Args:
        root_dir: 根目录

    Returns:
        MDX 文件路径列表
    """
    return list(root_dir.rglob("*.mdx"))


def replace_urls_in_file(
    file_path: Path,
    replacements: List[Dict],
    dry_run: bool = False
) -> Dict[str, int]:
    """
    在单个文件中替换 URL。

    Args:
        file_path: 文件路径
        replacements: 替换规则列表
        dry_run: 是否只预览不实际修改

    Returns:
        替换统计信息
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content
    stats = {"total_replaced": 0, "by_url": {}}

    for item in replacements:
        original_url = item["original_url"]
        url_path = item["url_path"]

        # 统计原始 URL 出现次数
        count = content.count(original_url)
        if count > 0:
            # 直接字符串替换（完全匹配）
            new_content = content.replace(original_url, url_path)

            if new_content != content:
                actual_replaced = content.count(original_url)
                stats["total_replaced"] += actual_replaced
                stats["by_url"][original_url] = actual_replaced
                content = new_content

    # 如果有替换且不是 dry_run，写回文件
    if stats["total_replaced"] > 0 and not dry_run:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    return stats


def apply_replacements(
    result_file: str = None,
    root_dir: str = None,
    dry_run: bool = False,
    verbose: bool = False
) -> Dict:
    """
    应用所有重定向替换。

    Args:
        result_file: check_redirect_result.json 文件路径
        root_dir: 文档根目录
        dry_run: 是否只预览不实际修改
        verbose: 是否输出详细信息

    Returns:
        总体统计信息
    """
    if result_file is None:
        result_file = Path(__file__).parent / "check_redirect_result.json"
    else:
        result_file = Path(result_file)

    if root_dir is None:
        # 默认为 docs_all_1 根目录
        root_dir = Path(__file__).parent.parent.parent
    else:
        root_dir = Path(root_dir)

    print(f"加载重定向结果: {result_file}")
    replacements = load_redirect_results(result_file)
    print(f"找到 {len(replacements)} 个需要替换的 URL\n")

    if verbose:
        print("替换规则:")
        for item in replacements:
            print(f"  {item['original_url']}")
            print(f"    → {item['url_path']}")
        print()

    # 查找所有 MDX 文件
    mdx_files = find_mdx_files(root_dir)
    print(f"找到 {len(mdx_files)} 个 MDX 文件\n")

    # 统计信息
    total_stats = {
        "files_modified": 0,
        "total_replacements": 0,
        "by_url": {},
        "file_details": []
    }

    # 处理每个文件
    for file_path in mdx_files:
        stats = replace_urls_in_file(file_path, replacements, dry_run)

        if stats["total_replaced"] > 0:
            total_stats["files_modified"] += 1
            total_stats["total_replacements"] += stats["total_replaced"]

            # 合并 URL 统计
            for url, count in stats["by_url"].items():
                if url not in total_stats["by_url"]:
                    total_stats["by_url"][url] = 0
                total_stats["by_url"][url] += count

            file_detail = {
                "file": str(file_path.relative_to(root_dir)),
                "replacements": stats["total_replaced"],
                "urls": stats["by_url"]
            }
            total_stats["file_details"].append(file_detail)

            if verbose:
                print(f"  {file_path.relative_to(root_dir)}: {stats['total_replaced']} 处替换")

    # 输出汇总
    print("=" * 60)
    print(f"{'[DRY RUN] ' if dry_run else ''}替换汇总:")
    print(f"  修改文件数: {total_stats['files_modified']}")
    print(f"  总替换次数: {total_stats['total_replacements']}")
    print()

    if total_stats["by_url"]:
        print("各 URL 替换次数:")
        for url, count in sorted(total_stats["by_url"].items(), key=lambda x: -x[1]):
            # 找到对应的替换目标
            target = next((r["url_path"] for r in replacements if r["original_url"] == url), "?")
            print(f"  {url} → {target}")
            print(f"    替换: {count} 处")

    return total_stats


def main():
    parser = argparse.ArgumentParser(
        description="根据重定向结果自动替换文档中的旧链接"
    )
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help="check_redirect_result.json 文件路径"
    )
    parser.add_argument(
        "--root",
        type=str,
        default=None,
        help="文档根目录（默认为 docs_all_1 根目录）"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只预览不实际修改"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="输出详细信息"
    )

    args = parser.parse_args()

    apply_replacements(
        result_file=args.input,
        root_dir=args.root,
        dry_run=args.dry_run,
        verbose=args.verbose
    )


if __name__ == "__main__":
    main()
