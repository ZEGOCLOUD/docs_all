#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 搜索映射生成脚本
用于生成旧文档链接到新文档链接的映射关系
"""

import os
import re
import json
import sys
import requests
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

def find_links_in_file(file_path):
    """
    在单个文件中查找匹配的链接
    
    Args:
        file_path: 文件路径
    
    Returns:
        list: 找到的链接列表
    """
    links = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # 匹配 https://doc-zh.zego.im/article/数字ID 格式的链接
            link_pattern = re.compile(r'https://doc-zh\.zego\.im/article/(\d+)')
            matches = link_pattern.findall(content)
            links.extend(matches)
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
    
    return links

def load_sidebar_info(sidebar_file):
    """
    加载 sidebar.json 文件并提取文档 ID 和路径信息
    
    Args:
        sidebar_file: sidebar.json 文件路径
    
    Returns:
        tuple: (文章ID到路径ID的映射, 文章ID到sidebar路径的映射)
    """
    article_to_path = {}
    article_to_sidebar = {}
    try:
        with open(sidebar_file, 'r', encoding='utf-8') as f:
            sidebar_data = json.load(f)
            
        def process_items(items):
            for item in items:
                if isinstance(item, dict):
                    if 'articleID' in item and 'id' in item:
                        article_id = str(item['articleID'])
                        article_to_path[article_id] = item['id']
                        article_to_sidebar[article_id] = os.path.dirname(sidebar_file)
                    if 'items' in item:
                        process_items(item['items'])
        
        # 处理根级别的项目
        if isinstance(sidebar_data, dict) and 'mySidebar' in sidebar_data:
            process_items(sidebar_data['mySidebar'])
        elif isinstance(sidebar_data, list):
            process_items(sidebar_data)
            
    except Exception as e:
        print(f"处理 sidebar 文件 {sidebar_file} 时出错: {e}")
    
    return article_to_path, article_to_sidebar

def load_docuo_config(target_dir):
    """
    加载 docuo.config.json 文件并提取路由信息
    
    Args:
        target_dir: 目标目录路径
        
    Returns:
        dict: 路径到 routeBasePath 的映射
    """
    config_file = os.path.join(target_dir, 'docuo.config.json')
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        path_to_route = {}
        for instance in config.get('instances', []):
            if 'path' in instance and 'routeBasePath' in instance:
                path_to_route[instance['path']] = instance['routeBasePath']
                
        return path_to_route
    except Exception as e:
        print(f"处理 docuo.config.json 时出错: {e}")
        return {}

def find_all_sidebars(root_dir):
    """
    在项目中查找所有的 sidebars.json 文件
    
    Args:
        root_dir: 项目根目录
    
    Returns:
        list: sidebars.json 文件路径列表
    """
    sidebar_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file == 'sidebars.json':
                sidebar_files.append(os.path.join(root, file))
    return sidebar_files

def should_exclude_path(path, exclude_dirs):
    """
    检查路径是否应该被排除
    
    Args:
        path: 路径
        exclude_dirs: 要排除的目录列表
    
    Returns:
        bool: 是否应该排除
    """
    path_str = str(path)
    for exclude_dir in exclude_dirs:
        if exclude_dir in path_str:
            return True
    return False

def get_default_exclude_dirs():
    """
    获取默认的排除目录列表
    
    Returns:
        list: 默认排除目录列表
    """
    return [
        ".git",
        "node_modules", 
        ".vscode",
        "__pycache__",
        ".DS_Store",
        "dist",
        "build",
        "coverage",
        ".idea",
        "*.log",
        "tmp",
        "temp",
        ".sass-cache",
        ".npm",
        ".yarn",
        ".cache"
    ]

def find_matching_route(sidebar_path, path_to_route, target_dir):
    """
    根据 sidebar 路径找到匹配的 routeBasePath
    
    Args:
        sidebar_path: sidebar 文件所在目录路径
        path_to_route: 路径到 routeBasePath 的映射
        target_dir: 目标目录路径
    
    Returns:
        str: 匹配的 routeBasePath，如果没找到则返回 None
    """
    # 将路径转换为相对路径
    rel_path = os.path.relpath(sidebar_path, target_dir)
    
    # 遍历所有配置的路径
    for config_path, route in path_to_route.items():
        # 如果配置路径以 core_products/real-time-voice-video/zh/ 开头
        if config_path.startswith('core_products/real-time-voice-video/zh/'):
            # 获取配置路径中 core_products/real-time-voice-video/zh/ 之后的部分
            config_suffix = config_path.split('core_products/real-time-voice-video/zh/')[-1]
            # 如果相对路径包含这个后缀
            if config_suffix in rel_path:
                return route
            
    return None

def generate_mapping(target_dir, exclude_dirs=None):
    """
    生成旧链接到新链接的映射
    
    Args:
        target_dir: 目标目录
        exclude_dirs: 要排除的目录列表
    
    Returns:
        dict: 映射关系字典
    """
    if exclude_dirs is None:
        exclude_dirs = get_default_exclude_dirs()
    
    # 收集所有链接
    all_links = set()
    target_path = Path(target_dir)
    
    print("正在搜索文档链接...")
    for root, _, files in os.walk(target_dir):
        if should_exclude_path(root, exclude_dirs):
            continue
            
        for file in files:
            if file.endswith(('.md', '.mdx', '.txt', '.html', '.htm', '.js', '.jsx', '.ts', '.tsx')):
                file_path = os.path.join(root, file)
                links = find_links_in_file(file_path)
                all_links.update(links)
    
    print(f"找到 {len(all_links)} 个不同的文档链接")
    
    # 加载所有 sidebar 文件
    print("\n正在加载 sidebar 文件...")
    sidebar_files = find_all_sidebars(target_dir)
    print(f"找到 {len(sidebar_files)} 个 sidebar 文件")
    
    # 合并所有 sidebar 信息
    article_to_path = {}
    article_to_sidebar = {}
    for sidebar_file in sidebar_files:
        path_map, sidebar_map = load_sidebar_info(sidebar_file)
        article_to_path.update(path_map)
        article_to_sidebar.update(sidebar_map)
    
    # 加载 docuo.config.json
    print("\n正在加载 docuo.config.json...")
    path_to_route = load_docuo_config(target_dir)
    
    # 检查 console-old 和 console-new 目录
    console_old_path = os.path.join(target_dir, 'general/zh/console/old')
    console_new_path = os.path.join(target_dir, 'general/zh/console/new')
    
    def check_article_in_console(article_id):
        """检查文章是否在 console-old 或 console-new 目录中"""
        # 遍历 console-old 和 console-new 目录中的所有 .mdx 文件
        for console_path in [console_old_path, console_new_path]:
            if os.path.exists(console_path):
                for root, _, files in os.walk(console_path):
                    for file in files:
                        if file.endswith('.mdx'):
                            file_path = os.path.join(root, file)
                            try:
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                    if f'articleID: {article_id}' in content:
                                        return True
                            except Exception as e:
                                print(f"读取文件 {file_path} 时出错: {e}")
        return False
    
    # 生成映射关系
    mapping = {}
    for article_id in all_links:
        old_link = f"https://doc-zh.zego.im/article/{article_id}"
        path_id = article_to_path.get(article_id)
        sidebar_path = article_to_sidebar.get(article_id)
        
        if path_id and sidebar_path:
            # 根据 sidebar 路径查找对应的 routeBasePath
            route_base_path = find_matching_route(sidebar_path, path_to_route, target_dir)
            
            if route_base_path:
                new_link = f"/{route_base_path}/{path_id}"
                mapping[old_link] = new_link
            else:
                # 如果未找到路由，检查是否在 console 目录中
                if not check_article_in_console(article_id):
                    print(f"警告: 未找到文章 ID {article_id} 对应的 routeBasePath")
        else:
            # 如果未找到路径，检查是否在 console 目录中
            if not check_article_in_console(article_id):
                print(f"警告: 未找到文章 ID {article_id} 对应的路径 ID")
    
    return mapping

def save_mapping(mapping, output_file):
    """
    保存映射关系到文件
    
    Args:
        mapping: 映射关系字典
        output_file: 输出文件路径
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, ensure_ascii=False, indent=2)
        print(f"\n映射关系已保存到: {output_file}")
    except Exception as e:
        print(f"保存映射文件时出错: {e}")

def verify_single_link(local_link):
    """
    验证单个链接是否可访问
    
    Args:
        local_link: 本地链接
        
    Returns:
        tuple: (链接, 是否可访问, 状态码或错误信息)
    """
    try:
        response = requests.get(local_link, timeout=5)
        return local_link, response.ok, response.status_code
    except requests.RequestException as e:
        return local_link, False, str(e)

def verify_links(mapping):
    """
    验证新生成的链接
    
    Args:
        mapping: 映射关系字典
    """
    print("\n开始验证新链接...")
    print("="*60)
    
    # 创建验证任务
    tasks = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for old_link, new_link in mapping.items():
            local_link = f"http://localhost:3000{new_link}"
            task = executor.submit(verify_single_link, local_link)
            tasks.append((old_link, task))
    
    # 收集验证结果
    success_count = 0
    failed_links = []
    
    for old_link, task in tasks:
        local_link, is_ok, status = task.result()
        if is_ok:
            success_count += 1
            print(f"✅ 验证成功: {local_link}")
        else:
            failed_links.append((old_link, local_link, status))
            print(f"❌ 验证失败: {local_link}")
            print(f"   错误信息: {status}")
            print(f"   对应旧链接: {old_link}")
        print("-"*60)
    
    # 打印统计信息
    total = len(mapping)
    print(f"\n验证完成!")
    print(f"总计: {total} 个链接")
    print(f"成功: {success_count} 个")
    print(f"失败: {len(failed_links)} 个")
    
    if failed_links:
        print("\n以下链接验证失败:")
        for old_link, local_link, status in failed_links:
            print(f"\n旧链接: {old_link}")
            print(f"新链接: {local_link}")
            print(f"错误: {status}")

def main():
    # 获取目标目录
    target_dir = input("请输入目标文件夹路径: ").strip()
    if not target_dir:
        print("错误: 必须指定目标文件夹路径")
        sys.exit(1)
        
    # 检查目录是否存在
    if not os.path.exists(target_dir):
        print(f"错误: 目标目录 '{target_dir}' 不存在")
        sys.exit(1)
        
    # 检查是否为目录
    if not os.path.isdir(target_dir):
        print(f"错误: '{target_dir}' 不是一个目录")
        sys.exit(1)
    
    exclude_dirs = get_default_exclude_dirs()
    output_file = 'ai_search_mapping.json'
    
    print(f"\n开始生成 AI 搜索映射...")
    print(f"目标目录: {target_dir}")
    print(f"输出文件: {output_file}")
    
    # 生成映射关系
    mapping = generate_mapping(target_dir, exclude_dirs)
    
    # 验证新链接
    verify_links(mapping)
    
    # 保存映射关系
    save_mapping(mapping, output_file)
    
    print(f"\n处理完成! 共生成 {len(mapping)} 个映射关系")

if __name__ == "__main__":
    main()