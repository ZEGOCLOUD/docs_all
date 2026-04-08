#!/usr/bin/env python3
"""在 MDX 文件中为指定元素插入新锚点 ID。

Usage:
    python3 add-anchor.py <mdx-file> --type <type> --value <value> --new-id <new-id>

Arguments:
    <mdx-file>   MDX 文件路径（相对仓库根目录或绝对路径）
    --type       锚点类型: md_heading | a_tag | h_tag | step | param_field
    --value      collect-valid-anchors.py 返回的锚点 value 字段
    --new-id     新锚点 ID（只允许小写 ASCII 字母、数字和连字符）

Behavior:
    - md_heading: 在对应 Markdown 标题行末尾追加 <a id="new-id" />
    - a_tag:      在含有该 <a id="value"> 的行末尾追加 <a id="new-id" />
    - h_tag:      在含有该 <hN id="value"> 的行末尾追加 <a id="new-id" />
    - step:       不支持，跳过并提示
    - param_field:不支持，跳过并提示
"""

import os
import sys
import re
import argparse

_SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.normpath(os.path.join(_SKILL_DIR, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO_ROOT, '.scripts', 'check'))
from check_links import heading_to_anchor
_VALID_ID_RE = re.compile(r'^[a-z0-9][a-z0-9-]*$')


def _resolve_path(path: str) -> str:
    if not os.path.isabs(path):
        # 优先从当前工作目录解析相对路径，兜底用仓库根目录
        candidate = os.path.normpath(os.path.join(os.getcwd(), path))
        if os.path.exists(candidate):
            return candidate
        return os.path.normpath(os.path.join(REPO_ROOT, path))
    return os.path.normpath(path)


def _find_md_heading_line(lines: list, anchor_value: str) -> int:
    """返回与 anchor_value 匹配的 Markdown 标题行下标（0-based），未找到返回 -1。

    处理重复标题：check_links 约定首个标题产生 value 和 value-1，
    第 n 个重复产生 value-n（n >= 2）。
    """
    m = re.match(r'^(.+)-(\d+)$', anchor_value)
    if m:
        base, n = m.group(1), int(m.group(2))
        target_base = base
        target_occ = 1 if n == 1 else n   # -1 → 1st occ, -2 → 2nd occ
    else:
        target_base = anchor_value
        target_occ = 1

    occ = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith('#'):
            continue
        text = stripped.lstrip('#').strip()
        if text and heading_to_anchor(text) == target_base:
            occ += 1
            if occ == target_occ:
                return i
    return -1


def _find_tag_line(lines: list, tag_pattern: re.Pattern) -> int:
    for i, line in enumerate(lines):
        if tag_pattern.search(line):
            return i
    return -1


def _append_anchor_to_line(lines: list, idx: int, new_id: str) -> tuple:
    """在 lines[idx] 末尾（保留换行符）追加 <a id="new-id" />。"""
    line = lines[idx]
    if f'id="{new_id}"' in line or f"id='{new_id}'" in line:
        return False, f'Anchor id="{new_id}" already exists on line {idx + 1}.'
    core = line.rstrip('\r\n')
    eol = line[len(core):]
    lines[idx] = core + f' <a id="{new_id}" />' + eol
    return True, None


def main():
    parser = argparse.ArgumentParser(description='在 MDX 文件中插入锚点')
    parser.add_argument('file', help='MDX 文件路径')
    parser.add_argument('--type', required=True, dest='anchor_type',
                        choices=['md_heading', 'a_tag', 'h_tag', 'step', 'param_field'])
    parser.add_argument('--value', required=True, dest='anchor_value',
                        help='collect-valid-anchors.py 返回的锚点 value')
    parser.add_argument('--new-id', required=True, dest='new_id',
                        help='新锚点 ID（小写 ASCII 字母/数字/连字符）')
    args = parser.parse_args()

    # 不支持的类型直接跳过
    if args.anchor_type in ('step', 'param_field'):
        print(f"Skipped: type '{args.anchor_type}' does not support anchor insertion.")
        sys.exit(0)

    if not _VALID_ID_RE.match(args.new_id):
        print(f"Error: --new-id must match [a-z0-9][a-z0-9-]*. Got: {args.new_id!r}")
        sys.exit(1)

    file_path = _resolve_path(args.file)
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    t = args.anchor_type
    v = args.anchor_value
    new_id = args.new_id

    if t == 'md_heading':
        idx = _find_md_heading_line(lines, v)
        if idx == -1:
            print(f"Error: No markdown heading with anchor value '{v}' found.")
            sys.exit(1)

    elif t == 'a_tag':
        pat = re.compile(
            r'<a\b(?:[^>"\']*|"[^"]*"|\'[^\']*\')*\bid\s*=\s*[\'"]' + re.escape(v) + r'[\'"]',
            re.IGNORECASE,
        )
        idx = _find_tag_line(lines, pat)
        if idx == -1:
            print(f"Error: No <a id=\"{v}\"> found in file.")
            sys.exit(1)

    elif t == 'h_tag':
        pat = re.compile(
            r'<h[1-6]\b(?:[^>"\']*|"[^"]*"|\'[^\']*\')*\bid\s*=\s*[\'"]' + re.escape(v) + r'[\'"]',
            re.IGNORECASE,
        )
        idx = _find_tag_line(lines, pat)
        if idx == -1:
            print(f"Error: No <h1-h6 id=\"{v}\"> found in file.")
            sys.exit(1)

    ok, err = _append_anchor_to_line(lines, idx, new_id)
    if not ok:
        print(f"Notice: {err}")
        sys.exit(0)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f'Success: Added <a id="{new_id}" /> at line {idx + 1} in {file_path}')


if __name__ == '__main__':
    main()
