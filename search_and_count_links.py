#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
链接搜索和统计脚本
用于搜索 https://doc-zh.zego.im/article/数字ID 格式的链接
按数字ID分组统计并按降序排列
"""

import os
import re
import argparse
from collections import defaultdict
from pathlib import Path
import sys

def find_links_in_file(file_path, link_pattern):
    """
    在单个文件中查找匹配的链接
    
    Args:
        file_path: 文件路径
        link_pattern: 链接匹配模式
    
    Returns:
        list: 找到的链接列表
    """
    links = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            matches = link_pattern.findall(content)
            links.extend(matches)
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
    
    return links

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

def search_links_in_directory(target_dir, exclude_dirs=None):
    """
    在目标目录中搜索链接
    
    Args:
        target_dir: 目标目录
        exclude_dirs: 要排除的目录列表
    
    Returns:
        dict: 按ID分组的链接统计
    """
    if exclude_dirs is None:
        exclude_dirs = []
    
    # 链接匹配模式
    link_pattern = re.compile(r'https://doc-zh\.zego\.im/article/(\d+)')
    
    # 统计字典
    link_stats = defaultdict(list)
    
    target_path = Path(target_dir)
    if not target_path.exists():
        print(f"错误: 目标目录 '{target_dir}' 不存在")
        return {}
    
    print(f"开始在目录 '{target_dir}' 中搜索链接...")
    print(f"排除目录: {exclude_dirs if exclude_dirs else '无'}")
    
    # 遍历所有文件
    file_count = 0
    for root, dirs, files in os.walk(target_dir):
        # 检查是否应该排除当前目录
        if should_exclude_path(root, exclude_dirs):
            continue
        
        for file in files:
            file_path = os.path.join(root, file)
            
            # 只处理文本文件
            if file.endswith(('.md', '.mdx', '.txt', '.html', '.htm', '.js', '.jsx', '.ts', '.tsx')):
                file_count += 1
                if file_count % 100 == 0:
                    print(f"已处理 {file_count} 个文件...")
                
                links = find_links_in_file(file_path, link_pattern)
                for link_id in links:
                    link_stats[link_id].append(file_path)
    
    print(f"搜索完成，共处理了 {file_count} 个文件")
    return link_stats

def print_results(link_stats):
    """
    打印统计结果
    
    Args:
        link_stats: 链接统计字典
    """
    if not link_stats:
        print("未找到任何匹配的链接")
        return
    
    # 按出现次数降序排列
    sorted_stats = sorted(link_stats.items(), key=lambda x: len(x[1]), reverse=True)
    
    print("\n" + "="*60)
    print("链接统计结果 (按出现次数降序排列)")
    print("="*60)
    
    for link_id, file_paths in sorted_stats:
        count = len(file_paths)
        print(f"\n文章ID: {link_id}")
        print(f"出现次数: {count}")
        print(f"完整链接: https://doc-zh.zego.im/article/{link_id}")
        print("出现在以下文件中:")
        
        # 显示前10个文件路径，如果超过10个则显示省略号
        for i, file_path in enumerate(file_paths[:10]):
            print(f"  {i+1}. {file_path}")
        
        if len(file_paths) > 10:
            print(f"  ... 还有 {len(file_paths) - 10} 个文件")
    
    print(f"\n总计找到 {len(link_stats)} 个不同的文章ID")

def save_results_to_file(link_stats, output_file):
    """
    将结果保存到文件
    
    Args:
        link_stats: 链接统计字典
        output_file: 输出文件路径
    """
    if not link_stats:
        return
    
    sorted_stats = sorted(link_stats.items(), key=lambda x: len(x[1]), reverse=True)
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("链接统计结果 (按出现次数降序排列)\n")
            f.write("="*60 + "\n\n")
            
            for link_id, file_paths in sorted_stats:
                count = len(file_paths)
                f.write(f"文章ID: {link_id}\n")
                f.write(f"出现次数: {count}\n")
                f.write(f"完整链接: https://doc-zh.zego.im/article/{link_id}\n")
                f.write("出现在以下文件中:\n")
                
                for i, file_path in enumerate(file_paths):
                    f.write(f"  {i+1}. {file_path}\n")
                
                f.write("\n" + "-"*40 + "\n\n")
            
            f.write(f"总计找到 {len(link_stats)} 个不同的文章ID\n")
        
        print(f"\n结果已保存到: {output_file}")
    except Exception as e:
        print(f"保存结果到文件时出错: {e}")

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

def main():
    parser = argparse.ArgumentParser(description='搜索和统计指定格式的链接')
    parser.add_argument('--target-dir', '-t', help='目标目录路径')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--exclude', '-e', nargs='*', help='要排除的目录列表（覆盖默认配置）')
    
    args = parser.parse_args()
    
    # 如果没有通过命令行参数指定目标目录，则交互式输入
    target_dir = args.target_dir
    if not target_dir:
        target_dir = input("请输入目标文件夹路径: ").strip()
        if not target_dir:
            print("错误: 必须指定目标文件夹路径")
            sys.exit(1)
    
    # 排除目录 - 优先使用命令行参数，否则使用默认配置
    exclude_dirs = args.exclude if args.exclude else get_default_exclude_dirs()
    
    # 输出文件
    output_file = args.output
    if not output_file:
        output_file = input("请输入输出文件路径（直接回车跳过保存）: ").strip()
        if not output_file:
            output_file = None
    
    # 执行搜索
    link_stats = search_links_in_directory(target_dir, exclude_dirs)
    
    # 显示结果
    print_results(link_stats)
    
    # 保存结果
    if output_file:
        save_results_to_file(link_stats, output_file)

if __name__ == "__main__":
    main() 