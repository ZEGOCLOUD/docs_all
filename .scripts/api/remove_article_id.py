#!/usr/bin/env python3
"""
递归遍历指定目录中的所有 .md 和 .mdx 文件，
删除 frontmatter 中的 articleID 属性行。

用法：
    python remove_article_id.py <目录路径>

示例：
    python remove_article_id.py ./docs
    python remove_article_id.py /path/to/markdown/files
"""

import os
import re
import sys
from pathlib import Path


def remove_article_id_from_frontmatter(content: str) -> tuple[str, bool]:
    """
    从文件内容中删除 frontmatter 的 articleID 行。

    Args:
        content: 文件内容

    Returns:
        (修改后的内容, 是否有修改)
    """
    # 匹配 frontmatter (以 --- 开头和结尾)
    frontmatter_pattern = re.compile(r'^---\s*\n(.*?)\n---', re.DOTALL)
    match = frontmatter_pattern.match(content)

    if not match:
        return content, False

    frontmatter = match.group(1)

    # 删除 articleID 行 (匹配 articleID: 任意值)
    # 支持各种格式：articleID: 123, articleID: "123", articleID: '123'
    article_id_pattern = re.compile(r'^articleID:.*\n?', re.MULTILINE)

    if not article_id_pattern.search(frontmatter):
        return content, False

    new_frontmatter = article_id_pattern.sub('', frontmatter)

    # 清理可能产生的多余空行
    new_frontmatter = re.sub(r'\n{2,}', '\n', new_frontmatter)
    new_frontmatter = new_frontmatter.strip()

    # 重新构建内容
    new_content = f"---\n{new_frontmatter}\n---{content[match.end():]}"

    return new_content, True


def process_file(file_path: Path, dry_run: bool = False) -> bool:
    """
    处理单个文件。

    Args:
        file_path: 文件路径
        dry_run: 如果为 True，只检查不修改

    Returns:
        是否有修改
    """
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"  ❌ 读取失败: {e}")
        return False

    new_content, modified = remove_article_id_from_frontmatter(content)

    if modified and not dry_run:
        try:
            file_path.write_text(new_content, encoding='utf-8')
        except Exception as e:
            print(f"  ❌ 写入失败: {e}")
            return False

    return modified


def process_directory(directory: str, dry_run: bool = False) -> tuple[int, int]:
    """
    递归处理目录中的所有 .md 和 .mdx 文件。

    Args:
        directory: 目录路径
        dry_run: 如果为 True，只检查不修改

    Returns:
        (处理的文件数, 修改的文件数)
    """
    dir_path = Path(directory)

    if not dir_path.exists():
        print(f"❌ 目录不存在: {directory}")
        sys.exit(1)

    if not dir_path.is_dir():
        print(f"❌ 不是目录: {directory}")
        sys.exit(1)

    total_files = 0
    modified_files = 0

    # 递归查找所有 .md 和 .mdx 文件
    for pattern in ['**/*.md', '**/*.mdx']:
        for file_path in dir_path.glob(pattern):
            total_files += 1

            if process_file(file_path, dry_run):
                modified_files += 1
                action = "将删除" if dry_run else "已删除"
                print(f"  ✅ {action} articleID: {file_path.relative_to(dir_path)}")

    return total_files, modified_files


def main():
    if len(sys.argv) < 2:
        print("用法: python remove_article_id.py <目录路径> [--dry-run]")
        print("")
        print("选项:")
        print("  --dry-run    只检查，不实际修改文件")
        print("")
        print("示例:")
        print("  python remove_article_id.py ./docs")
        print("  python remove_article_id.py ./docs --dry-run")
        sys.exit(1)

    directory = sys.argv[1]
    dry_run = '--dry-run' in sys.argv

    if dry_run:
        print(f"🔍 预览模式: 检查目录 {directory}")
    else:
        print(f"🔧 处理目录: {directory}")

    print("-" * 50)

    total, modified = process_directory(directory, dry_run)

    print("-" * 50)
    print(f"📊 统计: 共扫描 {total} 个文件，{'发现' if dry_run else '修改了'} {modified} 个包含 articleID 的文件")

    if dry_run and modified > 0:
        print("")
        print("💡 提示: 去掉 --dry-run 参数以实际执行修改")


if __name__ == '__main__':
    main()
