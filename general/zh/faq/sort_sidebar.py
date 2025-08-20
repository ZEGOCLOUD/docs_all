import json
import re

def extract_titles_from_overview(overview_path):
    """从 overview.mdx 文件中提取标题顺序"""
    with open(overview_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找所有 FilteredLink 标签中的标题
    titles = []
    link_pattern = r'<FilteredLink[^>]*>(.*?)</FilteredLink>'
    matches = re.finditer(link_pattern, content, re.DOTALL)
    
    for match in matches:
        title = match.group(1).strip()
        titles.append(title)
    
    return titles

def sort_sidebar_items(sidebar_data, overview_titles):
    """根据 overview 中的标题顺序重新排序 sidebar 中的 items"""
    # 找到常见问题分类
    for item in sidebar_data["mySidebar"]:
        if item.get("type") == "category" and item.get("label") == "常见问题":
            faq_items = item["items"]
            
            # 创建一个标题到项目的映射
            title_to_item = {item["label"]: item for item in faq_items}
            
            # 按照 overview 中的顺序重新排列项目
            sorted_items = []
            for title in overview_titles:
                if title in title_to_item:
                    sorted_items.append(title_to_item[title])
            
            # 添加未在 overview 中出现但在 sidebar 中存在的项目
            remaining_items = [item for item in faq_items if item["label"] not in overview_titles]
            sorted_items.extend(remaining_items)
            
            # 更新 items
            item["items"] = sorted_items
            break

def main():
    # 设置文件路径
    overview_path = "/Users/zego/Documents/docs_all/general/zh/faq/overview.mdx"
    sidebar_path = "/Users/zego/Documents/docs_all/general/zh/faq/sidebars.json"
    
    try:
        # 从 overview.mdx 提取标题顺序
        overview_titles = extract_titles_from_overview(overview_path)
        
        # 读取 sidebar.json
        with open(sidebar_path, 'r', encoding='utf-8') as f:
            sidebar_data = json.load(f)
        
        # 重新排序
        sort_sidebar_items(sidebar_data, overview_titles)
        
        # 写回文件
        with open(sidebar_path, 'w', encoding='utf-8') as f:
            json.dump(sidebar_data, f, ensure_ascii=False, indent=4)
        
        print("成功更新 sidebars.json 文件中的顺序")
        
    except Exception as e:
        print(f"执行脚本时出错: {e}")

if __name__ == '__main__':
    main()
