"""
docuo 配置辅助工具。用于给 claude code 的插件提供辅助功能。

功能：
- 根据 mdx 文件路径获取实例信息
- 根据 mdx 文件路径获取对应实例的 sidebars.json 文件内容
- 根据 mdx 文件路径获取 URL
- 根据 URL 解析出对应的 MDX/MD 文件路径（新增）

支持自动识别语言：
- 路径包含 /en/ 使用 docuo.config.en.json
- 路径包含 /zh/ 使用 docuo.config.zh.json
- 其他情况使用 docuo.config.json
"""

import json
import os
import re
from pathlib import Path
from typing import Optional, Dict, Any, Tuple


def _detect_locale(file_path: str) -> str:
    """
    从文件路径中检测语言

    Args:
        file_path: mdx 文件路径

    Returns:
        locale: 语言标识 ('en', 'zh', 或 '')
    """
    normalized = file_path.replace("\\", "/")

    if "/en/" in normalized:
        return "en"
    elif "/zh/" in normalized:
        return "zh"
    return ""


def _get_docuo_config_path(file_path: str = "") -> Tuple[Path, str]:
    """
    获取 docuo.config.json 文件路径

    根据文件路径自动选择对应的配置文件：
    - 包含 /en/ 的路径使用 docuo.config.en.json
    - 包含 /zh/ 的路径使用 docuo.config.zh.json
    - 其他情况使用 docuo.config.json

    Args:
        file_path: mdx 文件路径（用于判断语言）

    Returns:
        (config_path, locale): 配置文件路径和语言标识
    """
    # 从当前脚本位置向上查找 workspace 根目录
    # 脚本位于 .docuo/scripts/，需要向上两级到 workspace 根目录
    script_dir = Path(__file__).parent.resolve()
    workspace_root = script_dir.parent.parent.resolve()

    # 检测语言
    locale = _detect_locale(file_path)

    # 根据语言选择配置文件
    if locale == "en":
        config_filename = "docuo.config.en.json"
    elif locale == "zh":
        config_filename = "docuo.config.zh.json"
    else:
        config_filename = "docuo.config.json"

    config_path = workspace_root / config_filename

    if not config_path.exists():
        # 尝试从环境变量获取
        workspace_path = os.environ.get("CLAUDE_CODE_WORKSPACE")
        if workspace_path:
            config_path = Path(workspace_path) / config_filename

    if not config_path.exists():
        raise FileNotFoundError(f"无法找到 {config_filename} 文件，查找路径: {config_path}")

    return config_path, locale


def _load_docuo_config(file_path: str = "") -> Tuple[Dict[str, Any], str]:
    """
    加载 docuo.config.json 配置文件

    Args:
        file_path: mdx 文件路径（用于判断使用哪个配置文件）

    Returns:
        (config, locale): 配置内容和语言标识
    """
    config_path, locale = _get_docuo_config_path(file_path)

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f), locale


def _to_workspace_relative_path(file_path: str) -> str:
    """
    如果传入的是绝对路径，转换为相对于 workspace 根目录的相对路径；
    否则原样返回。
    """
    p = Path(file_path)
    if p.is_absolute():
        script_dir = Path(__file__).parent.resolve()
        workspace_root = script_dir.parent.parent.resolve()
        try:
            return str(p.relative_to(workspace_root))
        except ValueError:
            pass  # 不在 workspace 下，保持原样
    return file_path


def _normalize_file_path(file_path: str) -> str:
    """
    标准化文件路径

    - Windows反斜杠 (\\) → 正斜杠 (/)
    - 移除开头的 docs/ 或 .docuo/docs/（如果存在）
    - 移除文件扩展名

    Args:
        file_path: mdx 文件路径

    Returns:
        标准化后的路径
    """
    # 转换反斜杠为正斜杠
    normalized = file_path.replace("\\", "/")

    # 移除可能的前缀
    prefixes_to_remove = ["docs/", ".docuo/docs/", "docs\\"]
    for prefix in prefixes_to_remove:
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix):]

    # 移除文件扩展名
    for ext in [".mdx", ".md", ".MDX", ".MD"]:
        if normalized.endswith(ext):
            normalized = normalized[: -len(ext)]

    return normalized


def convert_to_doc_id(file_path: str) -> str:
    """
    将文件路径转换为文档 ID

    转换规则：
    1. 大写字母 → 小写字母
    2. 空格 → 连字符 (-)
    3. URL编码空格 (%20) → 连字符 (-)
    4. Windows反斜杠 (\\) → 正斜杠 (/)
    5. 数字前缀移除（如 01-、02-）

    Args:
        file_path: 文件路径

    Returns:
        转换后的文档 ID
    """
    # 标准化路径
    doc_id = _normalize_file_path(file_path)

    # 移除数字前缀（针对每个路径段）
    parts = doc_id.split("/")
    normalized_parts = []
    for part in parts:
        # 移除开头的 "数字-" 格式
        part = re.sub(r"^(\d+)-", "", part)
        normalized_parts.append(part)

    doc_id = "/".join(normalized_parts)

    # 空格和 URL 编码空格转为连字符
    doc_id = doc_id.replace(" ", "-").replace("%20", "-")

    # 大写转小写
    doc_id = doc_id.lower()

    return doc_id


def _get_instance_info_by_slug(slug: str) -> Optional[Dict[str, Any]]:
    """
    根据 slug（URL路径）获取实例信息

    匹配逻辑：
    1. 以中文配置文件为基准
    2. 把 instances 项的所有 routeBasePath 去匹配这个 slug 的开头，哪个匹配上了就返回哪个实例信息
    3. 如果中文找不到，换成英文配置文件来找，重复步骤2

    Args:
        slug: URL路径（以 / 开头，无后缀，如：/real-time-video-ios-oc/introduction/overview）

    Returns:
        instance_info: 实例信息，如果未找到返回 None
    """
    def _find_by_route_base_path(slug: str, locale: str) -> Optional[Dict[str, Any]]:
        """在指定语言的配置中查找匹配的实例"""
        config = _load_docuo_config(f"core_products/{locale}/dummy.mdx")[0]
        instances = config.get("instances", [])

        for instance in instances:
            route_base_path = instance.get("routeBasePath", "")
            if not route_base_path:
                continue

            # 标准化 routeBasePath，确保以 / 开头
            normalized_route = route_base_path if route_base_path.startswith("/") else f"/{route_base_path}"

            # 检查 slug 是否以 routeBasePath 开头
            if slug.startswith(normalized_route):
                return {
                    "id": instance.get("id"),
                    "label": instance.get("label"),
                    "path": instance.get("path"),
                    "clientApiPath": instance.get("clientApiPath"),
                    "routeBasePath": route_base_path,
                    "locale": instance.get("locale", locale),
                }
        return None

    # 1. 先用中文配置查找
    result = _find_by_route_base_path(slug, "zh")
    if result:
        return result

    # 2. 中文找不到，用英文配置查找
    return _find_by_route_base_path(slug, "en")


def get_instance_info_by_path(file_path: str) -> Optional[Dict[str, Any]]:
    """
    根据 mdx 文件路径或 slug 获取实例信息

    支持两种输入模式：
    1. 文件路径（带 .mdx/.md 后缀）：自动根据路径选择对应的配置文件
       - 包含 /en/ 的路径使用 docuo.config.en.json
       - 包含 /zh/ 的路径使用 docuo.config.zh.json
       - 其他情况使用 docuo.config.json
    2. slug（无后缀且以 / 开头）：根据 routeBasePath 匹配
       - 先用中文配置查找，找不到再用英文配置

    Args:
        file_path: mdx 文件路径（如：core_products/aiagent/zh/android/quick-start.mdx）
                   或 slug（如：/real-time-video-ios-oc/introduction/overview）

    Returns:
        instance_info: 实例信息，如果未找到返回 None
          - id: 实例ID
          - label: 实例名称
          - path: 实例路径
          - clientApiPath: 客户端API路径
          - routeBasePath: 路由基础路径
          - locale: 语言
    """
    # 如果是绝对路径，转换为相对于 workspace 根目录的相对路径
    file_path = _to_workspace_relative_path(file_path)

    # 判断是否为 slug 模式：无后缀且以 / 开头
    is_slug = file_path.startswith("/") and not any(
        file_path.lower().endswith(ext) for ext in [".mdx", ".md"]
    )

    if is_slug:
        # Slug 模式：根据 routeBasePath 匹配
        return _get_instance_info_by_slug(file_path)

    # 文件路径模式：保持原逻辑
    config, locale = _load_docuo_config(file_path)
    instances = config.get("instances", [])

    # 标准化文件路径
    normalized_path = _normalize_file_path(file_path)

    # 尝试匹配实例
    for instance in instances:
        instance_path = instance.get("path", "")

        # 检查文件路径是否以实例路径开头
        if normalized_path.startswith(instance_path):
            return {
                "id": instance.get("id"),
                "label": instance.get("label"),
                "path": instance_path,
                "clientApiPath": instance.get("clientApiPath"),
                "routeBasePath": instance.get("routeBasePath"),
                "locale": instance.get("locale", locale or "zh"),
            }

    return None


def get_sidebars_json_by_path(file_path: str) -> Optional[Dict[str, Any]]:
    """
    根据 mdx 文件路径获取对应实例的 sidebars.json 文件内容

    自动根据路径选择对应的配置文件：
    - 包含 /en/ 的路径使用 docuo.config.en.json
    - 包含 /zh/ 的路径使用 docuo.config.zh.json
    - 其他情况使用 docuo.config.json

    Args:
        file_path: mdx 文件路径

    Returns:
        sidebars_json: sidebars.json 文件内容，如果未找到返回 None
    """
    instance_info = get_instance_info_by_path(file_path)

    if not instance_info:
        return None

    # 获取配置文件路径（用于定位 workspace 根目录）
    config_path, _ = _get_docuo_config_path(file_path)
    workspace_root = config_path.parent

    # 构建 sidebars.json 文件路径
    sidebars_path = workspace_root / "docs" / instance_info["path"] / "sidebars.json"

    if not sidebars_path.exists():
        # 尝试直接在实例目录下查找
        sidebars_path = workspace_root / instance_info["path"] / "sidebars.json"

    if not sidebars_path.exists():
        return None

    with open(sidebars_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_url_by_path(file_path: str) -> Optional[str]:
    """
    根据 mdx 文件路径获取 URL

    自动根据路径选择对应的配置文件：
    - 包含 /en/ 的路径使用 docuo.config.en.json
    - 包含 /zh/ 的路径使用 docuo.config.zh.json
    - 其他情况使用 docuo.config.json

    Args:
        file_path: mdx 文件路径

    Returns:
        url: URL，如果未找到返回 None
    """
    # 如果是绝对路径，转换为相对于 workspace 根目录的相对路径
    file_path = _to_workspace_relative_path(file_path)

    instance_info = get_instance_info_by_path(file_path)

    if not instance_info:
        return None

    # 标准化文件路径和实例路径
    normalized_path = _normalize_file_path(file_path)
    instance_path = _normalize_file_path(instance_info["path"])

    # 计算相对于实例目录的路径（移除实例路径前缀）
    relative_path = normalized_path
    if normalized_path.startswith(instance_path):
        relative_path = normalized_path[len(instance_path):].lstrip("/")

    # 将相对路径转换为文档 ID（应用所有转换规则）
    doc_id = convert_to_doc_id(relative_path)

    # 组合 URL
    route_base_path = instance_info.get("routeBasePath", "")
    url = f"/{route_base_path}/{doc_id}"

    return url


def _get_config_file_by_domain(url: str) -> str:
    """
    根据域名判断要读取的配置文件名

    Args:
        url: 完整的 URL 或路径

    Returns:
        config_filename: 配置文件名
    """
    from urllib.parse import urlparse

    try:
        # 尝试解析 URL
        parsed = urlparse(url)
        hostname = parsed.hostname

        if hostname in ('doc-zh.zego.im', 'localhost', '127.0.0.1'):
            return 'docuo.config.zh.json'
        else:
            return 'docuo.config.en.json'
    except Exception:
        return 'docuo.config.json'



def _path_to_file_id(file_path: str) -> str:
    """
    将文件路径转换为 fileId 格式（用于匹配）
    处理大写、空格、数字前缀等

    Args:
        file_path: 文件路径

    Returns:
        file_id: 转换后的文件 ID
    """
    # 移除扩展名
    no_ext = re.sub(r'\.(md|mdx)$', '', file_path, flags=re.IGNORECASE)

    # 分割路径并处理每个段
    parts = no_ext.split('/')
    processed_parts = []

    for seg in parts:
        # 移除数字前缀如 "01-"
        s = re.sub(r'^[0-9]+-', '', seg)
        # 转小写
        s = s.lower()
        # 空格转连字符
        s = re.sub(r'\s+', '-', s)
        processed_parts.append(s)

    file_id = '/'.join(processed_parts)

    # 移除末尾的 /index
    if file_id.endswith('/index'):
        file_id = file_id[:-6]  # len('/index') = 6

    return file_id


def _find_best_match_instance(url_path: str, instances: list) -> Optional[Dict[str, Any]]:
    """
    使用贪心匹配法找到最佳匹配的 instance

    Args:
        url_path: URL 路径部分
        instances: 实例列表

    Returns:
        匹配结果字典，包含 instance 和 remainingPath，如果未找到返回 None
    """
    # 移除开头的斜杠并分割路径
    path_segments = [s for s in url_path.strip('/').split('/') if s]

    best_match = None

    for inst in instances:
        route_base_path = (inst.get('routeBasePath') or '').strip('/')
        if not route_base_path:
            continue

        route_segments = [s for s in route_base_path.split('/') if s]

        # 检查是否匹配
        matches = True
        for i in range(len(route_segments)):
            if i >= len(path_segments) or path_segments[i] != route_segments[i]:
                matches = False
                break

        if matches:
            # 贪心匹配：选择匹配最多段的 instance
            if not best_match or len(route_segments) > best_match['match_length']:
                remaining = '/'.join(path_segments[len(route_segments):])
                best_match = {
                    'instance': inst,
                    'match_length': len(route_segments),
                    'remaining_path': remaining
                }

    if best_match:
        return {
            'instance': best_match['instance'],
            'remainingPath': best_match['remaining_path']
        }

    return None


def _find_all_mdx_files(directory: Path) -> list:
    """
    递归查找所有 MD/MDX 文件

    Args:
        directory: 目录路径

    Returns:
        文件路径列表
    """
    file_list = []

    if not directory.exists() or not directory.is_dir():
        return file_list

    for item in directory.rglob('*'):
        if item.is_file() and item.suffix.lower() in ['.md', '.mdx']:
            file_list.append(item)

    return file_list


def _find_file_by_file_id(instance_path: Path, target_file_id: str) -> Optional[Path]:
    """
    在指定目录下查找匹配 fileId 的文件

    Args:
        instance_path: 实例目录路径
        target_file_id: 目标文件 ID

    Returns:
        匹配的文件路径，如果未找到返回 None
    """
    files = _find_all_mdx_files(instance_path)

    for file in files:
        relative_path = file.relative_to(instance_path).as_posix()
        file_id = _path_to_file_id(relative_path)

        if file_id == target_file_id:
            return file

    return None


def url_to_file_path(url: str, docs_root: Optional[str] = None) -> Dict[str, Any]:
    """
    主函数：URL 转文件路径

    Args:
        url: 文档 URL（完整 URL 或路径，如 /real-time-video-ios-oc/introduction/overview）
        docs_root: 文档根目录，默认为脚本所在目录的上两级

    Returns:
        结果字典，包含：
        - filePath: 文件的绝对路径
        - instance: 匹配到的 instance 信息
        - fileId: 文件的 ID（用于 URL 路由）
        - configFile: 使用的配置文件名

    Raises:
        ValueError: URL 格式无效或未找到匹配
        FileNotFoundError: 配置文件或文件不存在
    """
    from urllib.parse import urlparse

    # 1. 解析 URL
    try:
        # 如果 URL 不包含协议，添加一个默认协议以便解析
        if not url.startswith(('http://', 'https://', '//')):
            if url.startswith('/'):
                url = 'http://localhost' + url
            else:
                url = 'http://localhost/' + url

        parsed = urlparse(url)
        url_path = parsed.path

        # 移除路径开头的 /docs/ 前缀（如果存在）
        # 因为发布到线上时会自动在 routeBasePath 前拼接 /docs
        if url_path.startswith('/docs/'):
            url_path = url_path[5:]  # 移除 '/docs'，保留后面的 '/'
    except Exception as e:
        raise ValueError(f'无效的 URL 格式: {url}') from e

    # 2. 确定文档根目录
    if docs_root is None:
        script_dir = Path(__file__).parent.resolve()
        docs_root = str(script_dir.parent.parent.resolve())

    docs_root_path = Path(docs_root)

    # 3. 根据域名确定配置文件
    config_filename = _get_config_file_by_domain(url)
    config_path = docs_root_path / config_filename

    # 4. 读取配置文件
    try:
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            default_path = docs_root_path / 'docuo.config.json'
            with open(default_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
    except Exception as e:
        raise FileNotFoundError(f'读取配置文件失败: {config_filename} - {str(e)}') from e

    instances = config.get('instances', [])
    if not instances:
        raise ValueError('配置文件中没有 instances')

    # 5. 使用贪心匹配找到最佳 instance
    match_result = _find_best_match_instance(url_path, instances)
    if not match_result:
        raise ValueError('未找到匹配的 instance')

    instance = match_result['instance']
    remaining_path = match_result['remainingPath']

    instance_path = docs_root_path / (instance.get('path') or '').strip('/')

    # 6. 查找匹配的文件
    target_file_id = remaining_path.lower()
    file_path = _find_file_by_file_id(instance_path, target_file_id)

    if not file_path:
        raise FileNotFoundError(
            f'未找到匹配文件: {remaining_path} 在目录: {instance.get("path")}'
        )

    return {
        'filePath': str(file_path.resolve()),
        'instance': {
            'id': instance.get('id'),
            'label': instance.get('label'),
            'path': instance.get('path'),
            'routeBasePath': instance.get('routeBasePath')
        },
        'fileId': target_file_id,
        'configFile': config_filename
    }


# 添加一个主函数用于命令行测试
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法:")
        print("  1. 文件路径转 URL:")
        print("     python3 config_helper.py <file_path> [--info|--sidebars|--url|--locale]")
        print()
        print("  2. URL 转文件路径:")
        print("     python3 config_helper.py --resolve-url <url>")
        print()
        print("示例:")
        print("  python3 config_helper.py core_products/aiagent/zh/android/quick-start.mdx --info")
        print("  python3 config_helper.py core_products/aiagent/en/android/quick-start.mdx --url")
        print("  python3 config_helper.py --resolve-url /real-time-video-ios-oc/introduction/overview")
        print("  python3 config_helper.py --resolve-url https://doc-zh.zego.im/real-time-video-ios-oc/introduction/overview")
        print()
        print("选项:")
        print("  --info        显示实例信息")
        print("  --sidebars    显示侧边栏配置")
        print("  --url         显示文档 URL")
        print("  --locale      显示检测到的语言")
        print("  --resolve-url 将 URL 解析为文件路径")
        sys.exit(1)

    # 检查是否是 URL 解析模式
    if sys.argv[1] == "--resolve-url":
        if len(sys.argv) < 3:
            print("错误: --resolve-url 需要提供 URL 参数")
            sys.exit(1)

        url = sys.argv[2]
        docs_root = sys.argv[3] if len(sys.argv) > 3 else None

        try:
            result = url_to_file_path(url, docs_root)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        except Exception as e:
            print(f"错误: {str(e)}", file=sys.stderr)
            sys.exit(1)
    else:
        # 原有的文件路径模式
        file_path = sys.argv[1]
        option = sys.argv[2] if len(sys.argv) > 2 else "--info"

        if option == "--info":
            result = get_instance_info_by_path(file_path)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif option == "--sidebars":
            result = get_sidebars_json_by_path(file_path)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif option == "--url":
            result = get_url_by_path(file_path)
            print(result)
        elif option == "--locale":
            locale = _detect_locale(file_path)
            # 如果检测不到语言，默认返回 zh
            print(locale or "zh")
        else:
            print(f"未知选项: {option}")
            sys.exit(1)
