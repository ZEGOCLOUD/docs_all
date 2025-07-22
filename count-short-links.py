#!/usr/bin/env python3
"""
统计 Markdown / MDX 文件中的短链接出现次数。
短链接格式示例：
[下载示例源码](!DownloadDemo/DownloadDemo)
[快速开始 - 集成](!Integration/SDK_Integration)

使用方法：
1. 交互式：直接运行脚本，按照提示输入目标目录以及要排除的目录；
2. 命令行：python count_short_links.py -d <目录路径> -e <排除目录1> -e <排除目录2>

结果按出现次数降序输出，例如：
DownloadDemo/DownloadDemo  12次
Integration/SDK_Integration  8次
"""

import argparse
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import List

# 正则表达式：匹配形如 [xxx](!path/to/link) 的短链接，捕获括号内去掉惊叹号后的路径
SHORT_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(!([^\)]+)\)")


def parse_args() -> argparse.Namespace:
    """解析命令行参数，如果未提供目录路径，则稍后进行交互式输入。"""
    parser = argparse.ArgumentParser(
        description="统计指定目录（含子目录）中的短链接出现次数，可排除指定目录。"
    )
    parser.add_argument(
        "-d",
        "--dir",
        help="目标目录路径 (可选。不提供时将交互式输入)",
        default=None,
    )
    parser.add_argument(
        "-e",
        "--exclude",
        action="append",
        default=[],
        help="需要排除的目录 (可多次使用)"
    )
    return parser.parse_args()


def prompt_for_missing_args(args: argparse.Namespace) -> None:
    """对缺失的命令行参数进行交互式输入。"""
    if not args.dir:
        args.dir = input("请输入目标目录路径: ").strip()
    if not args.exclude:
        exclude_input = input("请输入要排除的目录 (以逗号分隔，留空则不排除): ").strip()
        if exclude_input:
            args.exclude = [e.strip() for e in exclude_input.split(',') if e.strip()]


def normalize_paths(base_dir: Path, paths: List[str]) -> List[Path]:
    """将排除目录转换为绝对路径，便于比较。"""
    normalized = []
    for p in paths:
        path_obj = (base_dir / p).resolve()
        normalized.append(path_obj)
    return normalized


def should_skip_dir(directory: Path, exclude_dirs: List[Path]) -> bool:
    """判断当前目录是否需要被排除。"""
    for ex in exclude_dirs:
        # 若当前目录是排除目录或位于排除目录之下
        try:
            if directory.resolve().is_relative_to(ex):  # Python 3.9+
                return True
        except AttributeError:
            # 兼容 Python <3.9
            try:
                directory.resolve().relative_to(ex)
                return True
            except ValueError:
                continue
    return False


def collect_short_links(root_dir: Path, exclude_dirs: List[Path]) -> Counter:
    """在 root_dir 下扫描文件，统计短链接出现次数。"""
    counts: Counter = Counter()
    for current_root, dirnames, filenames in os.walk(root_dir):
        current_path = Path(current_root)
        # 过滤要排除的子目录
        dirnames[:] = [d for d in dirnames if not should_skip_dir(current_path / d, exclude_dirs)]

        for filename in filenames:
            if not filename.lower().endswith((".md", ".mdx", ".markdown")):
                continue
            file_path = current_path / filename
            try:
                content = file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                # 跳过无法解码的文件
                continue
            for match in SHORT_LINK_PATTERN.findall(content):
                # 忽略 # 及其后的锚点部分，将其视为同一短链接
                base_link = match.split('#', 1)[0]
                counts[base_link] += 1
    return counts


def main() -> None:
    args = parse_args()
    prompt_for_missing_args(args)

    root_dir = Path(args.dir).expanduser().resolve()
    if not root_dir.is_dir():
        print(f"错误: 指定的目录不存在 -> {root_dir}")
        sys.exit(1)

    exclude_dirs = normalize_paths(root_dir, args.exclude)

    results = collect_short_links(root_dir, exclude_dirs)

    if not results:
        print("未找到任何短链接。")
        return

    # 统计总数
    total_occurrences = sum(results.values())
    unique_links = len(results)

    # 输出结果
    print("短链接统计：")
    print(f"  总出现次数（不去重）：{total_occurrences}")
    print(f"  短链接种类数（去重后）：{unique_links}")
    print("\n各短链接出现次数：")
    for link_path, count in results.most_common():
        print(f"{link_path}  {count}次")


if __name__ == "__main__":
    main()
