import os
import json
import re

def extract_title_from_mdx(file_path):
    """从 MDX 文件中提取标题"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 查找以 # 开头的第一行作为标题
            match = re.search(r'^#\s+(.+?)(?:\n|$)', content, re.MULTILINE)
            if match:
                return match.group(1).strip()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return None

def generate_sidebar_items(directory):
    """生成侧边栏配置项"""
    items = []
    
    # 遍历目录下的所有 .mdx 文件
    for filename in os.listdir(directory):
        if filename.endswith('.mdx'):
            file_path = os.path.join(directory, filename)
            title = extract_title_from_mdx(file_path)
            
            if title:
                # 文件 ID 是相对于 faq 目录的路径（不包含扩展名）
                file_id = os.path.join('general-product-inquiry', os.path.splitext(filename)[0])
                
                item = {
                    "type": "doc",
                    "label": title,
                    "id": file_id
                }
                items.append(item)
    
    # 按标题排序
    items.sort(key=lambda x: x['label'])
    return items

def update_sidebar_json(sidebar_file, product_inquiry_items):
    """更新 sidebars.json 文件"""
    try:
        with open(sidebar_file, 'r', encoding='utf-8') as f:
            sidebar_data = json.load(f)
        
        # 查找产品咨询分类并更新其项目
        for category in sidebar_data['mySidebar']:
            if category.get('label') == '产品咨询':
                category['items'] = product_inquiry_items
                break
        
        # 写入更新后的配置
        with open(sidebar_file, 'w', encoding='utf-8') as f:
            json.dump(sidebar_data, f, ensure_ascii=False, indent=4)
            
        print("Sidebar configuration updated successfully!")
        
    except Exception as e:
        print(f"Error updating sidebar file: {e}")

def main():
    # 设置目录路径
    faq_dir = os.path.dirname(os.path.abspath(__file__))
    product_inquiry_dir = os.path.join(faq_dir, 'general-product-inquiry')
    sidebar_file = os.path.join(faq_dir, 'sidebars.json')
    
    # 生成产品咨询分类的项目
    items = generate_sidebar_items(product_inquiry_dir)
    
    # 更新 sidebars.json
    update_sidebar_json(sidebar_file, items)

if __name__ == '__main__':
    main()