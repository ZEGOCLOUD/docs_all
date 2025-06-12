import os

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

if __name__ == "__main__":
    target_dir = input("请输入目标目录路径: ")
    rename_all(target_dir)
    print("重命名完成！") 