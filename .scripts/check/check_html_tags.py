#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML元素闭合检查脚本

功能说明：
- 检查MDX文件中的HTML元素是否正确配对闭合
- 支持嵌套元素、自闭合元素、跨行元素等
- 自动过滤代码块中的内容和编程语言泛型语法
- 支持常见的HTML标签和MDX组件

检查类型：
1. 未闭合的标签 - 开放标签没有对应的闭合标签
2. 多余的闭合标签 - 闭合标签没有对应的开放标签
3. 标签嵌套错误 - 标签闭合顺序不正确
4. 自闭合标签错误闭合 - 自闭合标签不应该有闭合标签（如 </br>）
5. 自闭合标签格式错误 - 自闭合标签应该以 /> 结尾（如 <br> 应该写成 <br/>）

使用方法：
python3 .scripts/check/check_html_tags.py

然后按提示选择语言、组和实例即可开始检查。
"""

import os
import re
import json
import sys
from collections import defaultdict, deque

# 终端彩色输出
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Dummy:
        def __getattr__(self, name):
            return ''
    Fore = Style = Dummy()

# 自闭合标签列表（HTML标准 + 常见的MDX组件）
SELF_CLOSING_TAGS = {
    # HTML标准自闭合标签
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 
    'link', 'meta', 'param', 'source', 'track', 'wbr',
    # 常见的MDX组件自闭合标签
    'Video', 'Image', 'Icon', 'Divider', 'Spacer'
}

def choose_language():
    """选择文档语言"""
    while True:
        print('请选择文档语言:')
        print('1. 中文')
        print('2. 英文')
        choice = input('输入数字选择(1/2): ').strip()
        if choice == '1':
            return 'zh'
        elif choice == '2':
            return 'en'
        else:
            print('输入无效，请重新输入。')

def get_repo_root():
    """获取仓库根目录路径"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while current_dir != os.path.dirname(current_dir):
        if any(f.startswith('docuo.config.') and f.endswith('.json')
               for f in os.listdir(current_dir)):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    return None

def load_config(language):
    """加载配置文件"""
    repo_root = get_repo_root()
    if not repo_root:
        print(f'{Fore.RED}未找到仓库根目录（包含docuo.config.*.json的目录）{Style.RESET_ALL}')
        sys.exit(1)

    config_file = os.path.join(repo_root, f'docuo.config.{language}.json')
    if not os.path.exists(config_file):
        print(f'{Fore.RED}未找到配置文件: {config_file}{Style.RESET_ALL}')
        sys.exit(1)
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config, repo_root

def choose_instance(instances):
    """选择要检查的实例"""
    # 按组分类实例
    groups = {}
    for inst in instances:
        group_id = inst.get("navigationInfo", {}).get("group", {}).get("id", "未分组")
        group_name = inst.get("navigationInfo", {}).get("group", {}).get("name", "未分组")
        if group_id not in groups:
            groups[group_id] = {
                "name": group_name,
                "instances": []
            }
        groups[group_id]["instances"].append(inst)

    # 显示组列表
    print('请选择要检查的组:')
    sorted_groups = sorted(groups.items(), key=lambda x: x[1]["name"])
    for idx, (group_id, group_info) in enumerate(sorted_groups, 1):
        print(f'{idx}. {group_info["name"]}')

    # 选择组
    while True:
        group_choice = input('输入数字选择组: ').strip()
        if group_choice.isdigit() and 1 <= int(group_choice) <= len(sorted_groups):
            selected_group = sorted_groups[int(group_choice)-1][1]
            break
        else:
            print('输入无效，请重新输入。')

    # 显示选中组下的实例列表
    print(f'\n请选择 {selected_group["name"]} 下的实例:')
    sorted_instances = sorted(selected_group["instances"], key=lambda x: x.get("label", ""))
    for idx, inst in enumerate(sorted_instances, 1):
        label = inst.get("label", "(无名实例)")
        platform = inst.get("navigationInfo", {}).get("platform", "")
        if platform:
            display_name = f"{label} ({platform})"
        else:
            display_name = label
        print(f'{idx}. {display_name}')

    # 选择实例
    while True:
        instance_choice = input('输入数字选择实例: ').strip()
        if instance_choice.isdigit() and 1 <= int(instance_choice) <= len(sorted_instances):
            return sorted_instances[int(instance_choice)-1]
        else:
            print('输入无效，请重新输入。')

def find_mdx_files(root_path):
    """查找所有MDX文件"""
    mdx_files = []
    for dirpath, _, filenames in os.walk(root_path):
        for fname in filenames:
            if fname.lower().endswith('.mdx'):
                mdx_files.append(os.path.join(dirpath, fname))
    return mdx_files

class HTMLTag:
    """HTML标签类"""
    def __init__(self, name, line_num, col_num, is_opening=True, is_self_closing=False):
        self.name = name.lower()
        self.line_num = line_num
        self.col_num = col_num
        self.is_opening = is_opening
        self.is_self_closing = is_self_closing
    
    def __repr__(self):
        tag_type = "self-closing" if self.is_self_closing else ("opening" if self.is_opening else "closing")
        return f"<{self.name} {tag_type} at {self.line_num}:{self.col_num}>"

def is_likely_html_tag(tag_name, line_content, match_start, match_end):
    """判断是否可能是HTML标签而不是代码中的泛型语法"""
    tag_name_lower = tag_name.lower()

    # 常见的HTML标签和MDX组件
    html_tags = {
        'div', 'span', 'p', 'a', 'img', 'br', 'hr', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'ul', 'ol', 'li', 'table', 'tr', 'td', 'th', 'thead', 'tbody', 'tfoot',
        'form', 'input', 'button', 'select', 'option', 'textarea', 'label',
        'header', 'footer', 'nav', 'section', 'article', 'aside', 'main',
        'video', 'audio', 'source', 'track', 'canvas', 'svg', 'path',
        # 常见的MDX组件
        'note', 'warning', 'tip', 'info', 'danger', 'success',
        'tabs', 'tab', 'steps', 'step', 'codegroup', 'code',
        'accordion', 'accordionitem', 'callout', 'card', 'cardgroup',
        'image', 'video', 'audio', 'embed', 'iframe'
    }

    # 如果是已知的HTML标签，很可能是HTML标签
    if tag_name_lower in html_tags:
        return True

    # 常见的编程语言泛型类型
    generic_types = {
        'any', 'string', 'number', 'boolean', 'object', 'array', 'void', 'null', 'undefined',
        'int', 'float', 'double', 'char', 'bool', 'long', 'short', 'byte',
        'list', 'map', 'set', 'vector', 'queue', 'stack', 'pair',
        'promise', 'future', 'optional', 'result', 'either',
        # 常见的类名模式
        't', 'k', 'v', 'e', 'r'
    }

    # 如果是常见的泛型类型，很可能不是HTML标签
    if tag_name_lower in generic_types:
        return False

    # 检查上下文：如果在代码块中，更可能是泛型
    # 简单检查：如果前面有 : 或 < 或者后面紧跟 > 且没有空格，可能是泛型
    before_tag = line_content[:match_start].strip()
    after_tag = line_content[match_end:].strip()

    # 检查是否在代码上下文中
    if (before_tag.endswith(':') or before_tag.endswith('<') or
        after_tag.startswith('>') or '(' in before_tag[-10:] or ')' in after_tag[:10]):
        return False

    # 如果标签名看起来像类名（首字母大写），可能是MDX组件
    if tag_name[0].isupper():
        return True

    # 默认情况下，如果不确定，倾向于认为是HTML标签
    return True

def extract_html_tags(content):
    """从内容中提取所有HTML标签"""
    tags = []
    lines = content.split('\n')
    in_code_block = False

    # 匹配HTML标签的正则表达式
    # 支持: <tag>, <tag attr="value">, </tag>, <tag/>, <tag attr="value"/>
    tag_pattern = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)[^>]*?(/?)>', re.IGNORECASE)

    for line_num, line in enumerate(lines, 1):
        # 检查是否在代码块中
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue

        # 如果在代码块中，跳过这一行
        if in_code_block:
            continue

        for match in tag_pattern.finditer(line):
            is_closing = bool(match.group(1))  # 是否是闭合标签 </tag>
            tag_name = match.group(2)
            has_slash_end = bool(match.group(3))  # 是否以 /> 结尾
            col_num = match.start() + 1

            # 判断是否可能是HTML标签
            if not is_likely_html_tag(tag_name, line, match.start(), match.end()):
                continue

            # 检查自闭合标签的情况
            if tag_name.lower() in SELF_CLOSING_TAGS:
                if is_closing:
                    # 错误：自闭合标签不应该有闭合标签（如 </br>）
                    tags.append(HTMLTag(tag_name, line_num, col_num, is_opening=False, is_self_closing=True))
                    continue
                elif has_slash_end:
                    # 正确：自闭合标签以 /> 结尾（如 <br/>）
                    continue
                else:
                    # 问题：自闭合标签没有以 /> 结尾（如 <br>）
                    # 这种情况应该被标记为需要修正
                    tags.append(HTMLTag(tag_name, line_num, col_num, is_opening=True, is_self_closing=False))
                    continue

            # 普通标签处理
            if has_slash_end and not is_closing:
                # 普通标签以 /> 结尾，跳过（如 <div/>，虽然不常见但有效）
                continue

            tags.append(HTMLTag(tag_name, line_num, col_num, is_opening=not is_closing))

    return tags

def check_html_tags_balance(tags):
    """检查HTML标签是否平衡配对"""
    problems = []
    stack = deque()  # 用栈来跟踪开放的标签

    for tag in tags:
        if tag.is_self_closing and not tag.is_opening:
            # 错误：自闭合标签不应该有闭合标签
            problems.append({
                'type': '自闭合标签错误闭合',
                'tag': tag,
                'message': f'自闭合标签 <{tag.name}> 不应该有闭合标签 </{tag.name}>'
            })
            continue

        # 检查自闭合标签是否缺少斜杠
        if tag.is_opening and tag.name.lower() in SELF_CLOSING_TAGS:
            problems.append({
                'type': '自闭合标签格式错误',
                'tag': tag,
                'message': f'自闭合标签 <{tag.name}> 应该写成 <{tag.name}/> 的形式'
            })
            continue

        if tag.is_opening:
            # 开放标签，压入栈
            stack.append(tag)
        else:
            # 闭合标签
            if not stack:
                # 栈为空，说明没有对应的开放标签
                problems.append({
                    'type': '多余的闭合标签',
                    'tag': tag,
                    'message': f'找不到与 </{tag.name}> 匹配的开放标签'
                })
                continue

            # 检查是否与栈顶标签匹配
            last_opening = stack[-1]
            if last_opening.name == tag.name:
                # 匹配，弹出栈顶
                stack.pop()
            else:
                # 不匹配，可能是嵌套错误
                # 查找栈中是否有匹配的标签
                found_match = False
                temp_stack = []

                while stack:
                    temp_tag = stack.pop()
                    temp_stack.append(temp_tag)
                    if temp_tag.name == tag.name:
                        found_match = True
                        break

                if found_match:
                    # 找到匹配的标签，但中间有未闭合的标签
                    for unclosed_tag in reversed(temp_stack[:-1]):
                        problems.append({
                            'type': '标签嵌套错误',
                            'tag': unclosed_tag,
                            'message': f'标签 <{unclosed_tag.name}> 在 </{tag.name}> 之前未正确闭合'
                        })
                        stack.append(unclosed_tag)  # 重新放回栈中
                else:
                    # 没找到匹配的标签
                    problems.append({
                        'type': '多余的闭合标签',
                        'tag': tag,
                        'message': f'找不到与 </{tag.name}> 匹配的开放标签'
                    })
                    # 将临时栈中的标签放回原栈
                    for temp_tag in reversed(temp_stack):
                        stack.append(temp_tag)

    # 检查栈中剩余的未闭合标签
    while stack:
        unclosed_tag = stack.pop()
        problems.append({
            'type': '未闭合的标签',
            'tag': unclosed_tag,
            'message': f'标签 <{unclosed_tag.name}> 未找到对应的闭合标签'
        })

    return problems

def check_file_html_tags(file_path):
    """检查单个文件的HTML标签"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        tags = extract_html_tags(content)
        problems = check_html_tags_balance(tags)

        return problems
    except Exception as e:
        return [{
            'type': '文件读取错误',
            'tag': None,
            'message': f'无法读取文件: {str(e)}'
        }]

def get_line_content(file_path, line_num):
    """获取指定行的内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if 1 <= line_num <= len(lines):
                return lines[line_num - 1].strip()
    except:
        pass
    return ""

def check_files_from_command_line(file_paths):
    """从命令行参数检查指定的文件"""
    has_problems = False

    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f'{Fore.RED}文件不存在: {file_path}{Style.RESET_ALL}')
            continue

        # 获取绝对路径
        abs_file_path = os.path.abspath(file_path)
        problems = check_file_html_tags(file_path)

        if problems:
            has_problems = True
            print(f'{Fore.RED}❌ 文件 {abs_file_path} 发现HTML标签问题:{Style.RESET_ALL}')

            for problem in problems:
                if problem['tag']:
                    tag = problem['tag']
                    line_content = get_line_content(file_path, tag.line_num)
                    print(f'  {abs_file_path}:{tag.line_num} - {problem["message"]}')
                    if line_content:
                        print(f'    行内容: {line_content}')
                else:
                    print(f'  {abs_file_path} - {problem["message"]}')
            print("")

    if has_problems:
        print(f'{Fore.RED}❌ 发现HTML标签问题，请修复后再提交！{Style.RESET_ALL}')
        return False
    else:
        print(f'{Fore.GREEN}✅ 所有Markdown文件的HTML标签检查通过{Style.RESET_ALL}')
        return True

def main():
    """主函数"""
    # 检查是否有命令行参数指定文件
    if len(sys.argv) > 1:
        # 命令行模式：检查指定的文件
        file_paths = sys.argv[1:]
        success = check_files_from_command_line(file_paths)
        sys.exit(0 if success else 1)

    # 交互模式：原有的交互式检查逻辑
    print(f'{Fore.CYAN}HTML元素闭合检查脚本{Style.RESET_ALL}')
    print('=' * 50)

    language = choose_language()
    config, repo_root = load_config(language)
    instances = config.get('instances', [])

    if not instances:
        print(f'{Fore.RED}未找到任何实例，请检查配置文件。{Style.RESET_ALL}')
        sys.exit(1)

    instance = choose_instance(instances)
    instance_path = instance['path']

    # 确保实例路径是绝对路径
    if not os.path.isabs(instance_path):
        instance_path = os.path.join(repo_root, instance_path)

    instance_label = instance.get("label", "未知实例")
    platform = instance.get("navigationInfo", {}).get("platform", "")
    if platform:
        display_name = f"{instance_label} ({platform})"
    else:
        display_name = instance_label

    print(f'\n正在检查实例: {display_name}')
    print(f'路径: {instance_path}')

    mdx_files = find_mdx_files(instance_path)
    print(f'共找到 {len(mdx_files)} 个MDX文件。')

    if not mdx_files:
        print(f'{Fore.YELLOW}未找到任何MDX文件。{Style.RESET_ALL}')
        return

    print('\n开始检查HTML标签...')

    all_problems = defaultdict(list)
    total_files_with_problems = 0

    for i, file_path in enumerate(mdx_files, 1):
        print(f'\r检查进度: {i}/{len(mdx_files)} ({i/len(mdx_files)*100:.1f}%)', end='', flush=True)

        problems = check_file_html_tags(file_path)

        if problems:
            total_files_with_problems += 1
            for problem in problems:
                problem['file'] = file_path
                if problem['tag']:
                    problem['line_content'] = get_line_content(file_path, problem['tag'].line_num)
                all_problems[problem['type']].append(problem)

    print('\n\n检查完成！')
    print('=' * 50)

    # 输出结果
    if not all_problems:
        print(f'{Fore.GREEN}✅ 未发现任何HTML标签问题！{Style.RESET_ALL}')
        return

    print(f'{Fore.RED}发现问题总结:{Style.RESET_ALL}')
    print(f'问题文件数: {total_files_with_problems}')
    print(f'问题总数: {sum(len(problems) for problems in all_problems.values())}')

    for problem_type, problems in all_problems.items():
        print(f'\n{Fore.YELLOW}{problem_type} (共 {len(problems)} 个):{Style.RESET_ALL}')

        for problem in problems:
            if problem['tag']:
                tag = problem['tag']
                print(f'  "{problem["file"]}":{tag.line_num}')
                print(f'    {problem["message"]}')
                if problem.get('line_content'):
                    print(f'    行内容: {problem["line_content"]}')
            else:
                print(f'  "{problem["file"]}": {problem["message"]}')
            print()

if __name__ == '__main__':
    main()
