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
            
            # 解析 rewrite 规则
            match = re.search(r'rewrite \^/article/(\d+)\$ (https://doc-zh\.zego\.im)?([^?]+)', line)
            if match:
                article_id = match.group(1)
                new_path = match.group(3)
                mapping[article_id] = new_path
    
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
    # transfer.conf 的完整路径
    transfer_conf = '/Users/zego/Documents/docs_all/transfer.conf'
    # 获取脚本所在目录的父目录路径
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
