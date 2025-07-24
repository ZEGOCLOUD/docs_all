import os
import json

# 指定目录路径
directory = "/Users/zego/Documents/docs_all/core_products/low-latency-live-streaming/zh"

def add_tag_to_recording(data):
    """递归遍历JSON数据并添加标签"""
    if isinstance(data, dict):
        # 如果找到label为"音视频录制"的项，添加tag
        if data.get("label") == "AI 降噪":
            data["tag"] = {
                "label": "进阶",
                "color": "Warning"
            }
        # 递归处理所有值
        for key, value in data.items():
            add_tag_to_recording(value)
    elif isinstance(data, list):
        # 递归处理列表中的每个项
        for item in data:
            add_tag_to_recording(item)

def process_sidebar_files():
    """处理目录下的所有sidebars.json文件"""
    # 遍历目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == "sidebars.json":
                file_path = os.path.join(root, file)
                print(f"Processing: {file_path}")
                
                try:
                    # 读取JSON文件
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # 添加标签
                    add_tag_to_recording(data)
                    
                    # 写回文件
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    
                    print(f"Successfully updated: {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")

if __name__ == "__main__":
    process_sidebar_files()
