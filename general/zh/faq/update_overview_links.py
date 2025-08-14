import os
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

def update_overview_file(overview_path, title_to_file):
    """更新 overview.mdx 文件中的产品咨询部分的链接"""
    try:
        with open(overview_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 找到产品咨询部分
        product_section_pattern = r'(## 产品咨询\n<ul>)(.*?)(</ul>)'
        product_section_match = re.search(product_section_pattern, content, re.DOTALL)
        
        if not product_section_match:
            print("未找到产品咨询部分")
            return

        # 获取产品咨询部分的内容
        product_section = product_section_match.group(2)
        updated_section = product_section

        # 对每个 FilteredLink 进行处理
        link_pattern = r'<FilteredLink[^>]*>(.*?)</FilteredLink>'
        for match in re.finditer(link_pattern, product_section, re.DOTALL):
            link_content = match.group(0)
            title = match.group(1).strip()
            
            # 查找匹配的文件
            if title in title_to_file:
                file_id = os.path.splitext(title_to_file[title])[0]
                # 只替换这个特定链接的 href
                new_link = re.sub(
                    r'href="[^"]*"',
                    f'href="/faq/general-product-inquiry/{file_id}"',
                    link_content
                )
                updated_section = updated_section.replace(link_content, new_link)

        # 替换产品咨询部分的内容
        new_content = content.replace(
            product_section_match.group(0),
            f"## 产品咨询\n<ul>{updated_section}</ul>"
        )

        # 写入文件
        with open(overview_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print("成功更新 overview.mdx 文件中的链接")

    except Exception as e:
        print(f"更新 overview.mdx 文件时出错: {e}")

def main():
    # 设置目录路径
    faq_dir = os.path.dirname(os.path.abspath(__file__))
    product_inquiry_dir = os.path.join(faq_dir, 'general-product-inquiry')
    overview_path = os.path.join(faq_dir, 'overview.mdx')

    # 获取所有 MDX 文件的标题和文件名的映射
    title_to_file = {}
    for filename in os.listdir(product_inquiry_dir):
        if filename.endswith('.mdx'):
            file_path = os.path.join(product_inquiry_dir, filename)
            title = extract_title_from_mdx(file_path)
            if title:
                title_to_file[title] = filename
                print(f"找到文件: {filename} -> {title}")

    # 更新 overview.mdx 文件中的链接
    update_overview_file(overview_path, title_to_file)

if __name__ == '__main__':
    main()