import json
import os

def adjust_sidebar(file_path):
    print(f"\n开始处理文件: {file_path}")
    # 读取 JSON 文件
    with open(file_path, 'r', encoding='utf-8') as f:
        sidebar_data = json.load(f)
    
    # 找到 API 参考文档中的客户端 API 链接
    client_api_item = None
    new_mysidebar = []
    
    for category in sidebar_data['mySidebar']:
        if category.get('label') == 'API 参考文档':
            for item in category.get('items', []):
                if item.get('label') == '客户端 API':
                    client_api_item = item
                    print("找到客户端 API 链接")
        else:
            new_mysidebar.append(category)
    
    # 更新 mySidebar
    sidebar_data['mySidebar'] = new_mysidebar
    
    # 在客户端 SDK 分类中添加客户端 API 链接
    if client_api_item:
        for category in sidebar_data['mySidebar']:
            if category.get('label') == '客户端 SDK':
                items = category['items']
                # 找到下载 SDK 的位置
                for i, item in enumerate(items):
                    if item.get('label') == '下载':
                        print("找到下载 SDK，插入客户端 API")
                        items.insert(i + 1, client_api_item)
                        category['items'] = items
                        break
            

    
    # 保存修改后的文件
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(sidebar_data, f, ensure_ascii=False, indent=2)

def process_all_sidebars(root_dir):
    print(f"开始在目录 {root_dir} 中查找 sidebars.json 文件")
    found_files = False
    # 遍历所有目录查找 sidebars.json 文件
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == 'sidebars.json':
                found_files = True
                file_path = os.path.join(root, file)
                adjust_sidebar(file_path)
    
    if not found_files:
        print(f"警告：在目录 {root_dir} 中没有找到任何 sidebars.json 文件")

if __name__ == "__main__":
    # 设置指定目录
    target_dir = "/Users/zego/Documents/docs_all/core_products/zim/zh"
    if not os.path.exists(target_dir):
        print(f"错误：目录不存在: {target_dir}")
        exit(1)
    process_all_sidebars(target_dir)
    print("侧边栏调整完成！")
