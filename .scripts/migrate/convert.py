#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档迁移工具
包含多种迁移功能：
1. 目录及文件名格式化：将混合大小写转换为小写加连字符格式
2. 文档转换：将 .md 文件转换为 .mdx 文件并重新组织目录结构
"""

import os
import re
import sys
import json
import shutil
from pathlib import Path


def convert_name_format(name):
    """
    将混合大小写的名称转换为小写加连字符的格式

    Args:
        name (str): 原始名称

    Returns:
        str: 转换后的名称
    """
    # 特殊处理常见缩写词，直接替换
    # 按照从长到短的顺序处理，避免部分匹配问题
    special_replacements = [
        ('APIs', 'apis'),
        ('API', 'api'),
        ('URLs', 'urls'),
        ('URL', 'url'),
        ('HTTPS', 'https'),
        ('HTTP', 'http'),
        ('JSON', 'json'),
        ('XML', 'xml'),
        ('HTML', 'html'),
        ('CSS', 'css'),
        ('SDK', 'sdk'),
        ('UUID', 'uuid'),
        ('UI', 'ui'),
        ('ID', 'id'),
        ('JS', 'js'),
    ]

    # 先进行特殊词汇的替换
    for old_word, new_word in special_replacements:
        name = name.replace(old_word, f"__{new_word}__")

    # 处理驼峰命名：在大写字母前添加连字符（除了开头和连续大写字母）
    # 只在小写字母后跟大写字母时添加连字符
    name = re.sub(r'(?<=[a-z])(?=[A-Z])', '-', name)

    # 将下划线和空格替换为连字符
    name = name.replace('_', '-')
    name = name.replace(' ', '-')

    # 转换为小写
    name = name.lower()

    # 恢复特殊词汇（去掉标记）
    name = name.replace('--', '-')

    # 处理连续的连字符
    name = re.sub(r'-+', '-', name)

    # 去除开头和结尾的连字符
    name = name.strip('-')

    return name


# ==================== 文档转换功能 ====================

def get_relative_paths(root_path):
    """
    获取指定目录下所有 .md 和 .mdx 文件的相对路径

    Args:
        root_path (Path): 根目录路径

    Returns:
        list: 相对路径列表
    """
    file_paths = []

    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(('.md', '.mdx')):
                full_path = Path(root) / file
                relative_path = full_path.relative_to(root_path)
                file_paths.append(str(relative_path))

    return file_paths


def transform_directory_structure(old_path):
    """
    根据旧目录结构转换新目录结构
    将 .md 文件转换为 .mdx 文件并重新组织目录结构

    Args:
        old_path (str): 旧目录路径

    Returns:
        list: 新、旧目录的文件映射图
    """
    old_path = Path(old_path)
    if not old_path.exists():
        raise FileNotFoundError(f"目录不存在: {old_path}")

    # 获取所有 .md 文件的相对路径
    relative_paths = get_relative_paths(old_path)

    # 生成映射关系
    path_map = []
    for item in relative_paths:
        # 移除开头的斜杠（如果有）
        item = item.lstrip('/')

        # 格式化新目录：将下划线替换为空格，提取目录部分，添加 .mdx 扩展名
        # 同时对目录名和文件名进行格式化处理
        # 例如: "dir1/dir2/file_name.md" -> "dir-1/dir-2.mdx"
        path_parts = Path(item).parts
        if len(path_parts) > 1:
            # 有子目录的情况：格式化所有目录名
            formatted_dirs = []
            for part in path_parts[:-1]:
                formatted_part = convert_name_format(part.replace('_', ' '))
                formatted_dirs.append(formatted_part)
            new_item = '/'.join(formatted_dirs) + '.mdx'
        else:
            # 直接在根目录的文件：格式化文件名
            formatted_name = convert_name_format(Path(item).stem.replace('_', ' '))
            new_item = formatted_name + '.mdx'

        # 提取平台信息（文件名去掉扩展名）
        platform = Path(item).stem

        path_map.append({
            'old_path': item,
            'new_path': new_item,
            'platform': platform
        })

    return path_map


def create_directories_and_files(old_path, path_map):
    """
    根据映射图创建新的目录结构和文件

    Args:
        old_path (str): 原始目录路径
        path_map (list): 文件映射关系
    """
    old_path = Path(old_path)
    dist_path = Path("dist") / old_path.name

    # 获取所有平台
    platforms = list(set(item['platform'] for item in path_map))

    for item in path_map:
        # 确定新文件的完整路径
        if item['platform'].lower() == 'all':
            new_full_path = dist_path / item['new_path']
        else:
            # 处理多平台情况
            if '_zh' in str(dist_path):
                # 包含中文的情况
                zh_path = str(dist_path).replace('_zh', '')
                new_full_path = Path(f"{zh_path}_{item['platform']}_zh") / item['new_path']
            else:
                # 不包含中文的情况
                new_full_path = Path(f"{dist_path}_{item['platform']}") / item['new_path']

        old_full_path = old_path / item['old_path']

        # 创建目录（如果不存在）
        new_full_path.parent.mkdir(parents=True, exist_ok=True)

        # 复制文件
        if old_full_path.exists():
            shutil.copy2(old_full_path, new_full_path)
            print(f"复制文件: {old_full_path} -> {new_full_path}")
        else:
            print(f"警告: 源文件不存在: {old_full_path}")


def remove_heading_numbers(content):
    """
    去掉 Markdown 标题中的数字序号

    Args:
        content (str): 文件内容

    Returns:
        str: 处理后的内容
    """
    def replace_heading(match):
        # 获取井号和标题内容
        hashes = match.group(1)
        title_content = match.group(2).strip()
        
        # 各种序号模式
        patterns = [
            # 数字序号：1, 2, 3, 1.1, 1.2.3, 等
            # 但排除版本号格式（后面跟着版本相关关键词的情况）
            r'^\d+(?:\.\d+)*\.?\s+(?!.*(?:版本|及以上|升级|更新|发布|release|version|v\d|API|SDK|以上版本|或更高|或以上))',
            # 中文数字序号：一、二、三、1、2、3、等
            r'^[一二三四五六七八九十百千万]+[、．]\s*',
            r'^[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]\s*',
            # 括号数字：(1) (2) （1） （2） [1] [2] 等
            r'^[\(\（\[]?\d+[\)\）\]]\s*',
            # 字母序号：a) b) A) B) a. b. A. B. 等
            r'^[a-zA-Z][\)\.]]\s*',
            # 罗马数字：i) ii) I) II) 等
            r'^[ivxlcdmIVXLCDM]+[\)\.]]\s*',
        ]
        
        # 依次尝试匹配各种序号模式
        for pattern in patterns:
            title_content = re.sub(pattern, '', title_content)
        
        # 确保标题不为空
        if not title_content.strip():
            return match.group(0)  # 如果去掉序号后标题为空，返回原内容
        
        return f"{hashes} {title_content}"
    
    # 匹配 Markdown 标题（1-6级）
    heading_pattern = r'^(#{1,6})\s+(.+)$'
    content = re.sub(heading_pattern, replace_heading, content, flags=re.MULTILINE)
    
    return content


def replace_content(file_path, language='zh'):
    """
    替换文件内容，将旧的 Markdown 语法转换为新的 MDX 语法

    Args:
        file_path (Path): 文件路径
        language (str): 语言 ('zh' 或 'en')
    """
    file_path = Path(file_path)

    if not file_path.exists():
        print(f"警告: 文件不存在: {file_path}")
        return

    # 读取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"读取文件失败: {file_path}, 错误: {e}")
        return

    # 根据语言设置标题
    if language == 'zh':
        note_title = "说明"
        warning_title = "注意"
    else:
        note_title = "Note"
        warning_title = "Warning"

    # 定义替换规则
    replacements = [
        # Note 标签 - 处理带空格的 class 属性和缩进，支持单引号和双引号
        (r'(\s*)<div\s+class\s*=\s*["\']mk-hint["\']>([\s\S]*?)</div>', rf'\n\n<Note title="{note_title}">\n\2\n</Note>\n\n'),
        # Note 标签 - 处理无引号的 class 属性
        (r'(\s*)<div\s+class\s*=\s*mk-hint(?:\s+[^>]*)?>([\s\S]*?)</div>', rf'\n\n<Note title="{note_title}">\n\2\n</Note>\n\n'),
        # Warning 标签 - 处理带空格的 class 属性和缩进，支持单引号和双引号
        (r'(\s*)<div\s+class\s*=\s*["\']mk-warning["\']>([\s\S]*?)</div>', rf'\n\n<Warning title="{warning_title}">\n\2\n</Warning>\n\n'),
        # Warning 标签 - 处理无引号的 class 属性
        (r'(\s*)<div\s+class\s*=\s*mk-warning(?:\s+[^>]*)?>([\s\S]*?)</div>', rf'\n\n<Warning title="{warning_title}">\n\2\n</Warning>\n\n'),
        # 移除 style 标签
        (r'^[\s]*<style[^>]*>[\s\S]*?</style>', ''),
        # 移除 colgroup 标签
        (r'<colgroup[^>]*>[\s\S]*?</colgroup>', ''),
        # 修复 br 标签
        (r'<br>', '<br />'),
    ]

    # 执行替换
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.IGNORECASE)

    # 处理标题序号去除
    content = remove_heading_numbers(content)

    # 处理 HTML 表格转换为 Markdown 表格
    # content = convert_html_tables_to_markdown(content)

    # 处理 YouTube 视频容器转换
    content = convert_youtube_videos(content)

    # 处理按钮组件转换
    content = convert_buttons(content)

    # 处理卡片组转换
    content = convert_card_groups(content)

    # 处理资源布局转换
    content = convert_resource_layouts(content)

    # 处理 SDK 下载区域转换
    content = convert_sdk_downloads(content)

    # 处理代码组转换
    content = convert_code_groups(content)

    # 处理图片标签 - 改进版本
    content = convert_images_to_frames(content)

    # 处理折叠内容转换
    content = convert_details_to_accordion(content)

    # 处理特殊链接格式（处理 \|_blank 标记）
    content = re.sub(r'\[([^\]]+)\\\|_blank\]\(([^)]+)\)', r'[\1](\2)', content)

    # 处理链接转换
    content = convert_links(content, file_path.parent, language)

    # 移除前导空格
    content = content.lstrip()

    # 写回文件
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"内容替换完成: {file_path}")
    except Exception as e:
        print(f"写入文件失败: {file_path}, 错误: {e}")


def convert_html_tables_to_markdown(content):
    """
    将 HTML 表格转换为 Markdown 表格

    Args:
        content (str): 文件内容

    Returns:
        str: 转换后的内容
    """
    import re

    def table_replacer(match):
        html_table = match.group(0)

        # 提取表格行
        rows = re.findall(r'<tr[^>]*>([\s\S]*?)</tr>', html_table, re.IGNORECASE)
        if not rows:
            return html_table

        markdown_table = ''
        is_header_row = True

        for row in rows:
            # 提取表头和数据单元格
            header_cells = re.findall(r'<th[^>]*>([\s\S]*?)</th>', row, re.IGNORECASE)
            data_cells = re.findall(r'<td[^>]*>([\s\S]*?)</td>', row, re.IGNORECASE)
            cells = header_cells if header_cells else data_cells

            if not cells:
                continue

            # 处理每个单元格内容
            processed_cells = []
            for cell in cells:
                # 移除 HTML 标签并清理内容
                cell_content = re.sub(r'<[^>]+>', '', cell)
                cell_content = cell_content.strip().replace('\n', ' ')
                processed_cells.append(cell_content)

            # 构建 Markdown 表格行
            markdown_table += '| ' + ' | '.join(processed_cells) + ' |\n'

            # 在表头后添加分隔符
            if is_header_row and header_cells:
                markdown_table += '| ' + ' | '.join([':--'] * len(processed_cells)) + ' |\n'
                is_header_row = False

        return markdown_table

    # 匹配 HTML 表格
    table_pattern = r'<table[^>]*>[\s\S]*?</table>'
    content = re.sub(table_pattern, table_replacer, content, flags=re.IGNORECASE)

    return content


def convert_youtube_videos(content):
    """
    将 YouTube 视频容器转换为 Video 组件

    Args:
        content (str): 文件内容

    Returns:
        str: 转换后的内容
    """
    def video_replacer(match):
        video_container = match.group(0)

        # 提取 iframe src 属性
        src_match = re.search(r'<iframe\s+src="([^"]+)"', video_container, re.IGNORECASE)
        if not src_match:
            return video_container

        src = src_match.group(1)
        return f'<Video src="{src}"/>'

    # 匹配 YouTube 视频容器
    video_pattern = r'<div class="youtube-video-container">[\s\S]*?</div>'
    content = re.sub(video_pattern, video_replacer, content, flags=re.IGNORECASE)

    return content


def convert_buttons(content):
    """
    将按钮 HTML 转换为 Button 组件

    Args:
        content (str): 文件内容

    Returns:
        str: 转换后的内容
    """
    # 定义不同类型的按钮模式
    button_patterns = [
        # Simple 按钮
        (r'<a\s+href="([^"]+)"\s+class="md-btn-primary simple"[^>]*>(?:\s*<img\s+[^>]*>)*\s*<span\s+class="text">([^<]+)</span>\s*</a>',
         r'<Button href="\1" primary-color="Orange" target="_blank">\2</Button>'),
        # Normal 按钮
        (r'<a\s+href="([^"]+)"\s+class="md-btn-primary normal"[^>]*>(?:\s*<img\s+[^>]*>)*\s*<span\s+class="text">([^<]+)</span>\s*</a>',
         r'<Button href="\1" primary-color="NavyBlue" target="_blank">\2</Button>'),
        # Important 按钮
        (r'<a\s+href="([^"]+)"\s+class="md-btn-primary important"[^>]*>(?:\s*<img\s+[^>]*>)*\s*<span\s+class="text">([^<]+)</span>\s*</a>',
         r'<Button href="\1" primary-color="Red" target="_blank">\2</Button>'),
    ]

    for pattern, replacement in button_patterns:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

    return content


def convert_card_groups(content):
    """
    将卡片组 HTML 转换为 CardGroup 组件

    Args:
        content (str): 文件内容

    Returns:
        str: 转换后的内容
    """
    def card_group_replacer(match):
        group_content = match.group(1)

        # 提取列数
        cols_match = re.search(r'grid-(\d+)', match.group(0))
        cols = int(cols_match.group(1)) if cols_match else 2

        # 提取卡片
        card_pattern = r'<a href="([^"]+)" class="md-grid-item"(?: target="_blank")?>\s*<div class="grid-title">([^<]+)</div>\s*<div class="grid-desc">([\s\S]*?)</div>\s*</a>'
        cards = re.findall(card_pattern, group_content + '\n</a>', re.IGNORECASE)

        card_components = []
        for href, title, desc in cards:
            card_components.append(f'<Card title="{title.strip()}" href="{href.strip()}">\n  {desc.strip()}\n</Card>')

        cards_content = '\n  '.join(card_components)
        return f'<CardGroup cols={{{cols}}}>\n  {cards_content}\n</CardGroup>'

    # 匹配卡片组
    card_group_pattern = r'<div class="md-grid-list-box(?: grid-\d+)?">((?:.|\n)*?)</a>\s*</div>'
    content = re.sub(card_group_pattern, card_group_replacer, content, flags=re.IGNORECASE)

    return content


def convert_resource_layouts(content):
    """
    将资源布局 HTML 转换为 CardGroup 组件

    Args:
        content (str): 文件内容

    Returns:
        str: 转换后的内容
    """
    def resource_layout_replacer(match):
        layout_content = match.group(1)

        # 提取资源项目
        item_pattern = r'<div class="md-resource-layout-item">((?:.|\n)*?)</div>'
        items = re.findall(item_pattern, layout_content, re.IGNORECASE)

        card_components = []
        for item_content in items:
            card_title = ''
            card_desc = ''
            card_links = ''
            card_bottom = ''

            # 提取顶部内容
            top_match = re.search(r'<div class="item-top">((?:.|\n)*?)</div>', item_content, re.IGNORECASE)
            if top_match:
                top_content = top_match.group(1)

                # 提取标题
                title_match = re.search(r'<div class="resource-title">([^<]+)</div>', top_content, re.IGNORECASE)
                if title_match:
                    card_title = title_match.group(1).strip()

                # 提取描述
                desc_match = re.search(r'<div class="resource-desc">([^<]+)</div>', top_content, re.IGNORECASE)
                if desc_match:
                    card_desc = desc_match.group(1).strip()

                # 提取链接
                link_matches = re.findall(r'<a href="([^"]*)" class="md-btn-primary important" target="_blank">\s*<span class="text">([^<]+)</span>\s*</a>', top_content, re.IGNORECASE)
                for href, text in link_matches:
                    card_links += f'<Button primary-color="NavyBlue" target="_blank" href="{href.strip()}">{text.strip()}</Button>\n'

            # 提取底部内容
            bottom_match = re.search(r'<div class="item-bottom">((?:.|\n)*?)</div>', item_content, re.IGNORECASE)
            if bottom_match:
                bottom_content = bottom_match.group(1)

                # 提取段落
                p_matches = re.findall(r'<p class="margin-top-20">([^<]+)</p>', bottom_content, re.IGNORECASE)
                for p_content in p_matches:
                    card_bottom += f'<p>{p_content.strip()}</p>\n'

                # 提取底部链接
                link_matches = re.findall(r'<a href="([^"]*)" class="md-btn-primary important" target="_blank">\s*<span class="text">([^<]+)</span>\s*</a>', bottom_content, re.IGNORECASE)
                for href, text in link_matches:
                    card_bottom += f'<Button primary-color="NavyBlue" target="_blank" href="{href.strip()}">{text.strip()}</Button>\n'

            card_content = card_links + card_bottom.strip()
            card_components.append(f'<Card title="{card_title}" description="{card_desc}">\n  {card_content}\n</Card>')

        cards_content = '\n  '.join(card_components)
        return f'<CardGroup cols={{2}}>\n  {cards_content.strip()}\n</CardGroup>'

    # 匹配资源布局
    resource_layout_pattern = r'<div class="md-resource-layout">((?:.|\n)*?)</div>'
    content = re.sub(resource_layout_pattern, resource_layout_replacer, content, flags=re.IGNORECASE)

    return content


def convert_sdk_downloads(content):
    """
    将旧版 SDK 下载 HTML 结构转换为 Card 组件

    Args:
        content (str): 文件内容

    Returns:
        str: 转换后的内容
    """
    def replacer(match):
        block = match.group(0)

        # 提取标题
        title_match = re.search(r'<div\s+class="download-title">\s*([^<]+?)\s*</div>', block, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else "下载"

        # 提取链接
        href_match = re.search(r'data-href="([^"]+)"', block)
        if not href_match:
            href_match = re.search(r'<a[^>]+href="([^"]+)"[^>]*>', block, re.IGNORECASE)
        href = href_match.group(1).strip() if href_match else "#"

        # 提取按钮文本
        text_match = re.search(r'<li[^>]*>\s*([^<]+?)\s*</li>', block)
        if not text_match:
            text_match = re.search(r'<a[^>]*class="download-target-btn"[^>]*>\s*([^<]+?)\s*</a>', block, re.IGNORECASE)
        text = text_match.group(1).strip() if text_match else title

        return f'<Card title="{title}" href="{href}" target="_blank">\n{text}\n</Card>'

    # 使用非贪婪匹配获取下载块
    pattern = r'<div[^>]*class="sdk-download-wrapper[^"]*"[\s\S]*?</div>\s*</div>'
    content = re.sub(pattern, replacer, content, flags=re.IGNORECASE)

    return content


def convert_code_groups(content):
    """
    将代码组 HTML 转换为 CodeGroup 组件

    Args:
        content (str): 文件内容

    Returns:
        str: 转换后的内容
    """
    def code_group_replacer(match):
        group_content = match.group(0)

        # 提取标签标题
        tab_pattern = r'<span class="tab-item">\s*<span>(.*?)</span>\s*</span>'
        titles = re.findall(tab_pattern, group_content, re.IGNORECASE)

        # 提取代码块
        code_pattern = r'```(\w+)([\s\S]*?)```'
        codes = re.findall(code_pattern, group_content)

        result = '<CodeGroup>\n'
        for i, (lang, code_content) in enumerate(codes):
            title = titles[i] if i < len(titles) else ''
            title_attr = f' title="{title}"' if title else ''
            result += f'```{lang}{title_attr}{code_content}```\n'
        result += '</CodeGroup>'

        return result

    # 这个模式需要根据实际的 HTML 结构调整
    # 由于代码组的 HTML 结构可能比较复杂，这里提供一个基础实现
    # 可能需要根据实际情况进一步调整

    return content


def convert_details_to_accordion(content):
    """
    将 HTML details/summary 标签转换为 Accordion 组件

    Args:
        content (str): 文件内容

    Returns:
        str: 转换后的内容
    """
    def details_replacer(match):
        details_tag = match.group(0)
        
        # 检查是否有 open 属性
        is_open = 'open' in details_tag
        default_open = "true" if is_open else "false"
        
        # 提取 summary 内容
        summary_match = re.search(r'<summary[^>]*>([\s\S]*?)</summary>', details_tag, re.IGNORECASE)
        if summary_match:
            title = summary_match.group(1).strip()
            # 移除 HTML 标签
            title = re.sub(r'<[^>]+>', '', title)
        else:
            title = "折叠内容"  # 默认标题
        
        # 提取 details 内容（除了 summary）
        content_without_summary = re.sub(r'<summary[^>]*>[\s\S]*?</summary>', '', details_tag, flags=re.IGNORECASE)
        # 移除外层的 details 标签
        content_match = re.search(r'<details[^>]*>([\s\S]*?)</details>', content_without_summary, re.IGNORECASE)
        if content_match:
            accordion_content = content_match.group(1).strip()
        else:
            accordion_content = ""
        
        # 如果没有内容，添加占位符
        if not accordion_content:
            accordion_content = "内容"
        
        return f'<Accordion title="{title}" defaultOpen="{default_open}">\n{accordion_content}\n</Accordion>'
    
    # 匹配 details 标签
    details_pattern = r'<details[^>]*>[\s\S]*?</details>'
    content = re.sub(details_pattern, details_replacer, content, flags=re.IGNORECASE)
    
    return content


def convert_images_to_frames(content):
    """
    将图片标签转换为 Frame 组件，改进版本

    Args:
        content (str): 文件内容

    Returns:
        str: 转换后的内容
    """
    def replace_img(match):
        # 获取 src 属性
        src = match.group(1)

        # 跳过已经处理过的图片
        if src.startswith('https://storage.zego.im/sdk-doc'):
            return match.group(0)

        if src.startswith('/Pics'):
            # 构建完整 URL
            full_url = f"https://storage.zego.im/sdk-doc{src}"
            return f'<Frame width="512" height="auto" caption=""><img src="{full_url}" /></Frame>'
        elif src.startswith('http://doc.oa.zego.im'):
            # 处理 http://doc.oa.zego.im 链接
            path = src.replace('http://doc.oa.zego.im', '')
            full_url = f"https://storage.zego.im/sdk-doc{path}"
            return f'<Frame width="512" height="auto" caption=""><img src="{full_url}" /></Frame>'
        elif src.startswith('//doc.oa.zego.im'):
            # 处理内部链接
            full_url = f"https://storage.zego.im/sdk-doc{src.replace('//doc.oa.zego.im', '')}"
            return f'<Frame width="512" height="auto" caption=""><img src="{full_url}" /></Frame>'
        elif src.startswith('https'):
            # 处理 HTTPS 链接
            return f'<Frame width="512" height="auto" caption=""><img src="{src}" /></Frame>'

        return match.group(0)

    def replace_markdown_img(match):
        # 获取 alt 和 src
        alt = match.group(1)
        src = match.group(2)

        # 跳过已经处理过的图片
        if src.startswith('https://storage.zego.im/sdk-doc'):
            return match.group(0)

        if src.startswith('/Pics'):
            # 构建完整 URL
            full_url = f"https://storage.zego.im/sdk-doc{src}"
            return f'<Frame width="512" height="auto" caption=""><img src="{full_url}" /></Frame>'
        elif src.startswith('http://doc.oa.zego.im'):
            # 处理 http://doc.oa.zego.im 链接
            path = src.replace('http://doc.oa.zego.im', '')
            full_url = f"https://storage.zego.im/sdk-doc{path}"
            return f'<Frame width="512" height="auto" caption=""><img src="{full_url}" /></Frame>'
        elif src.startswith('//doc.oa.zego.im'):
            # 处理内部链接
            full_url = f"https://storage.zego.im/sdk-doc{src.replace('//doc.oa.zego.im', '')}"
            return f'<Frame width="512" height="auto" caption=""><img src="{full_url}" /></Frame>'
        elif src.startswith('https'):
            # 处理 HTTPS 链接
            return f'<Frame width="512" height="auto" caption=""><img src="{src}" /></Frame>'

        return match.group(0)

    # 处理 Markdown 图片语法
    content = re.sub(r'!\[(.*?)\]\((\/Pics.*?)\)', replace_markdown_img, content)
    content = re.sub(r'!\[(.*?)\]\((http://doc\.oa\.zego\.im.*?)\)', replace_markdown_img, content)
    content = re.sub(r'!\[(.*?)\]\((//doc\.oa\.zego\.im.*?)\)', replace_markdown_img, content)
    content = re.sub(r'!\[(.*?)\]\((https.*?)\)', replace_markdown_img, content)

    # 处理 HTML 图片标签
    content = re.sub(r'<img\s+[^>]*src="([^"]+)"[^>]*>', replace_img, content)

    return content


def process_doc_conversion(source_dir):
    """
    处理文档转换的完整流程

    Args:
        source_dir (str): 源目录路径
    """
    print("=" * 60)
    print("开始文档转换流程")
    print("=" * 60)

    try:
        source_path = Path(source_dir)
        if not source_path.exists():
            print(f"错误: 源目录不存在: {source_path}")
            return

        print("\n========= 开始转换文件目录 =========")
        path_map = transform_directory_structure(source_dir)
        create_directories_and_files(source_dir, path_map)
        print("========= 文件目录转换完成 =========")

    except Exception as e:
        print(f"❌ 文档转换失败: {e}")

def process_content_conversion(source_dir, language='zh'):
    """
    处理内容转换的完整流程
    """
    print("=" * 60)
    print("开始内容转换流程")
    print("=" * 60)

    # 内容替换
    print("\n========= 开始替换语法内容 =========")
    print(f"处理目录: {source_dir}")
    print(f"处理语言: {'中文' if language == 'zh' else '英文'}")
    source_path = Path(source_dir)
    file_paths = get_relative_paths(source_path)
    for file_path in file_paths:
        full_file_path = source_path / file_path
        if full_file_path.suffix in ['.md', '.mdx']:
            replace_content(full_file_path, language)
    print("========= 所有页面语法内容替换完成 =========")
    print(f"\n✅ 内容转换完成！输出目录: dist/{source_path.name}")


# ==================== 原有的文件名格式化功能 ====================

def should_rename(name):
    """
    判断是否需要重命名

    Args:
        name (str): 文件或目录名

    Returns:
        bool: 是否需要重命名
    """
    converted = convert_name_format(name)
    return name != converted


def rename_item(old_path, new_path):
    """
    重命名文件或目录

    Args:
        old_path (Path): 原路径
        new_path (Path): 新路径

    Returns:
        bool: 是否成功重命名
    """
    try:
        if old_path.exists() and not new_path.exists():
            old_path.rename(new_path)
            print(f"重命名: {old_path} -> {new_path}")
            return True
        elif new_path.exists():
            print(f"警告: 目标路径已存在，跳过重命名: {new_path}")
            return False
        else:
            print(f"错误: 源路径不存在: {old_path}")
            return False
    except Exception as e:
        print(f"重命名失败: {old_path} -> {new_path}, 错误: {e}")
        return False


def process_directory(directory_path):
    """
    递归处理目录，重命名所有需要格式化的文件和目录

    Args:
        directory_path (Path): 要处理的目录路径
    """
    if not directory_path.exists():
        print(f"错误: 目录不存在: {directory_path}")
        return

    if not directory_path.is_dir():
        print(f"错误: 路径不是目录: {directory_path}")
        return

    print(f"正在处理目录: {directory_path}")

    # 收集所有需要重命名的项目
    items_to_rename = []

    # 使用 os.walk 遍历目录树，从最深层开始处理
    for root, dirs, files in os.walk(directory_path, topdown=False):
        root_path = Path(root)

        # 处理文件
        for file_name in files:
            if should_rename(file_name):
                old_file_path = root_path / file_name
                new_file_name = convert_name_format(file_name)
                new_file_path = root_path / new_file_name
                items_to_rename.append((old_file_path, new_file_path, 'file'))

        # 处理目录
        for dir_name in dirs:
            if should_rename(dir_name):
                old_dir_path = root_path / dir_name
                new_dir_name = convert_name_format(dir_name)
                new_dir_path = root_path / new_dir_name
                items_to_rename.append((old_dir_path, new_dir_path, 'directory'))

    # 执行重命名
    success_count = 0
    total_count = len(items_to_rename)

    if total_count == 0:
        print("没有找到需要重命名的文件或目录。")
        return

    print(f"\n找到 {total_count} 个需要重命名的项目:")
    for old_path, new_path, item_type in items_to_rename:
        print(f"  {item_type}: {old_path.name} -> {new_path.name}")

    confirm = input(f"\n是否继续执行重命名操作？(y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("操作已取消。")
        return

    print("\n开始执行重命名操作...")
    for old_path, new_path, item_type in items_to_rename:
        if rename_item(old_path, new_path):
            success_count += 1

    print(f"\n重命名完成: {success_count}/{total_count} 个项目成功重命名。")


def get_user_choice():
    """
    获取用户选择的功能

    Returns:
        tuple: (choice, language) 用户选择的功能和语言
    """
    # 首先选择语言
    while True:
        print("\n" + "=" * 60)
        print("选择处理语言")
        print("=" * 60)
        print("请选择要处理的语言：")
        print("1. 中文 (默认)")
        print("2. 英文")
        print("=" * 60)

        lang_choice = input("请输入选项 (1-2, 直接回车默认中文): ")


        if lang_choice == '1' or lang_choice == '':
            language = 'zh'
            print("✅ 已选择中文")
            break
        elif lang_choice == '2':
            language = 'en'
            print("✅ 已选择英文")
            break
        else:
            print("❌ 无效选项，请输入 1-2")

    # 然后选择功能
    while True:
        print("\n" + "=" * 60)
        print("文档迁移工具")
        print("=" * 60)
        print("请选择要执行的功能：")
        print("1. 文档转换 (md -> mdx + 目录重组)")
        print("2. 更新 sidebars.json")
        print("3. 内容语法替换 (已把实例放到 docuo.config.json 配置好)")
        print("4. 生成nginx重定向配置")
        print("5. 退出")
        print("=" * 60)

        choice = input("请输入选项 (1-5): ").strip()

        if choice == '1':
            return 'convert', language
        elif choice == '2':
            return 'update_sidebar', language
        elif choice == '3':
            return 'content', language
        elif choice == '4':
            return 'generate_redirect', language
        elif choice == '5':
            return 'quit', language
        else:
            print("❌ 无效选项，请输入 1-5")


def get_target_directory_for_format():
    """
    获取用户指定的目标目录（用于格式化功能）

    Returns:
        Path: 目标目录路径，如果用户取消则返回 None
    """
    while True:
        user_input = input("请输入要处理的目录路径（绝对路径或相对路径）: ").strip()

        if not user_input:
            print("路径不能为空，请重新输入。")
            continue

        # 处理相对路径和绝对路径
        if os.path.isabs(user_input):
            target_path = Path(user_input)
        else:
            # 相对路径基于项目根目录
            project_root = Path(__file__).parent.parent.parent
            target_path = project_root / user_input

        # 规范化路径
        target_path = target_path.resolve()

        if target_path.exists():
            if target_path.is_dir():
                print(f"目标目录: {target_path}")
                confirm = input("确认处理此目录？(y/N): ").strip().lower()
                if confirm in ['y', 'yes']:
                    return target_path
                else:
                    continue
            else:
                print(f"错误: 路径不是目录: {target_path}")
                continue
        else:
            print(f"错误: 路径不存在: {target_path}")
            continue


def get_source_directory_for_convert():
    """
    获取用户指定的源目录（用于文档转换功能）

    Returns:
        str: 源目录路径，如果用户取消则返回 None
    """
    while True:
        user_input = input("请输入要转换的源目录路径（绝对路径或相对路径）: ").strip()

        if not user_input:
            print("路径不能为空，请重新输入。")
            continue

        # 处理相对路径和绝对路径
        if os.path.isabs(user_input):
            source_path = Path(user_input)
        else:
            # 相对路径基于当前工作目录
            source_path = Path.cwd() / user_input

        # 规范化路径
        source_path = source_path.resolve()

        if source_path.exists():
            if source_path.is_dir():
                print(f"源目录: {source_path}")
                confirm = input("确认转换此目录？(y/N): ").strip().lower()
                if confirm in ['y', 'yes']:
                    return str(source_path)
                else:
                    continue
            else:
                print(f"错误: 路径不是目录: {source_path}")
                continue
        else:
            print(f"错误: 路径不存在: {source_path}")
            continue


def extract_title_from_mdx(file_path):
    """
    从 MDX 文件中提取一级标题

    Args:
        file_path (Path): MDX 文件路径

    Returns:
        str: 一级标题内容，如果没有找到则返回 None
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 使用正则表达式匹配一级标题
            match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if match:
                return match.group(1).strip()
    except Exception as e:
        print(f"读取文件失败: {file_path}, 错误: {e}")
    return None

def get_relative_path(file_path, base_dir):
    """
    获取文件相对于基础目录的路径

    Args:
        file_path (Path): 文件路径
        base_dir (Path): 基础目录路径

    Returns:
        str: 相对路径
    """
    try:
        relative_path = file_path.relative_to(base_dir)
        # 移除 .mdx 扩展名
        return str(relative_path.with_suffix(''))
    except Exception as e:
        print(f"获取相对路径失败: {file_path}, 错误: {e}")
        return None

def update_sidebars_json(source_dir):
    """
    更新 sidebars.json 文件

    Args:
        source_dir (str): 源目录路径
    """
    print("=" * 60)
    print("开始更新 sidebars.json")
    print("=" * 60)

    try:
        source_path = Path(source_dir)
        if not source_path.exists():
            print(f"错误: 源目录不存在: {source_path}")
            return

        # 检查 sidebars.json 是否存在
        sidebars_path = source_path / 'sidebars.json'
        if not sidebars_path.exists():
            print(f"错误: sidebars.json 文件不存在: {sidebars_path}")
            return

        # 读取 sidebars.json
        try:
            with open(sidebars_path, 'r', encoding='utf-8') as f:
                sidebars_data = json.load(f)
        except Exception as e:
            print(f"读取 sidebars.json 失败: {e}")
            return

        # 遍历目录，收集所有 MDX 文件的信息
        title_to_path = {}
        for root, dirs, files in os.walk(source_path):
            for file in files:
                if file.endswith('.mdx'):
                    file_path = Path(root) / file
                    title = extract_title_from_mdx(file_path)
                    if title:
                        relative_path = get_relative_path(file_path, source_path)
                        if relative_path:
                            title_to_path[title] = relative_path

        # 递归更新 sidebars.json 中的 id
        def update_items(items):
            for item in items:
                if item.get('type') == 'doc':
                    label = item.get('label')
                    if label in title_to_path:
                        # 保存原有的 articleID
                        article_id = item.get('articleID')
                        if article_id:
                            # 更新对应 MDX 文件的 frontmatter
                            mdx_path = source_path / f"{title_to_path[label]}.mdx"
                            try:
                                with open(mdx_path, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                
                                # 检查是否已有 frontmatter
                                if not content.startswith('---'):
                                    # 如果没有 frontmatter，添加新的
                                    content = f"---\narticleID: {article_id}\n---\n{content}"
                                else:
                                    # 提取现有的 frontmatter
                                    frontmatter_match = re.match(r'^---(.*?)---', content, re.DOTALL)
                                    if frontmatter_match:
                                        frontmatter = frontmatter_match.group(1)
                                        remaining_content = content[len(frontmatter_match.group(0)):]
                                        
                                        # 检查是否已存在 articleID
                                        if re.search(r'^articleID:', frontmatter, re.MULTILINE):
                                            # 更新现有的 articleID
                                            updated_frontmatter = re.sub(
                                                r'^articleID:.*$',
                                                f'articleID: {article_id}',
                                                frontmatter,
                                                flags=re.MULTILINE
                                            )
                                        else:
                                            # 添加新的 articleID
                                            updated_frontmatter = frontmatter.rstrip() + f'\narticleID: {article_id}'
                                        
                                        # 重组内容
                                        content = f"---{updated_frontmatter}---{remaining_content}"
                                
                                with open(mdx_path, 'w', encoding='utf-8') as f:
                                    f.write(content)
                            except Exception as e:
                                print(f"更新 MDX 文件 frontmatter 失败: {mdx_path}, 错误: {e}")
                        
                        # 更新 id
                        item['id'] = title_to_path[label]
                elif item.get('type') == 'category' and 'items' in item:
                    update_items(item['items'])

        # 更新 sidebars.json
        update_items(sidebars_data['mySidebar'])

        # 保存更新后的 sidebars.json
        try:
            with open(sidebars_path, 'w', encoding='utf-8') as f:
                json.dump(sidebars_data, f, indent=2, ensure_ascii=False)
            print(f"✅ sidebars.json 更新完成！")
        except Exception as e:
            print(f"保存 sidebars.json 失败: {e}")

    except Exception as e:
        print(f"❌ 更新 sidebars.json 失败: {e}")

def convert_links(content, target_dir, language):
    """
    转换文档中的链接

    Args:
        content (str): 文档内容
        target_dir (Path): 目标目录路径
        language (str): 语言 ('zh' 或 'en')

    Returns:
        str: 转换后的内容
    """
    target_dir = Path(target_dir)
    
    # 根据语言确定域名
    if language == 'zh':
        domain = 'https://doc-zh.zego.im'
        config_file = 'docuo.config.zh.json'
    else:
        domain = 'https://docs.zegocloud.com'
        config_file = 'docuo.config.en.json'

    def replace_link(match):
        full_match = match.group(0)
        link_text = match.group(1)
        link_url = match.group(2)

        # 处理 /article/api? 开头的链接
        if link_url.startswith('/article/api?'):
            return f'[{link_text}]({domain}{link_url})'
        
        # 处理 /unique-api/ 开头的链接
        elif link_url.startswith('/unique-api/'):
            return f'[{link_text}]({domain}{link_url})'
        
        # 处理 #数字 开头的链接
        elif re.match(r'^#\d+', link_url):
            # 提取文章ID和锚点
            match_id = re.match(r'^#(\d+)(#.*)?$', link_url)
            if match_id:
                article_id = match_id.group(1)
                anchor = match_id.group(2) if match_id.group(2) else ''
                
                # 查找对应的路径
                new_url = find_article_path(target_dir, article_id, language, config_file)
                if new_url:
                    return f'[{link_text}]({new_url}{anchor})'
                else:
                    # 如果找不到对应路径，使用域名前缀
                    return f'[{link_text}]({domain}/article/{article_id}{anchor})'
        
        # 其他链接保持不变
        return full_match

    # 匹配 Markdown 链接格式 [text](url)
    link_pattern = r'\[([^\]]*)\]\(([^)]+)\)'
    content = re.sub(link_pattern, replace_link, content)
    
    return content


def find_article_path(target_dir, article_id, language, config_file):
    """
    根据文章ID查找对应的路径

    Args:
        target_dir (Path): 目标目录
        article_id (str): 文章ID
        language (str): 语言
        config_file (str): 配置文件名

    Returns:
        str: 找到的路径，如果没找到则返回None
    """
    target_dir = Path(target_dir)
    
    # 1. 读取配置文件获取 routeBasePath
    # 配置文件在项目根目录
    project_root = Path(__file__).parent.parent.parent
    config_path = project_root / config_file
    route_base_path = ''
    
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                
            # 查找匹配的实例
            instances = config_data.get('instances', [])
            for instance in instances:
                instance_path = instance.get('path', '')
                # 检查目标目录是否匹配实例路径
                target_relative = target_dir.relative_to(project_root) if project_root in target_dir.parents else target_dir
                if str(target_relative) in instance_path or target_dir.name in instance_path:
                    route_base_path = instance.get('routeBasePath', '')
                    break
        except Exception as e:
            print(f"读取配置文件失败: {e}")
    
    # 2. 查找 sidebars.json 中的对应项
    def search_in_sidebars(sidebars_path):
        if not sidebars_path.exists():
            return None
            
        try:
            with open(sidebars_path, 'r', encoding='utf-8') as f:
                sidebars_data = json.load(f)
            
            def find_in_items(items):
                for item in items:
                    if item.get('articleID') == article_id:
                        return item.get('id')
                    elif item.get('type') == 'category' and 'items' in item:
                        result = find_in_items(item['items'])
                        if result:
                            return result
                return None
            
            sidebar_items = sidebars_data.get('mySidebar', [])
            found_id = find_in_items(sidebar_items)
            
            if found_id and route_base_path:
                return f"/{route_base_path}/{found_id}"
            elif found_id:
                return f"/{found_id}"
                
        except Exception as e:
            print(f"读取 sidebars.json 失败: {e}")
        
        return None
    
    # 3. 先在目标目录查找
    sidebars_path = target_dir / 'sidebars.json'
    result = search_in_sidebars(sidebars_path)
    if result:
        return result
    
    # 4. 在兄弟目录查找
    if target_dir.parent.exists():
        for sibling_dir in target_dir.parent.iterdir():
            if sibling_dir.is_dir() and sibling_dir != target_dir:
                sibling_sidebars = sibling_dir / 'sidebars.json'
                result = search_in_sidebars(sibling_sidebars)
                if result:
                    return result
    
    return None

def generate_nginx_redirect_config(source_dir, language='zh'):
    """
    生成nginx重定向配置文件

    Args:
        source_dir (str): 包含sidebars.json的源目录路径
        language (str): 语言 ('zh' 或 'en')
    """
    print("=" * 60)
    print("开始生成nginx重定向配置")
    print("=" * 60)

    try:
        source_path = Path(source_dir)
        if not source_path.exists():
            print(f"错误: 源目录不存在: {source_path}")
            return

        # 检查 sidebars.json 是否存在
        sidebars_path = source_path / 'sidebars.json'
        if not sidebars_path.exists():
            print(f"错误: sidebars.json 文件不存在: {sidebars_path}")
            return

        # 根据语言确定域名和配置文件
        if language == 'zh':
            domain = 'https://doc-zh.zego.im'
            config_file = 'docuo.config.zh.json'
        else:
            domain = 'https://www.zegocloud.com/docs'
            config_file = 'docuo.config.en.json'

        # 获取 routeBasePath
        route_base_path = get_route_base_path(source_path, config_file)
        if not route_base_path:
            print("警告: 无法找到匹配的 routeBasePath，将使用空路径")
            route_base_path = ''

        print(f"找到 routeBasePath: {route_base_path}")

        # 读取 sidebars.json
        try:
            with open(sidebars_path, 'r', encoding='utf-8') as f:
                sidebars_data = json.load(f)
        except Exception as e:
            print(f"读取 sidebars.json 失败: {e}")
            return

        # 收集所有重定向规则
        redirect_rules = []
        missing_article_ids = []
        
        def collect_redirects(items):
            for item in items:
                if item.get('type') == 'doc':
                    article_id = item.get('articleID')
                    item_id = item.get('id')
                    label = item.get('label', '')
                    
                    if not article_id:
                        missing_article_ids.append(f"  - {label} (id: {item_id})")
                        continue
                        
                    if article_id and item_id:
                        # 构建新链接
                        if route_base_path:
                            new_url = f"{domain}/{route_base_path}/{item_id}"
                        else:
                            new_url = f"{domain}/{item_id}"
                        
                        # 生成重定向规则
                        redirect_rule = f"if ($request_uri ~ /{article_id}) {{rewrite ^ {new_url}? permanent;}}"
                        redirect_rules.append(redirect_rule)
                        
                elif item.get('type') == 'category' and 'items' in item:
                    collect_redirects(item['items'])

        # 遍历 sidebars.json 收集重定向规则
        sidebar_items = sidebars_data.get('mySidebar', [])
        collect_redirects(sidebar_items)

        # 检查是否有缺失的 articleID
        if missing_article_ids:
            print(f"⚠️  检测到 {len(missing_article_ids)} 个文档项缺少 articleID 字段:")
            for missing in missing_article_ids:
                print(missing)
            print("\n💡 提示:")
            print("1. 如果您的 sidebars.json 还没有 articleID，可以先使用 '更新 sidebars.json' 功能添加 articleID")
            print("2. 或者手动在 sidebars.json 的每个 doc 项中添加 articleID 字段")
            print("3. articleID 是旧系统中的文章编号，用于重定向到新系统")
            
            if not redirect_rules:
                print("\n❌ 没有找到任何有效的重定向规则，操作终止")
                return
            else:
                print(f"\n继续处理 {len(redirect_rules)} 条有效的重定向规则...")

        if not redirect_rules:
            print("❌ 没有找到有效的重定向规则")
            return

        # 写入 redirect.txt 文件
        redirect_file_path = source_path / 'redirect.txt'
        try:
            with open(redirect_file_path, 'w', encoding='utf-8') as f:
                for rule in redirect_rules:
                    f.write(rule + '\n')
            
            print(f"✅ nginx重定向配置生成完成！")
            print(f"文件位置: {redirect_file_path}")
            print(f"共生成 {len(redirect_rules)} 条重定向规则")
            
        except Exception as e:
            print(f"写入 redirect.txt 失败: {e}")

    except Exception as e:
        print(f"❌ 生成nginx重定向配置失败: {e}")


def get_route_base_path(target_dir, config_file):
    """
    根据目标目录从配置文件获取 routeBasePath

    Args:
        target_dir (Path): 目标目录
        config_file (str): 配置文件名

    Returns:
        str: routeBasePath，如果没找到则返回空字符串
    """
    target_dir = Path(target_dir)
    
    # 配置文件在项目根目录
    project_root = Path(__file__).parent.parent.parent
    config_path = project_root / config_file
    
    if not config_path.exists():
        print(f"警告: 配置文件不存在: {config_path}")
        return ''
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
            
        # 获取目标目录相对于项目根目录的路径
        try:
            target_relative = target_dir.relative_to(project_root)
            target_path_str = str(target_relative).replace('\\', '/')  # 统一使用正斜杠
        except ValueError:
            # 如果不在项目根目录下，使用绝对路径
            target_path_str = str(target_dir).replace('\\', '/')
        
        print(f"目标路径: {target_path_str}")
        
        # 查找匹配的实例 - 使用精确匹配
        instances = config_data.get('instances', [])
        matched_instances = []
        
        for instance in instances:
            instance_path = instance.get('path', '')
            instance_id = instance.get('id', '')
            route_base_path = instance.get('routeBasePath', '')
            
            # 精确匹配路径
            if instance_path == target_path_str:
                print(f"精确匹配找到实例: {instance_id} -> {route_base_path}")
                return route_base_path
            
            # 检查是否是路径的一部分（用于部分匹配）
            if target_path_str in instance_path or instance_path in target_path_str:
                matched_instances.append({
                    'id': instance_id,
                    'path': instance_path,
                    'routeBasePath': route_base_path,
                    'score': len(instance_path) if instance_path in target_path_str else len(target_path_str)
                })
        
        # 如果没有精确匹配，选择最佳的部分匹配
        if matched_instances:
            # 按匹配度排序，选择最长匹配
            best_match = max(matched_instances, key=lambda x: x['score'])
            print(f"部分匹配找到最佳实例: {best_match['id']} (路径: {best_match['path']}) -> {best_match['routeBasePath']}")
            return best_match['routeBasePath']
        
        # 如果还是没找到，尝试目录名匹配
        target_dir_name = target_dir.name
        for instance in instances:
            instance_path = instance.get('path', '')
            if target_dir_name in instance_path:
                print(f"目录名匹配找到实例: {instance.get('id', '')} -> {instance.get('routeBasePath', '')}")
                return instance.get('routeBasePath', '')
                
    except Exception as e:
        print(f"读取配置文件失败: {e}")
    
    print("未找到匹配的实例")
    return ''

def main():
    """
    主函数
    """
    try:
        while True:
            choice, language = get_user_choice()

            if choice == 'quit':
                print("👋 再见！")
                break
            elif choice == 'content':
                source_directory = get_source_directory_for_convert()
                if source_directory:
                    process_content_conversion(source_directory, language)
                else:
                    print("操作已取消。")
            elif choice == 'convert':
                source_directory = get_source_directory_for_convert()
                if source_directory:
                    process_doc_conversion(source_directory)
                else:
                    print("操作已取消。")
            elif choice == 'update_sidebar':
                source_directory = get_source_directory_for_convert()
                if source_directory:
                    update_sidebars_json(source_directory)
                else:
                    print("操作已取消。")
            elif choice == 'generate_redirect':
                source_directory = get_source_directory_for_convert()
                if source_directory:
                    generate_nginx_redirect_config(source_directory, language)
                else:
                    print("操作已取消。")

            # 询问是否继续
            continue_choice = input("\n是否继续使用其他功能？(y/N): ").strip().lower()
            if continue_choice not in ['y', 'yes']:
                print("👋 再见！")
                break

    except KeyboardInterrupt:
        print("\n\n操作被用户中断。")
    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()