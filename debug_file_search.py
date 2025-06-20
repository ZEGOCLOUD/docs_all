#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件搜索调试工具
帮助诊断为什么找不到指定文件
"""

import os
import glob
from pathlib import Path

def debug_file_search():
    print("=== 文件搜索调试工具 ===\n")
    
    # 获取用户输入
    folder_path = input("请输入文件夹路径: ").strip()
    if not folder_path:
        folder_path = "."
    
    file_pattern = input("请输入文件名模式: ").strip()
    
    print(f"\n=== 调试信息 ===")
    
    # 1. 检查文件夹是否存在
    print(f"1. 检查文件夹路径:")
    abs_folder_path = os.path.abspath(folder_path)
    print(f"   输入路径: {folder_path}")
    print(f"   绝对路径: {abs_folder_path}")
    print(f"   文件夹存在: {os.path.exists(abs_folder_path)}")
    print(f"   是否为目录: {os.path.isdir(abs_folder_path)}")
    
    if not os.path.exists(abs_folder_path):
        print("   ❌ 文件夹不存在！")
        return
    
    if not os.path.isdir(abs_folder_path):
        print("   ❌ 路径不是一个文件夹！")
        return
    
    # 2. 列出文件夹内容
    print(f"\n2. 文件夹内容:")
    try:
        all_items = os.listdir(abs_folder_path)
        files = [f for f in all_items if os.path.isfile(os.path.join(abs_folder_path, f))]
        dirs = [d for d in all_items if os.path.isdir(os.path.join(abs_folder_path, d))]
        
        print(f"   总共 {len(all_items)} 个项目")
        print(f"   文件数量: {len(files)}")
        print(f"   文件夹数量: {len(dirs)}")
        
        if files:
            print("   文件列表:")
            for f in sorted(files)[:20]:  # 最多显示20个文件
                print(f"     - {f}")
            if len(files) > 20:
                print(f"     ... 还有 {len(files) - 20} 个文件")
        else:
            print("   ❌ 文件夹中没有文件")
            
        if dirs:
            print("   子文件夹:")
            for d in sorted(dirs)[:10]:  # 最多显示10个文件夹
                print(f"     - {d}/")
            if len(dirs) > 10:
                print(f"     ... 还有 {len(dirs) - 10} 个文件夹")
                
    except PermissionError:
        print("   ❌ 没有读取文件夹的权限")
        return
    
    # 3. 测试搜索模式
    print(f"\n3. 搜索模式测试:")
    search_pattern = os.path.join(abs_folder_path, file_pattern)
    print(f"   搜索模式: {search_pattern}")
    
    matched_files = glob.glob(search_pattern)
    print(f"   匹配结果: {len(matched_files)} 个文件")
    
    if matched_files:
        print("   匹配的文件:")
        for f in matched_files:
            print(f"     ✓ {f}")
    else:
        print("   ❌ 没有找到匹配的文件")
        
        # 4. 提供建议
        print(f"\n4. 调试建议:")
        
        # 检查是否有类似的文件
        if file_pattern.startswith('*'):
            # 如果是以*开头的模式，检查扩展名
            if '.' in file_pattern:
                ext = file_pattern.split('.')[-1]
                similar_files = [f for f in files if f.endswith('.' + ext)]
                if similar_files:
                    print(f"   💡 找到相似扩展名的文件 (.{ext}):")
                    for f in similar_files[:10]:
                        print(f"      - {f}")
                        
        # 检查大小写问题
        if file_pattern.replace('*', ''):
            pattern_lower = file_pattern.lower()
            case_matches = glob.glob(os.path.join(abs_folder_path, pattern_lower))
            if case_matches:
                print(f"   💡 发现大小写匹配的文件（使用小写模式 '{pattern_lower}'）:")
                for f in case_matches:
                    print(f"      - {f}")
        
        # 建议递归搜索
        print(f"   💡 如果文件在子文件夹中，可以尝试递归搜索")
        recursive_pattern = os.path.join(abs_folder_path, '**', file_pattern)
        recursive_matches = glob.glob(recursive_pattern, recursive=True)
        if recursive_matches:
            print(f"   🎯 递归搜索找到 {len(recursive_matches)} 个文件:")
            for f in recursive_matches[:10]:
                print(f"      - {f}")
            if len(recursive_matches) > 10:
                print(f"      ... 还有 {len(recursive_matches) - 10} 个文件")
        
        # 5. 常见模式示例
        print(f"\n5. 常见搜索模式示例:")
        print("   *.txt          - 所有txt文件")
        print("   *.py           - 所有Python文件")
        print("   test*.py       - 以test开头的Python文件")
        print("   config.json    - 特定文件名")
        print("   **/*.txt       - 递归搜索所有txt文件（需要修改脚本）")

def main():
    debug_file_search()
    
    print(f"\n=== 解决方案建议 ===")
    print("1. 确认文件夹路径正确")
    print("2. 检查文件名模式是否正确")
    print("3. 注意大小写敏感问题")
    print("4. 如果文件在子文件夹中，考虑递归搜索")
    print("5. 检查文件权限")

if __name__ == "__main__":
    main() 