#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理重复的 articleID 脚本
用于在指定文件夹中查找并修复重复的 articleID，只保留第一个出现的ID
"""

import os
import re
import sys
from pathlib import Path

def find_mdx_files(directory):
    """查找目录中的所有 .mdx 文件"""
    mdx_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mdx'):
                mdx_files.append(os.path.join(root, file))
    return mdx_files

def fix_duplicate_article_ids(file_path):
    """修复单个文件中的重复 articleID"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否包含 frontmatter
        if not content.startswith('---'):
            return False, "文件不包含 frontmatter"
        
        # 查找 frontmatter 结束位置
        lines = content.split('\n')
        frontmatter_end = -1
        for i, line in enumerate(lines):
            if i > 0 and line.strip() == '---':
                frontmatter_end = i
                break
        
        if frontmatter_end == -1:
            return False, "无法找到 frontmatter 结束位置"
        
        # 提取 frontmatter 部分
        frontmatter_lines = lines[1:frontmatter_end]
        
        # 查找所有 articleID 行
        article_id_lines = []
        for i, line in enumerate(frontmatter_lines):
            if line.strip().startswith('articleID:'):
                article_id_lines.append((i, line))
        
        # 如果没有找到 articleID 或只有一个，无需处理
        if len(article_id_lines) <= 1:
            return False, "没有重复的 articleID"
        
        # 保留第一个 articleID，删除其余的
        first_line = article_id_lines[0]
        lines_to_remove = [line_info[0] for line_info in article_id_lines[1:]]
        
        # 从后往前删除，避免索引变化
        for line_index in sorted(lines_to_remove, reverse=True):
            del frontmatter_lines[line_index]
        
        # 重新构建文件内容
        new_content = '---\n' + '\n'.join(frontmatter_lines) + '\n---\n' + '\n'.join(lines[frontmatter_end + 1:])
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, f"已修复 {len(lines_to_remove)} 个重复的 articleID"
        
    except Exception as e:
        return False, f"处理文件时出错: {str(e)}"

def main():
    """主函数"""
    print("=== 处理重复 articleID 脚本 ===")
    print()
    
    # 获取用户输入的目标文件夹
    while True:
        target_dir = input("请输入目标文件夹路径: ").strip()
        
        if not target_dir:
            print("路径不能为空，请重新输入")
            continue
        
        # 展开用户路径（处理 ~ 等）
        target_dir = os.path.expanduser(target_dir)
        
        if not os.path.exists(target_dir):
            print(f"路径不存在: {target_dir}")
            continue
        
        if not os.path.isdir(target_dir):
            print(f"路径不是文件夹: {target_dir}")
            continue
        
        break
    
    print(f"\n正在扫描文件夹: {target_dir}")
    
    # 查找所有 .mdx 文件
    mdx_files = find_mdx_files(target_dir)
    
    if not mdx_files:
        print("未找到任何 .mdx 文件")
        return
    
    print(f"找到 {len(mdx_files)} 个 .mdx 文件")
    print()
    
    # 处理每个文件
    processed_count = 0
    fixed_count = 0
    error_count = 0
    
    for file_path in mdx_files:
        print(f"处理文件: {os.path.relpath(file_path, target_dir)}")
        
        success, message = fix_duplicate_article_ids(file_path)
        processed_count += 1
        
        if success:
            if "没有重复" in message:
                print(f"  ✓ {message}")
            else:
                print(f"  ✓ {message}")
                fixed_count += 1
        else:
            print(f"  ✗ {message}")
            error_count += 1
    
    print()
    print("=== 处理完成 ===")
    print(f"总文件数: {processed_count}")
    print(f"修复文件数: {fixed_count}")
    print(f"错误文件数: {error_count}")

if __name__ == "__main__":
    main() 