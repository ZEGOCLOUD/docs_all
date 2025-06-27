#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def process_release_notes():
    file_path = '/Users/zego/Documents/docs_all/core_products/real-time-voice-video/zh/ios-oc/over-view/release-notes.mdx'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 给二级标题版本添加版本号 (从a标签name属性获取)
    # 匹配模式: <a name="版本号"></a> 然后是 ## 版本
    def replace_version_title(match):
        version = match.group(1)
        return f'<a name="{version}"></a>\n\n## {version} 版本'
    
    content = re.sub(r'<a name="([^"]+)"></a>\s*\n\s*## 版本', replace_version_title, content)
    
    # 2. 将<p class="hthree">改为<h5>标签
    content = re.sub(r'<p class="hthree">([^<]+)</p>', r'<h5>\1</h5>', content)
    
    # 3. 大版本内四级标题改为**加粗，并且附上序号
    # 处理 #### 标题，在每个大版本区域内添加序号
    sections = re.split(r'(<a name="[^"]+"></a>)', content)
    
    processed_content = ""
    for i, section in enumerate(sections):
        if i == 0:
            processed_content += section
            continue
        
        if section.startswith('<a name="'):
            processed_content += section
            continue
        
        # 在每个版本区域内处理四级标题
        # 分别处理不同类型的标题区域
        def process_section_headers(text):
            lines = text.split('\n')
            result_lines = []
            current_section = None
            section_counter = 0
            
            for line in lines:
                if line.startswith('<h5>'):
                    # 重置计数器
                    section_counter = 0
                    current_section = line
                    result_lines.append(line)
                elif line.startswith('#### ') and current_section:
                    # 四级标题转为加粗并添加序号
                    section_counter += 1
                    title = line[5:]  # 去掉 '#### '
                    result_lines.append(f'**{section_counter}.{title}**')
                else:
                    result_lines.append(line)
            
            return '\n'.join(result_lines)
        
        processed_section = process_section_headers(section)
        processed_content += processed_section
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(processed_content)
    
    print("批量替换完成！")

if __name__ == "__main__":
    process_release_notes()