import os
import re

def convert_path_to_lowercase(path):
    """将路径转换为小写并用连字符替换空格"""
    # 分割路径为各个部分
    parts = path.split('/')
    converted_parts = []

    for part in parts:
        if part in ['.', '..', '']:
            # 保持相对路径标识符不变
            converted_parts.append(part)
        else:
            # 转换文件名/目录名：小写 + 空格替换为连字符
            converted_part = part.lower().replace(' ', '-')
            # 处理 URL 编码的空格 (%20)
            converted_part = converted_part.replace('%20', '-')
            converted_parts.append(converted_part)

    return '/'.join(converted_parts)

def update_markdown_links(file_path):
    """更新 Markdown 文件中的相对链接"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 匹配 Markdown 链接语法：[text](./path) 或 [text](../path)
        # 正则表达式解释：
        # \[([^\]]*)\] - 匹配 [链接文本]
        # \((\.\./|\./[^)]*)\) - 匹配 (相对路径)，以 ./ 或 ../ 开头
        pattern = r'\[([^\]]*)\]\((\.\.?/[^)]*)\)'

        def replace_link(match):
            link_text = match.group(1)
            original_path = match.group(2)
            converted_path = convert_path_to_lowercase(original_path)
            return f'[{link_text}]({converted_path})'

        # 替换所有匹配的链接
        updated_content = re.sub(pattern, replace_link, content)

        # 如果内容有变化，写回文件
        if updated_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"更新了 Markdown 链接: {file_path}")

    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")

def rename_all(root_dir):
    # 先处理子目录和文件，后处理当前目录，避免重命名冲突
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        # 重命名文件
        for filename in filenames:
            old_path = os.path.join(dirpath, filename)
            new_filename = filename.lower().replace(' ', '-')
            new_path = os.path.join(dirpath, new_filename)
            if old_path != new_path:
                os.rename(old_path, new_path)
        # 重命名文件夹
        for dirname in dirnames:
            old_dir = os.path.join(dirpath, dirname)
            new_dirname = dirname.lower().replace(' ', '-')
            new_dir = os.path.join(dirpath, new_dirname)
            if old_dir != new_dir:
                os.rename(old_dir, new_dir)

    # 重命名完成后，更新所有 Markdown 文件中的相对链接
    print("开始更新 Markdown 文件中的相对链接...")
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(('.md', '.mdx')):
                file_path = os.path.join(dirpath, filename)
                update_markdown_links(file_path)

if __name__ == "__main__":
    target_dir = input("请输入目标目录路径: ")
    rename_all(target_dir)
    print("重命名完成！") 