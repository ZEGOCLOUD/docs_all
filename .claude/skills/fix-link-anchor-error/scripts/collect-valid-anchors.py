#!/usr/bin/env python3
"""收集 MDX 文件中所有有效锚点，输出带类型信息的 JSON。

Usage:
    python3 collect-valid-anchors.py <mdx-file-path>

    <mdx-file-path> 可以是相对于仓库根目录的相对路径，也可以是绝对路径。

Output JSON:
    {
        "count": <total>,
        "anchors": [ { "type": "<type>", "value": "<anchor-id>" }, ... ]
    }
    当锚点数量超过 100 时，返回实际数量但只包含前 100 条。

Anchor types:
    "md_heading"  - Markdown 标题（# ## ### 等）
    "a_tag"       - HTML <a id="..."> 标签
    "h_tag"       - HTML <h1>-<h6> 标签带 id 属性
    "step"        - Step 组件（titleSize 为 h1-h5 时生成锚点）
    "param_field" - ParamField 组件
"""

import os
import sys
import json
import re

# 将 .scripts/check 目录加入 path，以便从 check_links.py 导入工具函数
_SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.normpath(os.path.join(_SKILL_DIR, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO_ROOT, '.scripts', 'check'))
from check_links import (
    heading_to_anchor,
    extract_paramfield_anchors,
    extract_steps_anchors,
)
MAX_ANCHORS = 100

# 匹配 HTML 开标签，捕获标签名和 id 属性值
_TAG_ID_RE = re.compile(
    r'<([a-zA-Z][a-zA-Z0-9]*)\b(?:[^>"\']*|"[^"]*"|\'[^\']*\')*\bid\s*=\s*[\'"]([^\'"]+)[\'"]',
    re.IGNORECASE,
)
# 匹配 MDX import 语句
_IMPORT_RE = re.compile(r'import\s+\w+\s+from\s+[\'"]([^\'"]+\.mdx)[\'"]')


def collect_anchors(file_path: str) -> list:
    """递归收集 MDX 文件（含 import 的子文件）中所有锚点，返回带类型的列表。"""
    anchors = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return anchors

    # ── 处理 MDX import，递归收集子文件锚点 ──────────────────────────────
    for m in _IMPORT_RE.finditer(content):
        import_path = m.group(1)
        if import_path.startswith('/'):
            sub = os.path.join(REPO_ROOT, import_path.lstrip('/'))
        else:
            sub = os.path.normpath(os.path.join(os.path.dirname(file_path), import_path))
        if os.path.exists(sub):
            anchors.extend(collect_anchors(sub))

    # ── 1. Markdown 标题 → md_heading ────────────────────────────────────
    heading_counts: dict = {}
    for line in content.split('\n'):
        stripped = line.strip()
        if not stripped.startswith('#'):
            continue
        heading_text = stripped.lstrip('#').strip()
        if not heading_text:
            continue
        anchor = heading_to_anchor(heading_text)
        if anchor in heading_counts:
            heading_counts[anchor] += 1
            anchors.append({"type": "md_heading", "value": f"{anchor}-{heading_counts[anchor]}"})
        else:
            heading_counts[anchor] = 0
            anchors.append({"type": "md_heading", "value": anchor})
            anchors.append({"type": "md_heading", "value": f"{anchor}-1"})

    # ── 2. HTML 标签 id 属性 → a_tag / h_tag ────────────────────────────
    for m in _TAG_ID_RE.finditer(content):
        tag = m.group(1).lower()
        anchor_id = m.group(2).strip()
        if not anchor_id:
            continue
        if tag == 'a':
            anchors.append({"type": "a_tag", "value": anchor_id})
        elif re.match(r'^h[1-6]$', tag):
            anchors.append({"type": "h_tag", "value": anchor_id})
        # 其他标签（div/span 等）忽略

    # ── 3. ParamField 组件 → param_field ────────────────────────────────
    for value in extract_paramfield_anchors(file_path):
        if value:
            anchors.append({"type": "param_field", "value": value})

    # ── 4. Steps/Step 组件 → step ────────────────────────────────────────
    for value in extract_steps_anchors(content):
        if value:
            anchors.append({"type": "step", "value": value})

    return anchors


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 collect-valid-anchors.py <mdx-file-path>"}))
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.isabs(file_path):
        # 优先从当前工作目录解析相对路径，兜底用仓库根目录
        candidate = os.path.normpath(os.path.join(os.getcwd(), file_path))
        if os.path.exists(candidate):
            file_path = candidate
        else:
            file_path = os.path.normpath(os.path.join(REPO_ROOT, file_path))
    else:
        file_path = os.path.normpath(file_path)

    if not os.path.exists(file_path):
        print(json.dumps({"error": f"File not found: {file_path}"}))
        sys.exit(1)

    anchors = collect_anchors(file_path)
    count = len(anchors)
    print(json.dumps({"count": count, "anchors": anchors[:MAX_ANCHORS]}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
