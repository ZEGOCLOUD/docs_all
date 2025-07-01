#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发版说明格式统一脚本
将 #### 标题 格式修改为 **N. 标题** 格式，按照3.21.0版本的格式要求
"""

import re
import os
import sys
from typing import List, Tuple


def format_release_notes(file_path: str, backup: bool = True) -> None:
    """
    格式化发版说明文件
    
    Args:
        file_path: 文件路径
        backup: 是否创建备份文件
    """
    print(f"正在处理文件: {file_path}")
    
    # 读取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"读取文件失败: {e}")
        return
    
    # 创建备份文件
    if backup:
        backup_path = file_path + '.backup'
        try:
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"已创建备份文件: {backup_path}")
        except Exception as e:
            print(f"创建备份文件失败: {e}")
            return
    
    # 处理格式转换
    new_content = process_content(content)
    
    # 写入新内容
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"文件格式化完成: {file_path}")
    except Exception as e:
        print(f"写入文件失败: {e}")


def process_content(content: str) -> str:
    """
    处理文件内容，转换格式
    
    Args:
        content: 原始文件内容
        
    Returns:
        处理后的文件内容
    """
    lines = content.split('\n')
    result_lines = []
    current_section = None
    section_counter = 0
    
    # 定义需要处理的分类
    section_patterns = {
        r'<h5>新增功能</h5>': '新增功能',
        r'<h5>改进优化</h5>': '改进优化', 
        r'<h5>问题修复</h5>': '问题修复',
        r'<h5>废弃删除</h5>': '废弃删除',
        r'<h5>其他变更</h5>': '其他变更',
        r'<h5>兼容性变更</h5>': '兼容性变更'
    }
    
    for line in lines:
        # 检查是否是新的分类标题
        section_found = False
        for pattern, section_name in section_patterns.items():
            if re.match(pattern, line.strip()):
                current_section = section_name
                section_counter = 0
                section_found = True
                break
        
        if section_found:
            result_lines.append(line)
            continue
        
        # 检查是否遇到新版本（重置分类）
        if re.match(r'## \d+\.\d+\.\d+ 版本', line.strip()) or re.match(r'<a id=', line.strip()):
            current_section = None
            section_counter = 0
            result_lines.append(line)
            continue
        
        # 处理功能条目
        if current_section and line.strip().startswith('#### '):
            # 提取标题内容
            title = line.strip()[4:].strip()
            
            # 跳过已经是正确格式的条目（以数字开头的）
            if re.match(r'^\d+\.', title):
                result_lines.append(line)
                continue
            
            # 跳过特殊格式的条目（已经包含编号的）
            if title.startswith('1. ') or title.startswith('2. ') or title.startswith('3. '):
                result_lines.append(line)
                continue
            
            # 生成新的格式
            section_counter += 1
            new_line = line.replace(f'#### {title}', f'**{section_counter}. {title}**')
            result_lines.append(new_line)
            print(f"  转换: #### {title} -> **{section_counter}. {title}**")
        else:
            result_lines.append(line)
    
    return '\n'.join(result_lines)


def find_release_notes_files(directory: str) -> List[str]:
    """
    查找目录下所有的release-notes.mdx文件
    
    Args:
        directory: 搜索目录
        
    Returns:
        文件路径列表
    """
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if filename == 'release-notes.mdx':
                files.append(os.path.join(root, filename))
    return files


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python format_release_notes.py <文件路径>           # 处理单个文件")
        print("  python format_release_notes.py <目录路径> --batch   # 批量处理目录下所有release-notes.mdx文件")
        print("  python format_release_notes.py <文件路径> --no-backup  # 不创建备份文件")
        return
    
    path = sys.argv[1]
    batch_mode = '--batch' in sys.argv
    no_backup = '--no-backup' in sys.argv
    create_backup = not no_backup
    
    if batch_mode:
        if not os.path.isdir(path):
            print(f"错误: {path} 不是一个有效的目录")
            return
        
        files = find_release_notes_files(path)
        if not files:
            print(f"在目录 {path} 中没有找到 release-notes.mdx 文件")
            return
        
        print(f"找到 {len(files)} 个文件:")
        for file_path in files:
            print(f"  {file_path}")
        
        confirm = input("\n确认要批量处理这些文件吗? (y/N): ")
        if confirm.lower() != 'y':
            print("已取消操作")
            return
        
        for file_path in files:
            format_release_notes(file_path, create_backup)
            print()
    
    else:
        if not os.path.isfile(path):
            print(f"错误: {path} 不是一个有效的文件")
            return
        
        format_release_notes(path, create_backup)


if __name__ == '__main__':
    main() 