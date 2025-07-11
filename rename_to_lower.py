#!/usr/bin/env python3
"""
文件和目录重命名脚本
将文件名和目录名转换为小写，并将空格替换为连字符
同时更新 Markdown 文件中的相对链接和跨实例的import引用

功能：
1. 递归重命名目录和文件（小写 + 空格转连字符）
2. 更新 Markdown 文件中的相对链接
3. 检查并更新跨实例的 import 引用（基于 docuo.config.json）

使用方法：
python3 rename_to_lower.py

注意：
- 会自动查找当前目录下的 docuo.config.json 配置文件
- 如果找到配置文件，会检查所有实例中的 import 引用
- 建议在运行前备份重要文件
"""

import os
import re
import json

def convert_path_to_lowercase(path):
    """将路径转换为小写并用连字符替换空格"""
    # 分割路径为各个部分
    parts = path.split('/')
    converted_parts = []

    for part in parts:
        if part in ['.', '..', '']:
            # 保持相对路径标识符不变
            converted_parts.append(part)
        else:
            # 转换文件名/目录名：小写 + 空格替换为连字符
            converted_part = part.lower().replace(' ', '-')
            # 处理 URL 编码的空格 (%20)
            converted_part = converted_part.replace('%20', '-')
            converted_parts.append(converted_part)

    return '/'.join(converted_parts)

def get_all_instance_paths(config_file):
    """从配置文件中获取所有实例的路径"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        instance_paths = []
        for instance in config.get('instances', []):
            path = instance.get('path', '')
            # 只处理本地路径（不是 https:// 开头的）
            if path and not path.startswith('http'):
                instance_paths.append(path)

        return instance_paths
    except Exception as e:
        print(f"读取配置文件 {config_file} 时出错: {e}")
        return []

def find_import_references(file_path):
    """查找文件中的import引用"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 匹配 import 语句：import Content from '/path/to/file.mdx'
        # 支持单引号和双引号
        import_pattern = r'import\s+\w+\s+from\s+[\'"]([^\'"]+\.mdx?)[\'"]'

        imports = re.findall(import_pattern, content)
        return imports
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
        return []

def update_import_references(file_path, old_import_path, new_import_path):
    """更新文件中的import引用"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 替换import路径（支持单引号和双引号）
        pattern = r'(import\s+\w+\s+from\s+[\'"])' + re.escape(old_import_path) + r'([\'"])'
        replacement = r'\1' + new_import_path + r'\2'

        updated_content = re.sub(pattern, replacement, content)

        if updated_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"更新了import引用: {file_path}")
            print(f"  {old_import_path} -> {new_import_path}")
            return True
        return False
    except Exception as e:
        print(f"更新文件 {file_path} 时出错: {e}")
        return False

def update_markdown_links(file_path):
    """更新 Markdown 文件中的相对链接"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 匹配 Markdown 链接语法：[text](./path) 或 [text](../path)
        # 正则表达式解释：
        # \[([^\]]*)\] - 匹配 [链接文本]
        # \((\.\./|\./[^)]*)\) - 匹配 (相对路径)，以 ./ 或 ../ 开头
        pattern = r'\[([^\]]*)\]\((\.\.?/[^)]*)\)'

        def replace_link(match):
            link_text = match.group(1)
            original_path = match.group(2)
            converted_path = convert_path_to_lowercase(original_path)
            return f'[{link_text}]({converted_path})'

        # 替换所有匹配的链接
        updated_content = re.sub(pattern, replace_link, content)

        # 如果内容有变化，写回文件
        if updated_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"更新了 Markdown 链接: {file_path}")

    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")



def collect_all_md_files(root_dir, config_file):
    """收集所有需要检查的md/mdx文件"""
    all_md_files = []

    # 获取所有实例路径
    instance_paths = get_all_instance_paths(config_file) if config_file else []

    # 如果有配置文件，优先检查实例路径
    if instance_paths:
        print(f"从配置文件中找到 {len(instance_paths)} 个实例路径")
        for instance_path in instance_paths:
            full_instance_path = os.path.join(root_dir, instance_path)
            if os.path.exists(full_instance_path):
                for dirpath, _, filenames in os.walk(full_instance_path):
                    for filename in filenames:
                        if filename.lower().endswith(('.md', '.mdx')):
                            file_path = os.path.join(dirpath, filename)
                            all_md_files.append(file_path)

    # 同时也检查整个根目录下的所有md/mdx文件（避免遗漏）
    print("扫描整个目录结构...")
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(('.md', '.mdx')):
                file_path = os.path.join(dirpath, filename)
                if file_path not in all_md_files:  # 避免重复
                    all_md_files.append(file_path)

    return all_md_files

def check_import_references_against_renames(target_dir, rename_mapping, docs_root_dir, config_file):
    """检查所有文件的import引用，找出需要更新的"""
    print("检查import引用与重命名文件的匹配...")

    # 收集所有md/mdx文件（从文档根目录开始扫描）
    all_md_files = collect_all_md_files(docs_root_dir, config_file)
    print(f"共找到 {len(all_md_files)} 个md/mdx文件")

    # 构建重命名文件的查找映射
    rename_lookup = {}
    for old_rel_path, new_rel_path in rename_mapping.items():
        # 将相对于target_dir的路径转换为相对于docs_root_dir的路径
        target_rel_to_docs = os.path.relpath(target_dir, docs_root_dir)

        old_full_rel_path = os.path.join(target_rel_to_docs, old_rel_path).replace('\\', '/')
        new_full_rel_path = os.path.join(target_rel_to_docs, new_rel_path).replace('\\', '/')

        # 添加绝对路径映射（import语句中使用的格式）
        old_abs_path = '/' + old_full_rel_path
        new_abs_path = '/' + new_full_rel_path
        rename_lookup[old_abs_path] = new_abs_path

        print(f"  重命名映射: {old_abs_path} -> {new_abs_path}")

    # 检查每个文件中的import引用
    files_to_update = {}
    total_imports_found = 0
    matching_imports = 0

    for file_path in all_md_files:
        imports = find_import_references(file_path)
        if imports:
            total_imports_found += len(imports)
            updates_for_file = []

            for import_path in imports:
                # 检查这个import路径是否匹配任何待重命名的文件
                if import_path in rename_lookup:
                    new_path = rename_lookup[import_path]
                    updates_for_file.append((import_path, new_path))
                    matching_imports += 1
                    print(f"  匹配: {import_path} -> {new_path}")

            if updates_for_file:
                files_to_update[file_path] = updates_for_file

    print(f"扫描结果: 共 {total_imports_found} 个import引用，其中 {matching_imports} 个需要更新")
    return files_to_update

def check_broken_import_references(target_dir, docs_root_dir, config_file):
    """检查需要修复的import引用（当没有重命名操作时）"""
    print("检查需要修复的import引用...")

    # 收集所有md/mdx文件
    all_md_files = collect_all_md_files(docs_root_dir, config_file)
    print(f"共找到 {len(all_md_files)} 个md/mdx文件")

    files_to_update = {}
    total_imports_found = 0
    matching_imports = 0

    # 计算target_dir相对于docs_root_dir的路径
    target_rel_to_docs = os.path.relpath(target_dir, docs_root_dir)

    for file_path in all_md_files:
        imports = find_import_references(file_path)
        if imports:
            total_imports_found += len(imports)
            updates_for_file = []

            for import_path in imports:
                # 只处理指向target_dir内文件的import
                should_process = False

                if import_path.startswith('/'):
                    # 绝对路径，检查是否指向target_dir
                    clean_import_path = import_path.lstrip('/')
                    if clean_import_path.startswith(target_rel_to_docs + '/'):
                        should_process = True
                else:
                    # 相对路径，检查解析后的绝对路径是否在target_dir内
                    file_dir = os.path.dirname(file_path)
                    resolved_path = os.path.join(file_dir, import_path)
                    resolved_path = os.path.normpath(resolved_path)

                    # 检查解析后的路径是否在target_dir内
                    if resolved_path.startswith(target_dir + '/') or resolved_path == target_dir:
                        should_process = True

                if should_process:
                    # 检查这个import路径是否需要转换为小写格式
                    converted_path = convert_path_to_lowercase(import_path)

                    if converted_path != import_path:
                        # 检查转换后的文件是否存在
                        if import_path.startswith('/'):
                            check_path = os.path.join(docs_root_dir, converted_path.lstrip('/'))
                        else:
                            file_dir = os.path.dirname(file_path)
                            check_path = os.path.join(file_dir, converted_path)

                        check_path = os.path.normpath(check_path)

                        if os.path.exists(check_path):
                            # 转换后的文件存在，需要更新引用
                            updates_for_file.append((import_path, converted_path))
                            matching_imports += 1
                            print(f"  需要修复: {import_path} -> {converted_path}")

            if updates_for_file:
                files_to_update[file_path] = updates_for_file

    print(f"扫描结果: 共 {total_imports_found} 个import引用，其中 {matching_imports} 个需要修复")
    return files_to_update

def final_check_and_fix(docs_root_dir, target_dir=None):
    """最终检查并修复剩余的引用"""
    print("扫描剩余的大小写问题...")

    # 收集所有md/mdx文件
    all_md_files = []
    for dirpath, _, filenames in os.walk(docs_root_dir):
        for filename in filenames:
            if filename.lower().endswith(('.md', '.mdx')):
                file_path = os.path.join(dirpath, filename)
                all_md_files.append(file_path)

    # 计算target_dir相对于docs_root_dir的路径（如果提供了target_dir）
    target_rel_to_docs = None
    if target_dir:
        target_rel_to_docs = os.path.relpath(target_dir, docs_root_dir)

    # 查找包含大写路径的import
    problematic_imports = []
    for file_path in all_md_files:
        imports = find_import_references(file_path)
        for import_path in imports:
            # 如果指定了target_dir，只处理指向该目录的import
            if target_rel_to_docs:
                if import_path.startswith('/'):
                    # 绝对路径
                    clean_import_path = import_path.lstrip('/')
                    if not clean_import_path.startswith(target_rel_to_docs + '/'):
                        continue  # 跳过不相关的import
                else:
                    # 相对路径，检查解析后的绝对路径是否在target_dir内
                    file_dir = os.path.dirname(file_path)
                    resolved_path = os.path.join(file_dir, import_path)
                    resolved_path = os.path.normpath(resolved_path)

                    # 检查解析后的路径是否在target_dir内
                    if not resolved_path.startswith(target_dir + '/') and resolved_path != target_dir:
                        continue  # 跳过不相关的import

            # 检查是否包含大写字母或空格
            if any(c.isupper() or c == ' ' for c in import_path):
                converted_path = convert_path_to_lowercase(import_path)
                if converted_path != import_path:
                    # 检查转换后的文件是否存在
                    if import_path.startswith('/'):
                        target_file = os.path.join(docs_root_dir, converted_path.lstrip('/'))
                    else:
                        file_dir = os.path.dirname(file_path)
                        target_file = os.path.join(file_dir, converted_path)

                    target_file = os.path.normpath(target_file)

                    if os.path.exists(target_file):
                        problematic_imports.append((file_path, import_path, converted_path))

    if problematic_imports:
        print(f"发现 {len(problematic_imports)} 个需要修复的引用:")
        fixed_count = 0
        for file_path, old_path, new_path in problematic_imports:
            rel_file_path = os.path.relpath(file_path, docs_root_dir)
            print(f"  修复: {rel_file_path}")
            print(f"    {old_path} -> {new_path}")
            if update_import_references(file_path, old_path, new_path):
                fixed_count += 1

        print(f"最终修复了 {fixed_count} 个引用")
    else:
        print("✅ 没有发现需要修复的引用")

def rename_all(root_dir, config_file=None):
    # 收集重命名映射
    rename_mapping = {}

    # 先收集所有需要重命名的文件和目录
    print("收集重命名映射...")
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        # 收集文件重命名映射
        for filename in filenames:
            old_path = os.path.join(dirpath, filename)
            new_filename = filename.lower().replace(' ', '-')
            new_path = os.path.join(dirpath, new_filename)
            if old_path != new_path:
                # 转换为相对路径用于import检查
                rel_old_path = os.path.relpath(old_path, root_dir)
                rel_new_path = os.path.relpath(new_path, root_dir)
                rename_mapping[rel_old_path] = rel_new_path

        # 收集目录重命名映射
        for dirname in dirnames:
            old_dir = os.path.join(dirpath, dirname)
            new_dirname = dirname.lower().replace(' ', '-')
            new_dir = os.path.join(dirpath, new_dirname)
            if old_dir != new_dir:
                rel_old_dir = os.path.relpath(old_dir, root_dir)
                rel_new_dir = os.path.relpath(new_dir, root_dir)
                rename_mapping[rel_old_dir] = rel_new_dir

    print(f"找到 {len(rename_mapping)} 个需要重命名的文件/目录")

    # 查找文档根目录（包含docuo.config.json的目录）
    docs_root_dir = root_dir
    config_file = None
    current_dir = root_dir
    while current_dir != os.path.dirname(current_dir):  # 直到根目录
        if os.path.exists(os.path.join(current_dir, 'docuo.config.json')):
            docs_root_dir = current_dir
            config_file = os.path.join(current_dir, 'docuo.config.json')
            print(f"找到文档根目录: {docs_root_dir}")
            break
        current_dir = os.path.dirname(current_dir)

    # 检查所有import引用（无论是否有文件需要重命名）
    files_to_update = {}
    if rename_mapping:
        # 如果有重命名映射，检查相关的import引用
        files_to_update = check_import_references_against_renames(root_dir, rename_mapping, docs_root_dir, config_file)
    else:
        # 如果没有重命名映射，检查是否有需要修复的import引用
        print("没有文件需要重命名，检查是否有需要修复的import引用...")
        files_to_update = check_broken_import_references(root_dir, docs_root_dir, config_file)

    # 执行重命名
    print("开始重命名文件和目录...")
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        # 重命名文件
        for filename in filenames:
            old_path = os.path.join(dirpath, filename)
            new_filename = filename.lower().replace(' ', '-')
            new_path = os.path.join(dirpath, new_filename)
            if old_path != new_path:
                os.rename(old_path, new_path)
                print(f"重命名文件: {old_path} -> {new_path}")

        # 重命名文件夹
        for dirname in dirnames:
            old_dir = os.path.join(dirpath, dirname)
            new_dirname = dirname.lower().replace(' ', '-')
            new_dir = os.path.join(dirpath, new_dirname)
            if old_dir != new_dir:
                os.rename(old_dir, new_dir)
                print(f"重命名目录: {old_dir} -> {new_dir}")

    # 更新import引用
    if files_to_update:
        print("更新import引用...")
        updated_files_count = 0
        total_imports_updated = 0
        failed_updates = []

        for file_path, updates in files_to_update.items():
            file_updated = False
            for old_import_path, new_import_path in updates:
                if update_import_references(file_path, old_import_path, new_import_path):
                    file_updated = True
                    total_imports_updated += 1
                else:
                    failed_updates.append((file_path, old_import_path, new_import_path))

            if file_updated:
                updated_files_count += 1

        print(f"共更新了 {updated_files_count} 个文件中的 {total_imports_updated} 个import引用")

        # 如果有失败的更新，进行二次尝试
        if failed_updates:
            print(f"有 {len(failed_updates)} 个import引用更新失败，进行二次尝试...")
            retry_success = 0
            for file_path, old_import_path, new_import_path in failed_updates:
                # 检查目标文件是否真的存在
                if new_import_path.startswith('/'):
                    target_file = os.path.join(docs_root_dir, new_import_path.lstrip('/'))
                else:
                    file_dir = os.path.dirname(file_path)
                    target_file = os.path.join(file_dir, new_import_path)

                target_file = os.path.normpath(target_file)

                if os.path.exists(target_file):
                    if update_import_references(file_path, old_import_path, new_import_path):
                        retry_success += 1
                        print(f"  重试成功: {os.path.relpath(file_path, docs_root_dir)}")
                    else:
                        print(f"  重试失败: {os.path.relpath(file_path, docs_root_dir)}")
                        print(f"    {old_import_path} -> {new_import_path}")
                else:
                    print(f"  目标文件不存在: {target_file}")

            print(f"重试成功 {retry_success} 个引用")
    else:
        print("未检查到需要更新的import引用")

    # 重命名完成后，更新所有 Markdown 文件中的相对链接
    print("开始更新 Markdown 文件中的相对链接...")
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(('.md', '.mdx')):
                file_path = os.path.join(dirpath, filename)
                update_markdown_links(file_path)

    # 最终检查：查找剩余的未修复引用
    print("\n进行最终检查...")
    final_check_and_fix(docs_root_dir if 'docs_root_dir' in locals() else root_dir, root_dir)

if __name__ == "__main__":
    target_dir = input("请输入目标目录路径: ")

    # 配置文件查找将在rename_all函数中处理
    rename_all(target_dir)
    print("重命名完成！")