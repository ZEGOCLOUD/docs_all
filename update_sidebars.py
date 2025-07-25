#!/usr/bin/env python3
import json
import os
import copy

def update_sidebar_content(content):
    """更新单个 sidebar.json 文件的内容"""
    if "mySidebar" not in content:
        return content
    
    sidebar = content["mySidebar"]
    
    # 找到需要移动的条目
    download_item = None
    release_notes_item = None
    error_code_item = None
    upgrade_guide_item = None
    
    # 从原位置删除这些条目
    # 1. 查找并移除根级别的"下载"和"常见错误码"
    new_sidebar = []
    for item in sidebar:
        if item.get("type") == "doc" and item.get("label") == "下载":
            download_item = copy.deepcopy(item)
            continue
        elif item.get("type") == "doc" and item.get("label") == "常见错误码":
            error_code_item = copy.deepcopy(item)
            continue
        new_sidebar.append(item)
    
    # 2. 从"产品简介"中移除"发布日志"和"升级指南"
    for category in new_sidebar:
        if category.get("type") == "category" and category.get("label") == "产品简介":
            new_items = []
            for item in category["items"]:
                if item.get("type") == "doc" and item.get("label") == "发布日志":
                    release_notes_item = copy.deepcopy(item)
                    continue
                elif item.get("type") == "category" and item.get("label") == "升级指南":
                    upgrade_guide_item = copy.deepcopy(item)
                    continue
                new_items.append(item)
            category["items"] = new_items
    
    # 创建新的"客户端 SDK"分类
    client_sdk_category = {
        "type": "category",
        "label": "客户端 SDK",
        "collapsed": False,
        "items": []
    }
    
    # 添加找到的条目到新分类中
    if download_item:
        client_sdk_category["items"].append(download_item)
    if release_notes_item:
        client_sdk_category["items"].append(release_notes_item)
    if upgrade_guide_item:
        client_sdk_category["items"].append(upgrade_guide_item)
    if error_code_item:
        client_sdk_category["items"].append(error_code_item)
    
    # 在产品简介之后插入新分类
    for i, item in enumerate(new_sidebar):
        if item.get("type") == "category" and item.get("label") == "产品简介":
            new_sidebar.insert(i + 1, client_sdk_category)
            break
    
    content["mySidebar"] = new_sidebar
    return content

def process_file(file_path):
    """处理单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        updated_content = update_sidebar_content(content)
        
        # 保存更新后的文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(updated_content, f, ensure_ascii=False, indent=2)
        print(f"成功更新文件: {file_path}")
        
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")

def find_and_process_files(root_dir):
    """查找并处理所有 sidebars.json 文件"""
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == "sidebars.json":
                file_path = os.path.join(root, file)
                process_file(file_path)

if __name__ == "__main__":
    # 设置要处理的根目录
    root_directory = "/Users/zego/Documents/docs_all/core_products/low-latency-live-streaming"
    
    print(f"开始处理目录: {root_directory}")
    find_and_process_files(root_directory)
    print("处理完成!")
