import os
import re
import json

def update_overview_file(overview_path, sidebar_data):
    """更新 overview.mdx 文件中的链接"""
    try:
        with open(overview_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 找到所有 FilteredLink 标签
        link_pattern = r'<FilteredLink[^>]*>(.*?)</FilteredLink>'
        links = re.finditer(link_pattern, content, re.DOTALL)
        updated_content = content

        # 获取 sidebar 中的所有文档
        faq_docs = {}
        for item in sidebar_data["mySidebar"]:
            if item.get("type") == "category" and item.get("label") == "常见问题":
                for doc in item.get("items", []):
                    if doc.get("type") == "doc":
                        faq_docs[doc["label"].strip()] = doc["id"]

        # 对每个 FilteredLink 进行处理
        for match in links:
            link_content = match.group(0)
            title = match.group(1).strip()
            
            # 查找匹配的文档
            if title in faq_docs:
                doc_id = faq_docs[title]
                # 替换这个特定链接的 href
                new_link = re.sub(
                    r'href="[^"]*"',
                    f'href="/faq/{doc_id}"',
                    link_content
                )
                updated_content = updated_content.replace(link_content, new_link)

        # 写入文件
        with open(overview_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
            
        print("成功更新 overview.mdx 文件中的链接")

    except Exception as e:
        print(f"更新 overview.mdx 文件时出错: {e}")

def main():
    # 设置目录路径
    faq_dir = os.path.dirname(os.path.abspath(__file__))
    overview_path = os.path.join(faq_dir, 'overview.mdx')
    sidebar_path = os.path.join(faq_dir, 'sidebars.json')

    try:
        # 读取 sidebar.json
        with open(sidebar_path, 'r', encoding='utf-8') as f:
            sidebar_data = json.load(f)

        # 更新 overview.mdx 文件
        update_overview_file(overview_path, sidebar_data)

    except Exception as e:
        print(f"执行脚本时出错: {e}")

if __name__ == '__main__':
    main()