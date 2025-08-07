#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件内容替换脚本
根据提供的articleID列表，找到对应的文件并替换其内容为引用语句
"""

import os
import re
from pathlib import Path
from typing import List, Set

# ========== 配置区域 - 在这里修改你的参数 ==========
CONFIG = {
    # 要替换的articleID列表
    "ids":["18698", "18699", "18869"],
    
    # 引用语句 - 注意这里可以直接使用单引号，不需要转义
    "import_statement": """import Content from '/cloud-market/ai-voice-changer/zh/ios/overview.mdx'

<Content />""",
    
    # 搜索路径
    "path": "/Users/zego/Documents/docs_all/cloud-market",

    # 排除路径（多个）- 这些路径下的文件将不会被处理
    "exclude_paths": [
        # 示例：排除特定文件夹
        # "/Users/zego/Documents/docs_all/core_products/real-time-voice-video/zh/android-java/snippets",
        # "/Users/zego/Documents/docs_all/core_products/real-time-voice-video/zh/ios-oc/snippets",
        # 您可以在这里添加要排除的路径
        "/Users/zego/Documents/docs_all/core_products/aiagent",
        "/Users/zego/Documents/docs_all/core_products/zim",
    ],
    
    # 是否为预览模式（True: 只预览不修改，False: 实际执行修改）
    "dry_run": False
}
# ===============================================


def parse_article_id(content: str) -> str:
    """
    从文件内容中解析articleID
    
    Args:
        content: 文件内容
        
    Returns:
        articleID字符串，如果未找到返回空字符串
    """
    # 匹配 ---\narticleID: xxxxx\n--- 模式
    pattern = r'---\s*\narticleID:\s*(\d+)\s*\n---'
    match = re.search(pattern, content)
    if match:
        return match.group(1)
    return ""


def extract_frontmatter(content: str) -> str:
    """
    提取文件的frontmatter部分（---到---之间的内容）
    
    Args:
        content: 文件内容
        
    Returns:
        frontmatter内容，包括前后的---
    """
    pattern = r'(---.*?---)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1)
    return ""


def find_mdx_files(search_path: str, exclude_paths: List[str] = None) -> List[Path]:
    """
    递归查找指定路径下的所有.mdx文件，支持排除指定路径
    
    Args:
        search_path: 搜索路径
        exclude_paths: 要排除的路径列表
        
    Returns:
        .mdx文件路径列表
    """
    search_path = Path(search_path)
    if not search_path.exists():
        print(f"错误：路径 {search_path} 不存在")
        return []
    
    # 将排除路径转换为Path对象
    exclude_paths = exclude_paths or []
    exclude_path_objects = [Path(path) for path in exclude_paths]
    
    mdx_files = []
    for file_path in search_path.rglob("*.mdx"):
        if file_path.is_file():
            # 检查文件是否在排除路径中
            should_exclude = False
            for exclude_path in exclude_path_objects:
                try:
                    # 检查文件路径是否在排除路径下
                    file_path.relative_to(exclude_path)
                    should_exclude = True
                    break
                except ValueError:
                    # 如果文件不在排除路径下，relative_to会抛出ValueError
                    continue
            
            if not should_exclude:
                mdx_files.append(file_path)
    
    return mdx_files


def replace_file_content(file_path: Path, target_ids: Set[str], import_statement: str, dry_run: bool = False) -> bool:
    """
    检查并替换文件内容
    
    Args:
        file_path: 文件路径
        target_ids: 目标articleID集合
        import_statement: 引用语句
        dry_run: 是否为预览模式
        
    Returns:
        是否进行了替换
    """
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析articleID
        article_id = parse_article_id(content)
        if not article_id:
            return False
        
        # 检查是否在目标ID列表中
        if article_id not in target_ids:
            return False
        
        # 提取frontmatter
        frontmatter = extract_frontmatter(content)
        if not frontmatter:
            print(f"警告：文件 {file_path} 没有找到有效的frontmatter")
            return False
        
        # 构建新内容
        new_content = f"{frontmatter}\n{import_statement}"
        
        if dry_run:
            print(f"[预览] 将替换文件: {file_path}")
            print(f"  ArticleID: {article_id}")
            print(f"  新内容预览:")
            print(f"  {frontmatter}")
            print(f"  {import_statement}")
            print("-" * 50)
        else:
            # 写入新内容
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ 已替换文件: {file_path} (ArticleID: {article_id})")
        
        return True
        
    except Exception as e:
        print(f"错误：处理文件 {file_path} 时出错: {e}")
        return False


def main():
    # 从配置中读取参数
    target_ids = set(CONFIG["ids"])
    import_statement = CONFIG["import_statement"]
    search_path = CONFIG["path"]
    exclude_paths = CONFIG.get("exclude_paths", [])
    dry_run = CONFIG["dry_run"]
    
    print("=== 文件内容替换脚本 ===")
    print(f"目标ArticleID列表: {', '.join(target_ids)}")
    print(f"搜索路径: {search_path}")
    if exclude_paths:
        print(f"排除路径: ")
        for path in exclude_paths:
            print(f"  - {path}")
    else:
        print("排除路径: 无")
    print(f"引用语句:\n{import_statement}")
    print(f"预览模式: {'是' if dry_run else '否'}")
    print("=" * 50)
    
    # 查找所有.mdx文件
    mdx_files = find_mdx_files(search_path, exclude_paths)
    print(f"找到 {len(mdx_files)} 个.mdx文件")
    
    # 如果是预览模式，询问用户是否继续
    if dry_run:
        print("\n当前为预览模式，将显示哪些文件会被修改...")
        print("如需实际执行替换，请将CONFIG中的'dry_run'设置为False")
        print("-" * 50)
    
    # 处理文件
    replaced_count = 0
    for file_path in mdx_files:
        if replace_file_content(file_path, target_ids, import_statement, dry_run):
            replaced_count += 1
    
    print("-" * 50)
    if dry_run:
        print(f"预览完成，共找到 {replaced_count} 个匹配的文件")
        print("如需实际执行替换，请将CONFIG中的'dry_run'设置为False，然后重新运行脚本")
    else:
        print(f"替换完成，共处理了 {replaced_count} 个文件")


if __name__ == "__main__":
    main() 