import os
import re
import json

def extract_title_from_mdx(file_path):
    """从 MDX 文件中提取标题"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 查找以 # 开头的第一行作为标题
            match = re.search(r'^#\s+(.+?)(?:\n|$)', content, re.MULTILINE)
            if match:
                return match.group(1).strip()
            # 如果没有找到 # 标题，使用文件名作为标题
            filename = os.path.basename(file_path)
            return filename.replace('.mdx', '').replace('-', ' ').title()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def update_sidebar(faq_dir, sidebar_path):
    """更新 sidebar.json 文件"""
    try:
        # 读取现有的 sidebar 配置
        with open(sidebar_path, 'r', encoding='utf-8') as f:
            sidebar_data = json.load(f)

        # 获取 FAQ 文档目录
        faq_doc_dir = os.path.join(faq_dir, 'faq-doc-zh')
        
        # 收集所有 FAQ 文档
        faq_items = []
        for filename in os.listdir(faq_doc_dir):
            if filename.endswith('.mdx'):
                file_path = os.path.join(faq_doc_dir, filename)
                title = extract_title_from_mdx(file_path)
                if title:
                    doc_id = f"faq-doc-zh/{filename.replace('.mdx', '')}"
                    faq_items.append({
                        "type": "doc",
                        "label": title,
                        "id": doc_id
                    })
                    print(f"添加文档: {title} -> {doc_id}")

        # 按标题排序
        faq_items.sort(key=lambda x: x['label'])

        # 创建 FAQ 文档分类
        faq_category = {
            "type": "category",
            "label": "常见问题",
            "collapsed": True,
            "items": faq_items
        }

        # 更新 sidebar
        # 保留原有的概览等配置
        overview_items = [item for item in sidebar_data["mySidebar"] if item.get("label") == "概览"]
        sidebar_data["mySidebar"] = overview_items + [faq_category]

        # 写入更新后的配置
        with open(sidebar_path, 'w', encoding='utf-8') as f:
            json.dump(sidebar_data, f, ensure_ascii=False, indent=4)
            
        print("成功更新 sidebar.json 文件")

    except Exception as e:
        print(f"更新 sidebar.json 文件时出错: {e}")

def main():
    # 设置目录路径
    faq_dir = os.path.dirname(os.path.abspath(__file__))
    sidebar_path = os.path.join(faq_dir, 'sidebars.json')

    # 更新 sidebar
    update_sidebar(faq_dir, sidebar_path)

if __name__ == '__main__':
    main()