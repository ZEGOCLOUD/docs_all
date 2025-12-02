#!/usr/bin/env python3
"""从各平台 JSON 实体定义生成汇总 MDX 文件的脚本。

用法示例：
    python scripts/generate_api_mdx.py express_video_sdk/zh/java_android class
    python scripts/generate_api_mdx.py --config

规则概要：
- 遍历 <root>/<kind> 目录下的所有 .json 文件（如 class/enum/interface/struct）。
- 每个 json -> 一个 <APIField> 组件；object_attrs -> ParamField；object_methods -> MethodField。
- object_detail 与 各节点 detail 的处理逻辑、support 覆盖逻辑等，严格按照对话中约定的规则实现。
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def read_json_files(src_dir: Path) -> List[Dict[str, Any]]:
    files = sorted([p for p in src_dir.iterdir() if p.suffix == ".json" and p.is_file()])
    result = []
    for p in files:
        try:
            with p.open("r", encoding="utf-8") as f:
                obj = json.load(f)
            obj["__file_name"] = p.name
            result.append(obj)
        except Exception as e:
            print(f"[WARN] 读取 JSON 失败: {p}: {e}")
    return result


def escape_mdx_text(s: str) -> str:
    """简单转义 MDX 中可能出问题的字符（最小化处理，尽量原样输出 Markdown）。"""
    # 先修复不合法的 </br> 标签为 <br/>
    s = s.replace("</br>", "<br/>")
    return s.replace("{", "{{").replace("}", "}}").replace("`", r"\`")


def escape_table_cell(s: str) -> str:
    """转义 Markdown 表格单元格中的特殊字符。

    在 Markdown 表格中，{ 和 } 不需要转义，只需要转义管道符 | 和反引号。
    """
    # 转义管道符，避免破坏表格结构
    # 注意：反引号在表格中通常不需要转义
    return s.replace("|", r"\|")


def escape_attr_value(s: str) -> str:
    """转义 JSX 属性值中的特殊字符。

    在被引号包裹的属性值中，{ 和 } 不需要转义，只需要转义反引号。
    同时修复不合法的 </br> 标签为 <br/>。
    """
    # 先修复不合法的 </br> 标签为 <br/>
    s = s.replace("</br>", "<br/>")
    return s.replace("`", r"\`")


def quote_attr_value(value: str) -> str:
    """智能选择引号包裹属性值。

    如果值中包含双引号，使用单引号包裹；否则使用双引号包裹。
    如果同时包含单引号和双引号，使用双引号并转义内部的双引号。

    注意：属性值会先经过 escape_attr_value 处理，然后再用引号包裹。

    Args:
        value: 属性值（未转义）

    Returns:
        带引号的属性值字符串
    """
    # 先转义属性值中的特殊字符（但不转义 { 和 }）
    escaped = escape_attr_value(value)

    has_double_quote = '"' in escaped
    has_single_quote = "'" in escaped

    if has_double_quote and has_single_quote:
        # 同时包含单引号和双引号，使用双引号并转义内部的双引号
        final_value = escaped.replace('"', r'\"')
        return f'"{final_value}"'
    elif has_double_quote:
        # 只包含双引号，使用单引号包裹（需要转义单引号，如果有的话）
        # 在 JSX 中，单引号包裹的字符串内部的单引号需要用 HTML 实体或转义
        # 但实际上 JSX 单引号字符串中的单引号不需要转义
        return f"'{escaped}'"
    else:
        # 不包含双引号或只包含单引号，使用双引号包裹
        return f'"{escaped}"'


def escape_jsx_in_text(s: str) -> str:
    r"""转义文本中的 JSX 敏感字符（{、}、<、>），但保留 MDX 组件标签。

    策略：
    1. 先修复不合法的 </br> 标签为 <br/>
    2. 标记所有 MDX 组件标签（<Note>、<Warning> 等）和 <br/> 标签
    3. 转义剩余的 {、}、<、> 为 \{、\}、\<、\>
    4. 恢复 MDX 组件标签和 <br/> 标签
    """
    import re

    # 修复不合法的 </br> 标签为 <br/>
    s = s.replace('</br>', '<br/>')

    # 先标记所有 MDX 组件标签和 <br/> 标签，用占位符替换
    # 匹配 <Note、<Warning、<Tip、</Note>、</Warning>、</Tip>、<br/> 等
    mdx_tag_pattern = r'</?(?:Note|Warning|Tip)(?:\s[^>]*)?>|</(?:Note|Warning|Tip)>|<br\s*/>'

    placeholders = []
    def replace_with_placeholder(match):
        placeholder = f"__MDX_TAG_{len(placeholders)}__"
        placeholders.append(match.group(0))
        return placeholder

    # 用占位符替换所有 MDX 标签和 <br/> 标签
    text_with_placeholders = re.sub(mdx_tag_pattern, replace_with_placeholder, s)

    # 转义 JSX 敏感字符：{、}、<、>
    escaped_text = text_with_placeholders
    escaped_text = escaped_text.replace("{", r"\{")
    escaped_text = escaped_text.replace("}", r"\}")
    escaped_text = escaped_text.replace("<", r"\<")
    escaped_text = escaped_text.replace(">", r"\>")

    # 恢复 MDX 标签
    for i, tag in enumerate(placeholders):
        escaped_text = escaped_text.replace(f"__MDX_TAG_{i}__", tag)

    return escaped_text


# 顶层 object_detail：复用与字段/方法相同的 detail 规则（详情 + Note + Warning），但不包裹 ParamField。
def render_detail_section(details: List[Dict[str, Any]], support: Optional[Dict[str, Any]]) -> str:
    if not details and not (support and not support.get("hidden") and support.get("info")):
        return ""

    detail_map: Dict[str, str] = {}
    for item in details or []:
        key = item.get("name") or item.get("key") or ""
        value = item.get("value") or ""
        if key:
            detail_map[key] = value

    # support 覆盖 / 注入 支持版本
    if support and not support.get("hidden") and support.get("info"):
        detail_map["支持版本"] = support.get("info") or ""

    parts: List[str] = []

    # 详情描述：object_detail 一律带 "**详情**" 标题
    detail_desc = (detail_map.pop("详情描述", "") or "").strip()
    if detail_desc:
        # 不在这里转义，调用方会用 escape_jsx_in_text 处理
        parts.append(f"**详情**\n\n{detail_desc}")

    # 仅 支持版本 / 使用限制 / 注意事项 放 Warning，其余（除详情外）出 Note
    warning_keys = ["支持版本", "使用限制", "注意事项"]
    warning_bullets: List[str] = []

    for key in warning_keys:
        if key in detail_map and detail_map[key]:
            # 不在这里转义，调用方会用 escape_jsx_in_text 处理
            label = str(key)
            value = str(detail_map[key])
            warning_bullets.append(f"- **{label}**：{value}")
            detail_map.pop(key, None)

    # 剩余 key -> 合并为一个 Note 组件
    note_bullets: List[str] = []
    for key, value in detail_map.items():
        if not value:
            continue
        # 不在这里转义，调用方会用 escape_jsx_in_text 处理
        label = str(key)
        body = str(value)
        note_bullets.append(f"- **{label}**：{body}")

    if note_bullets:
        note_body = "\n".join(note_bullets)
        parts.append(f"<Note title=\"\">\n{note_body}\n</Note>")

    if warning_bullets:
        warning_body = "\n".join(warning_bullets)
        parts.append(f"<Warning title=\"\">\n{warning_body}\n</Warning>")

    return "\n\n".join(parts)


def render_params(params: List[Dict[str, Any]], with_heading: bool = True) -> str:
    if not params:
        return ""

    lines: List[str] = []
    if with_heading:
        # 带标题的“参数”章节
        lines.append("**参数**")
        lines.append("")

    lines.append("| 名称 | 类型 | 描述 |")
    lines.append("| --- | --- | --- |")
    for p in params:
        # 表格单元格中不需要转义 { 和 }，只需要转义管道符
        name = escape_table_cell(str(p.get("name", "")))
        t = escape_table_cell(str(p.get("type", "")))
        desc = escape_table_cell(str(p.get("desc", "")))
        lines.append(f"| {name} | {t} | {desc} |")
    return "\n".join(lines)


def render_return(ret: Optional[Dict[str, Any]], has_params: bool = False) -> str:
    """渲染返回值章节。

    Args:
        ret: return 节点数据
        has_params: 是否有参数章节（用于决定是否需要添加 **返回值** 标题）

    Returns:
        返回值章节的 Markdown 文本
    """
    if not ret:
        return ""
    info = (ret.get("info") or "").strip()
    if not info:
        return ""

    # 不在这里转义，最后统一用 escape_jsx_in_text 处理
    # 如果有参数章节，需要添加 **返回值** 标题；否则直接输出内容
    if has_params:
        return f"**返回值**\n\n{info}"
    else:
        return info


def render_deprecated_warning(deprecated: Optional[Dict[str, Any]]) -> str:
    if not deprecated:
        return ""
    info = (deprecated.get("info") or "").strip()
    if not info:
        return ""
    # 不在这里转义，最后统一用 escape_jsx_in_text 处理
    return f"<Warning title=\"已废弃\">{info}</Warning>"


def render_param_like(node: Dict[str, Any], obj_meta: Optional[Dict[str, str]] = None) -> str:
    """统一渲染“字段/方法”为 ParamField，封装公共逻辑。

    obj_meta: 顶层对象的元信息，用于透传到 ParamField：
      - parent_file
      - parent_name
      - parent_type
    """
    # 属性值：不使用 escape_mdx_text，因为 quote_attr_value 会处理转义
    # 只有在 children 内容中才需要 escape_mdx_text
    name_raw = str(node.get("name", ""))
    prototype_raw = str(node.get("full_code", ""))
    desc_raw = str(node.get("desc", ""))

    # 顶层对象元信息（如果有）
    parent_file_raw = ""
    parent_name_raw = ""
    parent_type_raw = ""
    if obj_meta:
        parent_file_raw = obj_meta.get("parent_file", "") or ""
        parent_name_raw = obj_meta.get("parent_name", "") or ""
        parent_type_raw = obj_meta.get("parent_type", "") or ""

    prefixes: List[str] = []
    if node.get("static") is True:
        prefixes.append("static")

    deprecated = node.get("deprecated") or {}
    suffixes: List[str] = []
    if deprecated and not deprecated.get("hidden"):
        suffixes.append("deprecated")

    prefixes_literal = "[" + ", ".join(f'"{p}"' for p in prefixes) + "]"
    suffixes_literal = "[" + ", ".join(f'"{s}"' for s in suffixes) + "]"

    # children
    parts: List[str] = []

    params = node.get("params") or []
    details = node.get("detail") or []
    support = node.get("support")

    # 1) 参数：根据是否还有详情决定是否要加 "**参数**" 标题
    with_detail = bool(details)
    params_section = render_params(params, with_heading=with_detail)
    if params_section:
        parts.append(params_section)

    # 2) detail + support：拆为 详情 + 若干 Note + 一个 Warning
    detail_map: Dict[str, str] = {}
    for item in details:
        key = item.get("name") or item.get("key") or ""
        value = item.get("value") or ""
        if key:
            detail_map[key] = value

    if support and not support.get("hidden") and support.get("info"):
        detail_map["支持版本"] = support.get("info") or ""

    detail_desc = (detail_map.pop("详情描述", "") or "").strip()

    warning_keys = ["支持版本", "使用限制", "注意事项"]
    warning_bullets: List[str] = []

    for key in warning_keys:
        if key in detail_map and detail_map[key]:
            # 不在这里转义，最后统一用 escape_jsx_in_text 处理
            label = str(key)
            value = str(detail_map[key])
            warning_bullets.append(f"- **{label}**：{value}")
            detail_map.pop(key, None)

    note_bullets: List[str] = []
    for key, value in detail_map.items():
        if not value:
            continue
        # 不在这里转义，最后统一用 escape_jsx_in_text 处理
        label = str(key)
        body = str(value)
        note_bullets.append(f"- **{label}**：{body}")

    # 详情：仅当既有 params 又有详情时才输出 **详情** 标题；否则只输出内容本身
    if detail_desc:
        # 不在这里转义，最后统一用 escape_jsx_in_text 处理
        if params:
            parts.append(f"**详情**\n\n{detail_desc}")
        else:
            parts.append(detail_desc)

    if note_bullets:
        note_body = "\n".join(note_bullets)
        parts.append(f"<Note title=\"\">\n{note_body}\n</Note>")

    if warning_bullets:
        warning_body = "\n".join(warning_bullets)
        parts.append(f"<Warning title=\"\">\n{warning_body}\n</Warning>")

    # 3) deprecated warning（已废弃）
    deprecated_section = render_deprecated_warning(deprecated)
    if deprecated_section:
        parts.append(deprecated_section)

    # 4) return 信息：放在 children 最后
    ret_section = render_return(node.get("return"), has_params=bool(params))
    if ret_section:
        parts.append(ret_section)

    children_raw = "\n\n".join([p for p in parts if p])
    # 对整个 children 做 JSX 转义（保留 MDX 组件标签）
    children = escape_jsx_in_text(children_raw) if children_raw else ""

    # 组件起始标签：按行输出，每个属性单独一行，空属性不输出
    # 使用 quote_attr_value 智能选择引号（会自动处理转义）
    attr_lines: List[str] = ["<ParamField"]
    attr_lines.append(f"  name={quote_attr_value(name_raw)}")
    attr_lines.append(f"  prototype={quote_attr_value(prototype_raw)}")
    if desc_raw:
        attr_lines.append(f"  desc={quote_attr_value(desc_raw)}")
    if prefixes:
        attr_lines.append(f"  prefixes={{{prefixes_literal}}}")
    if suffixes:
        attr_lines.append(f"  suffixes={{{suffixes_literal}}}")
    if parent_file_raw:
        attr_lines.append(f"  parent_file={quote_attr_value(parent_file_raw)}")
    if parent_name_raw:
        attr_lines.append(f"  parent_name={quote_attr_value(parent_name_raw)}")
    if parent_type_raw:
        attr_lines.append(f"  parent_type={quote_attr_value(parent_type_raw)}")

    opening = "\n".join(attr_lines) + ">"

    lines = [opening]
    if children:
        lines.append(children)
    lines.append("</ParamField>")
    return "\n".join(lines)


def rewrite_links_for_kind(text: str, platform: str, kind: str) -> str:
    """重写形如 /<platform>/<type>/<xxx> 的相对链接。

    规则：
    - 当前生成文件为 <kind>.mdx；链接类型与 kind 相同：
      [/platform/kind/xxx] -> [#xxx]（锚点转小写）
    - 链接类型与 kind 不同：
      [/platform/other/xxx] -> [./other#xxx]（锚点转小写）
    仅处理以指定 platform 开头的相对链接，避免误伤其它路径或外链。
    """

    # 使用普通字符串拼出模式，避免 raw f-string + 反斜杠混用导致转义混乱
    # ([^)]+) 会把后面 "xxx任意内容" 整段吃进去，如果原路径本身带 #anchor 也一并保留
    pattern_str = "\\[([^\\]]+)\\]\\(/" + re.escape(platform) + "/(class|enum|interface|struct)/([^)]+)\\)"
    pattern = re.compile(pattern_str)

    def _repl(m: re.Match) -> str:
        label = m.group(1)
        link_type = m.group(2)
        rest = m.group(3)  # xxx 任意内容
        # 将锚点转为小写
        rest_lower = rest.lower()
        if link_type == kind:
            new_url = f"#{rest_lower}"
        else:
            new_url = f"./{link_type}#{rest_lower}"
        return f"[{label}]({new_url})"

    return pattern.sub(_repl, text)


def render_api_field(obj: Dict[str, Any]) -> str:
    """将单个 JSON 对象渲染为 MDX 片段（不再使用 APIField）。"""
    name = escape_mdx_text(str(obj.get("object_name", "")))
    desc = escape_mdx_text(str(obj.get("object_desc", "")))
    # object_belong_file 中的反引号不需要转义,只转义 { 和 }
    belong_raw = str(obj.get("object_belong_file", ""))
    belong = belong_raw.replace("{", "{{").replace("}", "}}")

    lines: List[str] = []

    # 二级标题：对象名
    lines.append(f"## {name}")

    # 紧跟其后输出 object_desc（如果有）
    if desc:
        lines.append("")
        lines.append(desc)

    # object_detail：复用与字段/方法相同的 detail 规则（详情 + Note + Warning），但不包裹 ParamField
    detail_block = render_detail_section(obj.get("object_detail") or [], obj.get("support"))
    if detail_block:
        lines.append("")
        # 对 detail_block 做 JSX 转义（保留 MDX 组件标签）
        lines.append(escape_jsx_in_text(detail_block))

    # object_belong_file 用斜体渲染，放在 object_detail 的最后
    if belong:
        lines.append("")
        lines.append(f"*{belong}*")

    # 属性
    attrs = obj.get("object_attrs") or []
    if attrs:
        lines.append("")
        lines.append("### 属性")
        obj_meta = {
            # 属性下的 ParamField 不需要 parent_file，只透出父对象名称和类型
            "parent_name": obj.get("object_name", ""),
            "parent_type": obj.get("object_type", ""),
        }
        for a in attrs:
            lines.append(render_param_like(a, obj_meta=obj_meta))

    # 方法
    methods = obj.get("object_methods") or []
    if methods:
        lines.append("")
        lines.append("### 方法")
        obj_meta = {
            "parent_file": obj.get("object_belong_file", ""),
            "parent_name": obj.get("object_name", ""),
            "parent_type": obj.get("object_type", ""),
        }
        for m in methods:
            lines.append(render_param_like(m, obj_meta=obj_meta))

    return "\n".join(lines)


def generate_for(root: Path, kind: str, output_dir: Optional[Path] = None) -> None:
    """生成指定类型的 MDX 文件。

    Args:
        root: 平台目录路径（如 express_video_sdk/zh/java_android）
        kind: 类型名称（如 class、enum、protocol 等）
        output_dir: 可选的输出目录。如果指定，MDX 文件将生成到该目录；否则生成到 root 目录下
    """
    src_dir = root / kind
    if not src_dir.exists() or not src_dir.is_dir():
        print(f"[ERROR] 目录不存在: {src_dir}")
        return

    objs = read_json_files(src_dir)
    if not objs:
        print(f"[WARN] 目录下未找到 JSON 文件: {src_dir}")
        return

    blocks: List[str] = []
    for obj in objs:
        blocks.append(render_api_field(obj))

    # 总文件第一行：与 kind 同名的一级标题（首字母大写，例如 "# Class"），后面紧跟各对象内容
    heading = f"# {kind.capitalize()}"
    content = heading + "\n\n" + "\n\n".join(blocks) + "\n"

    # 重写当前平台下的相对链接
    platform = root.name
    content = rewrite_links_for_kind(content, platform, kind)

    # 确定输出目录
    if output_dir:
        # 如果指定了输出目录，确保目录存在
        output_dir.mkdir(parents=True, exist_ok=True)
        out_file = output_dir / f"{kind}.mdx"
    else:
        # 默认输出到平台目录下
        out_file = root / f"{kind}.mdx"

    out_file.write_text(content, encoding="utf-8")
    print(f"[OK] 生成 MDX: {out_file}")


def main(argv: List[str]) -> None:
    """命令行模式入口。

    用法1: python generate_api_mdx.py <platform_dir> <kind>
    示例: python generate_api_mdx.py express_video_sdk/zh/java_android class

    用法2: python generate_api_mdx.py <platform_dir> <output_dir>
    示例: python generate_api_mdx.py express_video_sdk/zh/java_android /Users/oliver/Documents/docuo/docs_all/core_products/real-time-voice-video/zh/android-java/client-sdk/api-reference
    """
    if len(argv) < 3:
        print("用法1: python generate_api_mdx.py <platform_dir> <kind>")
        print("示例: python generate_api_mdx.py express_video_sdk/zh/java_android class")
        print()
        print("用法2: python generate_api_mdx.py <platform_dir> <output_dir>")
        print("示例: python generate_api_mdx.py express_video_sdk/zh/java_android /path/to/output")
        return

    platform_dir = Path(argv[1]).resolve()
    second_arg = argv[2]

    # 判断第二个参数是 kind 还是输出目录
    # 如果第二个参数是已知的 kind（class/enum/interface/struct/protocol 等），则按用法1处理
    # 否则按用法2处理（第二个参数是输出目录）
    if second_arg in ["class", "enum", "interface", "struct", "protocol"]:
        # 用法1: 指定单个 kind
        kind = second_arg
        generate_for(platform_dir, kind)
    else:
        # 用法2: 指定输出目录，生成所有类型
        output_dir = Path(second_arg).resolve()

        # 动态扫描平台目录下的类型
        kinds = get_kinds_from_platform(platform_dir)
        if not kinds:
            print(f"[WARN] 平台目录 {platform_dir} 下没有找到任何包含 JSON 的类型子目录")
            return

        print(f"[INFO] 平台目录: {platform_dir}")
        print(f"[INFO] 输出目录: {output_dir}")
        print(f"[INFO] 发现类型: {', '.join(kinds)}")

        for kind in kinds:
            print(f"[INFO] 生成 {kind}.mdx")
            generate_for(platform_dir, kind, output_dir)

        # 转换 funcList.md
        print(f"[INFO] 转换 funcList.md")
        convert_funclist_md(platform_dir, output_dir)



def find_single_project_dir(base_dir: Path) -> Optional[Path]:
    """在 base_dir 下查找唯一子目录，用作项目目录（仿照 merge_md_files/merge_json_files）。

    会自动忽略以 . 开头的隐藏目录以及 __pycache__ 目录。
    """
    subdirs = [
        d
        for d in base_dir.iterdir()
        if d.is_dir() and not d.name.startswith(".") and d.name != "__pycache__"
    ]
    if len(subdirs) == 1:
        return subdirs[0]
    elif len(subdirs) == 0:
        print(f"错误: {base_dir} 下未找到任何子目录")
        return None
    else:
        print(f"错误: {base_dir} 下找到多个子目录: {[d.name for d in subdirs]}")
        return None



def interactive_select_language(base_dir: Path) -> Optional[Path]:
    """仿照 merge_md_files.py：在 <base_dir> 下交互式选择语言目录。"""
    lang_dirs = sorted([d for d in base_dir.iterdir() if d.is_dir()])
    if not lang_dirs:
        print(f"未找到语言目录: {base_dir}")
        return None

    print(f"\n在 {base_dir} 中找到以下语言目录：")
    for i, lang_dir in enumerate(lang_dirs, 1):
        print(f"{i}. {lang_dir.name}")

    while True:
        choice = input("\n请选择语言目录编号: ").strip()
        try:
            idx = int(choice)
            if 1 <= idx <= len(lang_dirs):
                return lang_dirs[idx - 1]
            else:
                print(f"错误: 请输入 1-{len(lang_dirs)} 之间的数字")
        except ValueError:
            print("错误: 请输入有效的数字")


def interactive_select_platform(lang_dir: Path) -> List[Path]:
    """仿照 merge_md_files.py：在语言目录下交互式选择平台目录，支持 0=全部。"""
    platform_dirs = sorted([d for d in lang_dir.iterdir() if d.is_dir()])
    if not platform_dirs:
        print(f"未找到平台目录: {lang_dir}")
        return []

    print(f"\n在 {lang_dir} 中找到以下平台目录：")
    print("0. 处理所有平台 (默认)")
    for i, p in enumerate(platform_dirs, 1):
        print(f"{i}. {p.name}")

    while True:
        choice = input("\n请选择平台目录编号 (直接回车选择0): ").strip()
        if choice == "" or choice == "0":
            return platform_dirs
        try:
            idx = int(choice)
            if 1 <= idx <= len(platform_dirs):
                return [platform_dirs[idx - 1]]
            else:
                print(f"错误: 请输入 0-{len(platform_dirs)} 之间的数字")
        except ValueError:
            print("错误: 请输入有效的数字")


def get_kinds_from_platform(platform_dir: Path) -> List[str]:
    """从平台目录下扫描实际存在的类型子目录（如 class、enum、protocol 等）。

    只返回包含 JSON 文件的子目录名称。
    """
    if not platform_dir.exists() or not platform_dir.is_dir():
        return []

    kinds = []
    for item in platform_dir.iterdir():
        # 跳过隐藏目录和文件
        if item.name.startswith("."):
            continue
        # 只处理目录
        if not item.is_dir():
            continue
        # 检查目录下是否有 JSON 文件
        has_json = any(f.suffix == ".json" for f in item.iterdir() if f.is_file())
        if has_json:
            kinds.append(item.name)

    return sorted(kinds)


def interactive_main() -> None:
    """无命令行参数时的交互式入口：先选语言，再选平台，动态扫描类型。"""
    # 默认项目根目录：脚本所在目录下唯一的子目录（例如 express_video_sdk）
    script_dir = Path(__file__).parent
    project_root = find_single_project_dir(script_dir)
    if project_root is None:
        return

    print(f"项目根目录: {project_root}")

    # 选择语言目录（如 zh、en 等）
    lang_dir = interactive_select_language(project_root)
    if lang_dir is None:
        return

    print(f"已选择语言目录: {lang_dir.name}")

    # 选择平台目录（如 java_android、ios 等）
    platforms = interactive_select_platform(lang_dir)
    if not platforms:
        return

    for platform_dir in platforms:
        print(f"\n开始处理平台目录: {platform_dir}")

        # 动态扫描平台目录下的类型
        kinds = get_kinds_from_platform(platform_dir)
        if not kinds:
            print(f"[WARN] 平台目录 {platform_dir} 下没有找到任何包含 JSON 的类型子目录")
            continue

        print(f"[INFO] 发现类型: {', '.join(kinds)}")

        for kind in kinds:
            root = platform_dir / kind
            print(f"[INFO] 生成 {root} 下的 {kind}.mdx")
            generate_for(platform_dir, kind)


def convert_funclist_link(link_text: str, link_url: str) -> Tuple[str, str]:
    """转换 funcList.md 中的链接格式。

    Args:
        link_text: 链接文本,如 "createEngine \\|_blank"
        link_url: 链接 URL,如 "/zh/api?doc=express-video-sdk_API~java_android~class~ZegoExpressEngine#create-engine"

    Returns:
        (新链接文本, 新链接URL) 的元组
    """
    # 移除链接文本中的 \|_blank 或 |_blank
    new_text = link_text.replace(" \\|_blank", "").replace("\\|_blank", "").replace(" |_blank", "").replace("|_blank", "")

    # 解析链接 URL
    # 格式: /zh/api?doc=express-video-sdk_API~{platform}~{type}~{ClassName}#{method-name}
    # 需要提取: ~class~ 或 ~interface~ 或 ~protocol~ 等后面的部分

    # 使用正则匹配 ~(class|interface|protocol|enum|struct)~(.+)
    pattern = r'~(class|interface|protocol|enum|struct)~([^#]+)#(.+)'
    match = re.search(pattern, link_url)

    if not match:
        # 如果匹配失败,返回原链接
        return (new_text, link_url)

    parent_type = match.group(1)  # class, interface, protocol 等
    class_name = match.group(2)   # 如 ZegoExpressEngine
    method_name = match.group(3)  # 如 create-engine

    # 类名转小写
    class_name_lower = class_name.lower()

    # 方法名删除所有 - 并转小写
    method_name_clean = method_name.replace("-", "").lower()

    # 拼接新链接: ./class.mdx#{method_name_clean}-{class_name_lower}-class
    new_url = f"./{parent_type}.mdx#{method_name_clean}-{class_name_lower}-{parent_type}"

    return (new_text, new_url)


def convert_funclist_md(platform_dir: Path, output_dir: Optional[Path] = None) -> None:
    """转换 funcList.md 为 function-list.mdx。

    Args:
        platform_dir: 平台目录路径(如 express_video_sdk/zh/java_android)
        output_dir: 可选的输出目录。如果指定,MDX 文件将生成到该目录;否则生成到 platform_dir 下
    """
    funclist_file = platform_dir / "funcList.md"
    if not funclist_file.exists():
        print(f"[WARN] funcList.md 不存在: {funclist_file}")
        return

    # 读取原文件
    content = funclist_file.read_text(encoding="utf-8")

    # 删除 <style> 元素(包括其内容)
    # 匹配 <style> ... </style> (支持多行)
    style_pattern = r'<style>.*?</style>'
    content = re.sub(style_pattern, '', content, flags=re.DOTALL)

    # 正则匹配表格行中的链接: [xxx |_blank](url)
    # 匹配模式: \[([^\]]+)\]\(([^\)]+)\)
    link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'

    def replace_link(match):
        link_text = match.group(1)
        link_url = match.group(2)
        new_text, new_url = convert_funclist_link(link_text, link_url)
        return f"[{new_text}]({new_url})"

    # 替换所有链接
    new_content = re.sub(link_pattern, replace_link, content)

    # 确定输出文件路径
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        out_file = output_dir / "function-list.mdx"
    else:
        out_file = platform_dir / "function-list.mdx"

    # 写入新文件
    out_file.write_text(new_content, encoding="utf-8")
    print(f"[OK] 生成 function-list.mdx: {out_file}")


def config_based_main(config_path: Optional[Path] = None) -> None:
    """基于配置文件的批量生成模式。

    Args:
        config_path: 配置文件路径，默认为脚本所在目录下的 config.json
    """
    # 确定配置文件路径
    if config_path is None:
        script_dir = Path(__file__).parent
        config_path = script_dir / "config.json"

    if not config_path.exists():
        print(f"[ERROR] 配置文件不存在: {config_path}")
        return

    # 读取配置文件
    try:
        with config_path.open("r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        print(f"[ERROR] 读取配置文件失败: {e}")
        return

    if not config:
        print(f"[WARN] 配置文件为空: {config_path}")
        return

    print(f"[INFO] 从配置文件读取到 {len(config)} 个映射")

    # 遍历配置，处理每个源目录到目标目录的映射
    for source_dir_str, target_dir_str in config.items():
        print(f"\n{'='*60}")
        print(f"[INFO] 处理映射:")
        print(f"  源目录: {source_dir_str}")
        print(f"  目标目录: {target_dir_str}")

        # 解析路径（相对于仓库根目录）
        source_dir = Path(source_dir_str)
        target_dir = Path(target_dir_str)

        # 检查源目录是否存在
        if not source_dir.exists():
            print(f"[ERROR] 源目录不存在: {source_dir}")
            continue

        if not source_dir.is_dir():
            print(f"[ERROR] 源路径不是目录: {source_dir}")
            continue

        # 动态扫描源目录下的类型
        kinds = get_kinds_from_platform(source_dir)
        if not kinds:
            print(f"[WARN] 源目录 {source_dir} 下没有找到任何包含 JSON 的类型子目录")
            continue

        print(f"[INFO] 发现类型: {', '.join(kinds)}")

        # 为每个类型生成 MDX 文件
        for kind in kinds:
            print(f"[INFO] 生成 {kind}.mdx")
            generate_for(source_dir, kind, target_dir)

        # 转换 funcList.md
        print(f"[INFO] 转换 funcList.md")
        convert_funclist_md(source_dir, target_dir)

    print(f"\n{'='*60}")
    print("[INFO] 所有映射处理完成")


if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description="从各平台 JSON 实体定义生成汇总 MDX 文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
用法示例:
  1. 配置文件模式（根据 config.json 批量生成）:
     python generate_api_mdx.py --config
     python generate_api_mdx.py --config /path/to/config.json

  2. 单个类型生成:
     python generate_api_mdx.py <platform_dir> <kind>
     python generate_api_mdx.py express_video_sdk/zh/java_android class

  3. 指定输出目录生成所有类型:
     python generate_api_mdx.py <platform_dir> <output_dir>

  4. 交互式模式（无参数）:
     python generate_api_mdx.py
        """
    )

    parser.add_argument(
        "--config",
        nargs="?",
        const=True,
        metavar="CONFIG_FILE",
        help="使用配置文件模式。可选指定配置文件路径，默认使用脚本目录下的 config.json"
    )

    parser.add_argument(
        "args",
        nargs="*",
        help="位置参数：<platform_dir> <kind|output_dir>"
    )

    args = parser.parse_args()

    # 配置文件模式
    if args.config is not None:
        if args.config is True:
            # 使用默认配置文件
            config_based_main()
        else:
            # 使用指定的配置文件
            config_based_main(Path(args.config))
    # 位置参数模式
    elif len(args.args) >= 2:
        # 构造 sys.argv 格式供 main() 使用
        main([sys.argv[0]] + args.args)
    # 交互式模式
    else:
        interactive_main()

