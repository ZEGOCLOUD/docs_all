import os
import re
import json

def load_transfer_conf(conf_file):
    """加载 transfer.conf 文件并解析映射关系"""
    mapping = {}
    with open(conf_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            try:
                # 解析每一行的 JSON 格式
                data = json.loads(line)
                # 如果是旧文档链接格式，提取文章 ID 并建立映射
                if isinstance(data, str) and 'doc-zh.zego.im/article/' in data:
                    article_id = re.search(r'article/(\d+)', data)
                    if article_id:
                        article_id = article_id.group(1)
                        # 下一行应该是新的路径
                        new_path = json.loads(next(f).strip())
                        if new_path.startswith('/'):
                            mapping[article_id] = new_path
            except (json.JSONDecodeError, StopIteration):
                continue
    return mapping

def process_file(file_path, mapping):
    """处理单个文件中的链接替换"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式查找并替换链接
    def replace_link(match):
        article_id = match.group(1)
        if article_id in mapping:
            return mapping[article_id]
        return match.group(0)
    
    # 替换 https://doc-zh.zego.im/article/数字 格式的链接
    new_content = re.sub(r'https://doc-zh\.zego\.im/article/(\d+)', replace_link, content)
    
    # 如果内容有变化，写回文件
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"已处理文件: {file_path}")

def main():
    # 获取脚本所在目录的父目录路径
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 构建 transfer.conf 的完整路径
    transfer_conf = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(base_dir))), 'transfer.conf')
    # 构建 faq-doc-zh 目录的完整路径
    faq_dir = os.path.join(base_dir, 'faq', 'faq-doc-zh')
    
    # 加载映射关系
    mapping = load_transfer_conf(transfer_conf)
    if not mapping:
        print("未能从 transfer.conf 加载到有效的映射关系")
        return
    
    # 处理 faq-doc-zh 目录下的所有 .mdx 文件
    for filename in os.listdir(faq_dir):
        if filename.endswith('.mdx'):
            file_path = os.path.join(faq_dir, filename)
            process_file(file_path, mapping)

if __name__ == '__main__':
    main()
