#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FAQ文件分析工具

用途:
    分析FAQ目录下的mdx文件,将其分为"简单"和"复杂"两类,
    帮助决定哪些文件可以合并到一个统一的simple-qa.mdx文件中。

判断标准:
1. 简单文件(建议合并)的标准:
    - 文件大小 ≤ 500字节
    - 实际内容行数 ≤ 10行
    - 不包含代码块(```开头的代码)
    - 不包含图片(![或<img)
    - 不包含表格(|---)
    - 不包含复杂HTML标签(除了<br/>和<hr/>)
    - 不包含多个链接([...](...)格式)
    - 通常只包含一个简单的问题和答案

2. 复杂文件(建议独立)的标准:
    - 超过以上任一限制
    - 包含代码示例
    - 包含图片说明
    - 包含表格数据
    - 包含复杂格式化内容
    - 包含多个相关链接
    - 包含多个子问题或章节
"""

import os
import re
from collections import defaultdict

class FAQAnalyzer:
    def __init__(self, directory):
        self.directory = directory
        # 定义简单文件的判断标准
        self.SIMPLE_FILE_CRITERIA = {
            'max_lines': 10,  # 最大行数
            'max_size': 500,  # 最大文件大小(字节)
        }
        
    def is_simple_content(self, content, file_size):
        """判断内容是否为简单内容"""
        # 去除空行后计算实际行数
        non_empty_lines = [line for line in content.split('\n') if line.strip()]
        
        # 检查是否包含复杂元素
        has_code = bool(re.search(r'```[a-zA-Z]*\n', content))
        has_image = '![' in content or '<img' in content
        has_table = '|---' in content or '| ---' in content
        has_complex_format = bool(re.search(r'<(?!\/|br|hr)[a-zA-Z]+[^>]*>', content))
        has_multiple_links = len(re.findall(r'\[.*?\]\(.*?\)', content)) > 1
        
        # 判断是否为简单文件
        is_simple = all([
            len(non_empty_lines) <= self.SIMPLE_FILE_CRITERIA['max_lines'],
            file_size <= self.SIMPLE_FILE_CRITERIA['max_size'],
            not has_code,
            not has_image,
            not has_table,
            not has_complex_format,
            not has_multiple_links
        ])
        
        return {
            'is_simple': is_simple,
            'metrics': {
                'lines': len(non_empty_lines),
                'has_code': has_code,
                'has_image': has_image,
                'has_table': has_table,
                'has_complex_format': has_complex_format,
                'has_multiple_links': has_multiple_links
            }
        }

    def analyze_files(self):
        """分析目录下的所有 MDX 文件"""
        simple_files = []
        complex_files = []
        stats = defaultdict(int)
        
        # 遍历目录下的所有 mdx 文件
        for filename in os.listdir(self.directory):
            if not filename.endswith('.mdx'):
                continue
                
            filepath = os.path.join(self.directory, filename)
            file_size = os.path.getsize(filepath)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # 分析文件内容
                analysis = self.is_simple_content(content, file_size)
                
                # 提取文件标题
                title = self.extract_title(content)
                
                file_info = {
                    'name': filename,
                    'size': file_size,
                    'title': title,
                    **analysis['metrics']
                }
                
                if analysis['is_simple']:
                    simple_files.append(file_info)
                    stats['simple_files'] += 1
                else:
                    complex_files.append(file_info)
                    stats['complex_files'] += 1
                    
                stats['total_files'] += 1
                    
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {str(e)}")
                
        return simple_files, complex_files, stats
    
    def extract_title(self, content):
        """提取文件中的标题"""
        # 尝试匹配 # 开头的标题
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            return title_match.group(1)
        # 如果没有找到标题,返回 None
        return None

    def generate_report(self):
        """生成分析报告"""
        simple_files, complex_files, stats = self.analyze_files()
        
        report = []
        report.append("=== FAQ 文件分析报告 ===\n")
        report.append(f"总文件数: {stats['total_files']}")
        report.append(f"简单文件数: {stats['simple_files']}")
        report.append(f"复杂文件数: {stats['complex_files']}\n")
        
        report.append("=== 建议合并的简单文件 ===")
        report.append("以下文件建议合并到 simple-qa.mdx 中:")
        for file in sorted(simple_files, key=lambda x: x['size']):
            title_info = f"(标题: {file['title']})" if file['title'] else ""
            report.append(f"- {file['name']:<30} {title_info}")
            report.append(f"  大小: {file['size']} 字节, 行数: {file['lines']}")
        
        report.append("\n=== 建议保持独立的复杂文件 ===")
        report.append("以下文件建议保持独立:")
        for file in sorted(complex_files, key=lambda x: x['size'], reverse=True):
            features = []
            if file['has_code']: features.append('包含代码')
            if file['has_image']: features.append('包含图片')
            if file['has_table']: features.append('包含表格')
            if file['has_complex_format']: features.append('包含复杂格式')
            if file['has_multiple_links']: features.append('包含多个链接')
            features_str = '、'.join(features) if features else '内容较多'
            
            title_info = f"(标题: {file['title']})" if file['title'] else ""
            report.append(f"- {file['name']:<30} {title_info}")
            report.append(f"  大小: {file['size']} 字节, 行数: {file['lines']}, 特点: {features_str}")
        
        return '\n'.join(report)

def main():
    faq_dir = "/Users/zego/Documents/docs_all/general/zh/faq/faq-doc-zh"
    analyzer = FAQAnalyzer(faq_dir)
    report = analyzer.generate_report()
    print(report)
    
    # 将报告保存到文件
    report_path = os.path.join(os.path.dirname(faq_dir), 'faq_analysis_report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n报告已保存到: {report_path}")

if __name__ == "__main__":
    main()