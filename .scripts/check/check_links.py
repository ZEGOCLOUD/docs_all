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
import argparse
import urllib.parse
import requests
import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path

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
        choice = input('输入数字选择(1/2)，直接回车默认 1: ').strip()
        if choice == '':
            choice = '1'
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

def load_whitelist():
    """加载链接白名单"""
    script_dir = Path(__file__).parent
    whitelist_file = script_dir / 'link_whitelist.json'

    if not whitelist_file.exists():
        # 如果白名单文件不存在，创建一个空的白名单文件
        default_whitelist = {
            "urls": [],  # 完整URL白名单
            "patterns": []  # URL模式白名单（支持正则表达式）
        }
        whitelist_file.write_text(json.dumps(default_whitelist, indent=2, ensure_ascii=False), encoding='utf-8')
        return default_whitelist

    try:
        return json.loads(whitelist_file.read_text(encoding='utf-8'))
    except Exception as e:
        print(f'{Fore.YELLOW}警告：无法加载白名单文件：{e}{Style.RESET_ALL}')
        return {"urls": [], "patterns": []}

def is_url_whitelisted(url, whitelist):
    """检查URL是否在白名单中"""
    # 检查完整URL匹配
    if url in whitelist.get('urls', []):
        return True

    # 检查正则表达式模式匹配
    for pattern in whitelist.get('patterns', []):
        try:
            if re.search(pattern, url):
                return True
        except re.error:
            continue

    return False

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

def _load_json_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def load_config(language):
    repo_root = get_repo_root()
    if not repo_root:
        print(f'{Fore.RED}未找到仓库根目录（包含docuo.config.*.json 的目录）{Style.RESET_ALL}')
        sys.exit(1)

    # 优先按语言加载 docuo.config.{zh|en}.json；若不存在再回退到 docuo.config.json
    lang_path = os.path.join(repo_root, f'docuo.config.{language}.json')
    main_path = os.path.join(repo_root, 'docuo.config.json')

    config = None
    if os.path.exists(lang_path):
        config = _load_json_file(lang_path)
    elif os.path.exists(main_path):
        config = _load_json_file(main_path)
    else:
        # 兼容场景：如果只存在另一种语言的文件，尝试加载
        alt_lang = 'en' if language == 'zh' else 'zh'
        alt_lang_path = os.path.join(repo_root, f'docuo.config.{alt_lang}.json')
        config = _load_json_file(alt_lang_path)

    if not config:
        print(f'{Fore.RED}未找到配置文件: {main_path} 或 {lang_path}{Style.RESET_ALL}')
        sys.exit(1)
    return config, repo_root

def build_instance_platform_map(config):
    """从 themeConfig.instanceGroups 构建 instance_id -> platform 的映射"""
    instance_platform_map = {}
    instance_groups = config.get("themeConfig", {}).get("instanceGroups", [])
    for group in instance_groups:
        for inst_ref in group.get("instances", []):
            inst_id = inst_ref.get("id", "")
            platform = inst_ref.get("platform", "")
            if inst_id:
                instance_platform_map[inst_id] = platform
    return instance_platform_map


def get_instance_platform(instance, config):
    """获取实例的 platform 信息

    优先从 instance._platform 获取（如果已附加），
    否则从 themeConfig.instanceGroups 中查找
    """
    # 如果已经附加了 _platform，直接返回
    if "_platform" in instance:
        return instance.get("_platform", "")

    # 否则从 instanceGroups 中查找
    inst_id = instance.get("id", "")
    instance_groups = config.get("themeConfig", {}).get("instanceGroups", [])
    for group in instance_groups:
        for inst_ref in group.get("instances", []):
            if inst_ref.get("id") == inst_id:
                return inst_ref.get("platform", "")
    return ""


def build_instance_groups_map(config):
    """从 themeConfig.instanceGroups 构建实例分组映射

    返回:
        groups: dict, key 为 group_id, value 为 {"name": ..., "instance_ids": [...]}
        instance_platform_map: dict, key 为 instance_id, value 为 platform
    """
    groups = {}
    instance_platform_map = {}

    instance_groups = config.get("themeConfig", {}).get("instanceGroups", [])
    for group in instance_groups:
        group_id = group.get("id", "未分组")
        group_name = group.get("name", "未分组")
        if group_id not in groups:
            groups[group_id] = {
                "name": group_name,
                "instance_ids": []
            }
        for inst_ref in group.get("instances", []):
            inst_id = inst_ref.get("id", "")
            platform = inst_ref.get("platform", "")
            if inst_id:
                groups[group_id]["instance_ids"].append(inst_id)
                instance_platform_map[inst_id] = platform

    return groups, instance_platform_map


def choose_instance(instances, config):
    """选择要检查的实例

    Args:
        instances: 顶层 instances 列表
        config: 完整配置对象
    """
    # 从 themeConfig.instanceGroups 构建分组映射
    groups_map, instance_platform_map = build_instance_groups_map(config)

    # 构建 instance_id -> instance 的映射
    instances_by_id = {inst.get("id"): inst for inst in instances}

    # 按组分类实例（使用 instanceGroups 中的顺序）
    groups = {}
    for group_id, group_info in groups_map.items():
        group_instances = []
        for inst_id in group_info["instance_ids"]:
            if inst_id in instances_by_id:
                inst = instances_by_id[inst_id]
                # 附加 platform 信息
                inst["_platform"] = instance_platform_map.get(inst_id, "")
                group_instances.append(inst)
        if group_instances:
            groups[group_id] = {
                "name": group_info["name"],
                "instances": group_instances
            }

    if not groups:
        print('未找到任何分组，将显示所有实例。')
        return instances

    # 显示组列表
    print('请选择要检查的组:')
    # 按在 instanceGroups 中出现的顺序排列
    ordered_groups = list(groups.items())
    for idx, (group_id, group_info) in enumerate(ordered_groups, 1):
        print(f'{idx}. {group_info["name"]}')

    # 选择组
    while True:
        group_choice = input('输入数字选择组: ').strip()
        if group_choice.isdigit() and 1 <= int(group_choice) <= len(ordered_groups):
            selected_group = ordered_groups[int(group_choice)-1][1]
            break
        else:
            print('输入无效，请重新输入。')

    # 显示选中组下的实例列表
    print(f'\n请选择 {selected_group["name"]} 下的实例:')
    print('0. 选择所有')
    sorted_instances = sorted(selected_group["instances"], key=lambda x: x.get("label", ""))
    for idx, inst in enumerate(sorted_instances, 1):
        label = inst.get("label", "(无名实例)")
        platform = inst.get("_platform", "")
        if platform:
            display_name = f"{label} ({platform})"
        else:
            display_name = label
        print(f'{idx}. {display_name}')

    # 选择实例（回车默认选择所有=0）
    while True:
        instance_choice = input('输入数字选择实例 (0=所有)，直接回车默认 0: ').strip()
        if instance_choice == '':
            instance_choice = '0'
        if instance_choice == '0':
            return sorted_instances  # 返回所有实例
        elif instance_choice.isdigit() and 1 <= int(instance_choice) <= len(sorted_instances):
            return [sorted_instances[int(instance_choice)-1]]  # 返回单个实例的列表
        else:
            print('输入无效，请重新输入。')

def find_mdx_files(root_path):
    mdx_files = []
    for dirpath, _, filenames in os.walk(root_path):
        for fname in filenames:
            if fname.lower().endswith('.mdx'):
                mdx_files.append(os.path.join(dirpath, fname))
    return mdx_files

def remove_paramfield_attrs(content):
    """移除 ParamField 组件的属性部分，保留换行结构

    ParamField 组件属性中的链接不需要检查，如：
    prototype="[ZegoRoomState](./enum#zegoroomstate)"
    """
    # 匹配 <ParamField ... > 或 <ParamField ... />
    # 正则处理属性值中可能包含 > 字符的情况
    paramfield_regex = re.compile(
        r'<ParamField\s+((?:[^>"\']+|"[^"]*"|\'[^\']*\')*?)(/?>)',
        re.DOTALL
    )

    def replace_with_newlines(match):
        # 保留属性部分中的换行符数量，以保持行号一致
        attrs = match.group(1)
        closing = match.group(2)
        newline_count = attrs.count('\n')
        return '<ParamField' + '\n' * newline_count + closing

    return paramfield_regex.sub(replace_with_newlines, content)


def extract_links_from_file(file_path):
    # 匹配多种类型的链接
    # 1. markdown链接: [xxx](url)
    markdown_pattern = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
    # 2. HTML a标签链接: <a href="url"> 或 <a href='url'>
    html_a_pattern = re.compile(r'<a[^>]*href\s*=\s*[\'"]([^\'"]+)[\'"][^>]*>')
    # 3. 纯文本链接: http://xxx 或 https://xxx
    url_pattern = re.compile(r'https?://[^\s\'"<>()`]+')
    # 4. import语句: import xxx from 'path' 或 import { xxx } from 'path'
    mdx_import_pattern = re.compile(r'import\s+(?:{[^}]+}|\w+)\s+from\s+[\'"]([^\'"]+)[\'"]')

    links = []
    in_code_block = False  # 是否在代码块内
    code_block_indent = None  # 缩进代码块的缩进级别

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 移除 ParamField 组件的属性部分（保留换行结构以保持行号一致）
    content = remove_paramfield_attrs(content)

    for idx, line in enumerate(content.split('\n'), 1):
            # 检查是否进入/退出代码块（```标记的代码块）
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue

            # 检查缩进代码块
            if not in_code_block:
                # 计算当前行的缩进
                current_indent = len(line) - len(line.lstrip())
                if line.strip():  # 非空行
                    if code_block_indent is None and current_indent >= 4:
                        # 进入缩进代码块
                        code_block_indent = current_indent
                    elif code_block_indent is not None and current_indent < 4:
                        # 退出缩进代码块
                        code_block_indent = None

            # 如果在代码块内，跳过链接检查
            if in_code_block or code_block_indent is not None:
                continue
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

            # 检查HTML a标签链接
            for match in html_a_pattern.finditer(line):
                url = match.group(1).strip()
                links.append({
                    'url': url,
                    'line': idx,
                    'line_content': line_content,
                    'type': 'html_a'
                })

            # 检查纯文本链接（排除已经在markdown链接和HTML a标签中的）
            line_without_markdown = markdown_pattern.sub('', line)
            line_without_html = html_a_pattern.sub('', line_without_markdown)
            for match in url_pattern.finditer(line_without_html):
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
    # 这些域名是中英文共用的，不计入混用
    shared_domains = [
        'artifact-sdk.zego.im',
        'artifact-demo.zego.im',
        'doc-media.zego.im',
        'site-media.zego.im',
        'storage.zego.im',
    ]

    # 英文专用的域名
    en_only_domains = [
        'doc-en-api.zego.im',
    ]

    # 中文专用的域名
    zh_only_domains = [
        'doc-zh-api.zego.im',
    ]

    # 检查是否为共用域名
    for domain in shared_domains:
        if domain in link:
            return False

    # 检查是否为语言专用域名
    if language == 'en':
        # 英文文档中，英文专用域名是允许的
        for domain in en_only_domains:
            if domain in link:
                return False
    elif language == 'zh':
        # 中文文档中，中文专用域名是允许的
        for domain in zh_only_domains:
            if domain in link:
                return False

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

    # 如果有锚点，检查锚点是否存在（大小写不敏感）
    if anchor:
        headings = extract_headings_from_file(abs_path)
        # 宽松匹配：统一小写并移除空格与短横线
        anchor_norm = _normalize_for_anchor_compare(anchor)
        headings_norm = [_normalize_for_anchor_compare(h) for h in headings]
        if anchor_norm not in headings_norm:
            # 文件存在但锚点不存在
            return 'anchor_invalid'

    return True

def check_anchor_link(link, base_file_path):
    """检查锚点链接是否有效"""
    # 只检查以#开头的链接
    if not link.startswith('#'):
        return None

    # 提取锚点（去掉#号）
    anchor = link[1:]
    if not anchor:
        return False

    # 检查当前文件中的锚点（大小写不敏感）
    headings = extract_headings_from_file(base_file_path)
    # 将锚点和标题都转换为小写进行比较
    anchor_lower = anchor.lower()
    headings_lower = [h.lower() for h in headings]
    if anchor_lower not in headings_lower:
        return False

    return True

def get_file_id(filename):
    # 文件名转file_id规则
    name = os.path.splitext(os.path.basename(filename))[0]
    name = name.lower().replace(' ', '-')
    return name

def generate_slug_for_paramfield(text):
    """将文本转为 ParamField 锚点格式：小写，移除特殊字符，空格转连字符

    与 site-template/lib/trans-api-short-link/slug.ts 中的 generateSlug 保持一致
    """
    if not text:
        return ''
    result = text.lower()
    # 移除非字母数字字符（保留空格和连字符）
    result = re.sub(r'[^\w\s-]', '', result)
    # 空格转连字符
    result = re.sub(r'\s+', '-', result)
    return result.strip()


def parse_jsx_attributes(attrs_str):
    """解析 JSX 属性字符串，提取 key="value" 或 key='value' 形式的属性"""
    result = {}
    # 匹配 key="value" 或 key='value'
    attr_regex = re.compile(r'(\w+)\s*=\s*["\']([^"\']*)["\']')
    for match in attr_regex.finditer(attrs_str):
        result[match.group(1)] = match.group(2)
    return result


def extract_anchors_from_paramfield_attrs(name, parent_name, parent_type, anchor_suffix):
    """从 ParamField 属性中提取所有可能的锚点

    与 site-template/components/mdx/api/ParamField.tsx 中的锚点生成逻辑保持一致
    """
    anchors = []

    # 1. 基础锚点名称（如有 anchor_suffix 则拼接）
    anchor_base_name = f"{name}{anchor_suffix}" if anchor_suffix else name
    primary_anchor = generate_slug_for_paramfield(anchor_base_name)
    if primary_anchor:
        anchors.append(primary_anchor)

    # 2. 带 parent_name 的锚点（所有类型，包括 enum）
    if parent_type and parent_name:
        anchors.append(generate_slug_for_paramfield(f"{anchor_base_name}-{parent_name}"))
        # 非 enum 类型还生成带 parent_type 的锚点
        if parent_type != 'enum':
            anchors.append(generate_slug_for_paramfield(f"{anchor_base_name}-{parent_name}-{parent_type}"))

    # 3. OC 冒号方法名处理（如 "createEngineWithProfile:eventHandler:"）
    if ':' in name:
        first_segment = name.split(':')[0]
        if first_segment and first_segment != name:
            colon_anchor = generate_slug_for_paramfield(first_segment)
            if colon_anchor and colon_anchor != primary_anchor and colon_anchor not in anchors:
                anchors.append(colon_anchor)
            # 同样生成带 parent_name 的变体
            if parent_type and parent_name:
                colon_with_parent = generate_slug_for_paramfield(f"{first_segment}-{parent_name}")
                if colon_with_parent not in anchors:
                    anchors.append(colon_with_parent)
                if parent_type != 'enum':
                    colon_with_parent_type = generate_slug_for_paramfield(f"{first_segment}-{parent_name}-{parent_type}")
                    if colon_with_parent_type not in anchors:
                        anchors.append(colon_with_parent_type)

    return anchors


def extract_paramfield_anchors(file_path):
    """从 MDX 文件中提取所有 ParamField 组件生成的锚点"""
    anchors = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 将内容规范化为单行处理（去除换行），因为 ParamField 可能跨多行
        normalized_content = content.replace('\r\n', ' ').replace('\n', ' ')

        # 匹配 <ParamField ... > 或 <ParamField ... />
        # 正则处理属性值中可能包含 > 字符的情况
        paramfield_regex = re.compile(r'<ParamField\s+((?:[^>"\']+|"[^"]*"|\'[^\']*\')*?)(?:/>|>)')

        for match in paramfield_regex.finditer(normalized_content):
            attrs_str = match.group(1)
            attrs = parse_jsx_attributes(attrs_str)

            name = attrs.get('name', '')
            if not name:
                continue

            parent_name = attrs.get('parent_name', '')
            parent_type = attrs.get('parent_type', '')
            anchor_suffix = attrs.get('anchor_suffix', '')

            field_anchors = extract_anchors_from_paramfield_attrs(
                name, parent_name, parent_type, anchor_suffix
            )
            anchors.extend(field_anchors)

    except Exception:
        pass

    return anchors


def _is_heading_title_size(title_size):
    """判断 titleSize 是否会生成 heading 锚点（h1~h5）"""
    return bool(re.match(r'^h[1-5]$', title_size, re.IGNORECASE))


def extract_steps_anchors(content):
    """提取 Steps/Step 组件生成的锚点。

    优先级规则：
    - Step 自己的 titleSize 优先；未设置时继承 Steps 的 titleSize。
    - 有效值为 h1~h5，才会生成 heading 锚点。
    - 两者都未设置，或有效值非 h1~h5（如 p），则不生成锚点。
    """
    anchors = []

    # 将内容规范化为单行，方便正则跨行匹配
    normalized = content.replace('\r\n', ' ').replace('\n', ' ')

    # 与 ParamField 使用相同的属性匹配模式：<Tag attrs...>body</Tag>
    steps_block_pattern = re.compile(
        r'<Steps\s+((?:[^>"\']+|"[^"]*"|\'[^\']*\')*?)>(.*?)</Steps>'
    )
    # Steps 无属性的情况（仅有 > 直接闭合）
    steps_noattr_pattern = re.compile(
        r'<Steps\s*>(.*?)</Steps>'
    )
    step_pattern = re.compile(
        r'<Step\s+((?:[^>"\']+|"[^"]*"|\'[^\']*\')*?)(?:/>|>)'
    )

    def _process_steps_body(steps_title_size, steps_body):
        for step_match in step_pattern.finditer(steps_body):
            step_attrs = parse_jsx_attributes(step_match.group(1))
            # Step 自己的 titleSize 优先，未设置则继承 Steps 的
            effective = step_attrs.get('titleSize', '') or steps_title_size
            if not _is_heading_title_size(effective):
                continue
            title = step_attrs.get('title', '')
            if title:
                anchor = heading_to_anchor(title)
                if anchor:
                    anchors.append(anchor)
                    anchors.append(f"{anchor}-1")

    # 匹配有属性的 <Steps ...>
    for m in steps_block_pattern.finditer(normalized):
        steps_attrs = parse_jsx_attributes(m.group(1))
        _process_steps_body(steps_attrs.get('titleSize', ''), m.group(2))

    # 匹配无属性的 <Steps>（Step 可能有自己的 titleSize）
    for m in steps_noattr_pattern.finditer(normalized):
        _process_steps_body('', m.group(1))

    return anchors


def extract_headings_from_file(file_path):
    """从mdx文件中提取所有锚点（标题 + ParamField 组件），并转换为锚点格式"""
    headings = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 处理MDX导入：如果文件包含import Content from语句，则递归处理导入的文件
        import_pattern = re.compile(r'import\s+\w+\s+from\s+[\'"]([^\'"]+\.mdx)[\'"]')
        for match in import_pattern.finditer(content):
            import_path = match.group(1)
            # 处理相对路径
            if import_path.startswith('/'):
                # 绝对路径，从仓库根目录开始
                repo_root = get_repo_root()
                if repo_root:
                    imported_file_path = os.path.join(repo_root, import_path.lstrip('/'))
                else:
                    continue
            else:
                # 相对路径
                imported_file_path = os.path.normpath(os.path.join(os.path.dirname(file_path), import_path))

            if os.path.exists(imported_file_path):
                # 递归提取导入文件的标题
                imported_headings = extract_headings_from_file(imported_file_path)
                headings.extend(imported_headings)

        # 1. 匹配markdown标题 (# ## ### #### ##### ######)
        heading_counts = {}  # 用于跟踪重复标题
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('#'):
                # 提取标题文本
                heading_text = line.lstrip('#').strip()
                if heading_text:
                    # 转换为锚点格式
                    anchor = heading_to_anchor(heading_text)

                    # 处理重复标题，添加数字后缀
                    if anchor in heading_counts:
                        heading_counts[anchor] += 1
                        anchor_with_suffix = f"{anchor}-{heading_counts[anchor]}"
                        headings.append(anchor_with_suffix)
                    else:
                        heading_counts[anchor] = 0
                        headings.append(anchor)
                        # 同时添加带-1后缀的版本（某些系统从-1开始）
                        headings.append(f"{anchor}-1")


        # 2. 匹配任意HTML标签的id属性
        # 支持多种格式：<any id="anchor"></any>、<any id='anchor'></any>、<any id="anchor"/>等
        tag_id_pattern = re.compile(r'<[^>]+id\s*=\s*[\'"]([^\'"]+)[\'"][^>]*/?>', re.IGNORECASE)
        for match in tag_id_pattern.finditer(content):
            anchor_id = match.group(1).strip()
            if anchor_id:
                headings.append(anchor_id)

        # 3. 提取 ParamField 组件生成的锚点
        paramfield_anchors = extract_paramfield_anchors(file_path)
        headings.extend(paramfield_anchors)

        # 4. 提取 Steps/Step 组件生成的锚点（当 titleSize 为 h1~h5 时）
        steps_anchors = extract_steps_anchors(content)
        headings.extend(steps_anchors)

    except Exception:
        pass
    return headings

def heading_to_anchor(heading_text):
    """将标题文本转换为锚点格式

    规则：
    - 忽略冒号（: 与 ：）。
    - 忽略括号字符本身（() 与 （）），但保留括号内的文字。
    - 忽略斜杠（/ 与 \）。
    - 忽略逗号（, 与 ，）。
    - 保留开头的数字（如"1 "、"2 "等），但删除点号。
    - 空白转换为连字符（-）。
    - ASCII 英文字母转小写；中文及其他字符保持。
    """
    # 1) 删除冒号（半角与全角）
    cleaned = heading_text
    cleaned = cleaned.replace(":", "").replace("：", "")

    # 2) 删除括号字符但保留其中内容
    cleaned = cleaned.replace("(", "").replace(")", "")
    cleaned = cleaned.replace("（", "").replace("）", "")

    # 3) 删除斜杠
    cleaned = cleaned.replace("/", "").replace("\\", "")

    # 4) 删除逗号和顿号（半角与全角）
    cleaned = cleaned.replace(",", "").replace("，", "").replace("、", "")

    # 5) 删除开头的点号，但保留数字
    cleaned = re.sub(r'^(\d+)\.\s*', r'\1 ', cleaned.strip())

    # 6) 转换其他规则
    result = ""
    for char in cleaned:
        if char.isspace():
            # 空白转换为连字符
            result += "-"
        elif char.isascii() and char.isalpha():
            result += char.lower()
        else:
            result += char

    # 7) 清理多余的连字符
    # 去除开头和结尾的连字符，并将连续的连字符合并为一个
    result = re.sub(r'-+', '-', result)  # 合并连续连字符
    result = result.strip('-')  # 去除首尾连字符

    return result

def _normalize_for_anchor_compare(value: str) -> str:
    """用于宽松匹配锚点：统一小写，并移除空格、短横线、冒号、斜杠、逗号等。

    解决例如“rtc-推流” 与 “rtc推流”的匹配问题。
    """
    if not isinstance(value, str):
        return ''
    lowered = value.lower()
    # 去除空格、半角短横线、冒号、括号、斜杠、逗号等
    normalized = lowered.replace(' ', '').replace('-', '').replace(':', '').replace('：', '')
    normalized = normalized.replace('(', '').replace(')', '').replace('（', '').replace('）', '')
    normalized = normalized.replace('/', '').replace('\\', '')
    normalized = normalized.replace(',', '').replace('，', '').replace('、', '')
    # 去除开头的数字和点号（用于宽松匹配）
    normalized = re.sub(r'^[\d\.\s]*', '', normalized)
    return normalized

def check_root_link(link, config, instance, repo_root):
    """检查站内根路径链接是否有效

    支持跨实例链接检查，链接格式：/routeBasePath/file-path
    例如：/console/service-configuration-2/activate-cdn-service
    """
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

    # 在所有实例中查找匹配的routeBasePath（支持跨实例链接）
    matched_base = None
    matched_instances = []

    # 先尝试精确匹配，再尝试前缀匹配
    for inst in config['instances']:
        base = inst['routeBasePath'].strip('/')
        if not base:  # 跳过空的routeBasePath
            continue

        base_parts = base.split('/')
        # 检查链接是否以这个routeBasePath开头
        if len(parts) >= len(base_parts) and parts[:len(base_parts)] == base_parts:
            # 如果找到更长的匹配，替换之前的匹配
            if not matched_base or len(base_parts) > len(matched_base.split('/')):
                matched_base = base
                matched_instances = [inst]
            elif matched_base and len(base_parts) == len(matched_base.split('/')):
                # 同样长度的匹配，添加到列表中（处理复用情况）
                matched_instances.append(inst)

        # 如果精确匹配失败，尝试后缀匹配（处理ZIM等情况）
        # 例如：链接 /zim-android/... 匹配配置 zh/zim-android
        elif len(base_parts) > 1:
            # 取routeBasePath的最后几个部分进行匹配
            for i in range(1, len(base_parts)):
                suffix_parts = base_parts[i:]
                if len(parts) >= len(suffix_parts) and parts[:len(suffix_parts)] == suffix_parts:
                    # 如果找到更长的匹配，替换之前的匹配
                    if not matched_base or len(suffix_parts) > len(matched_base.split('/')[-len(suffix_parts):]):
                        matched_base = base
                        matched_instances = [inst]
                    elif matched_base and len(suffix_parts) == len(matched_base.split('/')[-len(suffix_parts):]):
                        # 同样长度的匹配，添加到列表中
                        matched_instances.append(inst)
                    break

    if not matched_base or not matched_instances:
        return False

    # 提取文件id（去掉routeBasePath部分）
    base_parts = matched_base.split('/')

    # 确定实际匹配的部分长度
    matched_length = len(base_parts)
    # 检查是否是后缀匹配
    if len(parts) >= len(base_parts) and parts[:len(base_parts)] == base_parts:
        # 精确匹配
        matched_length = len(base_parts)
    else:
        # 后缀匹配，找到实际匹配的长度
        for i in range(1, len(base_parts)):
            suffix_parts = base_parts[i:]
            if len(parts) >= len(suffix_parts) and parts[:len(suffix_parts)] == suffix_parts:
                matched_length = len(suffix_parts)
                break

    file_id_parts = parts[matched_length:]
    if not file_id_parts:
        # 如果没有文件id，可能是访问实例根路径，检查是否有index文件
        file_id = 'index'
    else:
        file_id = '/'.join(file_id_parts)

    # 在所有匹配的实例路径下查找文件（处理复用情况）
    found_file = None
    for matched_inst in matched_instances:
        path_dir = matched_inst['path']
        abs_path_dir = os.path.join(repo_root, path_dir) if not os.path.isabs(path_dir) else path_dir
        abs_path_dir = os.path.normpath(abs_path_dir)

        # 遍历该目录下所有mdx文件，找file_id是否能对上
        for dirpath, _, filenames in os.walk(abs_path_dir):
            for fname in filenames:
                if fname.lower().endswith('.mdx'):
                    # 获取文件的完整相对路径
                    full_path = os.path.join(dirpath, fname)
                    rel = os.path.relpath(full_path, abs_path_dir)
                    rel = rel.replace('\\', '/')

                    # 去掉.mdx后缀
                    rel_without_ext = os.path.splitext(rel)[0]

                    # 将路径转换为文件ID格式：小写+连接线
                    rel_id = '/'.join(part.lower().replace(' ', '-') for part in rel_without_ext.split('/'))

                    # 同时生成不带连字符的版本进行匹配
                    rel_id_no_dash = '/'.join(part.lower().replace(' ', '').replace('-', '') for part in rel_without_ext.split('/'))
                    file_id_no_dash = file_id.lower().replace('-', '').replace(' ', '')

                    if rel_id == file_id or rel_id_no_dash == file_id_no_dash:
                        found_file = full_path
                        break
            if found_file:
                break
        if found_file:
            break

    if not found_file:
        return False

    # 如果有锚点，检查锚点是否存在（大小写不敏感）
    if anchor:
        headings = extract_headings_from_file(found_file)
        # 宽松匹配：统一小写并移除空格与短横线
        anchor_norm = _normalize_for_anchor_compare(anchor)
        headings_norm = [_normalize_for_anchor_compare(h) for h in headings]
        if anchor_norm not in headings_norm:
            # 路径存在但锚点不存在
            return 'anchor_invalid'

    return True

def check_remote_link(link):
    # 只检查http/https开头，且不是zego.im/zegocloud.com
    if not re.match(r'https?://', link):
        return None
    if re.search(r'https?://[^/]*zego\.im', link) or re.search(r'https?://[^/]*zegocloud\.com', link):
        return None

    # old-doc 链接不发起请求
    if is_old_doc_url_any(link):
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
    # 处理相对路径（./或../开头）
    if import_path.startswith('./') or import_path.startswith('../'):
        # 相对于当前文件所在目录
        full_path = os.path.normpath(os.path.join(os.path.dirname(base_file_path), import_path))
    else:
        # 绝对路径（以/开头）或其他情况，相对于仓库根目录
        if import_path.startswith('/'):
            import_path = import_path[1:]
        full_path = os.path.join(repo_root, import_path)

    # 1) 明确以某个扩展名结尾：要求存在对应文件
    if import_path.lower().endswith(('.mdx', '.md', '.jsx', '.js', '.ts', '.tsx')):
        return os.path.isfile(full_path)

    # 2) 可能是省略扩展名的文件：尝试多种扩展名
    for ext in ['.mdx', '.jsx', '.js', '.ts', '.tsx']:
        candidate_file = full_path + ext
        if os.path.isfile(candidate_file):
            return True

    # 3) 可能是目录写法：尝试目录下的 index.mdx 或 index.jsx
    if os.path.isdir(full_path):
        for index_name in ['index.mdx', 'index.jsx', 'index.js', 'index.ts', 'index.tsx']:
            index_file = os.path.join(full_path, index_name)
            if os.path.isfile(index_file):
                return True
        return False

    # 4) 既不是文件也不是目录
    return False


def is_old_doc_url_any(url):
    """判断是否为旧文档链接（不区分实例语言）"""
    if not isinstance(url, str):
        return False
    # 包含 api?doc 的链接不计入 old-doc
    if 'api?doc' in url.lower():
        return False
    # 中文旧文档
    if url.startswith('https://doc-zh.zego.im/article'):
        return True
    # 英文旧文档
    old_en_prefixes = [
        'https://www.zegocloud.com/docs/video-call',
        'https://www.zegocloud.com/docs/voice-call',
        'https://www.zegocloud.com/docs/live-streaming',
        'https://www.zegocloud.com/docs/admin-console',
    ]
    return any(url.startswith(p) for p in old_en_prefixes)

def _load_all_instances_config(repo_root):
    """合并 en / zh / main 的 instances，用于 git 模式跨实例检查。"""
    merged = {'instances': []}
    paths = [
        os.path.join(repo_root, 'docuo.config.json'),
        os.path.join(repo_root, 'docuo.config.en.json'),
        os.path.join(repo_root, 'docuo.config.zh.json'),
    ]
    seen = set()
    for p in paths:
        if not os.path.exists(p):
            continue
        obj = _load_json_file(p) or {}
        for inst in obj.get('instances', []):
            # 根据 (id, path) 去重，避免重复合并
            key = (inst.get('id'), inst.get('path'))
            if key in seen:
                continue
            seen.add(key)
            merged['instances'].append(inst)
    return merged

def _collect_results(problems, collected_urls, display_name, structured_results, aggregated_by_url):
    """将 check_instance_links 的结果归并到 structured_results 和 aggregated_by_url"""
    if display_name not in structured_results:
        structured_results[display_name] = {}
    for ptype, items in problems.items():
        if ptype not in structured_results[display_name]:
            structured_results[display_name][ptype] = {}
        for it in items:
            abs_file = os.path.abspath(it.get('file', ''))
            line_num = it.get('line', 0)
            entry = {
                'url': it.get('url', ''),
                'line_content': it.get('line_content', ''),
                'file_with_line': f"{abs_file}:{line_num}",
            }
            if 'error' in it:
                entry['error'] = it['error']

            if abs_file not in structured_results[display_name][ptype]:
                structured_results[display_name][ptype][abs_file] = []
            structured_results[display_name][ptype][abs_file].append(entry)

            url_key = entry.get('url')
            if url_key:
                if url_key not in aggregated_by_url:
                    aggregated_by_url[url_key] = []
                aggregated_by_url[url_key].append({
                    'instance': display_name,
                    'error_type': ptype,
                    'file_path': abs_file,
                    'file_with_line': f"{abs_file}:{line_num}",
                    'line_content': entry.get('line_content', ''),
                    **({'error': entry['error']} if 'error' in entry else {})
                })

    for it in collected_urls:
        abs_file = os.path.abspath(it.get('file', ''))
        line_num = it.get('line', 0)
        url_key = it.get('url', '')
        if url_key:
            if url_key not in aggregated_by_url:
                aggregated_by_url[url_key] = []
            aggregated_by_url[url_key].append({
                'instance': display_name,
                'error_type': 'collected',
                'file_path': abs_file,
                'file_with_line': f"{abs_file}:{line_num}",
                'line_content': it.get('line_content', ''),
            })


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

    # 结构化结果：按实例名称 -> 错误类型 -> link_type -> 列表
    structured_results = {}
    # 额外聚合：按 URL 汇总
    aggregated_by_url = {}

    # 加载主配置文件（包含所有实例）
    try:
        repo_root = get_repo_root()
        if not repo_root:
            print(f'{Fore.RED}未找到仓库根目录{Style.RESET_ALL}')
            return False

        # 合并加载全部实例配置（支持 docuo.config.json / .en.json / .zh.json）
        config = _load_all_instances_config(repo_root)
        if not config.get('instances'):
            print(f'{Fore.RED}未找到任何实例，请检查配置文件。{Style.RESET_ALL}')
            return False

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
            platform = get_instance_platform(instance, config)
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

            problems, collected_urls = check_instance_links(mdx_files, config, instance, repo_root, check_remote=True)
            _collect_results(problems, collected_urls, display_name, structured_results, aggregated_by_url)

    except Exception as e:
        print(f'{Fore.RED}加载配置失败: {e}{Style.RESET_ALL}')
        return False

    # 写入结构化结果到 JSON 和 Markdown 文件
    write_result_files(mode='git', structured_results=structured_results, aggregated_by_url=aggregated_by_url)

    # git模式只输出警告，不返回失败
    return True

def check_invalid_numeric_link(url):
    """检查是否为无效的纯数字链接"""
    # 检查是否为纯数字（可能包含空白字符）
    if url.strip().isdigit():
        return True
    return False

def check_instance_links(mdx_files, config, instance, repo_root, check_remote=False):
    """检查实例中的链接"""
    problems = defaultdict(list)
    # 额外收集：仅用于聚合统计（例如 old-doc），不计入问题
    collected_urls = []

    # 加载白名单
    whitelist = load_whitelist()

    for file_path in mdx_files:
        links = extract_links_from_file(file_path)
        for link_info in links:
            url = link_info['url']
            line = link_info['line']
            line_content = link_info['line_content']
            link_type = link_info['type']

            # 检查链接是否在白名单中
            if is_url_whitelisted(url, whitelist):
                continue

            # 检查import路径
            if link_type == 'mdx_import':
                import_result = check_mdx_import(url, file_path, repo_root)
                if import_result is False:
                    problems['Import路径无效'].append({
                        'file': file_path,
                        'line': line,
                        'url': url,
                        'line_content': line_content,
                        'link_type': link_type
                    })
                continue

            # 0. 检查无效的纯数字链接
            if check_invalid_numeric_link(url):
                problems['无效的纯数字链接'].append({
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
            # 2. 检查锚点链接
            anchor_result = check_anchor_link(url, file_path)
            if anchor_result is False:
                problems['锚点链接无效'].append({
                    'file': file_path,
                    'line': line,
                    'url': url,
                    'line_content': line_content,
                    'link_type': link_type
                })
                continue
            elif anchor_result is True:
                continue
            # 3. 检查本地链接
            local_result = check_local_link(url, file_path)
            if local_result == 'anchor_invalid':
                problems['锚点链接无效'].append({
                    'file': file_path,
                    'line': line,
                    'url': url,
                    'line_content': line_content,
                    'link_type': link_type
                })
                continue
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
            # 4. 检查根路径链接
            root_result = check_root_link(url, config, instance, repo_root)
            if root_result == 'anchor_invalid':
                problems['锚点链接无效'].append({
                    'file': file_path,
                    'line': line,
                    'url': url,
                    'line_content': line_content,
                    'link_type': link_type
                })
                continue
            if root_result is False:
                problems['internal-link无效'].append({
                    'file': file_path,
                    'line': line,
                    'url': url,
                    'line_content': line_content,
                    'link_type': link_type
                })
                continue
            elif root_result is True:
                continue
            # 5. old-doc 收集（无论是否检查外链）
            if is_old_doc_url_any(url):
                collected_urls.append({
                    'file': file_path,
                    'line': line,
                    'url': url,
                    'line_content': line_content,
                    'link_type': link_type,
                })

            # 6. 检查远端链接（如果用户选择检查；old-doc 跳过请求）
            if check_remote and not is_old_doc_url_any(url):
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

    return problems, collected_urls

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

def run_non_interactive(args):
    """CLI 非交互模式"""
    # 确定语言
    if args.zh:
        language = 'zh'
    elif args.en:
        language = 'en'
    else:
        language = 'zh'  # 默认中文

    check_remote = args.remote
    config, repo_root = load_config(language)

    structured_results = {}
    aggregated_by_url = {}

    if args.file:
        # 单文件模式
        file_path = args.file
        if not os.path.isabs(file_path):
            file_path = os.path.join(repo_root, file_path)
        file_path = os.path.normpath(file_path)

        if not os.path.isfile(file_path):
            print(f'{Fore.RED}文件不存在: {file_path}{Style.RESET_ALL}')
            sys.exit(1)

        # 尝试找到对应实例（用于 locale 等上下文）
        rel_path = os.path.relpath(file_path, repo_root)
        instances_map = find_instances_for_files([rel_path], config, repo_root)
        if instances_map:
            instance = list(instances_map.values())[0]['instance']
        else:
            instance = {'locale': language}

        display_name = f"[文件] {os.path.relpath(file_path, repo_root)}"
        print(f'\n正在检查文件: {file_path}')

        problems, collected_urls = check_instance_links([file_path], config, instance, repo_root, check_remote)
        _collect_results(problems, collected_urls, display_name, structured_results, aggregated_by_url)

    elif args.instance:
        # 实例 ID 模式
        instances = config.get('instances', [])
        matched = [i for i in instances if i.get('id') == args.instance]
        if not matched:
            print(f'{Fore.RED}未找到实例ID: {args.instance}{Style.RESET_ALL}')
            avail = ', '.join(i.get('id', '') for i in instances if i.get('id'))
            print(f'可用实例ID:\n  {avail}')
            sys.exit(1)

        instance = matched[0]
        instance_path = instance['path']
        if not os.path.isabs(instance_path):
            instance_path = os.path.join(repo_root, instance_path)

        platform = get_instance_platform(instance, config)
        label = instance.get('label', '未知实例')
        display_name = f"{label} ({platform})" if platform else label

        print(f'\n正在检查实例: {display_name} ({instance_path})')

        if instance_path.startswith('http'):
            print(f'跳过外部链接实例: {instance_path}')
            sys.exit(0)

        mdx_files = find_mdx_files(instance_path)
        print(f'共找到{len(mdx_files)}个mdx文件。')

        problems, collected_urls = check_instance_links(mdx_files, config, instance, repo_root, check_remote)
        _collect_results(problems, collected_urls, display_name, structured_results, aggregated_by_url)

    elif args.instance_path:
        # 实例路径模式：直接指定实例目录，从配置中匹配对应实例
        inst_path = args.instance_path
        if not os.path.isabs(inst_path):
            inst_path = os.path.join(repo_root, inst_path)
        inst_path = os.path.normpath(inst_path)

        if not os.path.isdir(inst_path):
            print(f'{Fore.RED}路径不存在或不是目录: {inst_path}{Style.RESET_ALL}')
            sys.exit(1)

        # 从配置中找到 path 匹配的实例（用于上下文信息）
        instances = config.get('instances', [])
        instance = None
        for inst in instances:
            p = inst.get('path', '')
            if not os.path.isabs(p):
                p = os.path.normpath(os.path.join(repo_root, p))
            if p == inst_path:
                instance = inst
                break

        if instance:
            platform = get_instance_platform(instance, config)
            label = instance.get('label', '未知实例')
            display_name = f"{label} ({platform})" if platform else label
        else:
            display_name = os.path.basename(inst_path)

        print(f'\n正在检查实例路径: {inst_path}')

        mdx_files = find_mdx_files(inst_path)
        print(f'共找到{len(mdx_files)}个mdx文件。')

        problems, collected_urls = check_instance_links(mdx_files, config, instance, repo_root, check_remote)
        _collect_results(problems, collected_urls, display_name, structured_results, aggregated_by_url)

    else:
        print(f'{Fore.RED}请指定 --file <路径>、--instance <ID> 或 --instance-path <目录路径>{Style.RESET_ALL}')
        sys.exit(1)

    write_result_files(mode='cli', structured_results=structured_results, language=language,
                       check_remote=check_remote, aggregated_by_url=aggregated_by_url)


def main():
    # git 模式
    if len(sys.argv) > 1 and sys.argv[1] == 'git':
        return check_git_mode()

    # 解析 CLI 参数
    parser = argparse.ArgumentParser(
        description='检查文档链接有效性',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''\
示例:
  # 检查单个文件（相对根目录路径）
  python check_links.py --zh --file core_products/rtc/zh/android-java/intro.mdx
  # 检查单个文件（绝对路径）
  python check_links.py --file /abs/path/to/file.mdx
  # 检查整个实例
  python check_links.py --zh --instance rtc-android-java
  # 同时检查外链
  python check_links.py --zh --instance rtc-android-java --remote
  # 无参数进入交互模式
  python check_links.py
''')
    lang_group = parser.add_mutually_exclusive_group()
    lang_group.add_argument('--zh', action='store_true', help='使用中文配置（默认）')
    lang_group.add_argument('--en', action='store_true', help='使用英文配置')
    parser.add_argument('--instance', metavar='ID', help='要检查的实例ID')
    parser.add_argument('--instance-path', metavar='DIR', dest='instance_path', help='要检查的实例目录路径（相对根目录或绝对路径）')
    parser.add_argument('--file', metavar='PATH', help='要检查的单个文件路径（相对根目录或绝对路径）')
    parser.add_argument('--remote', action='store_true', help='同时检查外链（耗时较长）')

    # 有参数时进入非交互模式
    if len(sys.argv) > 1:
        args = parser.parse_args()
        return run_non_interactive(args)

    # 无参数：交互模式
    language = choose_language()
    check_remote = choose_check_remote()
    config, repo_root = load_config(language)
    instances = config.get('instances', [])
    if not instances:
        print(f'{Fore.RED}未找到任何实例，请检查配置文件。{Style.RESET_ALL}')
        sys.exit(1)
    selected_instances = choose_instance(instances, config)

    structured_results = {}
    aggregated_by_url = {}

    for instance in selected_instances:
        instance_path = instance['path']
        if not os.path.isabs(instance_path):
            instance_path = os.path.join(repo_root, instance_path)
        instance_label = instance.get("label", "未知实例")
        platform = get_instance_platform(instance, config)
        display_name = f"{instance_label} ({platform})" if platform else instance_label
        print(f'\n正在检查实例: {display_name} ({instance_path})')

        if instance_path.startswith('http'):
            print(f'跳过外部链接实例: {instance_path}')
            continue

        mdx_files = find_mdx_files(instance_path)
        print(f'共找到{len(mdx_files)}个mdx文件。')

        problems, collected_urls = check_instance_links(mdx_files, config, instance, repo_root, check_remote)
        _collect_results(problems, collected_urls, display_name, structured_results, aggregated_by_url)

    write_result_files(mode='interactive', structured_results=structured_results, language=language,
                       check_remote=check_remote, aggregated_by_url=aggregated_by_url)

def write_result_files(mode, structured_results, language=None, check_remote=None, aggregated_by_url=None):
    """将结果分别写入 JSON 和 Markdown 文件"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'check_link_result.json')
    md_path = os.path.join(base_dir, 'check_link_result.md')

    # 写 JSON
    if aggregated_by_url is None:
        aggregated_by_url = {}

    # 计算 URL 分类别汇总（按 count 降序）
    def categorize_url(u):
        if u.startswith('#'):
            return 'anchor'
        if u.startswith('/'):
            return 'internal'
        if re.match(r'https?://', u):
            return 'external'
        if u.startswith('./') or u.startswith('../'):
            return 'relative'
        return 'other'

    urls_by_category = {
        'anchor': [],
        'internal': {
            'anchor': [],
            'non_anchor': [],
        },
        'external': {
            'anchor': [],
            'non_anchor': [],
        },
        'relative': {
            'anchor': [],
            'non_anchor': [],
        },
        'import': [],
        'other': [],
    }
    for url_key, occurrences in aggregated_by_url.items():
        # 检查是否为 import 类型的 URL
        is_import = any(occ.get('error_type') == 'Import路径无效' for occ in occurrences)

        category = categorize_url(url_key)
        is_old_doc = (category == 'external' and is_old_doc_url_any(url_key))
        has_anchor_error = any((occ.get('error_type') == '锚点链接无效') for occ in occurrences)
        item = {
            'url': url_key,
            'count': len(occurrences),
        }

        # 如果是 import 类型，归入 import 分类
        if is_import:
            urls_by_category['import'].append(item)
            continue

        # 若为 internal/relative 且存在锚点错误，则归入顶级 anchor 分类
        if (category in ('internal', 'relative')) and has_anchor_error:
            urls_by_category['anchor'].append(item)
            continue
        if category == 'anchor':
            urls_by_category['anchor'].append(item)
        elif category in ('internal', 'external', 'relative'):
            if category == 'external' and is_old_doc:
                # external.old-doc 归类
                urls_by_category['external'].setdefault('old-doc', [])
                urls_by_category['external']['old-doc'].append(item)
            else:
                if '#' in url_key:
                    urls_by_category[category]['anchor'].append(item)
                else:
                    urls_by_category[category]['non_anchor'].append(item)
        else:
            urls_by_category['other'].append(item)
    # 各类内按 count 降序排序
    urls_by_category['anchor'].sort(key=lambda x: x['count'], reverse=True)
    urls_by_category['import'].sort(key=lambda x: x['count'], reverse=True)
    for cat in ('internal', 'external', 'relative'):
        urls_by_category[cat]['anchor'].sort(key=lambda x: x['count'], reverse=True)
        urls_by_category[cat]['non_anchor'].sort(key=lambda x: x['count'], reverse=True)
        if cat == 'external' and 'old-doc' in urls_by_category[cat]:
            urls_by_category[cat]['old-doc'].sort(key=lambda x: x['count'], reverse=True)
    urls_by_category['other'].sort(key=lambda x: x['count'], reverse=True)

    output_obj = {
        'mode': mode,
        'language': language,
        'check_remote': check_remote,
        'generated_at': datetime.now().isoformat(),
        'instances': structured_results,
        'urls_by_category': urls_by_category,
    }
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(output_obj, f, ensure_ascii=False, indent=2)
        print(f"结果已写入: {json_path}")
    except Exception as e:
        print(f"{Fore.RED}写入JSON结果失败: {e}{Style.RESET_ALL}")

    # 按需可扩展写入 Markdown 的逻辑；当前按需求不输出 Markdown 文件

if __name__ == '__main__':
    main()