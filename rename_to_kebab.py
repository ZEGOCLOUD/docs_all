import os
import re

def camel_to_kebab(name):
    # 处理驼峰命名
    name = re.sub('([a-z0-9])([A-Z])', r'\1-\2', name)
    # 处理下划线
    name = name.replace('_', '-')
    # 转换为小写
    name = name.lower()
    # 处理连续的连字符
    name = re.sub('-+', '-', name)
    return name

def rename_files_to_kebab(directory):
    # 确保目录存在
    if not os.path.exists(directory):
        print(f"目录不存在: {directory}")
        return

    # 获取目录中的所有文件
    for filename in os.listdir(directory):
        # 分离文件名和扩展名
        name, ext = os.path.splitext(filename)
        
        # 转换为连字符格式
        new_name = camel_to_kebab(name)
        
        # 如果文件名没有变化，跳过
        if new_name == name.lower():
            continue
            
        # 构建新的完整文件名
        new_filename = new_name + ext
        
        # 构建完整的文件路径
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_filename)
        
        # 重命名文件
        try:
            os.rename(old_path, new_path)
            print(f"已重命名: {filename} -> {new_filename}")
        except Exception as e:
            print(f"重命名失败 {filename}: {str(e)}")

if __name__ == "__main__":
    directory = "/Users/zego/Documents/docs_all/general/zh/faq/general-product-inquiry"
    rename_files_to_kebab(directory)
    print("重命名完成！")