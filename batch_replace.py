#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os

def process_release_notes(file_path=None):
    if file_path is None:
        file_path = '/Users/zego/Documents/docs_all/core_products/low-latency-live-streaming/zh/rn-js/over-view/release-notes.mdx'
    
    print(f"正在处理文件: {file_path}")
    
    # 创建备份文件
    backup_path = file_path + '.backup'
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"已创建备份文件: {backup_path}")
    except Exception as e:
        print(f"处理文件失败: {e}")
        return
    
    # 1. 给二级标题版本添加版本号 (从a标签name属性获取)
    # 匹配模式: <a name="版本号"></a> 然后是 ## 版本
    def replace_version_title(match):
        version = match.group(1)
        return f'<a name="{version}"></a>\n\n## {version} 版本'
    
    content = re.sub(r'<a name="([^"]+)"></a>\s*\n\s*## 版本', replace_version_title, content)
    
    # 2. 将<p class="hthree">改为<h5>标签
    content = re.sub(r'<p class="hthree">([^<]+)</p>', r'<h5>\1</h5>', content)
    
    # 3. 改进的四级标题处理逻辑 - 按照3.21.0版本格式要求
    content = process_headers_with_sections(content)
    
    # 4. 处理版本末尾的分隔符
    content = process_version_separators(content)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("批量替换完成！")
    except Exception as e:
        print(f"写入文件失败: {e}")

def process_headers_with_sections(content):
    """
    改进的四级标题处理逻辑
    处理所有四级标题，确保序号连贯，并在序号间添加空行
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
    
    conversion_count = 0
    
    for i, line in enumerate(lines):
        # 检查是否是新的分类标题
        section_found = False
        for pattern, section_name in section_patterns.items():
            if re.match(pattern, line.strip()):
                current_section = section_name
                section_counter = 0
                section_found = True
                print(f"  进入分类: {section_name}")
                break
        
        if section_found:
            result_lines.append(line)
            continue
        
        # 检查是否遇到新版本（重置分类）
        if re.match(r'## \d+\.\d+\.\d+ 版本', line.strip()) or re.match(r'<a id=', line.strip()) or re.match(r'<a name=', line.strip()):
            current_section = None
            section_counter = 0
            result_lines.append(line)
            continue
        
        # 处理所有四级标题，不管是否在分类下
        if line.strip().startswith('#### '):
            # 提取标题内容
            title = line.strip()[4:].strip()
            
            # 跳过已经是正确格式的条目（已经是**N. 格式的）
            if re.match(r'^\*\*\d+\.', title):
                # 检查是否需要更新计数器（处理序号不连贯的问题）
                if current_section:
                    match = re.match(r'^\*\*(\d+)\.', title)
                    if match:
                        existing_number = int(match.group(1))
                        section_counter = max(section_counter, existing_number)
                result_lines.append(line)
                continue
            
            # 处理已经包含编号的条目（如"#### 1. 标题"）
            if re.match(r'^\d+\.', title):
                # 如果在分类下，使用分类计数器
                if current_section:
                    section_counter += 1
                    indent = line[:len(line) - len(line.lstrip())]
                    new_line = f'{indent}**{section_counter}. {title[title.find(".")+1:].strip()}**'
                    
                    # 在序号条目前添加空行（除非是第一个条目）
                    if section_counter > 1 and result_lines and result_lines[-1].strip() != '':
                        result_lines.append('')
                    
                    result_lines.append(new_line)
                    conversion_count += 1
                    print(f"    转换: #### {title} -> **{section_counter}. {title[title.find('.')+1:].strip()}**")
                else:
                    # 不在分类下，保持原有编号但改为粗体格式
                    indent = line[:len(line) - len(line.lstrip())]
                    new_line = f'{indent}**{title}**'
                    result_lines.append(new_line)
                    conversion_count += 1
                    print(f"    转换: #### {title} -> **{title}**")
                continue
            
            # 处理没有编号的条目
            if current_section:
                # 在分类下，使用分类计数器
                section_counter += 1
                indent = line[:len(line) - len(line.lstrip())]
                new_line = f'{indent}**{section_counter}. {title}**'
                
                # 在序号条目前添加空行（除非是第一个条目）
                if section_counter > 1 and result_lines and result_lines[-1].strip() != '':
                    result_lines.append('')
                
                result_lines.append(new_line)
                conversion_count += 1
                print(f"    转换: #### {title} -> **{section_counter}. {title}**")
            else:
                # 不在分类下，直接转换为粗体格式
                indent = line[:len(line) - len(line.lstrip())]
                new_line = f'{indent}**{title}**'
                result_lines.append(new_line)
                conversion_count += 1
                print(f"    转换: #### {title} -> **{title}**")
        else:
            # 处理已经是**N. 格式的行，确保序号连贯
            if current_section and re.match(r'^\*\*\d+\.', line.strip()):
                match = re.match(r'^\*\*(\d+)\.(.*)$', line.strip())
                if match:
                    existing_number = int(match.group(1))
                    content_part = match.group(2)
                    
                    # 检查序号是否连贯
                    expected_number = section_counter + 1
                    if existing_number != expected_number:
                        # 修正序号
                        section_counter = expected_number
                        indent = line[:len(line) - len(line.lstrip())]
                        new_line = f'{indent}**{section_counter}.{content_part}**'
                        
                        # 在序号条目前添加空行（除非是第一个条目）
                        if section_counter > 1 and result_lines and result_lines[-1].strip() != '':
                            result_lines.append('')
                        
                        result_lines.append(new_line)
                        conversion_count += 1
                        print(f"    修正序号: **{existing_number}.{content_part}** -> **{section_counter}.{content_part}**")
                    else:
                        section_counter = existing_number
                        
                        # 在序号条目前添加空行（除非是第一个条目）
                        if section_counter > 1 and result_lines and result_lines[-1].strip() != '':
                            result_lines.append('')
                        
                        result_lines.append(line)
                else:
                    result_lines.append(line)
            else:
                result_lines.append(line)
    
    print(f"总共转换了 {conversion_count} 个标题")
    return '\n'.join(result_lines)

def process_version_separators(content):
    """
    处理版本末尾的分隔符
    1. 替换现有的HTML格式分隔符为---
    2. 为没有分隔符的版本添加---
    """
    lines = content.split('\n')
    result_lines = []
    separator_count = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 检查是否是HTML格式的分隔符组合
        if (line.strip() == '<br/>' or line.strip() == '<br>') and i + 1 < len(lines):
            next_line = lines[i + 1]
            if next_line.strip() == '<hr style="height:1px" />' or next_line.strip() == '<hr style="height:1px">':
                # 替换为---
                result_lines.append('---')
                separator_count += 1
                print(f"  替换HTML分隔符组合为---")
                i += 2  # 跳过两行
                continue
        
        # 检查是否是单独的hr标签
        if re.match(r'<hr\s+style="height:1px"\s*/>', line.strip()) or re.match(r'<hr\s+style="height:1px">', line.strip()):
            result_lines.append('---')
            separator_count += 1
            print(f"  替换HTML分隔符为---")
            i += 1
            continue
        
        result_lines.append(line)
        i += 1
    
    # 第二步：为没有分隔符的版本添加分隔符
    final_result = add_missing_separators(result_lines)
    
    print(f"总共处理了 {separator_count} 个版本分隔符")
    return final_result

def add_missing_separators(lines):
    """
    为没有分隔符的版本添加分隔符
    """
    result_lines = []
    version_positions = []
    
    # 找到所有版本的位置
    for i, line in enumerate(lines):
        if re.match(r'## \d+\.\d+\.\d+ 版本', line.strip()):
            version_positions.append(i)
    
    # 如果没有版本，直接返回原内容
    if not version_positions:
        return '\n'.join(lines)
    
    # 添加第一个版本之前的内容（如果有的话）
    if version_positions[0] > 0:
        header_lines = lines[:version_positions[0]]
        result_lines.extend(header_lines)
    
    # 处理每个版本
    for i, version_pos in enumerate(version_positions):
        # 确定当前版本的结束位置
        if i < len(version_positions) - 1:
            # 不是最后一个版本
            version_end = version_positions[i + 1] - 1
        else:
            # 最后一个版本
            version_end = len(lines) - 1
        
        # 添加版本标题和内容
        version_lines = lines[version_pos:version_end + 1]
        result_lines.extend(version_lines)
        
        # 检查版本末尾是否有---分隔符
        has_separator = False
        for j in range(min(5, len(version_lines))):
            if version_lines[-(j+1)].strip() == '---':
                has_separator = True
                break
        
        # 如果没有分隔符且不是最后一个版本，添加分隔符
        if not has_separator and i < len(version_positions) - 1:
            # 去除末尾的空行
            while result_lines and result_lines[-1].strip() == '':
                result_lines.pop()
            
            result_lines.append('')
            result_lines.append('---')
            print(f"  为版本添加分隔符: {lines[version_pos].strip()}")
    
    return '\n'.join(result_lines)

def batch_process_directory(directory):
    """
    批量处理目录下所有的release-notes.mdx文件
    """
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if filename == 'release-notes.mdx':
                files.append(os.path.join(root, filename))
    
    if not files:
        print(f"在目录 {directory} 中没有找到 release-notes.mdx 文件")
        return
    
    print(f"找到 {len(files)} 个文件:")
    for file_path in files:
        print(f"  {file_path}")
    
    confirm = input("\n确认要批量处理这些文件吗? (y/N): ")
    if confirm.lower() != 'y':
        print("已取消操作")
        return
    
    for file_path in files:
        process_release_notes(file_path)
        print()

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python batch_replace.py <文件路径>           # 处理单个文件")
        print("  python batch_replace.py <目录路径> --batch   # 批量处理目录下所有release-notes.mdx文件")
        print("  python batch_replace.py                     # 处理默认文件")
        return
    
    path = sys.argv[1]
    batch_mode = '--batch' in sys.argv
    
    if batch_mode:
        if not os.path.isdir(path):
            print(f"错误: {path} 不是一个有效的目录")
            return
        batch_process_directory(path)
    else:
        if not os.path.isfile(path):
            print(f"错误: {path} 不是一个有效的文件")
            return
        process_release_notes(path)

if __name__ == "__main__":
    if len(__import__('sys').argv) == 1:
        # 没有参数时执行原来的默认逻辑
        process_release_notes()
    else:
        main()