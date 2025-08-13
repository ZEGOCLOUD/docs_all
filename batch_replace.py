#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 将版本信息的格式修改一下，要求如下：
# 1. 将锚点放在2级标题这一行
# 2. h5 标签改成**的粗体
# 3. 列表的粗体移除，将列表下的普通文本缩进两次

# 例如：
# ```
# ## 3.20.5 版本 <a id="3.20.5"></a>

# **发布日期： 2025-04-25**

# **问题修复**

# 1. 修复部分 Android 6.0 及以下设备在外部采集或渲染场景下的崩溃问题
#     修复了部分 Android 6.0 及以下设备在外部采集或渲染场景下可能出现的崩溃问题。
# ---
# ```

# 调整版本信息格式
# 使用方法:
# python batch_replace.py <文件路径>                    # 处理单个文件
# python batch_replace.py <文件模式> --batch            # 批量处理匹配的文件
# python batch_replace.py --all                         # 处理所有release-notes.mdx文件
# python batch_replace.py --list                        # 列出所有release-notes.mdx文件


import re
import os
import glob

def replace_h5_tags(file_path):
    """替换文件中的h5标签格式"""
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 处理锚点位置：将独立的 <a id="版本号"></a> 移动到对应的 ## 版本号 版本 这一行的末尾
    lines = content.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 检查是否是独立的锚点行
        anchor_match = re.match(r'^\s*<a id="([^"]+)"></a>\s*$', line)
        if anchor_match:
            version_id = anchor_match.group(1)
            # 查找下一个版本标题行
            j = i + 1
            while j < len(lines):
                next_line = lines[j]
                # 检查是否是版本标题
                version_match = re.match(r'^\s*## ([^<]+) 版本\s*$', next_line)
                if version_match:
                    # 将锚点移动到版本标题行末尾
                    new_lines.append(f'## {version_match.group(1)} 版本 <a id="{version_id}"></a>')
                    i = j  # 跳过原版本标题行
                    break
                elif next_line.strip() and not next_line.strip().startswith('**'):
                    # 如果下一行不是版本标题，保持锚点独立
                    new_lines.append(line)
                    break
                j += 1
            else:
                # 没找到版本标题，保持锚点独立
                new_lines.append(line)
        else:
            new_lines.append(line)
        
        i += 1
    
    content = '\n'.join(new_lines)
    
    # 替换h5标签为粗体格式
    content = re.sub(r'<h5>新增功能</h5>', '**新增功能**', content)
    content = re.sub(r'<h5>改进优化</h5>', '**改进优化**', content)
    content = re.sub(r'<h5>问题修复</h5>', '**问题修复**', content)
    content = re.sub(r'<h5>废弃删除</h5>', '**废弃删除**', content)
    
    # 移除列表项的粗体，并缩进描述文本
    # 匹配 **数字. 内容** 格式，将其改为 数字. 内容
    content = re.sub(r'\*\*(\d+)\.\s*([^*]+)\*\*', r'\1. \2', content)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已处理文件: {file_path}")

def fix_indentation(file_path):
    """专门修复列表项描述文本的缩进"""
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # 检查是否是列表项（数字. 开头）
        if re.match(r'^\d+\.\s', line.strip()):
            # 查找下一个列表项或标题，将中间的文本缩进
            j = i + 1
            while j < len(lines):
                next_line = lines[j]
                # 如果遇到新的列表项、标题或空行，停止缩进
                if (re.match(r'^\d+\.\s', next_line.strip()) or 
                    re.match(r'^##\s', next_line.strip()) or
                    re.match(r'^\*\*[^*]+\*\*$', next_line.strip()) or
                    next_line.strip() == '---'):
                    break
                # 缩进非空行
                if next_line.strip():
                    new_lines.append('    ' + next_line)
                else:
                    new_lines.append(next_line)
                j += 1
            i = j - 1
        
        i += 1
    
    content = '\n'.join(new_lines)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已修复缩进: {file_path}")

def process_single_file(file_path):
    """处理单个文件"""
    if os.path.exists(file_path):
        print(f"\n正在处理文件: {file_path}")
        # 先运行完整的替换
        replace_h5_tags(file_path)
        # 再专门修复缩进
        fix_indentation(file_path)
        print(f"✅ 完成处理: {file_path}")
    else:
        print(f"❌ 文件不存在: {file_path}")

def process_multiple_files(file_pattern):
    """批量处理多个文件"""
    files = glob.glob(file_pattern, recursive=True)
    
    if not files:
        print(f"❌ 没有找到匹配的文件: {file_pattern}")
        return
    
    print(f"找到 {len(files)} 个文件:")
    for file_path in files:
        print(f"  - {file_path}")
    
    confirm = input(f"\n确认要处理这 {len(files)} 个文件吗? (y/N): ")
    if confirm.lower() != 'y':
        print("已取消操作")
        return
    
    for file_path in files:
        process_single_file(file_path)
    
    print(f"\n🎉 批量处理完成！共处理了 {len(files)} 个文件")

def find_release_notes_files():
    """查找项目中的所有release-notes.mdx文件"""
    pattern = "**/release-notes.mdx"
    files = glob.glob(pattern, recursive=True)
    
    if not files:
        print("❌ 没有找到release-notes.mdx文件")
        return []
    
    print(f"找到 {len(files)} 个release-notes.mdx文件:")
    for i, file_path in enumerate(files, 1):
        print(f"  {i:2d}. {file_path}")
    
    return files

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 1:
        # 没有参数时，查找并显示所有release-notes文件
        files = find_release_notes_files()
        if files:
            print(f"\n使用方法:")
            print(f"  python batch_replace.py <文件路径>                    # 处理单个文件")
            print(f"  python batch_replace.py <文件模式> --batch            # 批量处理匹配的文件")
            print(f"  python batch_replace.py --all                         # 处理所有release-notes.mdx文件")
            print(f"  python batch_replace.py --list                        # 列出所有release-notes.mdx文件")
    
    elif len(sys.argv) == 2:
        if sys.argv[1] == '--all':
            # 处理所有release-notes.mdx文件
            process_multiple_files("**/release-notes.mdx")
        elif sys.argv[1] == '--list':
            # 列出所有release-notes.mdx文件
            find_release_notes_files()
        else:
            # 处理单个文件
            file_path = sys.argv[1]
            process_single_file(file_path)
    
    elif len(sys.argv) == 3 and sys.argv[2] == '--batch':
        # 批量处理匹配的文件
        file_pattern = sys.argv[1]
        process_multiple_files(file_pattern)
    
    else:
        print("使用方法:")
        print(f"  python batch_replace.py <文件路径>                    # 处理单个文件")
        print(f"  python batch_replace.py <文件模式> --batch            # 批量处理匹配的文件")
        print(f"  python batch_replace.py --all                         # 处理所有release-notes.mdx文件")
        print(f"  python batch_replace.py --list                        # 列出所有release-notes.mdx文件")