import os
import json
from pathlib import Path

def check_sidebars_ids(base_dir):
    """检查指定目录下所有 sidebars.json 文件中的 id 是否与实际文件路径匹配"""
    errors = []
    
    # 遍历目录查找所有 sidebars.json 文件
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file == 'sidebars.json':
                sidebar_path = os.path.join(root, file)
                relative_dir = os.path.dirname(os.path.relpath(sidebar_path, base_dir))
                
                try:
                    with open(sidebar_path, 'r', encoding='utf-8') as f:
                        sidebar_data = json.load(f)
                    
                    # 检查每个 sidebar 中的 id
                    check_items(sidebar_data.get('mySidebar', []), relative_dir, base_dir, errors, sidebar_path)
                except Exception as e:
                    errors.append(f"Error processing {sidebar_path}: {str(e)}")
    
    return errors

def check_items(items, relative_dir, base_dir, errors, sidebar_path):
    """递归检查 sidebar 中的所有项目"""
    for item in items:
        if isinstance(item, dict):
            # 检查文档类型的项目
            if item.get('type') == 'doc' and 'id' in item:
                doc_id = item['id']
                expected_mdx_path = os.path.join(relative_dir, f"{doc_id}.mdx")
                full_path = os.path.join(base_dir, expected_mdx_path)
                
                if not os.path.exists(full_path):
                    errors.append(f"{sidebar_path}\nMissing file: {expected_mdx_path}\n")
            
            # 递归检查子项目
            if 'items' in item and isinstance(item['items'], list):
                check_items(item['items'], relative_dir, base_dir, errors, sidebar_path)

def main():
    base_dir = "/Users/zego/Documents/docs_all/solutions/video-call"
    errors = check_sidebars_ids(base_dir)
    
    if errors:
        print("发现以下问题：\n")
        for error in errors:
            print(error)
    else:
        print("所有 sidebars.json 文件中的 id 都有对应的文件存在。")

if __name__ == "__main__":
    main()