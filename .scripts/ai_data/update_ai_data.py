#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全新的AI数据更新脚本
整合页面下载、dataset创建/更新功能
"""

import json
import re
import asyncio
import sys
import os
import shutil
import requests
import xml.etree.ElementTree as ET
import subprocess
import logging
import argparse
from pathlib import Path
from urllib.parse import urlparse
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# 导入现有模块
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    import requests
    print(f"✅ requests 已加载，版本: {requests.__version__}")
except ImportError as e:
    print(f"❌ 需要安装 requests: pip install requests")
    requests = None


# 常量定义
CHINESE_SITEMAP_URL = "https://doc-zh.zego.im/sitemap.xml"
ENGLISH_SITEMAP_URL = "https://www.zegocloud.com/docs/sitemap.xml"
CHINESE_BASE_URL = "https://doc-zh.zego.im/"
ENGLISH_BASE_URL = "https://www.zegocloud.com/docs/"

@dataclass
class Config:
    """配置类"""
    ragflow_base_url: str = None
    api_key: str = None
    max_retries: int = 3
    retry_delay: int = 1
    concurrent_downloads: int = 5

    def __post_init__(self):
        # 优先尝试加载同目录下的 .env（无第三方依赖），仅设置未在环境中存在的键
        try:
            env_path = Path(__file__).parent / ".env"
            if env_path.exists():
                for line in env_path.read_text(encoding='utf-8').splitlines():
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        k, v = line.split('=', 1)
                        k = k.strip()
                        v = v.strip().strip('"').strip("'")
                        if k and k not in os.environ:
                            os.environ[k] = v
        except Exception:
            pass

        # 读取并规范化 RAGFlow 基础地址
        base = os.getenv('RAGFLOW_BASE_URL', '').strip().rstrip('/')
        if base:
            if not (base.startswith('http://') or base.startswith('https://')):
                base = 'https://' + base
            # 确保包含 /api/v1 前缀
            if not re.search(r"/api/v\d+($|/)", base):
                base = base + '/api/v1'
        self.ragflow_base_url = base

        # API Key
        self.api_key = os.getenv('RAGFLOW_API_KEY', '')

class UpdateAIDataManager:
    """AI数据更新管理器"""

    def __init__(self):
        self.config = Config()
        self.data_dir = Path("data")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.static_data_dir = Path("../../static/data")
        self.static_data_dir.mkdir(parents=True, exist_ok=True)

        # 设置日志
        self.setup_logging()

        # 语言相关配置
        self.language = None
        self.config_file = None
        self.sitemap_url = None
        self.base_url = None
        self.faq_dataset_name = None

        # 错误记录
        self.download_errors = {}
        self.dataset_errors = {}

    def setup_logging(self):
        """设置日志记录"""
        # 获取脚本所在目录
        script_dir = Path(__file__).parent
        log_file = script_dir / "update.log"

        # 配置日志格式
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()  # 同时输出到控制台
            ]
        )

        self.logger = logging.getLogger(__name__)
        self.logger.info("=== AI数据更新脚本启动 ===")

    def log_error(self, message: str):
        """记录错误信息，同时输出到控制台和日志文件"""
        print(f"❌ {message}")
        self.logger.error(message)

    def log_warning(self, message: str):
        """记录警告信息"""
        print(f"⚠️  {message}")
        self.logger.warning(message)

    def select_language(self) -> str:
        """选择处理语言"""
        print("\n=== 选择处理语言 ===")
        print("请选择要处理的语言:")
        print("1. 中文 (默认)")
        print("2. 英文")

        choice = input("\n请选择 (直接回车默认中文): ").strip()

        if choice == "2":
            self.language = "en"
            self.config_file = "../../docuo.config.en.json"
            self.sitemap_url = ENGLISH_SITEMAP_URL
            self.base_url = ENGLISH_BASE_URL
            self.faq_dataset_name = "FAQ-EN"
            print("✅ 已选择英文")
            self.logger.info("选择语言: 英文")
        else:
            self.language = "zh"
            self.config_file = "../../docuo.config.zh.json"
            self.sitemap_url = CHINESE_SITEMAP_URL
            self.base_url = CHINESE_BASE_URL
            self.faq_dataset_name = "FAQ-ZH"
            print("✅ 已选择中文")
            self.logger.info("选择语言: 中文")

        return self.language

    def get_git_commits(self, limit: int = 10) -> List[Dict]:
        """获取最近的git提交记录"""
        try:
            # 获取最近的提交记录
            cmd = ['git', 'log', '--oneline', f'-{limit}', '--pretty=format:%H|%s|%ad', '--date=short']
            result = subprocess.run(cmd, capture_output=True, text=True, cwd='../..')

            if result.returncode != 0:
                self.log_error(f"获取git提交记录失败: {result.stderr}")
                return []

            commits = []
            for line in result.stdout.strip().split('\n'):
                if '|' in line:
                    parts = line.split('|', 2)
                    if len(parts) >= 3:
                        commits.append({
                            'hash': parts[0],
                            'message': parts[1],
                            'date': parts[2]
                        })

            return commits
        except Exception as e:
            self.log_error(f"获取git提交记录异常: {e}")
            return []

    def get_changed_files_since_commit(self, commit_hash: str) -> List[str]:
        """获取从指定提交到最新提交的变更文件（包含指定提交本身）"""
        try:
            # 获取变更的文件列表，使用 commit_hash^..HEAD 来包含指定提交的变更
            cmd = ['git', 'diff', '--name-only', f'{commit_hash}^..HEAD']
            result = subprocess.run(cmd, capture_output=True, text=True, cwd='../..')

            if result.returncode != 0:
                self.log_error(f"获取变更文件失败: {result.stderr}")
                return []

            changed_files = []
            for line in result.stdout.strip().split('\n'):
                if line.strip() and line.endswith('.mdx'):
                    changed_files.append(line.strip())

            return changed_files
        except Exception as e:
            self.log_error(f"获取变更文件异常: {e}")
            return []

    def match_files_to_instances(self, changed_files: List[str], config_data: Dict) -> Dict[str, List[str]]:
        """将变更文件匹配到对应的实例"""
        instance_files = {}
        instances = config_data.get('instances', [])

        for file_path in changed_files:
            for instance in instances:
                instance_path = instance.get('path', '')
                instance_id = instance.get('id', '')
                locale = instance.get('locale', '')

                # 只处理当前语言的实例
                if locale != self.language:
                    continue

                # 检查文件路径是否以实例的path开头
                if instance_path and file_path.startswith(instance_path):
                    if instance_id not in instance_files:
                        instance_files[instance_id] = []
                    instance_files[instance_id].append(file_path)
                    break  # 找到匹配的实例后跳出循环，避免重复匹配

        return instance_files

    def convert_file_path_to_url(self, file_path: str, route_base_path: str, instance_path: str = None) -> str:
        """将文件路径转换为URL

        Args:
            file_path: 文件路径，如 core_products/aiagent/zh/server/API reference/Agent Configuration Management/Register Agent.mdx
            route_base_path: 路由基础路径，如 aiagent-server
            instance_path: 实例路径，如 core_products/aiagent/zh/server
        """
        # 移除文件扩展名
        path_without_ext = file_path.replace('.mdx', '').replace('.md', '')

        # 如果提供了instance_path，先移除匹配的路径部分
        if instance_path:
            # 确保instance_path不以/结尾
            instance_path = instance_path.rstrip('/')

            # 如果文件路径以instance_path开头，移除这部分
            if path_without_ext.startswith(instance_path):
                # 移除instance_path部分，保留剩余路径
                remaining_path = path_without_ext[len(instance_path):].lstrip('/')
            else:
                # 如果不匹配，使用原有逻辑作为fallback
                remaining_path = self._fallback_path_extraction(path_without_ext)
        else:
            # 没有instance_path时使用原有逻辑
            remaining_path = self._fallback_path_extraction(path_without_ext)

        # 如果remaining_path为空，返回基础URL
        if not remaining_path:
            base_domain = "https://doc-zh.zego.im" if self.language == 'zh' else "https://www.zegocloud.com/docs"
            return f"{base_domain}/{route_base_path}"

        # 转换为URL格式：小写，空格和下划线转为连字符
        url_path = remaining_path.lower().replace(' ', '-').replace('_', '-')

        # 构建完整URL
        base_domain = "https://doc-zh.zego.im" if self.language == 'zh' else "https://www.zegocloud.com/docs"
        full_url = f"{base_domain}/{route_base_path}/{url_path}"

        return full_url

    def _fallback_path_extraction(self, path_without_ext: str) -> str:
        """原有的路径提取逻辑，作为fallback"""
        path_parts = path_without_ext.split('/')

        # 找到语言标识符的位置
        lang_index = -1
        for i, part in enumerate(path_parts):
            if part in ['zh', 'en']:
                lang_index = i
                break

        # 如果找到语言标识符，取语言标识符后面的部分
        if lang_index >= 0 and lang_index < len(path_parts) - 1:
            remaining_parts = path_parts[lang_index + 1:]
        else:
            # 如果没找到语言标识符，取最后两个部分
            remaining_parts = path_parts[-2:] if len(path_parts) >= 2 else path_parts[-1:]

        return '/'.join(remaining_parts)

    def load_config_file(self) -> Dict:
        """加载配置文件"""
        config_path = Path(self.config_file)
        if not config_path.exists():
            error_msg = f"配置文件不存在: {self.config_file}"
            self.log_error(error_msg)
            raise FileNotFoundError(error_msg)

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            error_msg = f"加载配置文件失败: {e}"
            self.log_error(error_msg)
            raise

    def get_groups_from_config(self, config_data: Dict) -> Dict[str, Dict]:
        """从配置中提取group信息"""
        groups = {}
        instances = config_data.get('instances', [])

        for instance in instances:
            nav_info = instance.get('navigationInfo', {})
            group_info = nav_info.get('group', {})
            group_id = group_info.get('id')
            group_name = group_info.get('name')

            if group_id and group_name:
                if group_id not in groups:
                    groups[group_id] = {
                        'id': group_id,
                        'name': group_name,
                        'instances': []
                    }
                groups[group_id]['instances'].append(instance)

        return groups

    def select_groups_and_instances(self, groups: Dict[str, Dict]) -> List[Dict]:
        """选择要处理的groups和instances"""
        print("\n=== 选择要处理的产品组 ===")

        # 显示所有group选项
        group_list = list(groups.values())
        for i, group in enumerate(group_list, 1):
            print(f"{i}. {group['id']}-{group['name']} ({len(group['instances'])} 个实例)")

        while True:
            try:
                choice = input(f"\n请选择产品组 (1-{len(group_list)}): ").strip()
                group_index = int(choice) - 1
                if 0 <= group_index < len(group_list):
                    selected_group = group_list[group_index]
                    break
                else:
                    print("无效的选择，请重新输入!")
            except ValueError:
                print("请输入有效的数字!")

        print(f"\n已选择产品组: {selected_group['name']}")

        # 选择该group下的instances
        instances = selected_group['instances']
        print(f"\n=== 选择要处理的实例 ===")
        print("该产品组下的实例:")

        for i, instance in enumerate(instances, 1):
            platform = instance.get('navigationInfo', {}).get('platform', 'Unknown')
            print(f"{i}. {instance.get('id', 'Unknown')} - {platform}")

        print("0. 处理所有实例")

        while True:
            try:
                choice = input(f"\n请选择实例 (0-{len(instances)}, 直接回车处理所有): ").strip()
                if not choice:  # 直接回车
                    selected_instances = instances
                    print("✅ 将处理所有实例")
                    break
                elif choice == "0":
                    selected_instances = instances
                    print("✅ 将处理所有实例")
                    break
                else:
                    instance_index = int(choice) - 1
                    if 0 <= instance_index < len(instances):
                        selected_instances = [instances[instance_index]]
                        platform = selected_instances[0].get('navigationInfo', {}).get('platform', 'Unknown')
                        print(f"✅ 已选择实例: {selected_instances[0].get('id')} - {platform}")
                        break
                    else:
                        print("无效的选择，请重新输入!")
            except ValueError:
                print("请输入有效的数字!")

        return selected_instances

    def select_download_mode(self) -> str:
        """选择下载模式"""
        print("\n=== 选择下载模式 ===")
        print("请选择下载模式:")
        print("1. 根据git变更记录下载并更新")
        print("2. 选择指定实例更新")
        print("3. 跳过下载")

        while True:
            try:
                choice = input("\n请选择 (1-3)直接回车默认1: ").strip()
                if choice == "1":
                    return "git_changes"
                elif choice == "2":
                    return "select_instances"
                elif choice == "3":
                    return "skip_download"
                else:
                    return "git_changes"
            except ValueError:
                print("请输入有效的数字!")

    def select_dataset_mode(self) -> bool:
        """选择是否处理dataset"""
        print("\n=== 选择是否处理Dataset ===")
        print("请选择是否需要处理Dataset（知识库创建/更新）:")
        print("1. 处理Dataset (默认)")
        print("2. 跳过Dataset处理")

        while True:
            try:
                choice = input("\n请选择 (1-2, 直接回车默认处理): ").strip()
                if choice == "1" or choice == "":
                    print("✅ 将处理Dataset")
                    return True
                elif choice == "2":
                    print("⏭️  将跳过Dataset处理")
                    return False
                else:
                    print("请输入有效的数字!")
            except ValueError:
                print("请输入有效的数字!")

    def select_git_commit_and_get_changes(self, config_data: Dict) -> Tuple[List[Dict], Dict[str, List[str]]]:
        """选择git提交并获取变更"""
        print("\n=== 根据git变更记录下载 ===")

        # 获取最近的提交记录
        commits = self.get_git_commits(10)
        if not commits:
            self.log_error("无法获取git提交记录")
            return [], {}

        print("\n最近的10个提交:")
        for i, commit in enumerate(commits, 1):
            print(f"{i}. {commit['hash'][:8]} - {commit['message']} ({commit['date']})")

        # 让用户选择起始提交
        while True:
            choice = input(f"\n请选择从哪个提交开始统计变更 (1-{len(commits)}, 直接回车选择最新提交): ").strip()
            if not choice:  # 直接回车，选择最新提交
                selected_commit = commits[0]
                print(f"✅ 已选择最新提交: {selected_commit['hash'][:8]} - {selected_commit['message']}")
                break
            try:
                commit_index = int(choice) - 1
                if 0 <= commit_index < len(commits):
                    selected_commit = commits[commit_index]
                    print(f"✅ 已选择提交: {selected_commit['hash'][:8]} - {selected_commit['message']}")
                    break
                else:
                    print("无效的选择，请重新输入!")
            except ValueError:
                print("请输入有效的数字!")

        # 获取变更文件
        print(f"\n📊 正在获取从 {selected_commit['hash'][:8]} 到最新提交的变更文件...")
        changed_files = self.get_changed_files_since_commit(selected_commit['hash'])

        if not changed_files:
            self.log_error("没有找到变更的.mdx文件")
            return [], {}

        print(f"✅ 找到 {len(changed_files)} 个变更的.mdx文件:")
        for file in changed_files:
            print(f"  - {file}")

        # 匹配文件到实例
        print(f"\n🔍 正在匹配变更文件到实例...")
        instance_files = self.match_files_to_instances(changed_files, config_data)

        if not instance_files:
            self.log_error("没有找到匹配的实例")
            return [], {}

        print(f"✅ 匹配到 {len(instance_files)} 个实例:")
        affected_instances = []
        for instance_id, files in instance_files.items():
            print(f"  - {instance_id}: {len(files)} 个文件")
            # 找到对应的实例配置
            for instance in config_data.get('instances', []):
                if instance.get('id') == instance_id:
                    affected_instances.append(instance)
                    break

        return affected_instances, instance_files

    def get_sitemap_urls(self, route_base_path: str) -> List[str]:
        """从sitemap获取匹配的URLs（严格匹配一级 /{routeBasePath}/）"""
        try:
            print(f"正在获取sitemap: {self.sitemap_url}")

            # 英文暂未启用，预留逻辑
            if self.language == 'en':
                self.log_warning("英文 sitemap 暂未启用，先跳过。")
                return []

            if requests is None:
                self.log_error("requests 模块不可用，无法获取sitemap")
                return []

            response = requests.get(self.sitemap_url, timeout=30)
            response.raise_for_status()

            root = ET.fromstring(response.content)
            namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

            urls: List[str] = []
            url_elements = root.findall('.//ns:url', namespaces)
            if len(url_elements) == 0:
                url_elements = root.findall('.//url')

            rb = (route_base_path or '').strip('/')
            want_netloc = urlparse(self.base_url).netloc

            for url_elem in url_elements:
                loc_elem = url_elem.find('ns:loc', namespaces)
                if loc_elem is None:
                    loc_elem = url_elem.find('loc')

                if loc_elem is None or not loc_elem.text:
                    continue

                u = loc_elem.text.strip()
                parsed = urlparse(u)
                if parsed.netloc != want_netloc:
                    continue

                path = parsed.path or '/'
                if path == f"/{rb}" or path == f"/{rb}/" or path.startswith(f"/{rb}/"):
                    urls.append(f"{parsed.scheme}://{parsed.netloc}{path}")

            print(f"匹配到 {len(urls)} 个URLs (route: /{rb}/)")
            return urls

        except Exception as e:
            self.log_error(f"获取sitemap失败: {e}")
            return []

    def get_filename_from_url(self, url: str, title: str = "") -> str:
        """根据URL生成文件名"""
        parsed = urlparse(url)

        if title:
            # 去除标题中的 HTML/JSX 标签
            title = re.sub(r'<[^>]*>', '', title)
            clean_title = re.sub(r'[^\w\s-]', '', title).strip()
            clean_title = re.sub(r'[-\s]+', '-', clean_title)
            base_name = f"{clean_title}---{parsed.netloc}{parsed.path}"
        else:
            base_name = f"{parsed.netloc}{parsed.path}"

        filename = base_name.replace("/", ">").replace("&", "^^").replace('=', '^^^')
        return f"{filename}.md"

    def _to_md_url(self, page_url: str) -> str:
        parsed = urlparse(page_url)
        path = parsed.path.rstrip('/')
        if path.endswith('.md'):
            md_path = path
        else:
            md_path = f"{path}.md"
        return f"{parsed.scheme}://{parsed.netloc}{md_path}"

    def _extract_title_from_markdown(self, content: str) -> str:
        if not content:
            return ""
        # 优先匹配 Markdown 的一级标题
        m = re.search(r'(?im)^\s*#\s+(.+)$', content)
        if m:
            text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            if text:
                return text
        # 尝试匹配 HTML 的 <h1>
        m = re.search(r'(?is)<h1[^>]*>(.*?)</h1>', content)
        if m:
            text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            if text:
                return text
        # 顺延匹配二级到六级标题
        for level in range(2, 7):
            m = re.search(rf'(?im)^\s*#{{{level}}}\s+(.+)$', content)
            if m:
                text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
                if text:
                    return text
        # 兜底：返回第一行非空文本（移除可能存在的标签）
        for line in content.splitlines():
            if line.strip():
                text = re.sub(r'<[^>]+>', '', line).strip()
                if text:
                    return text[:80]
        return ""


    async def download_url_content(self, url: str, target_dir: Path, instance_label: str) -> bool:
        """直接下载对应 .md 内容并保存，标题取 instance.label + 首个 H1（无 H1 顺延 H2/H3...）"""
        page_url = url  # 用于生成最终文件名（不带 .md）
        md_url = self._to_md_url(page_url)

        for attempt in range(self.config.max_retries):
            try:
                if requests is None:
                    self.log_error("requests 模块不可用，无法下载")
                    return False

                loop = asyncio.get_running_loop()

                def _fetch():
                    return requests.get(md_url, timeout=30)

                response = await loop.run_in_executor(None, _fetch)

                if response.status_code == 200:
                    content = response.text
                    md_title = self._extract_title_from_markdown(content)
                    combined_title = f"{instance_label} {md_title}".strip() if (instance_label or md_title) else md_title

                    filename = self.get_filename_from_url(page_url, combined_title)
                    file_path = target_dir / filename

                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)

                    print(f"✅ 下载成功: {md_url}")
                    return True
                else:
                    self.log_warning(f"HTTP {response.status_code}: {md_url} (尝试 {attempt + 1}/{self.config.max_retries})")

            except Exception as e:
                self.log_warning(f"下载异常 (尝试 {attempt + 1}/{self.config.max_retries}): {md_url} - {e}")

            if attempt < self.config.max_retries - 1:
                await asyncio.sleep(self.config.retry_delay * (2 ** attempt))  # 指数退避

        self.log_error(f"下载最终失败: {md_url}")
        return False

    async def download_instance_files(self, instance: Dict, group_id: str) -> bool:
        """下载单个instance的文件"""
        instance_id = instance.get('id')
        route_base_path = instance.get('routeBasePath')
        platform = instance.get('navigationInfo', {}).get('platform', 'Unknown')

        print(f"\n📥 开始处理实例: {instance_id} - {platform}")

        if not route_base_path:
            self.log_error(f"实例 {instance_id} 缺少 routeBasePath")
            return False

        # 创建目录结构: data/group_id/instance_id
        target_dir = self.data_dir / group_id / instance_id

        # 检查是否已存在文件
        existing_files = []
        if target_dir.exists():
            existing_files = list(target_dir.glob("*.md"))

        if existing_files:
            print(f"📁 发现已存在 {len(existing_files)} 个文件在目录: {target_dir}")
            print(f"⚠️  重新下载将删除现有文件并重新获取所有内容")

            # 默认直接重新下载并覆盖
            print(f"🗑️  删除已存在的目录: {target_dir}")
            shutil.rmtree(target_dir)
            target_dir.mkdir(parents=True, exist_ok=True)
        else:
            target_dir.mkdir(parents=True, exist_ok=True)

        # 获取URLs
        urls = self.get_sitemap_urls(route_base_path)
        if not urls:
            self.log_error(f"未找到匹配的URLs，无法继续处理")
            return False

        print(f"📁 目标目录: {target_dir}")
        print(f"🚀 开始下载 {len(urls)} 个文件...")

        # 批量下载
        success_count = 0
        failed_count = 0
        batch_size = self.config.concurrent_downloads

        for i in range(0, len(urls), batch_size):
            batch = urls[i:i + batch_size]
            tasks = [self.download_url_content(url, target_dir, instance.get('label', '')) for url in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if result is True:
                    success_count += 1
                else:
                    failed_count += 1

        success_rate = success_count / len(urls) if urls else 0
        print(f"📊 下载统计: {success_count}/{len(urls)} 个文件成功 (成功率: {success_rate:.1%})")

        # 如果成功率低于50%，认为下载失败
        if success_rate < 0.5:
            self.log_error(f"下载失败率过高 ({failed_count}/{len(urls)} 失败)，终止处理")
            return False

        if failed_count > 0:
            self.log_warning(f"有 {failed_count} 个文件下载失败，但成功率可接受，继续处理")

        return success_count > 0

    async def download_git_changed_files(self, affected_instances: List[Dict], instance_files: Dict[str, List[str]]) -> bool:
        """根据git变更下载文件"""
        print(f"\n📥 开始根据git变更下载文件...")

        success_count = 0
        failed_count = 0

        for instance in affected_instances:
            instance_id = instance.get('id')
            route_base_path = instance.get('routeBasePath')
            platform = instance.get('navigationInfo', {}).get('platform', 'Unknown')
            group_id = instance.get('navigationInfo', {}).get('group', {}).get('id')

            print(f"\n📥 处理实例: {instance_id} - {platform}")

            if not route_base_path:
                self.log_error(f"实例 {instance_id} 缺少 routeBasePath")
                failed_count += 1
                continue

            if not group_id:
                self.log_error(f"实例 {instance_id} 缺少 group_id")
                failed_count += 1
                continue

            # 创建目录结构: data/group_id/instance_id
            target_dir = self.data_dir / group_id / instance_id
            target_dir.mkdir(parents=True, exist_ok=True)

            # 获取该实例的变更文件
            changed_files = instance_files.get(instance_id, [])
            if not changed_files:
                print(f"⚠️  实例 {instance_id} 没有变更文件")
                continue

            print(f"📁 目标目录: {target_dir}")
            print(f"🔄 处理 {len(changed_files)} 个变更文件:")
            # 先删除目标目录
            shutil.rmtree(target_dir, ignore_errors=True)
            target_dir.mkdir(parents=True, exist_ok=True)

            # 获取实例路径
            instance_path = instance.get('path', '')

            # 转换文件路径为URL并下载
            urls_to_download = []
            for file_path in changed_files:
                url = self.convert_file_path_to_url(file_path, route_base_path, instance_path)
                urls_to_download.append(url)
                print(f"  - {file_path} -> {url}")

            if not urls_to_download:
                self.log_error(f"没有有效的URL需要下载")
                failed_count += 1
                continue

            # 批量下载
            print(f"🚀 开始下载 {len(urls_to_download)} 个文件...")
            batch_success = 0
            batch_failed = 0
            batch_size = self.config.concurrent_downloads

            for i in range(0, len(urls_to_download), batch_size):
                batch = urls_to_download[i:i + batch_size]
                tasks = [self.download_url_content(url, target_dir, instance.get('label', '')) for url in batch]
                results = await asyncio.gather(*tasks, return_exceptions=True)

                for result in results:
                    if result is True:
                        batch_success += 1
                    else:
                        batch_failed += 1

            batch_success_rate = batch_success / len(urls_to_download) if urls_to_download else 0
            print(f"📊 实例 {instance_id} 下载统计: {batch_success}/{len(urls_to_download)} 个文件成功 (成功率: {batch_success_rate:.1%})")

            if batch_success_rate >= 0.5:  # 成功率50%以上认为成功
                success_count += 1
            else:
                failed_count += 1
                self.log_error(f"实例 {instance_id} 下载失败率过高")

        total_success_rate = success_count / len(affected_instances) if affected_instances else 0
        print(f"\n📊 总体下载统计: {success_count}/{len(affected_instances)} 个实例成功 (成功率: {total_success_rate:.1%})")

        return total_success_rate >= 0.5

    def get_documents_by_filename(self, dataset_id: str, filenames: List[str], instance: Dict = None) -> List[str]:
        """根据文件名获取文档ID

        Args:
            dataset_id: 数据集ID
            filenames: 文件路径列表（原始文件路径）
            instance: 实例信息，用于获取路径转换所需的参数
        """
        if not requests:
            self.log_error("requests 未安装，无法获取文档")
            return []

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.config.api_key}'
            }

        try:
            # 获取dataset中的所有文档
            response = requests.get(
                f"{self.config.ragflow_base_url}/datasets/{dataset_id}/documents",
                headers=headers,
                params={"page": 1, "page_size": 200},
                timeout=30,
            )

            if response.status_code != 200:
                self.log_error(f"获取文档列表失败: HTTP {response.status_code}")
                return []

            data = response.json()

            if data.get('code') == 102:
                print(f"⚠️  数据集为空: {dataset_id}")
                return []

            elif data.get('code') != 0:
                self.log_error(f"获取文档列表失败: {data.get('code')} {data.get('message')} {dataset_id}")
                return []

            data_content = data.get('data', {})

            # 根据RagFlow API文档，List documents返回的data是一个对象，包含docs数组
            if isinstance(data_content, dict):
                documents = data_content.get('docs', [])
            elif isinstance(data_content, list):
                # 兼容可能的直接数组格式
                documents = data_content
            else:
                self.log_error(f"文档数据格式错误: {type(data_content)}")
                return []

            if not isinstance(documents, list):
                self.log_error(f"文档列表格式错误: {type(documents)}")
                return []

            document_ids = []

            # 将文件路径转换为下载文件名格式
            converted_filenames = []
            if instance:
                route_base_path = instance.get('routeBasePath', '')
                instance_path = instance.get('path', '')

                for filename in filenames:
                    try:
                        # 将文件路径转换为URL
                        url = self.convert_file_path_to_url(filename, route_base_path, instance_path)
                        # 将URL转换为下载文件名格式（不带title，因为我们没有title信息）
                        download_filename = self.get_filename_from_url(url)
                        converted_filenames.append(download_filename)
                        print(f"🔄 文件路径转换: {filename} -> {url} -> {download_filename}")
                    except Exception as e:
                        print(f"⚠️  文件路径转换失败: {filename} - {e}")
                        # 如果转换失败，使用原始文件名作为fallback
                        converted_filenames.append(filename)
            else:
                # 如果没有实例信息，直接使用原始文件名
                converted_filenames = filenames
                print("⚠️  没有实例信息，无法进行文件名转换，使用原始文件名")

            # 匹配文件名
            for i, original_filename in enumerate(filenames):
                converted_filename = converted_filenames[i] if i < len(converted_filenames) else original_filename

                found_match = False
                for doc in documents:
                    if not isinstance(doc, dict):
                        continue

                    doc_name = doc.get('name', '')
                    doc_id = doc.get('id', '')

                    if not doc_id:
                        continue

                    # 匹配---后面的部分
                    if doc_name.endswith(f"---{converted_filename}"):
                        document_ids.append(doc_id)
                        print(f"✅ 找到匹配文档: {doc_name} (ID: {doc_id}) <- {original_filename}")
                        found_match = True
                        break

                if not found_match:
                    print(f"⚠️  未找到匹配文档: {original_filename} -> {converted_filename}")

            return document_ids

        except Exception as e:
            self.log_error(f"获取文档异常: {e}")
            return []

    def delete_specific_documents(self, dataset_id: str, document_ids: List[str]) -> bool:
        """删除指定的文档"""
        if not document_ids:
            print("⚠️  没有文档需要删除")
            return True

        if not requests:
            self.log_error("requests 未安装，无法删除文档")
            return False

        headers = {
            'Authorization': f'Bearer {self.config.api_key}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.delete(
                f"{self.config.ragflow_base_url}/datasets/{dataset_id}/documents",
                headers=headers,
                json={'ids': document_ids}
            )
            data = response.json()

            if data.get('code') == 0:
                print(f"✅ 成功删除 {len(document_ids)} 个文档")
                return True
            else:
                self.log_error(f"删除文档失败: {data.get('message')}")
                return False

        except Exception as e:
            self.log_error(f"删除文档异常: {e}")
            return False

    def create_or_get_dataset(self, dataset_name: str) -> Optional[str]:
        """创建或获取dataset"""
        print(f"📚 处理知识库: {dataset_name}")

        if not requests:
            self.log_error("requests 未安装，无法处理知识库")
            return None

        # 基础校验
        if not self.config.ragflow_base_url:
            self.log_error("RAGFLOW_BASE_URL 未设置或无效，请设置环境变量 RAGFLOW_BASE_URL（如：http://<host>:<port>/api/v1）")
            return None

        headers = {
            'Authorization': f'Bearer {self.config.api_key}',
            'Content-Type': 'application/json'
        }

        try:
            # 先查找是否存在（带分页，page_size=200）
            params = {"page": 1, "page_size": 200, "name": dataset_name}
            print(f"🔎 列举 Datasets 请求: url={self.config.ragflow_base_url}/datasets, params={params}")
            response = requests.get(
                f"{self.config.ragflow_base_url}/datasets",
                headers=headers,
                params=params,
                timeout=30,
            )
            print(f"🔎 列举 Datasets 响应: status={response.status_code}, body={response.text[:400]}")
            data = response.json()

            if data.get('code') == 0 and data.get('data'):
                items = data['data']
                for it in items:
                    if it.get('name', '').lower() == dataset_name.lower():
                        dataset_id = it['id']
                        print(f"✅ 找到已存在的知识库: {dataset_id}")
                        return dataset_id

            # 创建新的dataset（按文档：不传 language；确保 embedding_model 满足 name@factory；parser_config.chunk_token_num 为整数）
            # 计算 embedding_model
            if self.language == 'zh':
                default_model = 'BAAI/bge-large-zh-v1.5@BAAI'
                embedding_model = os.getenv('RAGFLOW_EMBEDDING_MODEL_ZH', default_model)
            else:
                default_model = 'bce-embedding-base_v1@maidalun1020'
                embedding_model = os.getenv('RAGFLOW_EMBEDDING_MODEL_EN', default_model)
            # 如果缺少 @factory，尽量补 @BAAI（兜底）
            if '@' not in embedding_model:
                embedding_model = embedding_model + '@BAAI'

            # 解析 chunk_token_num 为 int
            ctn_raw = os.getenv('RAGFLOW_CHUNK_TOKEN_NUM', '512')
            try:
                chunk_token_num = int(str(ctn_raw).strip())
            except Exception:
                print(f"⚠️  RAGFLOW_CHUNK_TOKEN_NUM 无法解析为整数，使用默认 512，原始值: {ctn_raw}")
                chunk_token_num = 512

            config = {
                'name': dataset_name,
                'permission': 'team',
                'embedding_model': embedding_model,
                'parser_config': {
                    'chunk_token_num': chunk_token_num
                }
            }
            print(f"🔧 创建 Dataset 请求: url={self.config.ragflow_base_url}/datasets, body={config}")

            response = requests.post(
                f"{self.config.ragflow_base_url}/datasets",
                headers=headers,
                json=config,
                timeout=30,
            )
            try:
                data = response.json()
            except Exception:
                data = {"code": -1, "message": response.text[:500]}

            if data.get('code') == 0:
                dataset_id = data['data']['id']
                print(f"✅ 创建知识库成功: {dataset_id}")
                return dataset_id
            else:
                self.log_error(f"创建知识库失败: HTTP {response.status_code}, code={data.get('code')}, message={data.get('message')}")
                return None

        except Exception as e:
            self.log_error(f"处理知识库异常: {e}")
            return None

    def upload_and_parse_documents(self, dataset_id: str, file_paths: List[str], clear_existing: bool = True) -> bool:
        """上传并解析文档"""
        if not file_paths:
            print("⚠️  没有文件需要上传")
            return False

        print(f"📤 上传 {len(file_paths)} 个文档到知识库")

        headers = {'Authorization': f'Bearer {self.config.api_key}'}

        try:
            # 根据参数决定是否清空现有文档
            if clear_existing:
                response = requests.delete(
                    f"{self.config.ragflow_base_url}/datasets/{dataset_id}/documents",
                    headers={**headers, 'Content-Type': 'application/json'},
                    json={'ids': None}
                )
                print("🗑️  已清空知识库中的现有文档")
            else:
                print("📝 保留现有文档，仅上传新文档")

            # 批量上传文件
            batch_size = 10
            all_file_ids = []

            for i in range(0, len(file_paths), batch_size):
                batch_files = file_paths[i:i + batch_size]
                files = []

                for file_path in batch_files:
                    if Path(file_path).exists():
                        files.append(('file', open(file_path, 'rb')))

                if files:
                    response = requests.post(
                        f"{self.config.ragflow_base_url}/datasets/{dataset_id}/documents",
                        headers=headers,
                        files=files
                    )

                    # 关闭文件句柄
                    for _, file_handle in files:
                        file_handle.close()

                    data = response.json()
                    if data.get('code') == 0 and data.get('data'):
                        batch_ids = [item['id'] for item in data['data']]
                        all_file_ids.extend(batch_ids)
                        print(f"✅ 批次上传成功: {len(batch_ids)} 个文件")

            if all_file_ids:
                # 解析文档
                response = requests.post(
                    f"{self.config.ragflow_base_url}/datasets/{dataset_id}/chunks",
                    headers={**headers, 'Content-Type': 'application/json'},
                    json={'document_ids': all_file_ids}
                )
                print("✅ 文档解析完成")
                return True
            else:
                self.log_error("没有成功上传的文件")
                return False

        except Exception as e:
            self.log_error(f"上传文档异常: {e}")
            return False





    def log_download_errors(self, failed_instances: List[str], failed_files: Dict[str, List[str]]):
        """记录下载错误"""
        if failed_instances:
            print("\n=== 下载错误总结 ===")
            print(f"❌ 以下实例下载失败:")
            for instance in failed_instances:
                print(f"  - {instance}")
                if instance in failed_files:
                    print("    失败文件:")
                    for file in failed_files[instance]:
                        print(f"      - {file}")

    def log_dataset_errors(self, failed_datasets: List[str], error_details: Dict[str, str]):
        """记录Dataset处理错误"""
        if failed_datasets:
            print("\n=== Dataset处理错误总结 ===")
            print(f"❌ 以下Dataset处理失败:")
            for dataset in failed_datasets:
                print(f"  - {dataset}")
                if dataset in error_details:
                    print(f"    错误原因: {error_details[dataset]}")


async def main():
    """主函数"""
    manager = UpdateAIDataManager()

    print("=== AI数据更新脚本 ===")
    print("本脚本将完整执行：页面下载 -> Dataset更新")

    try:
        # 1. 语言固定为中文（英文 sitemap 暂未启用）
        manager.language = 'zh'
        manager.config_file = "../../docuo.config.zh.json"
        manager.sitemap_url = CHINESE_SITEMAP_URL
        manager.base_url = CHINESE_BASE_URL
        manager.faq_dataset_name = "FAQ-ZH"
        print("✅ 已选择中文")

        # 2. 加载配置文件
        print(f"\n📖 加载配置文件: {manager.config_file}")
        config_data = manager.load_config_file()

        # 3. 提取groups
        groups = manager.get_groups_from_config(config_data)
        if not groups:
            manager.log_error("配置文件中没有找到有效的groups")
            return

        print(f"✅ 找到 {len(groups)} 个产品组")

        # 4. 解析命令行参数；支持 --all 全量模式
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--all", dest="all_mode", action="store_true", help="全量模式：遍历所有产品的所有实例")
        args, _ = parser.parse_known_args()

        if args.all_mode:
            print("\n=== 全量模式: 遍历所有产品的所有实例 ===")
            all_instances = []
            for grp in groups.values():
                all_instances.extend(grp.get('instances', []))

            total = len(all_instances)
            print(f"📦 共发现 {total} 个实例，将逐个下载并更新对应知识库（完成后删除本地文件）")

            success_cnt, fail_cnt, skipped_cnt = 0, 0, 0
            failure_details = {}
            success_groups = set()
            # 在全量模式下跳过冗余产品
            skip_ids = {"real_time_voice_zh", "live_streaming_zh"}

            for idx, instance in enumerate(all_instances, 1):
                instance_id = instance.get('id')
                if instance_id in skip_ids:
                    print(f"⏭️ 跳过冗余产品: {instance_id}")
                    skipped_cnt += 1
                    continue
                group_id_each = instance.get('navigationInfo', {}).get('group', {}).get('id')
                print(f"\n[{idx}/{total}] 实例 {instance_id} 开始")

                ok = await manager.download_instance_files(instance, group_id_each)
                if not ok:
                    reason = "页面下载失败"
                    print(f"❌ {reason}，跳过 Dataset 处理: {instance_id}")
                    failure_details[instance_id] = reason
                    fail_cnt += 1
                    continue

                # 收集文件
                target_dir = manager.data_dir / group_id_each / instance_id
                md_files = list(target_dir.glob("*.md"))
                if not md_files:
                    reason = "未找到markdown文件"
                    print(f"❌ {reason}，跳过: {instance_id}")
                    failure_details[instance_id] = reason
                    fail_cnt += 1
                    # 清理空目录
                    shutil.rmtree(target_dir, ignore_errors=True)
                    continue

                file_paths = [str(f) for f in md_files]

                # 创建/获取 dataset
                dataset_id = manager.create_or_get_dataset(instance_id)
                if not dataset_id:
                    reason = "无法创建或获取dataset"
                    print(f"❌ {reason}: {instance_id}")
                    failure_details[instance_id] = reason
                    fail_cnt += 1
                    shutil.rmtree(target_dir, ignore_errors=True)
                    continue

                # 全量模式：清空并重新上传
                upload_success = manager.upload_and_parse_documents(dataset_id, file_paths, clear_existing=True)
                if not upload_success:
                    reason = "文档上传失败"
                    print(f"❌ {reason}: {instance_id}")
                    failure_details[instance_id] = reason
                    fail_cnt += 1
                    shutil.rmtree(target_dir, ignore_errors=True)
                    continue

                print(f"✅ 实例完成: {instance_id}，开始清理本地文件")
                shutil.rmtree(target_dir, ignore_errors=True)
                # 若 group 目录为空，则一并删除
                group_dir = manager.data_dir / group_id_each
                try:
                    if group_dir.exists() and not any(group_dir.iterdir()):
                        shutil.rmtree(group_dir, ignore_errors=True)
                except Exception:
                    pass

                success_cnt += 1
                if group_id_each:
                    success_groups.add(group_id_each)

            # 全量模式完成后，如有 webhook 则发送飞书通知
            try:
                webhook = os.getenv('RUN_COMPLETED_NOTE_FEISHU_WEBHOOK', '').strip()
                if webhook:
                    total_attempted = total - skipped_cnt
                    products_updated = len(success_groups)
                    failed_list = ", ".join(list(failure_details.keys())[:20])
                    text = (
                        f"AI数据全量更新完成\n"
                        f"- 产品数(成功): {products_updated}\n"
                        f"- 实例：成功 {success_cnt} / 失败 {fail_cnt} / 跳过 {skipped_cnt} / 总计(尝试) {total_attempted}\n"
                        f"- 失败实例({len(failure_details)}): {failed_list}{' 等' if len(failure_details) > 20 else ''}\n"
                    )
                    payload = {"msg_type": "text", "content": {"text": text}}
                    try:
                        resp = requests.post(webhook, json=payload, timeout=15)
                        print(f"📣 飞书通知已发送: status={resp.status_code}, body={resp.text[:200]}")
                    except Exception as ne:
                        print(f"⚠️ 飞书通知发送失败: {ne}")
                else:
                    print("ℹ️ 未配置 RUN_COMPLETED_NOTE_FEISHU_WEBHOOK，跳过飞书通知")
            except Exception as e:
                print(f"⚠️ 汇总与通知阶段发生异常: {e}")

            print(f"\n🎉 全量模式完成：成功 {success_cnt}，失败 {fail_cnt}，跳过 {skipped_cnt}")
            return

        # 非 all 模式：默认进入“指定实例更新”（不再询问下载模式）
        download_mode = "select_instances"
        selected_instances = manager.select_groups_and_instances(groups)
        if not selected_instances:
            manager.log_error("没有选择任何实例")
            return

        group_id = selected_instances[0].get('navigationInfo', {}).get('group', {}).get('id')
        instance_files = {}

        print(f"\n🚀 开始处理 {len(selected_instances)} 个实例...")

        # 5. 下载页面文件
        print(f"\n=== 第1步: 下载页面文件 ===")

        failed_instances = []
        failed_files = {}

        if download_mode == "git_changes":
            # 根据git变更下载
            print(f"📊 将根据git变更下载 {len(selected_instances)} 个实例的变更文件")
            for instance in selected_instances:
                instance_id = instance.get('id')
                success = await manager.download_git_changed_files([instance], {instance_id: instance_files.get(instance_id, [])})
                if not success:
                    failed_instances.append(instance_id)
                    failed_files[instance_id] = instance_files.get(instance_id, [])

        elif download_mode == "select_instances":
            # 选择实例下载
            print(f"📊 将下载 {len(selected_instances)} 个实例的所有文件")
            for instance in selected_instances:
                instance_id = instance.get('id')
                success = await manager.download_instance_files(instance, group_id)
                if not success:
                    failed_instances.append(instance_id)
                    failed_files[instance_id] = []  # 这里无法获取具体失败的文件列表

        if failed_instances:
            manager.log_download_errors(failed_instances, failed_files)
            print("❌ 由于下载失败，终止执行流程")
            return

        # 6. 默认处理datasets（不再交互）
        process_datasets = True

        # 7. 创建或更新datasets
        failed_datasets = []
        dataset_errors = {}

        if process_datasets:
            print(f"\n=== 第2步: 创建或更新Datasets ===")

            for instance in selected_instances:
                instance_id = instance.get('id')

                # 获取文件路径
                target_dir = manager.data_dir / group_id / instance_id
                if not target_dir.exists():
                    print(f"❌ 实例 {instance_id} 目录不存在: {target_dir}")
                    failed_datasets.append(instance_id)
                    dataset_errors[instance_id] = f"目录不存在: {target_dir}"
                    continue

                md_files = list(target_dir.glob("*.md"))
                if not md_files:
                    print(f"❌ 实例 {instance_id} 没有找到markdown文件")
                    failed_datasets.append(instance_id)
                    dataset_errors[instance_id] = "没有找到markdown文件"
                    continue

                file_paths = [str(f) for f in md_files]
                print(f"📚 处理实例 {instance_id}，找到 {len(md_files)} 个文件")

                # 创建或获取dataset
                dataset_id = manager.create_or_get_dataset(instance_id)
                if not dataset_id:
                    print(f"❌ 无法创建或获取dataset: {instance_id}")
                    failed_datasets.append(instance_id)
                    dataset_errors[instance_id] = "无法创建或获取dataset"
                    continue

                # 根据下载模式处理文档
                if download_mode == "git_changes" and instance_id in instance_files:
                    # git变更模式：先删除对应的旧文档，再上传新文档
                    changed_files = instance_files[instance_id]
                    print(f"🔄 git变更模式：处理 {len(changed_files)} 个变更文件")

                    # 获取需要删除的文档ID，传入实例信息用于文件名转换
                    document_ids_to_delete = manager.get_documents_by_filename(dataset_id, changed_files, instance)
                    if document_ids_to_delete:
                        print(f"🗑️  删除 {len(document_ids_to_delete)} 个旧文档")
                        delete_success = manager.delete_specific_documents(dataset_id, document_ids_to_delete)
                        if not delete_success:
                            print(f"⚠️  删除旧文档失败，但继续上传新文档")

                    # 上传新文档（不清空整个dataset）
                    upload_success = manager.upload_and_parse_documents(dataset_id, file_paths, clear_existing=False)
                else:
                    # 传统模式：清空并重新上传所有文档
                    upload_success = manager.upload_and_parse_documents(dataset_id, file_paths, clear_existing=True)

                if not upload_success:
                    print(f"❌ 文档上传失败: {instance_id}")
                    failed_datasets.append(instance_id)
                    dataset_errors[instance_id] = "文档上传失败"
                    continue

                print(f"✅ Dataset处理成功: {instance_id}")

            if failed_datasets:
                manager.log_dataset_errors(failed_datasets, dataset_errors)
                print("❌ 由于Dataset创建/更新失败，终止执行流程")
                return
        else:
            print(f"\n=== 第2步: 跳过Dataset处理 ===")
            print(f"⏭️  跳过Dataset处理步骤")


        print(f"\n🎉 所有步骤执行完成!")
        print(f"✅ 成功处理了 {len(selected_instances)} 个实例")

        print(f"📁 文件保存在: {manager.data_dir / group_id}")

    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断执行")
    except Exception as e:
        print(f"\n❌ 执行过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
