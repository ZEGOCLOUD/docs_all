# 请帮我写一个无效链接检查python脚本check_links.py。功能要求如下：
# 0. 检查中英文文档中的链接是否有混
# 1. 能检查本地链接是否有效
# 2. 检查通过网站根路径访问的链接是否有效
# 3. 能检查远端链接是否能访问

# 中英文链接是否混淆说明：
# - 在脚本执行前给选项询问用户是英文还是中文
# - 在中文文档中，绝对不能出现二级域名为zegocloud.com的链接
# - 在英文文档中，绝对不能出现二级域名为zego.im的链接

# 本地链接检查说明：
# 示例：./../API%20reference/Agent%20Instance%20Management/Update%20Agent%20instance.mdx

# - 这种是通过相对路径访问的本地链接，路径层级计算从引用该链接所在文件位置计算。
# - 这种路径一定是./或者../开头，且URL经过编码，且以.mdx结尾
# 只要能在对应路径找到链接对应的.mdx文件，就说说明该链接有效

# 通过根路径访问的链接是否有效说明：
# 示例：/aiagent-server/quick-start
# 这个链接分为两部分，第一部分为routeBasePath，这里对应的是aiagent-server(实际也可能是多级的，比如en/aiagent-server)。它可以通过读取docuo.config.zh.json或docuo.config.en.json(根据选择得语言决定)的instances列表项的routeBasePath比较得出结论
# 第二部分为文件id，在匹配到routeBasePath的节点还有一个path属性，它从仓库根目录开始计算，它表示这个routeBasePath对应的所有子链接实际mdx文件存储的文件夹。文件id就是从该path目录下的完整路径做转换后得来得。转换规则为：把路径转为全小写，空格转为横杠(-)然后删除.mdx后缀。比如Quick Start.mdx就会被转成quick-start。
# 判断是否有效：只要在对应routeBasePath得path目录下存在文件按规则转换后得文件id对得上，那么就是有效得

# 检查远端网站是否有效：
# 除了二级域名为zego.im或者zegocloud.com外得域名都是外链。发起网络请求，如果不是返回404那么就证明能访问。

# 该脚本检查后要做一个总结，列出有问题得链接内容，如下：
# - 问题类型（比如：中文混英文链接）
# - 所在文件路径及行号（在vscode终端执行后点击文件路径能跳转打开到指定行）
# - 按问题分类进行分类输出


# 脚本在运行前先询问检查哪个实例下的链接。实例根据选择的语言从docuo.config.zh.json或docuo.config.en.json文件中的instances列表读取（按名字归类排序）

import os
import re
import json
import sys
import urllib.parse
import requests
import subprocess
from collections import defaultdict

# 终端彩色输出
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Dummy:
        def __getattr__(self, name):
            return ''
    Fore = Style = Dummy()

def choose_language():
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

def choose_check_remote():
    print('\n是否检查外链？')
    print('1. 是（耗时较长）')
    print('2. 否（仅检查内部链接）')
    choice = input('输入数字选择(1/2)，直接回车默认不检查: ').strip()
    return choice == '1'

def get_repo_root():
    """获取仓库根目录路径"""
    # 从脚本所在目录向上查找，直到找到包含docuo.config.*.json的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while current_dir != os.path.dirname(current_dir):  # 直到根目录
        if any(f.startswith('docuo.config.') and f.endswith('.json')
               for f in os.listdir(current_dir)):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    return None

def get_git_changed_files():
    """获取git变更的md/mdx文件"""
    try:
        # 获取待提交的文件
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=AM'],
            capture_output=True,
            text=True,
            check=True
        )
        changed_files = result.stdout.strip().split('\n') if result.stdout.strip() else []

        # 过滤出md/mdx文件
        md_files = [f for f in changed_files if f.lower().endswith(('.md', '.mdx'))]
        return md_files
    except subprocess.CalledProcessError:
        print(f'{Fore.RED}获取git变更文件失败，请确保在git仓库中运行{Style.RESET_ALL}')
        return []

def find_instances_for_files(files, config, repo_root):
    """根据文件路径找到对应的实例"""
    instances_map = {}
    instances = config.get('instances', [])

    for file_path in files:
        for instance in instances:
            instance_path = instance.get('path', '')
            instance_id = instance.get('id', '')

            # 检查文件路径是否以实例的path开头
            if instance_path and file_path.startswith(instance_path):
                if instance_id not in instances_map:
                    instances_map[instance_id] = {
                        'instance': instance,
                        'files': []
                    }
                instances_map[instance_id]['files'].append(file_path)
                break  # 找到匹配的实例后跳出循环

    return instances_map

def load_config(language):
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
    mdx_files = []
    for dirpath, _, filenames in os.walk(root_path):
        for fname in filenames:
            if fname.lower().endswith('.mdx'):
                mdx_files.append(os.path.join(dirpath, fname))
    return mdx_files

def extract_links_from_file(file_path):
    # 匹配多种类型的链接
    # 1. markdown链接: [xxx](url)
    markdown_pattern = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
    # 2. 纯文本链接: http://xxx 或 https://xxx
    url_pattern = re.compile(r'https?://[^\s\'"<>()]+')
    # 3. MDX导入语句: import xxx from 'path' 或 import xxx from "path" 或 import { xxx } from 'path'
    mdx_import_pattern = re.compile(r'import\s+(?:{[^}]+}|\w+)\s+from\s+[\'"]([^\'"]+)[\'"]')

    links = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f, 1):
            line_content = line.strip()

            # 检查markdown链接
            for match in markdown_pattern.finditer(line):
                url = match.group(1).strip()
                links.append({
                    'url': url,
                    'line': idx,
                    'line_content': line_content,
                    'type': 'markdown'
                })

            # 检查纯文本链接（排除已经在markdown链接中的）
            line_without_markdown = markdown_pattern.sub('', line)
            for match in url_pattern.finditer(line_without_markdown):
                url = match.group(0).strip()
                # 移除可能的尾部标点符号
                url = url.rstrip('.,;:!?')
                links.append({
                    'url': url,
                    'line': idx,
                    'line_content': line_content,
                    'type': 'plain_text'
                })

            # 检查MDX导入语句
            for match in mdx_import_pattern.finditer(line):
                import_path = match.group(1).strip()
                # 移除开头的斜杠（如果有）
                if import_path.startswith('/'):
                    import_path = import_path[1:]
                links.append({
                    'url': import_path,
                    'line': idx,
                    'line_content': line_content,
                    'type': 'mdx_import'
                })

    return links

def check_mixed_language(link, language):
    # 检查中英文链接混用
    if language == 'zh' and re.search(r'https?://[^/]*zegocloud\.com', link):
        return True
    if language == 'en' and re.search(r'https?://(?!storage\.|rtc-api\.)[^/]*zego\.im', link):
        return True
    return False

def check_local_link(link, base_file_path):
    # 只检查以./或../开头，且以.mdx结尾的链接
    if not (link.startswith('./') or link.startswith('../')):
        return None

    # 分离链接和锚点
    if '#' in link:
        link_path, anchor = link.split('#', 1)
    else:
        link_path, anchor = link, None

    if not link_path.lower().endswith('.mdx'):
        return None

    # URL解码
    rel_path = urllib.parse.unquote(link_path)
    abs_path = os.path.normpath(os.path.join(os.path.dirname(base_file_path), rel_path))

    if not os.path.exists(abs_path):
        return False

    # 如果有锚点，检查锚点是否存在
    if anchor:
        headings = extract_headings_from_file(abs_path)
        if anchor not in headings:
            return False

    return True

def get_file_id(filename):
    # 文件名转file_id规则
    name = os.path.splitext(os.path.basename(filename))[0]
    name = name.lower().replace(' ', '-')
    return name

def extract_headings_from_file(file_path):
    """从mdx文件中提取所有标题，并转换为锚点格式"""
    headings = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 匹配markdown标题 (# ## ### #### ##### ######)
                if line.startswith('#'):
                    # 提取标题文本
                    heading_text = line.lstrip('#').strip()
                    if heading_text:
                        # 转换为锚点格式
                        anchor = heading_to_anchor(heading_text)
                        headings.append(anchor)
    except Exception:
        pass
    return headings

def heading_to_anchor(heading_text):
    """将标题文本转换为锚点格式"""
    # 对于标题中的中文字符，所有字符不变
    # 对于标题的英文字符，所有字符转小写
    # 对于标题中的空格，转成横线（-）
    result = ""
    for char in heading_text:
        if char.isspace():
            result += '-'
        elif char.isascii() and char.isalpha():
            result += char.lower()
        else:
            result += char
    return result

def check_root_link(link, config, instance, repo_root):
    # 只检查以/开头的链接
    if not link.startswith('/'):
        return None

    # 分离链接和锚点
    if '#' in link:
        link_path, anchor = link.split('#', 1)
    else:
        link_path, anchor = link, None

    # /routeBasePath/xxx
    parts = link_path[1:].split('/')
    if not parts:
        return False
    # routeBasePath可能多级
    route_bases = [inst['routeBasePath'] for inst in config['instances']]
    matched_base = None
    matched_inst = None
    for inst in config['instances']:
        base = inst['routeBasePath'].strip('/')
        base_parts = base.split('/')
        if parts[:len(base_parts)] == base_parts:
            matched_base = base
            matched_inst = inst
            break
    if not matched_base or not matched_inst:
        return False
    # 文件id
    file_id = '/'.join(parts[len(matched_base.split('/')):])
    if not file_id:
        return False
    # 路径 - 使用仓库根目录
    path_dir = matched_inst['path']
    abs_path_dir = os.path.join(repo_root, path_dir) if not os.path.isabs(path_dir) else path_dir
    abs_path_dir = os.path.normpath(abs_path_dir)
    # 遍历该目录下所有mdx文件，找file_id是否能对上
    found_file = None
    for dirpath, _, filenames in os.walk(abs_path_dir):
        for fname in filenames:
            if fname.lower().endswith('.mdx'):
                rel = os.path.relpath(os.path.join(dirpath, fname), abs_path_dir)
                rel = rel.replace('\\', '/').replace('\\', '/')
                rel_id = '/'.join([get_file_id(x) for x in rel.split('/')])
                if rel_id == file_id:
                    found_file = os.path.join(dirpath, fname)
                    break
        if found_file:
            break

    if not found_file:
        return False

    # 如果有锚点，检查锚点是否存在
    if anchor:
        headings = extract_headings_from_file(found_file)
        if anchor not in headings:
            return False

    return True

def check_remote_link(link):
    # 只检查http/https开头，且不是zego.im/zegocloud.com
    if not re.match(r'https?://', link):
        return None
    if re.search(r'https?://[^/]*zego\.im', link) or re.search(r'https?://[^/]*zegocloud\.com', link):
        return None

    # 跳过特定格式的链接
    # https://xxx-api-xxx 或 https://xxxapi.xxx 或 https://yourxxx 或 以/chat/completions结尾的链接
    if re.search(r'https?://[^/]*-api-[^/]*', link) or \
       re.search(r'https?://[^/]*api\.[^/]*', link) or \
       re.search(r'https?://your[^/]*', link) or \
       link.endswith('/chat/completions'):
        return None

    try:
        resp = requests.head(link, allow_redirects=True, timeout=5)
        if resp.status_code != 200:
            return {'valid': False, 'error': f'HTTP {resp.status_code}'}
        return {'valid': True}
    except requests.exceptions.Timeout:
        return {'valid': False, 'error': '请求超时'}
    except requests.exceptions.ConnectionError:
        return {'valid': False, 'error': '连接错误'}
    except requests.exceptions.InvalidURL:
        return {'valid': False, 'error': '无效链接'}
    except Exception as e:
        return {'valid': False, 'error': f'其他错误: {str(e)}'}

def check_mdx_import(import_path, base_file_path, repo_root):
    """检查MDX导入路径是否有效"""
    # 只检查.mdx文件
    if not import_path.lower().endswith('.mdx'):
        return None

    # 使用仓库根目录作为根目录
    full_path = os.path.join(repo_root, import_path)

    # 检查文件是否存在
    if not os.path.exists(full_path):
        return False

    return True

def check_git_mode():
    """git模式：检查变更文件对应的实例"""
    print(f'{Fore.CYAN}Git模式：检查变更文件对应的实例{Style.RESET_ALL}')

    # 获取git变更的文件
    changed_files = get_git_changed_files()
    if not changed_files:
        print(f'{Fore.YELLOW}未发现待提交的md/mdx文件变更{Style.RESET_ALL}')
        return True

    print(f'发现{len(changed_files)}个变更的md/mdx文件:')
    for f in changed_files:
        print(f'  - {f}')

    all_problems = defaultdict(list)

    # 加载主配置文件（包含所有实例）
    try:
        repo_root = get_repo_root()
        if not repo_root:
            print(f'{Fore.RED}未找到仓库根目录{Style.RESET_ALL}')
            return False

        config_file = os.path.join(repo_root, 'docuo.config.json')
        if not os.path.exists(config_file):
            print(f'{Fore.RED}未找到配置文件: {config_file}{Style.RESET_ALL}')
            return False

        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # 找到对应的实例
        instances_map = find_instances_for_files(changed_files, config, repo_root)
        if not instances_map:
            print(f'{Fore.YELLOW}变更的文件未匹配到任何实例{Style.RESET_ALL}')
            return True

        print(f'\n匹配到{len(instances_map)}个实例需要检查:')

        for instance_id, instance_info in instances_map.items():
            instance = instance_info['instance']
            files = instance_info['files']

            # 获取实例语言
            instance_locale = instance.get('locale', 'en')  # 默认为英文

            instance_label = instance.get("label", "未知实例")
            platform = instance.get("navigationInfo", {}).get("platform", "")
            display_name = f"{instance_label} ({platform})" if platform else instance_label

            print(f'\n正在检查实例: {display_name} [语言: {instance_locale}]')
            print(f'变更文件: {", ".join(files)}')

            # 检查该实例下的所有文件（不仅仅是变更的文件）
            instance_path = instance['path']
            if not os.path.isabs(instance_path):
                instance_path = os.path.join(repo_root, instance_path)

            # 跳过外部链接实例
            if instance_path.startswith('http'):
                print(f'跳过外部链接实例: {instance_path}')
                continue

            mdx_files = find_mdx_files(instance_path)
            print(f'实例共有{len(mdx_files)}个mdx文件')

            problems = check_instance_links(mdx_files, config, instance, repo_root, check_remote=True)

            # 合并问题
            for ptype, items in problems.items():
                all_problems[ptype].extend(items)

    except Exception as e:
        print(f'{Fore.RED}加载配置失败: {e}{Style.RESET_ALL}')
        return False

    # 输出总结
    print_problems_summary(all_problems, is_warning=True)

    # git模式只输出警告，不返回失败
    return True

def check_instance_links(mdx_files, config, instance, repo_root, check_remote=False):
    """检查实例中的链接"""
    problems = defaultdict(list)

    for file_path in mdx_files:
        links = extract_links_from_file(file_path)
        for link_info in links:
            url = link_info['url']
            line = link_info['line']
            line_content = link_info['line_content']
            link_type = link_info['type']

            # 检查MDX导入
            if link_type == 'mdx_import':
                mdx_result = check_mdx_import(url, file_path, repo_root)
                if mdx_result is False:
                    problems['MDX导入路径无效'].append({
                        'file': file_path,
                        'line': line,
                        'url': url,
                        'line_content': line_content,
                        'link_type': link_type
                    })
                continue

            # 1. 检查中英文链接混用
            instance_locale = instance.get('locale', 'en')  # 默认为英文
            if check_mixed_language(url, instance_locale):
                problems['中英文链接混用'].append({
                    'file': file_path,
                    'line': line,
                    'url': url,
                    'line_content': line_content,
                    'link_type': link_type
                })
                continue
            # 2. 检查本地链接
            local_result = check_local_link(url, file_path)
            if local_result is False:
                problems['本地链接无效'].append({
                    'file': file_path,
                    'line': line,
                    'url': url,
                    'line_content': line_content,
                    'link_type': link_type
                })
                continue
            elif local_result is True:
                continue
            # 3. 检查根路径链接
            root_result = check_root_link(url, config, instance, repo_root)
            if root_result is False:
                problems['根路径链接无效'].append({
                    'file': file_path,
                    'line': line,
                    'url': url,
                    'line_content': line_content,
                    'link_type': link_type
                })
                continue
            elif root_result is True:
                continue
            # 4. 检查远端链接（如果用户选择检查）
            if check_remote:
                remote_result = check_remote_link(url)
                if remote_result is not None and not remote_result.get('valid', True):
                    error_msg = remote_result.get('error', '未知错误')
                    problems['远端链接无效'].append({
                        'file': file_path,
                        'line': line,
                        'url': url,
                        'line_content': line_content,
                        'link_type': link_type,
                        'error': error_msg
                    })
                    continue

    return problems

def print_problems_summary(problems, is_warning=False):
    """打印问题总结"""
    prefix = "⚠️  警告" if is_warning else "❌ 错误"

    if not problems:
        print(f'{Fore.GREEN}未发现任何问题链接！{Style.RESET_ALL}')
        return

    for ptype, items in problems.items():
        print(f'\n{Fore.YELLOW}{prefix} - {ptype}（共{len(items)}个）:{Style.RESET_ALL}')
        for item in items:
            # vscode终端可点击跳转格式: "file_path":line (用引号包围路径以支持空格)
            link_type = item.get('link_type', 'unknown')
            type_display = f"[{link_type}]" if link_type != 'unknown' else ""
            error_msg = item.get('error', '')
            error_display = f" - {error_msg}" if error_msg else ""
            print(f'  "{item["file"]}":{item["line"]}')
            print(f'    {type_display} {item["url"]}{error_display}')
            print(f'    {item["line_content"]}')
            print()

def main():
    # 检查是否是git模式
    if len(sys.argv) > 1 and sys.argv[1] == 'git':
        # git模式：检查变更文件对应的实例
        return check_git_mode()

    # 交互模式
    language = choose_language()
    check_remote = choose_check_remote()
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
    print(f'正在检查实例: {display_name} ({instance_path})')
    mdx_files = find_mdx_files(instance_path)
    print(f'共找到{len(mdx_files)}个mdx文件。')

    problems = check_instance_links(mdx_files, config, instance, repo_root, check_remote)

    # 输出总结
    print('\n检查结果总结:')
    print_problems_summary(problems)

if __name__ == '__main__':
    main()