import os
import re

def convert_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 分割 frontmatter 和正文
    parts = content.split('---', 2)
    if len(parts) >= 3:
        frontmatter = parts[0] + '---\n' + parts[1] + '---\n'
        body = parts[2]
    else:
        frontmatter = ''
        body = content

    # 查找第一个一级标题
    title_match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
    if title_match:
        title_text = title_match.group(1)
        # 添加 import 语句和新的标题格式
        new_content = frontmatter
        new_content += 'import { Title } from \'../title\';\n\n'
        new_content += f'<Title>{title_text}</Title>\n'
        # 替换原标题
        body = re.sub(r'^#\s+.+$', '', body, count=1, flags=re.MULTILINE)
        new_content += body
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Converted {file_path}')
    else:
        print(f'No title found in {file_path}')

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mdx'):
                file_path = os.path.join(root, file)
                convert_file(file_path)

if __name__ == '__main__':
    target_dir = '/Users/zego/Documents/docs_all/general/zh/faq/faq-doc-zh'
    process_directory(target_dir)
