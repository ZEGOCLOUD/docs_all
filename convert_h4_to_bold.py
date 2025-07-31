import re
import os

def convert_h4_to_bold(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        converted_content = re.sub(r'####\s+([^\n]+)', r'**\1**', content)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(converted_content)
        print(f"文件 {file_path} 转换完成！")
    except FileNotFoundError:
        print(f"错误：找不到文件 {file_path}")
    except Exception as e:
        print(f"发生错误：{str(e)}")

def process_directory(directory_path):
    try:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith(('.md', '.mdx')):
                    file_path = os.path.join(root, file)
                    convert_h4_to_bold(file_path)
        print(f"目录 {directory_path} 下的所有文件处理完成！")
    except Exception as e:
        print(f"处理目录时发生错误：{str(e)}")

if __name__ == "__main__":
    directory_path = input("请输入要转换的文件夹路径：")
    if os.path.isdir(directory_path):
        process_directory(directory_path)
    else:
        print("错误：输入的路径不是一个有效的目录！")
