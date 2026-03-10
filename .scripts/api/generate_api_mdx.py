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


# ============================================================================
# 国际化配置（i18n Configuration）
# ============================================================================

I18N_CONFIG = {
    "zh": {
        "detail_map_keys": {
            "support_version": "支持版本",
            "detail_description": "详情描述",
            "usage_limitation": "使用限制",
            "precautions": "注意事项"
        },
        "section_titles": {
            "detail": "详情",
            "params": "参数",
            "return": "返回值"
        },
        "table_headers": {
            "name": "名称",
            "type": "类型",
            "desc": "描述"
        },
        "component_titles": {
            "deprecated": "已废弃"
        },
        "structure_titles": {
            "properties": "属性",
            "methods": "方法"
        },
        "warning_keys": [
            "支持版本",
            "使用限制",
            "注意事项"
        ]
    },
    "en": {
        "detail_map_keys": {
            "support_version": "Available since",
            "detail_description": "Description",
            "usage_limitation": "Restrictions",
            "precautions": "Warning"
        },
        "section_titles": {
            "detail": "Details",
            "params": "Parameters",
            "return": "Return"
        },
        "table_headers": {
            "name": "Name",
            "type": "Type",
            "desc": "Description"
        },
        "component_titles": {
            "deprecated": "Deprecated"
        },
        "structure_titles": {
            "properties": "Properties",
            "methods": "Methods"
        },
        "warning_keys": [
            "Available since",
            "Restrictions",
            "Warning"
        ]
    }
}


def detect_language_from_path(path: Path) -> str:
    """根据路径检测语言。

    Args:
        path: 源目录路径

    Returns:
        语言代码: "zh" 或 "en"
    """
    path_str = str(path)
    if "/en/" in path_str or path_str.startswith("en/") or path_str.endswith("/en"):
        return "en"
    elif "/zh/" in path_str or path_str.startswith("zh/") or path_str.endswith("/zh"):
        return "zh"
    else:
        # 默认返回中文
        return "zh"


def get_lang_config(path: Path) -> Dict[str, Any]:
    """获取指定路径的语言配置。

    Args:
        path: 源目录路径

    Returns:
        语言配置字典
    """
    lang = detect_language_from_path(path)
    return I18N_CONFIG[lang], lang


# ============================================================================
# 文件读取
# ============================================================================

def read_json_files(src_dir: Path) -> List[Dict[str, Any]]:
    files = sorted([p for p in src_dir.iterdir() if p.suffix == ".json" and p.is_file()])
    result = []
    for p in files:
        try:
            with p.open("r", encoding="utf-8") as f:
                obj = json.load(f)
            # 跳过非字典类型的 JSON（如 hotObject.json 是数组）
            if not isinstance(obj, dict):
                continue
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
def render_detail_section(details: List[Dict[str, Any]], support: Optional[Dict[str, Any]], lang_config: Dict[str, Any]) -> str:
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
        detail_map[lang_config["detail_map_keys"]["support_version"]] = support.get("info") or ""

    parts: List[str] = []

    # 详情描述：object_detail 一律带 "**详情**" 标题
    detail_desc_key = lang_config["detail_map_keys"]["detail_description"]
    detail_desc = (detail_map.pop(detail_desc_key, "") or "").strip()

    if detail_desc:
        # 不在这里转义，调用方会用 escape_jsx_in_text 处理
        detail_title = lang_config["section_titles"]["detail"]
        parts.append(f"**{detail_title}**\n\n{detail_desc}")

    # 仅 支持版本 / 使用限制 / 注意事项 放 Warning，其余（除详情外）出 Note
    warning_keys = lang_config["warning_keys"]
    warning_bullets: List[str] = []

    # 根据语言选择冒号
    colon = "：" if warning_keys[0] == "支持版本" else ": "

    for key in warning_keys:
        if key in detail_map and detail_map[key]:
            # 不在这里转义，调用方会用 escape_jsx_in_text 处理
            label = str(key)
            value = str(detail_map[key])
            warning_bullets.append(f"- **{label}**{colon}{value}")
            detail_map.pop(key, None)

    # 剩余 key -> 合并为一个 Note 组件（如果有剩余内容）
    note_bullets: List[str] = []
    for key, value in detail_map.items():
        if not value:
            continue
        # 不在这里转义，调用方会用 escape_jsx_in_text 处理
        label = str(key)
        body = str(value)
        # 根据语言选择冒号：中文用中文冒号，英文用英文冒号
        colon = "：" if lang_config["warning_keys"][0] == "支持版本" else ": "
        note_bullets.append(f"- **{label}**{colon}{body}")

    if note_bullets:
        note_body = "\n".join(note_bullets)
        parts.append(f"<Note title=\"\">\n{note_body}\n</Note>")

    if warning_bullets:
        warning_body = "\n".join(warning_bullets)
        parts.append(f"<Warning title=\"\">\n{warning_body}\n</Warning>")

    return "\n\n".join(parts)


def render_params(params: List[Dict[str, Any]], lang_config: Dict[str, Any], with_heading: bool = True) -> str:
    if not params:
        return ""

    lines: List[str] = []
    if with_heading:
        # 带标题的"参数"章节
        params_title = lang_config["section_titles"]["params"]
        lines.append(f"**{params_title}**")
        lines.append("")

    headers = lang_config["table_headers"]
    lines.append(f"| {headers['name']} | {headers['type']} | {headers['desc']} |")
    lines.append("| --- | --- | --- |")
    for p in params:
        # 表格单元格中不需要转义 { 和 }，只需要转义管道符
        name = escape_table_cell(str(p.get("name", "")))
        t = escape_table_cell(str(p.get("type", "")))
        desc = escape_table_cell(str(p.get("desc", "")))
        lines.append(f"| {name} | {t} | {desc} |")
    return "\n".join(lines)


def render_return(ret: Optional[Dict[str, Any]], lang_config: Dict[str, Any], has_params: bool = False) -> str:
    """渲染返回值章节。

    Args:
        ret: return 节点数据
        lang_config: 语言配置
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
        return_title = lang_config["section_titles"]["return"]
        return f"**{return_title}**\n\n{info}"
    else:
        return info


def render_deprecated_warning(deprecated: Optional[Dict[str, Any]], lang_config: Dict[str, Any]) -> str:
    if not deprecated:
        return ""
    info = (deprecated.get("info") or "").strip()
    if not info:
        return ""
    # 不在这里转义，最后统一用 escape_jsx_in_text 处理
    deprecated_title = lang_config["component_titles"]["deprecated"]
    return f"<Warning title=\"{deprecated_title}\">{info}</Warning>"


def render_param_like(node: Dict[str, Any], lang_config: Dict[str, Any], obj_meta: Optional[Dict[str, str]] = None) -> str:
    """统一渲染"字段/方法"为 ParamField，封装公共逻辑。

    Args:
        node: 节点数据
        lang_config: 语言配置
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
    # overflow_anchor: 用于处理重载方法/属性的锚点后缀
    anchor_suffix_raw = str(node.get("overflow_anchor", "") or "")

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
    params_section = render_params(params, lang_config, with_heading=with_detail)
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
        detail_map[lang_config["detail_map_keys"]["support_version"]] = support.get("info") or ""

    detail_desc_key = lang_config["detail_map_keys"]["detail_description"]
    detail_desc = (detail_map.pop(detail_desc_key, "") or "").strip()

    warning_keys = lang_config["warning_keys"]
    warning_bullets: List[str] = []

    # 根据语言选择冒号
    colon = "：" if warning_keys[0] == "支持版本" else ": "

    for key in warning_keys:
        if key in detail_map and detail_map[key]:
            # 不在这里转义，最后统一用 escape_jsx_in_text 处理
            label = str(key)
            value = str(detail_map[key])
            warning_bullets.append(f"- **{label}**{colon}{value}")
            detail_map.pop(key, None)

    note_bullets: List[str] = []
    for key, value in detail_map.items():
        if not value:
            continue
        # 不在这里转义，最后统一用 escape_jsx_in_text 处理
        label = str(key)
        body = str(value)
        note_bullets.append(f"- **{label}**{colon}{body}")

    # 详情：仅当既有 params 又有详情时才输出 **详情** 标题；否则只输出内容本身
    if detail_desc:
        # 不在这里转义，最后统一用 escape_jsx_in_text 处理
        if params:
            detail_title = lang_config["section_titles"]["detail"]
            parts.append(f"**{detail_title}**\n\n{detail_desc}")
        else:
            parts.append(detail_desc)

    if note_bullets:
        note_body = "\n".join(note_bullets)
        parts.append(f"<Note title=\"\">\n{note_body}\n</Note>")

    if warning_bullets:
        warning_body = "\n".join(warning_bullets)
        parts.append(f"<Warning title=\"\">\n{warning_body}\n</Warning>")

    # 3) deprecated warning（已废弃）
    deprecated_section = render_deprecated_warning(deprecated, lang_config)
    if deprecated_section:
        parts.append(deprecated_section)

    # 4) return 信息：放在 children 最后
    ret_section = render_return(node.get("return"), lang_config, has_params=bool(params))
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
    if anchor_suffix_raw:
        attr_lines.append(f"  anchor_suffix={quote_attr_value(anchor_suffix_raw)}")

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
    pattern_str = "\\[([^\\]]+)\\]\\(/" + re.escape(platform) + "/(class|enum|interface|protocol|struct)/([^)]+)\\)"
    pattern = re.compile(pattern_str)

    def _repl(m: re.Match) -> str:
        label = m.group(1)
        link_type = m.group(2)
        rest = m.group(3)  # xxx 任意内容，可能包含 #anchor

        # 检查是否包含锚点
        if '#' in rest:
            # 有锚点：取 # 后面的部分作为锚点，并移除连接符
            anchor = rest.split('#', 1)[1].lower().replace('-', '')
        else:
            # 无锚点：整个 rest 转小写作为锚点
            anchor = rest.lower()

        if link_type == kind:
            new_url = f"#{anchor}"
        else:
            new_url = f"./{link_type}#{anchor}"
        return f"[{label}]({new_url})"

    return pattern.sub(_repl, text)


def generate_index_table(objs: List[Dict[str, Any]]) -> str:
    """生成对象名称的索引表格（两列，按字母顺序排列）。

    Args:
        objs: JSON 对象列表

    Returns:
        Markdown 表格字符串
    """
    # 提取所有 object_name 并按字母顺序排序
    names = []
    for obj in objs:
        name = str(obj.get("object_name", "")).strip()
        if name:
            names.append(name)

    names.sort(key=str.lower)  # 不区分大小写排序

    if not names:
        return ""

    # 生成表格行（每行两个单元格，无表头）
    lines = []
    lines.append("| | |")
    lines.append("| --- | --- |")

    for i in range(0, len(names), 2):
        # 第一列
        name1 = names[i]
        anchor1 = name1.lower()
        cell1 = f"[{name1}](#{anchor1})"

        # 第二列（如果存在）
        if i + 1 < len(names):
            name2 = names[i + 1]
            anchor2 = name2.lower()
            cell2 = f"[{name2}](#{anchor2})"
        else:
            cell2 = ""

        lines.append(f"| {cell1} | {cell2} |")

    return "\n".join(lines)


def rewrite_links_for_split(text: str, platform: str, kind: str, relative_path: Optional[str] = None) -> str:
    """重写 split 模式下的链接。

    当配置了 relativePath 时，链接相对于总文件目录计算：
    - 同 kind：{relativePath}/{kind}.mdx#{anchor}
    - 不同 kind：{relativePath}/{other_kind}.mdx#{anchor}

    Args:
        text: 原始文本内容
        platform: 平台名称（用于匹配链接）
        kind: 当前类型（class、enum 等）
        relative_path: 相对于总文件目录的路径（如 "../../api-reference"）

    Returns:
        重写后的文本
    """
    # 使用普通字符串拼出模式
    pattern_str = "\\[([^\\]]+)\\]\\(/" + re.escape(platform) + "/(class|enum|interface|protocol|struct)/([^)]+)\\)"
    pattern = re.compile(pattern_str)

    def _repl(m: re.Match) -> str:
        label = m.group(1)
        link_type = m.group(2)
        rest = m.group(3)  # xxx 任意内容，可能包含 #anchor

        # 检查是否包含锚点
        if '#' in rest:
            # 有锚点：取 # 后面的部分作为锚点，并移除连接符
            anchor = rest.split('#', 1)[1].lower().replace('-', '')
        else:
            # 无锚点：整个 rest 转小写作为锚点
            anchor = rest.lower()

        # 如果配置了 relativePath，链接指向总文件
        if relative_path:
            # 拼接相对路径 + 类型名 + 锚点
            new_url = f"{relative_path}/{link_type}#{anchor}"
        else:
            # 没有 relativePath，使用当前目录下的文件
            if link_type == kind:
                new_url = f"#{anchor}"
            else:
                new_url = f"./{link_type}#{anchor}"

        return f"[{label}]({new_url})"

    return pattern.sub(_repl, text)


def generate_split_mdx_for_object(obj: Dict[str, Any], lang_config: Dict[str, Any], kind: str, output_base_dir: Path,
                                   platform: str = "", relative_path: Optional[str] = None) -> None:
    """为单个对象生成独立的 MDX 文件（split 模式）。

    Args:
        obj: JSON 对象数据
        lang_config: 语言配置
        kind: 类型名称（class、enum、protocol 等）
        output_base_dir: 输出基础目录（会在其下创建 kind 子目录）
        platform: 平台名称（用于链接重写）
        relative_path: 相对于总文件目录的路径（用于链接重写）
    """
    object_name = str(obj.get("object_name", "")).strip()
    if not object_name:
        print(f"[WARN] 对象缺少 object_name，跳过")
        return

    # 生成该对象的内容
    content = render_api_field(obj, lang_config)

    # 如果有 platform，重写链接
    if platform:
        content = rewrite_links_for_split(content, platform, kind, relative_path)

    # 添加一级标题（对象名）
    heading = f"# {object_name}"

    # 添加 frontmatter
    frontmatter = "---\ndocType: API\n---\n\n"

    # 拼接内容
    final_content = frontmatter + heading + "\n\n" + content + "\n"

    # 在输出目录下按类型创建子目录
    output_dir = output_base_dir / kind
    output_dir.mkdir(parents=True, exist_ok=True)

    # 确定输出文件名：使用 object_name 作为文件名
    # 转换为小写并替换空格和特殊字符为连字符
    file_name = object_name.lower().replace(" ", "-").replace("/", "-").replace("\\", "-")
    out_mdx = output_dir / f"{file_name}.mdx"

    # 写入 MDX 文件
    out_mdx.write_text(final_content, encoding="utf-8")
    print(f"[OK] 生成独立 MDX: {out_mdx}")


def render_api_field(obj: Dict[str, Any], lang_config: Dict[str, Any]) -> str:
    """将单个 JSON 对象渲染为 MDX 片段（不再使用 APIField）。

    Args:
        obj: JSON 对象数据
        lang_config: 语言配置
    """
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
    detail_block = render_detail_section(obj.get("object_detail") or [], obj.get("support"), lang_config)
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
        props_title = lang_config["structure_titles"]["properties"]
        lines.append(f"### {props_title}")
        obj_meta = {
            # 属性下的 ParamField 不需要 parent_file，只透出父对象名称和类型
            "parent_name": obj.get("object_name", ""),
            "parent_type": obj.get("object_type", ""),
        }
        for a in attrs:
            lines.append(render_param_like(a, lang_config, obj_meta=obj_meta))

    # 方法
    methods = obj.get("object_methods") or []
    if methods:
        lines.append("")
        methods_title = lang_config["structure_titles"]["methods"]
        lines.append(f"### {methods_title}")
        obj_meta = {
            "parent_file": obj.get("object_belong_file", ""),
            "parent_name": obj.get("object_name", ""),
            "parent_type": obj.get("object_type", ""),
        }
        for m in methods:
            lines.append(render_param_like(m, lang_config, obj_meta=obj_meta))

    return "\n".join(lines)


def generate_for(root: Path, kind: str, output_dir: Optional[Path] = None) -> None:
    """生成指定类型的 MDX 文件。

    Args:
        root: 平台目录路径（如 express_video_sdk/zh/java_android）
        kind: 类型名称（如 class、enum、protocol 等）
        output_dir: 可选的输出目录。如果指定，文件将生成到该目录；否则生成到 root 目录下
    """
    src_dir = root / kind
    if not src_dir.exists() or not src_dir.is_dir():
        print(f"[ERROR] 目录不存在: {src_dir}")
        return

    objs = read_json_files(src_dir)
    if not objs:
        print(f"[WARN] 目录下未找到 JSON 文件: {src_dir}")
        return

    # 根据路径自动检测语言
    lang_config, lang_code = get_lang_config(root)
    print(f"[INFO] 检测到语言: {lang_code}")

    blocks: List[str] = []

    for obj in objs:
        blocks.append(render_api_field(obj, lang_config))

    # 总文件第一行：与 kind 同名的一级标题（首字母大写，例如 "# Class"）
    heading = f"# {kind.capitalize()}"

    # 生成索引表格（两列，按字母顺序排列的对象链接）
    index_table = generate_index_table(objs)

    # 拼接内容：一级标题 + 索引表格 + 各对象内容
    if index_table:
        content = heading + "\n\n" + index_table + "\n\n" + "\n\n".join(blocks) + "\n"
    else:
        content = heading + "\n\n" + "\n\n".join(blocks) + "\n"

    # 重写当前平台下的相对链接
    platform = root.name
    content = rewrite_links_for_kind(content, platform, kind)

    # 在文件最前面添加 frontmatter
    frontmatter = "---\ndocType: API\n---\n\n"
    content = frontmatter + content

    # 确定输出目录
    if output_dir:
        # 如果指定了输出目录，确保目录存在
        output_dir.mkdir(parents=True, exist_ok=True)
        out_mdx = output_dir / f"{kind}.mdx"
    else:
        # 默认输出到平台目录下
        out_mdx = root / f"{kind}.mdx"

    # 写入 MDX 文件
    out_mdx.write_text(content, encoding="utf-8")
    print(f"[OK] 生成 MDX: {out_mdx}")


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
    new_url = f"./{parent_type}.mdx#{method_name_clean}-{class_name_lower}"

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

    # 在文件最前面添加 frontmatter（如果还没有的话）
    frontmatter = "---\ndocType: API\n---\n\n"
    if not new_content.startswith("---"):
        new_content = frontmatter + new_content

    # 确定输出文件路径
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        out_file = output_dir / "function-list.mdx"
    else:
        out_file = platform_dir / "function-list.mdx"

    # 写入新文件
    out_file.write_text(new_content, encoding="utf-8")
    print(f"[OK] 生成 function-list.mdx: {out_file}")


def parse_config_value(value: Any) -> List[Dict[str, Any]]:
    """解析配置文件中的 value，返回标准化的目标配置列表。

    Args:
        value: 配置值，可以是字符串、对象或数组

    Returns:
        标准化的目标配置列表，每个配置包含：
        - path: 目标目录路径
        - type: 生成类型（"merge" 或 "split"）
        - splitTypes: split 模式下要生成的类型列表
        - withFunctionList: 是否生成 function-list.mdx
        - relativePath: split 模式下分文件相对于总文件目录的相对路径
    """
    results = []

    # 如果是字符串，转换为默认配置对象
    if isinstance(value, str):
        results.append({
            "path": value,
            "type": "merge",
            "splitTypes": None,
            "withFunctionList": True,  # 字符串默认生成 function-list
            "relativePath": None
        })
    # 如果是字典，单个配置对象
    elif isinstance(value, dict):
        results.append({
            "path": value.get("path", ""),
            "type": value.get("type", "merge"),
            "splitTypes": value.get("splitTypes"),
            "withFunctionList": value.get("withFunctionList", False),  # 对象默认不生成
            "relativePath": value.get("relativePath")
        })
    # 如果是列表，遍历处理每个元素
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, str):
                results.append({
                    "path": item,
                    "type": "merge",
                    "splitTypes": None,
                    "withFunctionList": True,  # 字符串默认生成 function-list
                    "relativePath": None
                })
            elif isinstance(item, dict):
                results.append({
                    "path": item.get("path", ""),
                    "type": item.get("type", "merge"),
                    "splitTypes": item.get("splitTypes"),
                    "withFunctionList": item.get("withFunctionList", False),  # 对象默认不生成
                    "relativePath": item.get("relativePath")
                })
            else:
                print(f"[WARN] 忽略不支持的配置项类型: {type(item)}")
    else:
        print(f"[WARN] 忽略不支持的配置值类型: {type(value)}")

    return results


def config_based_main(config_path: Optional[Path] = None) -> None:
    """基于配置文件的批量生成模式。

    新配置格式：
    - key: 源目录路径
    - value: 可以是字符串、对象或数组
      - 字符串: 目标目录路径（等同于 merge 模式）
      - 对象: { path: 目标目录, type: "merge"|"split", splitTypes: ["class", ...] }
      - 数组: 包含多个字符串或对象

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

    # 遍历配置，key 为源目录，value 为目标配置
    for source_dir_str, target_config in config.items():
        print(f"\n{'='*60}")
        print(f"[INFO] 处理源目录: {source_dir_str}")

        # 解析路径（相对于仓库根目录）
        source_dir = Path(source_dir_str)

        # 检查源目录是否存在
        if not source_dir.exists():
            print(f"[ERROR] 源目录不存在: {source_dir}")
            continue

        if not source_dir.is_dir():
            print(f"[ERROR] 源路径不是目录: {source_dir}")
            continue

        # 解析目标配置
        target_configs = parse_config_value(target_config)
        if not target_configs:
            print(f"[WARN] 源目录 {source_dir} 没有有效的目标配置")
            continue

        # 动态扫描源目录下的类型
        kinds = get_kinds_from_platform(source_dir)
        if not kinds:
            print(f"[WARN] 源目录 {source_dir} 下没有找到任何包含 JSON 的类型子目录")
            continue

        print(f"[INFO] 发现类型: {', '.join(kinds)}")

        # 获取平台名称（源目录名，用于链接重写）
        platform = source_dir.name

        # 处理每个目标配置
        for target_cfg in target_configs:
            target_dir_str = target_cfg.get("path", "")
            gen_type = target_cfg.get("type", "merge")
            split_types = target_cfg.get("splitTypes")
            with_funclist = target_cfg.get("withFunctionList", False)
            relative_path = target_cfg.get("relativePath")

            if not target_dir_str:
                print(f"[WARN] 跳过空路径的配置")
                continue

            target_dir = Path(target_dir_str)
            print(f"[INFO]   -> 目标目录: {target_dir}, 类型: {gen_type}, withFunctionList: {with_funclist}")
            if relative_path:
                print(f"[INFO]   -> relativePath: {relative_path}")

            # 处理 split 模式
            if gen_type == "split":
                # 确定要 split 的类型
                types_to_split = split_types if split_types else kinds

                if not types_to_split:
                    print(f"[WARN] splitTypes 为空，跳过 split 模式")
                    continue

                print(f"[INFO]   -> split 类型: {', '.join(types_to_split)}")

                # 根据源目录检测语言配置
                lang_config, lang_code = get_lang_config(source_dir)
                print(f"[INFO]   -> 检测到语言: {lang_code}")

                # 为指定的每个类型生成独立的 MDX 文件
                for kind in types_to_split:
                    if kind not in kinds:
                        print(f"[WARN]   -> 类型 {kind} 不存在，跳过")
                        continue

                    kind_dir = source_dir / kind
                    objs = read_json_files(kind_dir)

                    if not objs:
                        print(f"[WARN]   -> 类型 {kind} 下没有 JSON 文件")
                        continue

                    print(f"[INFO]   -> 为 {kind} 类型的 {len(objs)} 个对象生成独立 MDX")

                    for obj in objs:
                        generate_split_mdx_for_object(obj, lang_config, kind, target_dir,
                                                       platform=platform,
                                                       relative_path=relative_path)

                # 转换 funcList.md（如果配置允许）
                if with_funclist:
                    funclist_file = source_dir / "funcList.md"
                    if funclist_file.exists():
                        print(f"[INFO]   -> 转换 funcList.md")
                        convert_funclist_md(source_dir, target_dir)
                    else:
                        print(f"[WARN]   -> funcList.md 不存在，跳过")

            # 处理 merge 模式（默认）
            else:
                # 为每个类型生成合并的 MDX 文件
                for kind in kinds:
                    print(f"[INFO]   -> 生成 {kind}.mdx")
                    generate_for(source_dir, kind, target_dir)

                # 转换 funcList.md（如果配置允许）
                if with_funclist:
                    funclist_file = source_dir / "funcList.md"
                    if funclist_file.exists():
                        print(f"[INFO]   -> 转换 funcList.md")
                        convert_funclist_md(source_dir, target_dir)
                    else:
                        print(f"[WARN]   -> funcList.md 不存在，跳过")

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

