import re
import os
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple

def get_cell_content(cell) -> str:
    """处理单元格内容，保留HTML标签"""
    # 将cell内容转换为字符串，保留HTML标签
    content = str(cell)
    
    # 移除td或th标签
    content = re.sub(r'^<t[dh][^>]*>', '', content)
    content = re.sub(r'</t[dh]>$', '', content)
    
    return content.strip()

def process_table(html_content: str) -> str:
    """处理HTML表格并转换为Markdown格式"""
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')
    if not table:
        return ""

    # 收集所有行和层级信息
    rows_data = []
    for tr in table.find_all('tr'):
        level = tr.get('data-row-level', '1')
        is_child = tr.get('data-row-child', 'false') == 'true'
        cells = tr.find_all(['th', 'td'])
        
        # 处理单元格内容，保留HTML标签
        row_data = []
        for cell in cells:
            text = get_cell_content(cell)
            row_data.append(text)
            
        rows_data.append((level, is_child, row_data))

    if not rows_data:
        return ""

    # 分析表格结构，找出需要拆分的子表
    main_table_rows = []
    sub_tables: Dict[str, List[List[str]]] = {}
    
    # 处理主表内容
    header = rows_data[0][2]  # 获取表头
    main_table_rows.append(header)
    
    # 处理所有行
    prev_parent = None
    for i, (level, is_child, row_data) in enumerate(rows_data[1:]):  # 跳过表头
        # 确保 row_data 的长度与表头相同
        while len(row_data) < len(header):
            row_data.append("")
            
        # 检查是否是多级level（例如"5-1-1"）
        level_parts = level.split('-')
        
        if len(level_parts) == 1:  # 一级参数
            if is_child:  # 有子表
                prev_parent = row_data[0]
                main_table_rows.append(row_data)
            else:
                main_table_rows.append(row_data)
                prev_parent = None
        elif len(level_parts) == 2:  # 二级参数
            if prev_parent:  # 如果有前置父参数，使用└标识
                if is_child:  # 如果自己也是父参数，需要创建子表
                    # 保留原始描述，去掉末尾的句号，并添加跳转链接
                    original_desc = row_data[2].rstrip('。')
                    new_row = row_data.copy()
                    new_row[0] = f"└ {row_data[0]}"
                    new_row[2] = f"{original_desc}，详情可见[{row_data[0]}](#{row_data[0]})。"
                    main_table_rows.append(new_row)
                    # 创建子表，使用相同的表头
                    sub_tables[row_data[0]] = [header]
                else:
                    # 没有子表，保持原样
                    new_row = row_data.copy()
                    new_row[0] = f"└ {row_data[0]}"
                    main_table_rows.append(new_row)
            else:
                main_table_rows.append(row_data)
        else:  # 三级参数
            # 找到对应的子表
            parent_name = None
            for row in reversed(main_table_rows):
                if row[0].startswith('└ '):
                    parent_name = row[0].replace('└ ', '')
                    break
            
            if parent_name and parent_name in sub_tables:
                # 添加到子表
                sub_tables[parent_name].append(row_data)

    # 生成Markdown格式输出
    output = []
    
    # 生成主表
    output.append(f"| {' | '.join(header)} |")
    output.append("|" + "|".join(["---" for _ in header]) + "|")
    for row in main_table_rows[1:]:  # 跳过表头
        output.append(f"| {' | '.join(row)} |")
    output.append("")

    # 生成子表
    for table_name, rows in sub_tables.items():
        output.append(f"##### {table_name}")
        output.append(f"| {' | '.join(rows[0])} |")  # 使用原始表头
        output.append("|" + "|".join(["---" for _ in rows[0]]) + "|")
        for row in rows[1:]:  # 跳过表头
            output.append(f"| {' | '.join(row)} |")
        output.append("")

    return "\n".join(output)

def convert_file(input_file: str, output_file: str):
    """转换整个文件中的表格"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 查找所有表格
        table_pattern = r'<table.*?</table>'
        tables = re.finditer(table_pattern, content, re.DOTALL)
        
        new_content = content
        for table in tables:
            table_html = table.group(0)
            # 检查是否是多级表格
            if 'data-row-level' in table_html:
                markdown_table = process_table(table_html)
                new_content = new_content.replace(table_html, markdown_table)

        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"成功转换文件: {input_file}")
    except Exception as e:
        print(f"处理文件 {input_file} 时出错: {str(e)}")

def process_directory(input_dir: str):
    """处理目录下的所有.mdx文件"""
    # 获取所有.mdx文件
    mdx_files = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.mdx'):
                mdx_files.append(os.path.join(root, file))
    
    if not mdx_files:
        print(f"在目录 {input_dir} 中没有找到.mdx文件")
        return
    
    print(f"找到 {len(mdx_files)} 个.mdx文件")
    
    # 处理每个文件
    for file_path in mdx_files:
        # 输出文件路径与输入文件相同
        convert_file(file_path, file_path)

def main():
    """主函数"""
    print("表格转换工具")
    print("-" * 20)
    
    while True:
        print("\n请选择操作模式：")
        print("1. 处理单个文件")
        print("2. 处理整个目录")
        print("3. 退出")
        
        choice = input("请输入选项（1-3）: ").strip()
        
        if choice == "1":
            input_file = input("请输入源文件路径: ").strip()
            output_file = input("请输入目标文件路径: ").strip()
            if os.path.exists(input_file):
                convert_file(input_file, output_file)
            else:
                print("源文件不存在！")
        
        elif choice == "2":
            input_dir = input("请输入要处理的目录路径: ").strip()
            if os.path.isdir(input_dir):
                process_directory(input_dir)
            else:
                print("目录不存在！")
        
        elif choice == "3":
            print("程序退出")
            break
        
        else:
            print("无效的选项，请重新选择")

if __name__ == '__main__':
    main()