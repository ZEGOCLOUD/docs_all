# 为缺少锚点的2级标题添加锚点
# 使用方法:
# python add_missing_anchors.py <文件路径>                    # 处理单个文件
# python add_missing_anchors.py --pattern <文件模式>          # 批量处理匹配的文件
# python add_missing_anchors.py --all                        # 处理所有release-notes.mdx文件
# python add_missing_anchors.py --list                       # 列出所有release-notes.mdx文件

import re
import os
import glob

def add_missing_anchors(file_path):
    """为缺少锚点的2级标题添加锚点"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找所有版本标题（格式：## X.Y.Z 版本）
    version_pattern = r'^## (\d+\.\d+\.\d+) 版本$'
    
    def replace_version_title(match):
        version = match.group(1)
        return f'## {version} 版本 <a id="{version}"></a>'
    
    # 替换缺少锚点的版本标题
    new_content = re.sub(version_pattern, replace_version_title, content, flags=re.MULTILINE)
    
    # 如果内容有变化，写回文件
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def process_single_file(file_path):
    """处理单个文件"""
    print(f"正在处理文件: {file_path}")
    if add_missing_anchors(file_path):
        print(f"✅ 已添加缺失锚点: {file_path}")
    else:
        print(f"ℹ️  无需修改: {file_path}")

def process_multiple_files(file_pattern):
    """批量处理文件"""
    files = glob.glob(file_pattern, recursive=True)
    if not files:
        print(f"未找到匹配的文件: {file_pattern}")
        return
    
    print(f"找到 {len(files)} 个文件:")
    for file in files:
        print(f"  - {file}")
    
    confirm = input(f"\n确认要处理这 {len(files)} 个文件吗? (y/N): ")
    if confirm.lower() != 'y':
        print("操作已取消")
        return
    
    processed_count = 0
    for file_path in files:
        try:
            if add_missing_anchors(file_path):
                processed_count += 1
                print(f"✅ 已添加缺失锚点: {file_path}")
        except Exception as e:
            print(f"❌ 处理文件失败 {file_path}: {e}")
    
    print(f"\n🎉 批量处理完成！共处理了 {processed_count} 个文件")

def find_release_notes_files():
    """查找所有release-notes.mdx文件"""
    files = glob.glob("**/release-notes.mdx", recursive=True)
    return files

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 1:
        print("用法:")
        print("  python add_missing_anchors.py <文件路径>                    # 处理单个文件")
        print("  python add_missing_anchors.py --pattern <文件模式>          # 批量处理匹配的文件")
        print("  python add_missing_anchors.py --all                        # 处理所有release-notes.mdx文件")
        print("  python add_missing_anchors.py --list                       # 列出所有release-notes.mdx文件")
        sys.exit(1)
    
    if sys.argv[1] == "--all":
        files = find_release_notes_files()
        if not files:
            print("未找到任何release-notes.mdx文件")
            sys.exit(1)
        
        print(f"找到 {len(files)} 个release-notes.mdx文件:")
        for file in files:
            print(f"  - {file}")
        
        confirm = input(f"\n确认要处理所有 {len(files)} 个文件吗? (y/N): ")
        if confirm.lower() != 'y':
            print("操作已取消")
            sys.exit(0)
        
        processed_count = 0
        for file_path in files:
            try:
                if add_missing_anchors(file_path):
                    processed_count += 1
                    print(f"✅ 已添加缺失锚点: {file_path}")
            except Exception as e:
                print(f"❌ 处理文件失败 {file_path}: {e}")
        
        print(f"\n🎉 批量处理完成！共处理了 {processed_count} 个文件")
    
    elif sys.argv[1] == "--list":
        files = find_release_notes_files()
        if not files:
            print("未找到任何release-notes.mdx文件")
        else:
            print(f"找到 {len(files)} 个release-notes.mdx文件:")
            for file in files:
                print(f"  - {file}")
    
    elif sys.argv[1] == "--pattern":
        if len(sys.argv) < 3:
            print("请提供文件模式")
            sys.exit(1)
        process_multiple_files(sys.argv[2])
    
    else:
        # 处理单个文件
        file_path = sys.argv[1]
        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}")
            sys.exit(1)
        process_single_file(file_path) 