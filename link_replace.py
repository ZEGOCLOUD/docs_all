#!/usr/bin/env python3
import os
import json
import re

def load_mapping(mapping_file):
    with open(mapping_file, 'r') as f:
        return json.load(f)

def replace_links_in_file(file_path, mapping):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 记录是否有修改
        modified = False
        
        # 对每个映射进行替换
        for old_link, new_link in mapping.items():
            if old_link in content:
                content = content.replace(old_link, new_link)
                modified = True
                print(f"在文件 {file_path} 中将 {old_link} 替换为 {new_link}")
        
        # 如果有修改，写回文件
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"已更新文件: {file_path}")

    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")

def process_directory(directory, mapping):
    # 支持的文件扩展名
    supported_extensions = ('.md', '.mdx', '.markdown')
    
    # 遍历目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(supported_extensions):
                file_path = os.path.join(root, file)
                replace_links_in_file(file_path, mapping)

def main():
    # 配置路径
    target_dir = "/Users/zego/Documents/docs_all/core_products/real-time-voice"
    mapping_file = "/Users/zego/Documents/docs_all/ai_search_mapping.json"
    
    # 检查目录是否存在
    if not os.path.exists(target_dir):
        print(f"目标目录不存在: {target_dir}")
        return
    
    # 加载映射文件
    try:
        mapping = load_mapping(mapping_file)
        print(f"已加载 {len(mapping)} 个链接映射")
    except Exception as e:
        print(f"加载映射文件时出错: {str(e)}")
        return
    
    # 处理目录
    print(f"开始处理目录: {target_dir}")
    process_directory(target_dir, mapping)
    print("处理完成!")

if __name__ == "__main__":
    main()
