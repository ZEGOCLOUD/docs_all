#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

# 终端彩色输出
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Dummy:
        def __getattr__(self, name):
            return ''
    Fore = Style = Dummy()

def choose_language():
    """选择中文或英文"""
    while True:
        print('请选择文档语言:')
        print('1. 中文')
        print('2. 英文')
        choice = input('输入数字选择(1/2)，直接回车默认 1: ').strip()
        if choice == '':
            choice = '1'
        if choice == '1':
            return 'zh', 'https://doc-zh.zego.im'
        elif choice == '2':
            return 'en', 'https://zegocloud.com/docs'
        else:
            print('输入无效，请重新输入。')

def get_nginx_config_path():
    """获取nginx配置文件路径"""
    default_path = os.path.join(os.path.dirname(__file__), 'nginx_redirect.conf')
    user_input = input(f'输入nginx重定向配置文件路径，直接回车使用默认路径 ({default_path}): ').strip()

    if user_input == '':
        return default_path

    if os.path.exists(user_input):
        return user_input
    else:
        print(f'{Fore.RED}文件不存在: {user_input}{Style.RESET_ALL}')
        return get_nginx_config_path()

def parse_nginx_config(config_path, domain):
    """从nginx配置文件中解析article id到目标链接的映射"""
    article_map = {}

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f'{Fore.RED}读取nginx配置文件失败: {e}{Style.RESET_ALL}')
        return article_map

    # 模式1: 匹配多个ID的格式 rewrite ^/article/(id1|id2|id3)$ https://... permanent;
    # 注意：nginx配置中的 $ 是字面字符，需要用 \\$ 或 [$] 来匹配
    pattern1 = r'^\s*rewrite\s+\^/article/\(([^)]+)\)[$]\s+([^\s]+)\s+permanent;'

    # 模式2: 匹配单个ID的格式 rewrite ^/article/id$ https://... permanent;
    pattern2 = r'^\s*rewrite\s+\^/article/(\d+)[$]\s+([^\s]+)\s+permanent;'

    # 处理多个ID的情况
    for match in re.finditer(pattern1, content, re.MULTILINE):
        article_ids_str = match.group(1)
        target_url = match.group(2)

        # 提取目标链接中的路径部分（去掉域名和末尾的?）
        if target_url.endswith('?'):
            target_url = target_url[:-1]

        # 提取路径部分
        if domain in target_url:
            target_path = target_url.replace(domain, '')
        else:
            target_path = target_url

        # 处理多个article id的情况（用|分隔）
        article_ids = [aid.strip() for aid in article_ids_str.split('|')]
        for aid in article_ids:
            article_map[aid] = target_path

    # 处理单个ID的情况
    for match in re.finditer(pattern2, content, re.MULTILINE):
        article_id = match.group(1)
        target_url = match.group(2)

        # 提取目标链接中的路径部分（去掉域名和末尾的?）
        if target_url.endswith('?'):
            target_url = target_url[:-1]

        # 提取路径部分
        if domain in target_url:
            target_path = target_url.replace(domain, '')
        else:
            target_path = target_url

        article_map[article_id] = target_path

    print(f'{Fore.GREEN}成功解析 {len(article_map)} 个article id映射{Style.RESET_ALL}')
    return article_map

def get_target_directory():
    """获取要进行替换操作的目录"""
    while True:
        target_dir = input('输入要进行替换操作的目录路径: ').strip()

        if not target_dir:
            print('目录路径不能为空')
            continue

        if os.path.isdir(target_dir):
            return target_dir
        else:
            print(f'{Fore.RED}目录不存在: {target_dir}{Style.RESET_ALL}')

def find_mdx_files(root_path):
    """递归查找所有md/mdx文件"""
    mdx_files = []
    for dirpath, _, filenames in os.walk(root_path):
        for fname in filenames:
            if fname.lower().endswith(('.md', '.mdx')):
                mdx_files.append(os.path.join(dirpath, fname))
    return mdx_files

def extract_article_links(content, domain):
    """从内容中提取所有article类型的链接"""
    # 匹配 [xxx](https://doc-zh.zego.im/article/12345#anchor) 或 <a href="https://...">
    # 需要提取完整的链接包括锚点

    links = []

    # 1. 匹配markdown链接格式: [xxx](url)
    # 匹配任何包含 /article/ 的链接
    md_pattern = r'\[([^\]]*)\]\(([^)]+)\)'
    for match in re.finditer(md_pattern, content):
        url = match.group(2)
        if '/article/' in url:
            links.append({
                'url': url,
                'type': 'markdown',
                'full_match': match.group(0)
            })

    # 2. 匹配HTML a标签: <a href="url">
    html_pattern = r'<a[^>]*href\s*=\s*[\'"]([^\'"]+)[\'"][^>]*>'
    for match in re.finditer(html_pattern, content):
        url = match.group(1)
        if '/article/' in url:
            links.append({
                'url': url,
                'type': 'html_a',
                'full_match': match.group(0)
            })

    return links

def replace_article_links_in_file(file_path, article_map, domain, missing_ids):
    """替换文件中的article链接"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f'{Fore.YELLOW}读取文件失败 {file_path}: {e}{Style.RESET_ALL}')
        return 0

    original_content = content
    replaced_count = 0

    # 提取所有article链接
    links = extract_article_links(content, domain)

    for link_info in links:
        url = link_info['url']

        # 提取article id
        article_match = re.search(r'/article/(\d+)', url)
        if not article_match:
            continue

        article_id = article_match.group(1)

        # 检查是否在映射中
        if article_id not in article_map:
            # 记录缺失的ID
            missing_ids[article_id].append(file_path)
            continue

        target_path = article_map[article_id]

        # 提取锚点（如果有）
        anchor = ''
        if '#' in url:
            anchor = '#' + url.split('#', 1)[1]

        # 构造新的链接
        new_url = target_path + anchor

        # 替换链接
        if link_info['type'] == 'markdown':
            # 替换markdown格式的链接
            old_pattern = re.escape(url)
            content = re.sub(old_pattern, new_url, content)
        elif link_info['type'] == 'html_a':
            # 替换HTML a标签中的链接
            old_pattern = re.escape(url)
            content = re.sub(old_pattern, new_url, content)

        replaced_count += 1

    # 如果有替换，写回文件
    if content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'{Fore.GREEN}✓ {file_path} - 替换 {replaced_count} 个链接{Style.RESET_ALL}')
        except Exception as e:
            print(f'{Fore.RED}写入文件失败 {file_path}: {e}{Style.RESET_ALL}')

    return replaced_count

def main():
    print(f'{Fore.CYAN}=== Article 链接替换工具 ==={Style.RESET_ALL}\n')

    # 步骤1: 选择语言
    language, domain = choose_language()
    print(f'已选择: {language.upper()} (域名: {domain})\n')

    # 步骤2: 获取nginx配置文件路径
    config_path = get_nginx_config_path()
    print(f'使用配置文件: {config_path}\n')

    # 步骤3: 解析nginx配置
    article_map = parse_nginx_config(config_path, domain)
    if not article_map:
        print(f'{Fore.RED}未找到任何article映射，退出{Style.RESET_ALL}')
        return False

    # 步骤4: 获取目标目录
    target_dir = get_target_directory()
    print(f'目标目录: {target_dir}\n')

    # 步骤5: 查找所有md/mdx文件
    mdx_files = find_mdx_files(target_dir)
    print(f'找到 {len(mdx_files)} 个md/mdx文件\n')

    if not mdx_files:
        print(f'{Fore.YELLOW}未找到任何md/mdx文件{Style.RESET_ALL}')
        return True

    # 步骤6-7: 替换链接
    from collections import defaultdict
    missing_ids = defaultdict(list)  # 记录缺失的article ID
    total_replaced = 0

    for file_path in mdx_files:
        replaced = replace_article_links_in_file(file_path, article_map, domain, missing_ids)
        total_replaced += replaced

    print(f'\n{Fore.CYAN}=== 替换完成 ==={Style.RESET_ALL}')
    print(f'总共替换 {total_replaced} 个链接')

    # 输出缺失的article ID
    if missing_ids:
        print(f'\n{Fore.YELLOW}=== 以下 Article ID 在配置文件中未找到映射 ==={Style.RESET_ALL}')
        print(f'共 {len(missing_ids)} 个缺失的 Article ID:\n')

        # 按ID排序
        for article_id in sorted(missing_ids.keys(), key=int):
            files = missing_ids[article_id]
            print(f'{Fore.YELLOW}Article ID {article_id}{Style.RESET_ALL} (出现在 {len(files)} 个文件中):')
            for file_path in files[:3]:  # 只显示前3个文件
                print(f'  - {file_path}')
            if len(files) > 3:
                print(f'  ... 还有 {len(files) - 3} 个文件')
            print()

    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

