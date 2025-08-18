import os
import json
import shutil

def load_mapping(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # 创建映射字典
    name_mapping = {item['name']: item['new-name'] for item in data}
    return name_mapping

def rename_files(source_dir, mapping):
    # 确保目录存在
    if not os.path.exists(source_dir):
        print(f"目录不存在: {source_dir}")
        return

    # 获取目录中的所有文件
    files = os.listdir(source_dir)
    
    # 记录重命名操作
    renamed_count = 0
    skipped_count = 0
    
    for filename in files:
        # 获取文件名（不含扩展名）和扩展名
        name, ext = os.path.splitext(filename)
        
        # 检查文件名是否在映射中
        if name in mapping:
            new_name = mapping[name] + ext
            old_path = os.path.join(source_dir, filename)
            new_path = os.path.join(source_dir, new_name)
            
            # 如果新文件名已存在，添加数字后缀
            counter = 1
            while os.path.exists(new_path):
                base_name = mapping[name]
                new_name = f"{base_name}_{counter}{ext}"
                new_path = os.path.join(source_dir, new_name)
                counter += 1
            
            try:
                # 重命名文件
                shutil.move(old_path, new_path)
                print(f"已重命名: {filename} -> {new_name}")
                renamed_count += 1
            except Exception as e:
                print(f"重命名失败 {filename}: {str(e)}")
                skipped_count += 1
        else:
            print(f"跳过: {filename} (在映射中未找到)")
            skipped_count += 1
    
    print(f"\n重命名完成:")
    print(f"成功: {renamed_count} 个文件")
    print(f"跳过: {skipped_count} 个文件")

if __name__ == "__main__":
    # 配置路径
    json_file = "/Users/zego/Documents/docs_all/general/zh/faq/deepseek_json_formatted.json"
    faq_dir = "/Users/zego/Documents/docs_all/general/zh/faq/faq-doc-zh"
    
    # 加载映射
    mapping = load_mapping(json_file)
    
    # 执行重命名
    rename_files(faq_dir, mapping)
