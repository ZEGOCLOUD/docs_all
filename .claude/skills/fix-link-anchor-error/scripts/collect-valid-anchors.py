#!/usr/bin/env python3
"""收集 MDX 文件中所有有效锚点，输出带类型信息的 JSON。

Usage:
    python3 collect-valid-anchors.py <mdx-file-path> [--search-param-field <broken-anchor>]

    <mdx-file-path> 可以是相对于仓库根目录的相对路径，也可以是绝对路径。

    --search-param-field <broken-anchor>:
        特殊模式：当确认为客户端 API 文档（有 param_field 锚点）时使用。
        将尝试以去掉类型、去掉 parent 的 fallback 顺序匹配 ParamField 锚点，
        一旦匹配到任何层级，将返回该层级对应的所有锚点变体。

Output JSON (Normal mode):
    {
        "count": <total>,
        "anchors": [ { "type": "<type>", "value": "<anchor-id>" }, ... ]
    }
    当锚点数量超过 100 时，返回实际数量但只包含前 100 条。

Output JSON (--search-param-field mode):
    {
        "matches": [ "<anchor-1>", "<anchor-2>", ... ]
    }

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


def _collect_param_fields_only(file_path: str) -> list:
    """仅收集 param_field 锚点（含 import 子文件），跳过标题/标签/step 以加速。"""
    results = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return results

    # 递归 import 子文件
    for m in _IMPORT_RE.finditer(content):
        import_path = m.group(1)
        if import_path.startswith('/'):
            sub = os.path.join(REPO_ROOT, import_path.lstrip('/'))
        else:
            sub = os.path.normpath(os.path.join(os.path.dirname(file_path), import_path))
        if os.path.exists(sub):
            results.extend(_collect_param_fields_only(sub))

    for value in extract_paramfield_anchors(file_path):
        if value:
            results.append(value)
    return results


def search_param_field(file_path: str, broken_anchor: str) -> list:
    """
    当文件为客户端 API 文档时，查找 param_field 锚点。

    ParamField 锚点有三种形体：
        method                    （纯方法名）
        method-parent             （方法名-父类名）
        method-parent-class       （完整形式）

    Fallback 匹配顺序：
    1. 完整匹配：broken_anchor 原样在锚点列表中查找
    2. 去掉最后一个 - 段后再匹配（如 method-parent → method）
    3. 继续去掉 - 段直到只剩第一段

    在任意层级匹配到任何 param_field，立即返回所有以该 fallback 为前缀的锚点变体供 Agent 选择。
    """
    param_fields = _collect_param_fields_only(file_path)

    if not param_fields:
        return []

    parts = broken_anchor.split('-')
    for i in range(len(parts), 0, -1):
        fallback = "-".join(parts[:i])
        matches = []
        for pf in set(param_fields):
            if pf == fallback or pf.startswith(fallback + "-"):
                matches.append(pf)
        if matches:
            return sorted(matches)
    return []


def has_param_field(file_path: str) -> bool:
    """快速检测文件（含 import 子文件）是否包含 ParamField 组件。仅做文本搜索，不解析锚点。"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return False

    if '<ParamField' in content:
        return True

    # 检查 import 子文件
    for m in _IMPORT_RE.finditer(content):
        import_path = m.group(1)
        if import_path.startswith('/'):
            sub = os.path.join(REPO_ROOT, import_path.lstrip('/'))
        else:
            sub = os.path.normpath(os.path.join(os.path.dirname(file_path), import_path))
        if os.path.exists(sub):
            if has_param_field(sub):
                return True
    return False


def _resolve_file_path(file_path: str) -> str:
    """统一解析文件路径：支持相对路径和绝对路径。"""
    if not os.path.isabs(file_path):
        candidate = os.path.normpath(os.path.join(os.getcwd(), file_path))
        if os.path.exists(candidate):
            return candidate
        return os.path.normpath(os.path.join(REPO_ROOT, file_path))
    return os.path.normpath(file_path)


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 collect-valid-anchors.py <mdx-file-path> [--has-param-field] [--search-param-field <broken-anchor>]"}))
        sys.exit(1)

    file_path = sys.argv[1]

    # 检查子命令
    mode = "collect"
    search_anchor = None
    if len(sys.argv) >= 3:
        if sys.argv[2] == '--has-param-field':
            mode = "has_param_field"
        elif sys.argv[2] == '--search-param-field' and len(sys.argv) >= 4:
            mode = "search_param_field"
            search_anchor = sys.argv[3]

    file_path = _resolve_file_path(file_path)

    if not os.path.exists(file_path):
        print(json.dumps({"error": f"File not found: {file_path}"}))
        sys.exit(1)

    if mode == "has_param_field":
        result = has_param_field(file_path)
        print(json.dumps({"has_param_field": result}))
    elif mode == "search_param_field":
        matches = search_param_field(file_path, search_anchor)
        print(json.dumps({"matches": matches}, ensure_ascii=False, indent=2))
    else:
        anchors = collect_anchors(file_path)
        count = len(anchors)
        print(json.dumps({"count": count, "anchors": anchors[:MAX_ANCHORS]}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
