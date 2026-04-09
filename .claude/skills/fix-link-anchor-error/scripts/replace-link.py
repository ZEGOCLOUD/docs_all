#!/usr/bin/env python3
"""在整个仓库范围内对指定锚点链接做全局搜索替换。

仅支持内部 URL 路径链接和纯页内锚点，不支持相对路径链接。
相对路径链接（./file.mdx#anchor）因根据源文件位置不同解析结果不同，
全局替换会误伤其他平台的有效链接，必须逐文件手动修复。

Usage:
    python3 replace-link.py <old-link> <new-link> [--zh] [--dry-run]

Arguments:
    <old-link>   含旧锚点的完整链接，仅允许：
                   /instance/path#old-anchor   （内部 URL 路径）
                   #old-anchor                 （纯页内锚点）
    <new-link>   替换后的完整链接
    --zh         仅替换中文文件（路径含 /zh/ 或 _zh 的文件）；
                 不传此参数则仅替换英文文件
    --dry-run    仅打印将要修改的文件，不实际写入

搜索范围：仓库下所有 .mdx、.md、.yaml、.yml 文件（跳过隐藏目录和 node_modules）。
"""

import os
import sys
import argparse
from pathlib import Path

TARGET_EXTENSIONS = {'.mdx', '.md', '.yaml', '.yml'}
SKIP_DIRS = {'node_modules', '__pycache__'}


def _find_repo_root() -> str:
    """从脚本自身位置向上查找包含 docuo.config.json 的仓库根目录。"""
    current = Path(os.path.abspath(__file__)).parent
    while True:
        if (current / 'docuo.config.json').exists():
            return str(current)
        parent = current.parent
        if parent == current:
            return os.getcwd()
        current = parent


def _detect_file_lang(path: str) -> str:
    """检测文件所属语言分区。返回 'zh'、'en' 或 'neutral'（不属于任何语言分区）。"""
    normalized = path.replace('\\', '/')
    if '/zh/' in normalized or '_zh' in normalized:
        return 'zh'
    if '/en/' in normalized or '_en' in normalized:
        return 'en'
    return 'neutral'


def iter_files(root: str, zh_only: bool):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames
            if not d.startswith('.') and d not in SKIP_DIRS
        ]
        for fname in filenames:
            if os.path.splitext(fname)[1].lower() in TARGET_EXTENSIONS:
                fpath = os.path.join(dirpath, fname)
                lang = _detect_file_lang(fpath)
                # neutral 文件（不属于任何语言分区）两种模式都包含
                if lang == 'neutral' or (lang == 'zh') == zh_only:
                    yield fpath


def main():
    parser = argparse.ArgumentParser(description='全局替换锚点链接（不支持相对路径链接）')
    parser.add_argument('old_link', help='旧链接（内部URL路径或纯锚点，不可为相对路径）')
    parser.add_argument('new_link', help='新链接（完整）')
    parser.add_argument('--zh', action='store_true',
                        help='仅替换中文文件（路径含 /zh/ 或 _zh）；不传则仅替换英文文件')
    parser.add_argument('--dry-run', action='store_true',
                        help='仅显示将要修改的文件，不实际写入')
    args = parser.parse_args()

    old_link = args.old_link
    new_link = args.new_link

    # 拒绝相对路径链接
    if old_link.startswith('./') or old_link.startswith('../'):
        print("Error: Relative links cannot be globally replaced.")
        print("Reason: the same relative path resolves to different files in different")
        print("directories, so a global replace would corrupt valid links in other platforms.")
        print("Fix relative-link anchors manually in each affected file.")
        sys.exit(1)

    if old_link == new_link:
        print("Nothing to replace: old and new links are identical.")
        sys.exit(0)

    repo_root = _find_repo_root()
    lang_label = "zh" if args.zh else "en"
    print(f"Replacing: {old_link!r}  →  {new_link!r}")
    print(f"Language filter: {lang_label}")
    print(f"Scanning repo: {repo_root}\n")

    changed: list[tuple[str, int]] = []
    for fpath in iter_files(repo_root, zh_only=args.zh):
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue

        if old_link not in content:
            continue

        count = content.count(old_link)
        rel = os.path.relpath(fpath, repo_root)
        changed.append((rel, count))

        if not args.dry_run:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content.replace(old_link, new_link))

    if not changed:
        print("No occurrences found. Nothing changed.")
        return

    prefix = "[dry-run] " if args.dry_run else ""
    print(f"{prefix}Modified {len(changed)} file(s):")
    for rel, cnt in changed:
        print(f"  {rel}  ({cnt} occurrence{'s' if cnt > 1 else ''})")


if __name__ == '__main__':
    main()
