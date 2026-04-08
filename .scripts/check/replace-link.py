#!/usr/bin/env python3
"""在整个仓库范围内对指定链接做全局搜索替换（替换完整链接，含锚点）。

Usage:
    python3 replace-link.py <old-link> <new-link> [--dry-run]

Arguments:
    <old-link>   需要替换的旧链接（完整链接，可含锚点），例如：
                   /real-time-video-android/introduction/overview
                   /aiagent-android/quick-start#prerequisites
                   ./some-file.mdx
    <new-link>   替换后的新链接（完整链接）
    --dry-run    仅打印将要修改的文件，不实际写入

搜索范围：仓库下所有 .mdx、.md、.yaml、.yml 文件（跳过隐藏目录和 node_modules）。
"""

import os
import sys
import argparse

REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

TARGET_EXTENSIONS = {'.mdx', '.md', '.yaml', '.yml'}
SKIP_DIRS = {'node_modules', '__pycache__'}


def iter_files(root: str):
    """遍历仓库中所有目标文件，跳过隐藏目录和 node_modules。"""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames
            if not d.startswith('.') and d not in SKIP_DIRS
        ]
        for fname in filenames:
            if os.path.splitext(fname)[1].lower() in TARGET_EXTENSIONS:
                yield os.path.join(dirpath, fname)


def main():
    parser = argparse.ArgumentParser(description='全局替换完整链接')
    parser.add_argument('old_link', help='旧链接（完整，可含锚点）')
    parser.add_argument('new_link', help='新链接（完整，可含锚点）')
    parser.add_argument('--dry-run', action='store_true',
                        help='仅显示将要修改的文件，不实际写入')
    args = parser.parse_args()

    old_link = args.old_link
    new_link = args.new_link

    if old_link == new_link:
        print("Nothing to replace: old and new links are identical.")
        sys.exit(0)

    print(f"Replacing: {old_link!r}  →  {new_link!r}")
    print(f"Scanning repo: {REPO_ROOT}\n")

    changed: list[tuple[str, int]] = []
    for fpath in iter_files(REPO_ROOT):
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue

        if old_link not in content:
            continue

        count = content.count(old_link)
        rel = os.path.relpath(fpath, REPO_ROOT)
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
