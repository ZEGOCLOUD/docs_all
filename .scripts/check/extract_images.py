#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
import sys
import urllib.request
import urllib.parse
from pathlib import Path

def find_md_mdx_files(directory):
    """递归查找所有md/mdx文件"""
    md_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md') or file.endswith('.mdx'):
                md_files.append(os.path.join(root, file))
    return md_files

def extract_images_from_file(file_path):
    """从文件中提取所有图片链接"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f'读取文件失败 {file_path}: {e}', file=sys.stderr)
        return []

    image_urls = []

    # 1. 提取 Markdown 格式的图片: ![alt](url)
    md_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    for match in re.finditer(md_pattern, content):
        url = match.group(2)
        image_urls.append(url)

    # 2. 提取 HTML img 标签: <img src="url" />
    # 支持多种格式：<img src="..." />、<img src="...">、<img src='...' />等
    img_pattern = r'<img[^>]*src\s*=\s*["\']([^"\']+)["\'][^>]*/?>'
    for match in re.finditer(img_pattern, content, re.IGNORECASE):
        url = match.group(1)
        image_urls.append(url)

    return image_urls

def download_image(url, output_dir, mdx_filename_prefix=''):
    """下载图片到指定目录

    Args:
        url: 图片URL
        output_dir: 输出目录
        mdx_filename_prefix: mdx文件名前缀（不含扩展名）
    """
    try:
        # 解析 URL，获取文件名
        parsed_url = urllib.parse.urlparse(url)

        # 如果是相对路径，跳过
        if not parsed_url.scheme:
            print(f'  跳过相对路径: {url}', file=sys.stderr)
            return False

        # 从 URL 中提取文件名
        original_filename = os.path.basename(parsed_url.path)
        if not original_filename:
            # 如果没有文件名，使用 URL 的 hash 作为文件名
            original_filename = f'image_{hash(url)}.png'

        # 添加 mdx 文件名前缀
        if mdx_filename_prefix:
            filename = f'{mdx_filename_prefix}_{original_filename}'
        else:
            filename = original_filename

        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)

        # 完整的输出路径
        output_path = os.path.join(output_dir, filename)

        # 如果文件已存在，跳过
        if os.path.exists(output_path):
            print(f'  已存在: {filename}', file=sys.stderr)
            return True

        # 下载图片，添加 referer 头
        print(f'  下载: {url} -> {filename}', file=sys.stderr)

        # 创建请求对象，添加 referer 头
        req = urllib.request.Request(
            url,
            headers={
                'Referer': 'https://doc-zh.zego.im',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
        )

        # 下载文件
        with urllib.request.urlopen(req) as response:
            with open(output_path, 'wb') as out_file:
                out_file.write(response.read())

        return True

    except Exception as e:
        print(f'  下载失败 {url}: {e}', file=sys.stderr)
        return False

def main():
    if len(sys.argv) < 2:
        print('用法: python extract_images.py <目录路径>')
        print('示例: python extract_images.py general/en/faq')
        sys.exit(1)

    target_dir = sys.argv[1]

    if not os.path.isdir(target_dir):
        print(f'错误: 目录不存在: {target_dir}', file=sys.stderr)
        sys.exit(1)

    # 查找所有 md/mdx 文件
    md_files = find_md_mdx_files(target_dir)
    print(f'找到 {len(md_files)} 个 md/mdx 文件', file=sys.stderr)

    # 提取所有图片，保持与来源文件的关联
    # 格式: [(url, mdx_file_path), ...]
    all_images_with_source = []
    all_image_urls = []

    for file_path in md_files:
        urls = extract_images_from_file(file_path)
        for url in urls:
            all_images_with_source.append((url, file_path))
            all_image_urls.append(url)

    print(f'共提取 {len(all_image_urls)} 个图片链接', file=sys.stderr)
    print()  # 空行分隔

    # 输出 JSON 列表
    print(json.dumps(all_image_urls, ensure_ascii=False, indent=2))

    # 下载图片
    print('\n开始下载图片...', file=sys.stderr)

    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, 'images')

    print(f'图片将保存到: {images_dir}', file=sys.stderr)

    success_count = 0
    fail_count = 0
    skip_count = 0

    for i, (url, source_file) in enumerate(all_images_with_source, 1):
        print(f'\n[{i}/{len(all_images_with_source)}]', file=sys.stderr)

        # 获取 mdx 文件名（不含扩展名）作为前缀
        mdx_basename = os.path.basename(source_file)
        mdx_filename_prefix = os.path.splitext(mdx_basename)[0]

        print(f'  来源文件: {mdx_basename}', file=sys.stderr)

        # 如果是相对路径，计数后跳过
        parsed_url = urllib.parse.urlparse(url)
        if not parsed_url.scheme:
            skip_count += 1
            print(f'  跳过相对路径: {url}', file=sys.stderr)
            continue

        # 检查文件是否已存在
        original_filename = os.path.basename(parsed_url.path)
        if not original_filename:
            original_filename = f'image_{hash(url)}.png'
        filename = f'{mdx_filename_prefix}_{original_filename}'
        output_path = os.path.join(images_dir, filename)

        if os.path.exists(output_path):
            success_count += 1
            print(f'  已存在: {filename}', file=sys.stderr)
            continue

        # 下载
        if download_image(url, images_dir, mdx_filename_prefix):
            success_count += 1
        else:
            fail_count += 1

    # 输出统计
    print(f'\n=== 下载完成 ===', file=sys.stderr)
    print(f'成功: {success_count}', file=sys.stderr)
    print(f'失败: {fail_count}', file=sys.stderr)
    print(f'跳过: {skip_count}', file=sys.stderr)
    print(f'总计: {len(all_images_with_source)}', file=sys.stderr)

if __name__ == '__main__':
    main()

