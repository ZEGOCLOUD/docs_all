import os
import re

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找包含 ## 接口原型 的部分
    pattern = r'(## 接口原型[\s\S]*?请求地址：)([^`\n]+)'
    
    # 如果找到匹配且URL不在反引号中，则添加反引号
    def replace_func(match):
        prefix = match.group(1)
        url = match.group(2).strip()
        if not url.startswith('`'):
            return f'{prefix}`{url}`'
        return match.group(0)
    
    new_content = re.sub(pattern, replace_func, content)
    
    # 如果内容有变化，写回文件
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'已修改文件: {file_path}')

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mdx') or file.endswith('.md'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if '## 接口原型' in content and '请求地址：' in content:
                            process_file(file_path)
                except Exception as e:
                    print(f'处理文件 {file_path} 时出错: {str(e)}')

if __name__ == '__main__':
    # 获取用户输入的目标目录
    target_dir = input('请输入要处理的目录路径: ').strip()
    
    if os.path.exists(target_dir):
        print(f'正在处理目录: {target_dir}')
        process_directory(target_dir)
    else:
        print(f'目录不存在: {target_dir}')