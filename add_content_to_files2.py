#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件顶部内容添加脚本
功能：在指定文件夹中所有匹配的文件顶部添加指定内容
使用方法：
  python add_content_to_files.py "*.mdx" "# 限制说明"
  python add_content_to_files.py "restrictions.mdx" "# 版权声明"
"""

import os
import glob
import argparse
import sys
from pathlib import Path
import re

def add_content_to_files(folder_path, file_pattern, content_to_add, recursive=True, quiet=False):
    """
    在指定文件夹中所有匹配的文件顶部添加内容
    
    Args:
        folder_path (str): 文件夹路径
        file_pattern (str): 文件名模式（支持通配符，如 *.txt, test*.py 等）
        content_to_add (str): 要添加的内容
        recursive (bool): 是否递归搜索子文件夹（默认为True）
        quiet (bool): 是否静默模式（减少输出）
    """
    # 确保文件夹路径存在
    if not os.path.exists(folder_path):
        print(f"错误：文件夹 '{folder_path}' 不存在")
        return 0
    
    # 构建搜索模式
    if recursive:
        search_pattern = os.path.join(folder_path, '**', file_pattern)
        matched_files = glob.glob(search_pattern, recursive=True)
    else:
        search_pattern = os.path.join(folder_path, file_pattern)
        matched_files = glob.glob(search_pattern)
    
    if not quiet:
        print(f"搜索模式: {search_pattern}")
        print(f"找到 {len(matched_files)} 个匹配的文件")
    
    if not matched_files:
        if not quiet:
            print(f"在 '{folder_path}' 中没有找到匹配 '{file_pattern}' 的文件")
        return 0
    
    # 确保内容以换行符结尾
    if content_to_add and not content_to_add.endswith('\n'):
        content_to_add += '\n'
    
    processed_count = 0
    
    for file_path in matched_files:
        try:
            if not quiet:
                print(f"处理: {file_path}")
            
            # 读取原文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                original_content = file.read()
            
            # 检查文件顶部是否已经包含要添加的内容（避免重复添加）
            if original_content.startswith(content_to_add.strip()):
                if not quiet:
                    print(f"  跳过 - 已包含相同内容")
                continue
            
            # 将新内容添加到原内容前面
            new_content = content_to_add + original_content
            
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            
            if not quiet:
                print(f"  ✓ 成功")
            processed_count += 1
            
        except Exception as e:
            print(f"  ✗ 错误: {e}")
    
    if not quiet:
        print(f"\n完成！处理了 {processed_count} 个文件")
    
    return processed_count

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找包含 ## 接口原型 的部分
    pattern = r'(## 接口原型[\s\S]*?请求地址：)([^`\n]+)'
    
    # 如果找到匹配且URL不在反引号中，则添加反引号
    def replace_func(match):
        prefix = match.group(1)
        url = match.group(2).strip()
        if not url.startswith('`'):
            return f'{prefix}`{url}`'
        return match.group(0)
    
    new_content = re.sub(pattern, replace_func, content)
    
    # 如果内容有变化，写回文件
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'已修改文件: {file_path}')

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mdx') or file.endswith('.md'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if '## 接口原型' in content and '请求地址：' in content:
                            process_file(file_path)
                except Exception as e:
                    print(f'处理文件 {file_path} 时出错: {str(e)}')

def quick_mode():
    """快速模式 - 最少交互"""
    print("=== 快速模式 ===")
    
    # 获取文件模式
    file_pattern = input("文件模式 (如 *.mdx, restrictions.mdx): ").strip()
    if not file_pattern:
        print("错误：必须指定文件模式")
        return
    
    # 获取要添加的内容
    content = input("要添加的内容: ").strip()
    if not content:
        print("错误：必须指定要添加的内容")
        return
    
    # 直接执行，默认当前目录，递归搜索
    result = add_content_to_files(".", file_pattern, content, recursive=True, quiet=False)
    
    if result > 0:
        print(f"✓ 成功处理 {result} 个文件")
    else:
        print("✗ 没有处理任何文件")

def interactive_mode():
    """交互模式 - 完整选项"""
    print("=== 交互模式 ===")
    
    # 获取文件夹路径
    folder_path = input("文件夹路径 (默认当前目录): ").strip()
    if not folder_path:
        folder_path = "."
    
    # 获取文件模式
    file_pattern = input("文件模式 (如 *.mdx, restrictions.mdx): ").strip()
    if not file_pattern:
        print("错误：必须指定文件模式")
        return
    
    # 获取要添加的内容
    print("要添加的内容 (输入完成后按两次回车):")
    content_lines = []
    empty_count = 0
    
    while True:
        line = input()
        if line == "":
            empty_count += 1
            if empty_count >= 2:
                break
            content_lines.append(line)
        else:
            empty_count = 0
            content_lines.append(line)
    
    # 移除末尾空行
    while content_lines and content_lines[-1] == "":
        content_lines.pop()
    
    if not content_lines:
        print("错误：没有输入内容")
        return
    
    content = '\n'.join(content_lines)
    
    # 执行
    result = add_content_to_files(folder_path, file_pattern, content, recursive=True, quiet=False)
    
    if result > 0:
        print(f"✓ 成功处理 {result} 个文件")
    else:
        print("✗ 没有处理任何文件")

def main():
    parser = argparse.ArgumentParser(
        description='在文件顶部添加内容（默认递归搜索当前目录）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  python add_content_to_files.py "*.mdx" "# 限制说明"
  python add_content_to_files.py "restrictions.mdx" "# 版权声明"
  python add_content_to_files.py -f ./docs "*.md" "# 文档说明"
  python add_content_to_files.py --quick    # 快速交互模式
  python add_content_to_files.py --full     # 完整交互模式
        '''
    )
    
    parser.add_argument('pattern', nargs='?', help='文件名模式')
    parser.add_argument('content', nargs='?', help='要添加的内容')
    parser.add_argument('-f', '--folder', default='.', help='文件夹路径 (默认当前目录)')
    parser.add_argument('--no-recursive', action='store_true', help='禁用递归搜索')
    parser.add_argument('-q', '--quiet', action='store_true', help='静默模式')
    parser.add_argument('--quick', action='store_true', help='快速交互模式')
    parser.add_argument('--full', action='store_true', help='完整交互模式')
    
    args = parser.parse_args()
    
    # 如果指定了交互模式
    if args.quick:
        quick_mode()
        return
    
    if args.full:
        interactive_mode()
        return
    
    # 命令行模式
    if args.pattern and args.content:
        recursive = not args.no_recursive
        result = add_content_to_files(args.folder, args.pattern, args.content, recursive, args.quiet)
        if not args.quiet:
            if result > 0:
                print(f"✓ 成功处理 {result} 个文件")
            else:
                print("✗ 没有处理任何文件")
        sys.exit(0 if result > 0 else 1)
    
    # 如果没有足够参数，使用快速模式
    if not args.pattern or not args.content:
        print("参数不足，启动快速模式...")
        quick_mode()

if __name__ == "__main__":
    # 处理目标目录
    target_dirs = [
        'core_products',
        'cloud-market',
        'extended_services',
        'solutions'
    ]
    
    for dir_path in target_dirs:
        if os.path.exists(dir_path):
            print(f'正在处理目录: {dir_path}')
            process_directory(dir_path)
        else:
            print(f'目录不存在: {dir_path}') 