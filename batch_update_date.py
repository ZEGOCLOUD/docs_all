import os
import re

def update_file_metadata(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # 检查文件是否以 --- 开头
        if not content.startswith('---\n'):
            return False
            
        # 查找第一个 --- 到第二个 --- 之间的内容
        pattern = r'^---\n(.*?\n)---'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            metadata = match.group(1)
            new_metadata = metadata
            
            # 查找 articleID 行
            article_id_pattern = r'(articleID:\s*\d+\n)'
            article_id_match = re.search(article_id_pattern, metadata)
            
            if article_id_match:
                # 在 articleID 后添加 date
                date_pattern = r'date:\s*"[^"]*"'
                if not re.search(date_pattern, metadata):
                    article_id_line = article_id_match.group(1)
                    new_metadata = metadata.replace(
                        article_id_line,
                        f'{article_id_line}date: "2024-01-02"\n'
                    )
                    
                # 替换原文件内容
                new_content = f'---\n{new_metadata}---{content[match.end():]}'
                
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                    
                return True
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")
        return False

def find_and_update_files(directory, target_filename):
    """
    在指定目录中查找指定文件名并更新它们的元数据
    """
    # 遍历目录
    for root, _, files in os.walk(directory):
        for filename in files:
            # 只处理指定的文件名
            if filename == target_filename:
                file_path = os.path.join(root, filename)
                if update_file_metadata(file_path):
                    print(f"成功更新文件: {file_path}")
                else:
                    print(f"无法更新文件: {file_path}")

def main():
    # 指定要搜索的目录路径和文件名
    directory = "/Users/zego/Documents/docs_all/core_products/real-time-voice-video"
    target_filename = "audio-mixing.mdx"  # 指定要处理的文件名
    find_and_update_files(directory, target_filename)
    print("处理完成!")

if __name__ == "__main__":
    main()