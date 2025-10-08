#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全新的AI数据更新脚本
整合页面下载、dataset创建/更新、assistant创建/更新功能
"""

import json
import re
import asyncio
import sys
import os
import time
import shutil
import requests
import xml.etree.ElementTree as ET
import subprocess
import logging
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

# 导入现有模块
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    import requests
    print(f"✅ requests 已加载，版本: {requests.__version__}")
except ImportError as e:
    print(f"❌ 需要安装 requests: pip install requests")
    requests = None

try:
    from crawl4ai import AsyncWebCrawler
    CRAWL4AI_AVAILABLE = True
except ImportError:
    print("需要安装 crawl4ai: pip install crawl4ai")
    CRAWL4AI_AVAILABLE = False
    AsyncWebCrawler = None

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
        self.ragflow_base_url = os.getenv('RAGFLOW_BASE_URL', '')
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
        self.assistant_errors = {}
    
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
        """从sitemap获取匹配的URLs"""
        try:
            print(f"正在获取sitemap: {self.sitemap_url}")

            if requests is None:
                self.log_error("requests 模块不可用，无法获取sitemap")
                return []

            response = requests.get(self.sitemap_url, timeout=30)
            response.raise_for_status()

            root = ET.fromstring(response.content)
            namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

            urls = []
            url_elements = root.findall('.//ns:url', namespaces)
            if len(url_elements) == 0:
                url_elements = root.findall('.//url')

            # 构建匹配模式
            pattern = f"{self.base_url}{route_base_path}"

            for url_elem in url_elements:
                loc_elem = url_elem.find('ns:loc', namespaces)
                if loc_elem is None:
                    loc_elem = url_elem.find('loc')

                if loc_elem is not None and loc_elem.text:
                    url = loc_elem.text.strip()
                    if url.startswith(pattern):
                        urls.append(url)

            print(f"匹配到 {len(urls)} 个URLs (模式: {pattern})")
            return urls

        except Exception as e:
            self.log_error(f"获取sitemap失败: {e}")
            return []

    def get_filename_from_url(self, url: str, title: str = "") -> str:
        """根据URL生成文件名"""
        parsed = urlparse(url)

        if title:
            clean_title = re.sub(r'[^\w\s-]', '', title).strip()
            clean_title = re.sub(r'[-\s]+', '-', clean_title)
            base_name = f"{clean_title}---{parsed.netloc}{parsed.path}"
        else:
            base_name = f"{parsed.netloc}{parsed.path}"

        filename = base_name.replace("/", ">").replace("&", "^^").replace('=', '^^^')
        return f"{filename}.md"

    async def download_url_content(self, url: str, target_dir: Path) -> bool:
        """下载单个URL的内容，支持重试"""
        if not CRAWL4AI_AVAILABLE:
            self.log_error(f"crawl4ai 未安装: {url}")
            return False

        for attempt in range(self.config.max_retries):
            try:
                async with AsyncWebCrawler(verbose=False) as crawler:
                    result = await crawler.arun(
                        url=url,
                        word_count_threshold=10,
                        extraction_strategy="NoExtractionStrategy",
                        chunking_strategy="RegexChunking",
                        bypass_cache=True
                    )

                    if result.success:
                        title = result.metadata.get('title', '') if result.metadata else ''
                        filename = self.get_filename_from_url(url, title)
                        file_path = target_dir / filename

                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(f"# {title}\n\n")
                            f.write(f"**URL:** {url}\n\n")
                            f.write("---\n\n")
                            f.write(result.markdown)

                        print(f"✅ 下载成功: {url}")
                        return True
                    else:
                        self.log_error(f"下载失败 (尝试 {attempt + 1}/{self.config.max_retries}): {url} - {result.error_message}")
                        if attempt < self.config.max_retries - 1:
                            await asyncio.sleep(self.config.retry_delay * (2 ** attempt))  # 指数退避

            except Exception as e:
                self.log_error(f"下载异常 (尝试 {attempt + 1}/{self.config.max_retries}): {url} - {str(e)}")
                if attempt < self.config.max_retries - 1:
                    await asyncio.sleep(self.config.retry_delay * (2 ** attempt))  # 指数退避

        self.log_error(f"下载最终失败: {url}")
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

            while True:
                choice = input(f"是否重新下载所有文件? (y/n, 默认y): ").strip().lower()
                if choice in ['', 'y', 'yes']:
                    print(f"🗑️  删除已存在的目录: {target_dir}")
                    shutil.rmtree(target_dir)
                    target_dir.mkdir(parents=True, exist_ok=True)
                    break
                elif choice in ['n', 'no']:
                    print(f"✅ 跳过下载，使用现有文件")
                    return True
                else:
                    print("请输入 y 或 n")
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
            tasks = [self.download_url_content(url, target_dir) for url in batch]
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
                tasks = [self.download_url_content(url, target_dir) for url in batch]
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
                headers=headers
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

        headers = {
            'Authorization': f'Bearer {self.config.api_key}',
            'Content-Type': 'application/json'
        }

        try:
            # 先查找是否存在
            response = requests.get(
                f"{self.config.ragflow_base_url}/datasets?name={dataset_name}",
                headers=headers
            )
            data = response.json()

            if data.get('code') == 0 and data.get('data'):
                dataset_id = data['data'][0]['id']
                print(f"✅ 找到已存在的知识库: {dataset_id}")
                return dataset_id

            # 创建新的dataset
            config = {
                'name': dataset_name,
                'language': 'Chinese' if self.language == 'zh' else 'English',
                'permission': 'team',
                'embedding_model': os.getenv('RAGFLOW_EMBEDDING_MODEL_ZH', 'BAAI/bge-small-zh-v1.5') if self.language == 'zh' else os.getenv('RAGFLOW_EMBEDDING_MODEL_EN', 'BAAI/bge-small-en-v1.5'),
                'parser_config': {'chunk_token_num': os.getenv('RAGFLOW_CHUNK_TOKEN_NUM', 512)}
            }

            response = requests.post(
                f"{self.config.ragflow_base_url}/datasets",
                headers=headers,
                json=config
            )
            data = response.json()

            if data.get('code') == 0:
                dataset_id = data['data']['id']
                print(f"✅ 创建知识库成功: {dataset_id}")
                return dataset_id
            else:
                self.log_error(f"创建知识库失败: {data.get('message')}")
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
                    json={'ids': []}
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

    def get_group_questions(self, config_data: Dict, group_id: str) -> List[str]:
        """从同一group的其他实例中获取questions"""
        all_questions = []
        instances = config_data.get('instances', [])

        for instance in instances:
            nav_info = instance.get('navigationInfo', {})
            instance_group_id = nav_info.get('group', {}).get('id')

            if instance_group_id == group_id:
                questions = instance.get('askAi', {}).get('questions', [])
                if questions:
                    all_questions.extend(questions)

        # 去重并保持顺序
        unique_questions = []
        for q in all_questions:
            if q not in unique_questions:
                unique_questions.append(q)

        return unique_questions

    def generate_ai_search_mapping(self, selected_instances: List[Dict], group_id: str, config_data: Dict) -> Dict:
        """生成或更新AI搜索映射配置"""
        print(f"\n🔧 生成AI搜索映射配置...")

        # 加载现有配置
        mapping_file = self.static_data_dir / "ai_search_mapping.json"
        if mapping_file.exists():
            with open(mapping_file, 'r', encoding='utf-8') as f:
                mapping_config = json.load(f)
        else:
            mapping_config = {}

        # 确保group存在
        if group_id not in mapping_config:
            mapping_config[group_id] = {}

        # 获取同group的questions作为默认值
        group_questions = self.get_group_questions(config_data, group_id)
        print(f"📋 从同group获取到 {len(group_questions)} 个默认问题")

        # 为每个instance生成配置
        for instance in selected_instances:
            instance_id = instance.get('id')
            platform = instance.get('navigationInfo', {}).get('platform', 'Unknown')
            instance_questions = instance.get('askAi', {}).get('questions', [])

            # 如果实例没有questions，使用同group的questions
            questions = instance_questions if instance_questions else group_questions

            # dataset_names包含instance_id和FAQ
            dataset_names = [instance_id, self.faq_dataset_name]

            assistant_name = instance_id

            mapping_config[group_id][platform] = {
                "dataset_names": dataset_names,
                "assistant_name": assistant_name,
                "questions": questions,
                "chat_id": ""  # 将在创建assistant后更新
            }

            questions_source = "实例自有" if instance_questions else "同group默认"
            print(f"📝 {platform}: 使用了 {len(questions)} 个问题 ({questions_source})")

        # 保存配置
        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump(mapping_config, f, ensure_ascii=False, indent=2)

        print(f"✅ AI搜索映射配置已更新: {mapping_file}")
        return mapping_config

    def create_or_update_assistant(self, assistant_name: str, dataset_names: List[str]) -> Optional[str]:
        """创建或更新assistant，支持对code 102错误进行重试"""
        print(f"🤖 处理Assistant: {assistant_name}")

        if not requests:
            self.log_error("requests 未安装，无法处理Assistant")
            return None

        headers = {
            'Authorization': f'Bearer {self.config.api_key}',
            'Content-Type': 'application/json'
        }

        max_retries_for_102 = 3
        retry_delay_for_102 = 10  # 10秒

        for attempt in range(max_retries_for_102 + 1):  # 0, 1, 2, 3 共4次尝试（1次初始 + 3次重试）
            try:
                # 获取datasets映射
                dataset_ids = []
                for dataset_name in dataset_names:
                    dataset_id = self.create_or_get_dataset(dataset_name)
                    if dataset_id:
                        dataset_ids.append(dataset_id)
                    else:
                        self.log_error(f"无法获取dataset: {dataset_name}")
                        return None

                if not dataset_ids:
                    self.log_error("没有有效的dataset IDs")
                    return None

                # 检查是否已存在
                response = requests.get(
                    f"{self.config.ragflow_base_url}/chats",
                    headers=headers,
                    params={"name": assistant_name}
                )
                data = response.json()

                existing_id = None
                if data.get('code') == 0 and data.get('data'):
                    existing_id = data['data'][0]['id']
                    print(f"找到已存在的Assistant: {existing_id}")

                # 准备payload
                is_chinese = self.language == 'zh'
                empty_response = "非常抱歉，知识库中暂时找不到相关信息，请尝试更详细描述你的问题或者尝试其他问题。" if is_chinese else "Sorry, no relevant information found in the knowledge base. Please try to describe your question in more detail or try other questions."

                # 简化的prompt模板
                prompt_template = """
# 角色
你是一个智能助手，名字叫Miss Z。你的主要职责是基于知识库中的信息来总结并回答用户的问题。

## 技能
### 技能1: 回答简单问题
- 如果问题可以用一个接口、一个配置或者一句简短的话回答则是简单问题
- 简单明确的问题则直接用最简短的答案回答即可
- 简单问题不需要提供示例代码
- 如果一些操作有前提条件或者其他要求则也需要明确告知用户

### 技能2: 回答复杂问题
- 如果问题需要通过多个步骤或者多个接口配合实现的那么就是复杂问题
- 先根据知识库内容简要总结说明实现步骤
- 每个步骤配合最简洁且必要的示例代码说明

### 技能3: 多语言支持
- 使用中文进行回答，确保沟通无障碍

### 技能4: 提示
- 每次回答最后都提示用户：如果有任何疑问，请联系 ZEGO 技术支持。

## 限制
- 绝对不能捏造信息，特别是涉及到数字和代码时，必须保证信息的准确性
- 回答格式需遵循Markdown规范，使答案结构清晰、易读
- 当知识库中的信息与用户问题无关时，直接回复："{empty_response}"
- 所有回答都应基于知识库中的现有资料，不得超出其范围

## 知识库
{{knowledge}}

以上就是相关的知识。
""" if is_chinese else """
# Role
You are an intelligent assistant named Miss Z. Your primary duty is to summarize and answer user questions based on the information in the knowledge base.

## Skills
### Skill 1: Answering Simple Questions
- A simple question is one that can be answered with a single interface, configuration, or a brief statement
- For straightforward questions, provide the most concise answer possible
- Simple questions do not require example code
- If there are prerequisites or other requirements, make sure to inform the user clearly

### Skill 2: Answering Complex Questions
- A complex question requires multiple steps or interfaces to be addressed
- Begin by briefly summarizing the implementation steps based on the knowledge base content
- Provide the most concise and necessary example code for each step

### Skill 3: Multilingual Support
- Answer in English to ensure smooth communication

### Skill 4: Reminder
- End each response with: If you have any questions, please contact ZEGOCLOUD technical support.

## Limitations
- Never fabricate information, especially when it involves numbers and code; accuracy is crucial
- Follow Markdown format for clear and readable answers
- When the knowledge base information is irrelevant to the user's question, reply: "{empty_response}"
- All responses should be based on existing materials in the knowledge base and should not exceed its scope

## Knowledge Base
{{knowledge}}

Above is the relevant knowledge.
"""

                payload = {
                    "name": assistant_name,
                    "dataset_ids": dataset_ids,
                    "llm": {
                        "model_name": "qwen-plus",
                        "frequency_penalty": 0.7,
                        "max_tokens": 4096,
                        "presence_penalty": 0.4,
                        "temperature": 0.1,
                        "top_p": 0.3
                    },
                    "prompt": {
                        "empty_response": empty_response,
                        "prompt": prompt_template.format(empty_response=empty_response)
                    }
                }

                if existing_id:
                    # 更新
                    response = requests.put(
                        f"{self.config.ragflow_base_url}/chats/{existing_id}",
                        headers=headers,
                        json=payload
                    )
                    action = "更新"
                    assistant_id = existing_id
                else:
                    # 创建
                    response = requests.post(
                        f"{self.config.ragflow_base_url}/chats",
                        headers=headers,
                        json=payload
                    )
                    action = "创建"

                data = response.json()
                
                # 检查响应码
                if data.get('code') == 0:
                    # 成功
                    if existing_id:
                        assistant_id = existing_id
                    else:
                        assistant_id = data.get('data', {}).get('id')
                    
                    if assistant_id:
                        print(f"✅ {action}Assistant成功: {assistant_name} (ID: {assistant_id})")
                        return assistant_id
                    else:
                        self.log_error(f"{action}Assistant失败，未获取到ID: {assistant_name}")
                        return None
                        
                elif data.get('code') == 102:
                    # code 102 错误，需要重试
                    if attempt < max_retries_for_102:
                        print(f"⚠️  {action}Assistant遇到code 102错误 (尝试 {attempt + 1}/{max_retries_for_102 + 1}): {assistant_name} {data}")
                        print(f"⏳ 等待 {retry_delay_for_102} 秒后重试...")
                        time.sleep(retry_delay_for_102)
                        continue
                    else:
                        self.log_error(f"{action}Assistant失败，code 102 重试 {max_retries_for_102} 次后仍然失败: {assistant_name}")
                        return None
                else:
                    # 其他错误码，直接失败不重试
                    self.log_error(f"{action}Assistant失败，错误码 {data.get('code')}: {assistant_name} - {data.get('message', '未知错误')}")
                    return None

            except Exception as e:
                if attempt < max_retries_for_102:
                    self.log_error(f"处理Assistant异常 (尝试 {attempt + 1}/{max_retries_for_102 + 1}): {assistant_name} - {e}")
                    print(f"⏳ 等待 {retry_delay_for_102} 秒后重试...")
                    time.sleep(retry_delay_for_102)
                    continue
                else:
                    self.log_error(f"处理Assistant异常，重试 {max_retries_for_102} 次后仍然失败: {assistant_name} - {e}")
                    return None

        # 如果到达这里，说明所有重试都失败了
        return None

    def update_mapping_with_chat_ids(self, mapping_config: Dict, group_id: str, selected_instances: List[Dict]) -> List[str]:
        """更新映射配置中的chat_id，返回失败的Assistant列表"""
        print(f"\n🔄 更新映射配置中的chat_id...")

        failed_assistants = []

        for instance in selected_instances:
            platform = instance.get('navigationInfo', {}).get('platform', 'Unknown')
            instance_id = instance.get('id')

            if group_id in mapping_config and platform in mapping_config[group_id]:
                assistant_name = mapping_config[group_id][platform]['assistant_name']
                dataset_names = mapping_config[group_id][platform]['dataset_names']

                print(f"🤖 处理Assistant: {assistant_name}")

                # 创建或更新assistant
                chat_id = self.create_or_update_assistant(assistant_name, dataset_names)
                if chat_id:
                    mapping_config[group_id][platform]['chat_id'] = chat_id
                    print(f"✅ Assistant处理成功: {assistant_name}")
                else:
                    failed_assistants.append(assistant_name)
                    self.log_error(f"Assistant处理失败: {assistant_name}")
            else:
                print(f"⚠️  未找到映射配置: {group_id}/{platform}")
                failed_assistants.append(f"{instance_id}-{platform}")

        # 保存更新后的配置
        mapping_file = self.static_data_dir / "ai_search_mapping.json"
        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump(mapping_config, f, ensure_ascii=False, indent=2)

        if failed_assistants:
            print(f"⚠️  {len(failed_assistants)} 个Assistant处理失败")
        else:
            print(f"✅ 所有Assistant处理成功")

        print(f"✅ 映射配置已更新完成")
        return failed_assistants

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
    
    def log_assistant_errors(self, failed_assistants: List[str], error_details: Dict[str, str]):
        """记录Assistant处理错误"""
        if failed_assistants:
            print("\n=== Assistant处理错误总结 ===")
            print(f"❌ 以下Assistant处理失败:")
            for assistant in failed_assistants:
                print(f"  - {assistant}")
                if assistant in error_details:
                    print(f"    错误原因: {error_details[assistant]}")

async def main():
    """主函数"""
    manager = UpdateAIDataManager()

    print("=== AI数据更新脚本 ===")
    print("本脚本将完整执行：页面下载 -> Dataset更新 -> Assistant更新")

    try:
        # 1. 选择语言
        manager.select_language()

        # 2. 加载配置文件
        print(f"\n📖 加载配置文件: {manager.config_file}")
        config_data = manager.load_config_file()

        # 3. 提取groups
        groups = manager.get_groups_from_config(config_data)
        if not groups:
            manager.log_error("配置文件中没有找到有效的groups")
            return

        print(f"✅ 找到 {len(groups)} 个产品组")

        # 4. 选择下载模式
        download_mode = manager.select_download_mode()

        selected_instances = []
        instance_files = {}
        group_id = None

        if download_mode == "git_changes":
            # 根据git变更记录下载
            affected_instances, instance_files = manager.select_git_commit_and_get_changes(config_data)
            if not affected_instances:
                manager.log_error("没有找到受影响的实例")
                return

            selected_instances = affected_instances
            group_id = selected_instances[0].get('navigationInfo', {}).get('group', {}).get('id')

        elif download_mode == "select_instances":
            # 选择指定实例更新
            selected_instances = manager.select_groups_and_instances(groups)
            if not selected_instances:
                manager.log_error("没有选择任何实例")
                return

            group_id = selected_instances[0].get('navigationInfo', {}).get('group', {}).get('id')

        elif download_mode == "skip_download":
            # 跳过下载，但仍需要选择实例进行后续处理
            selected_instances = manager.select_groups_and_instances(groups)
            if not selected_instances:
                manager.log_error("没有选择任何实例")
                return

            group_id = selected_instances[0].get('navigationInfo', {}).get('group', {}).get('id')

        if not group_id:
            print("❌ 无法获取group_id")
            return

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

        # 6. 选择是否处理datasets
        process_datasets = manager.select_dataset_mode()

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
            print(f"⏭️  跳过Dataset处理步骤，直接进入Assistant处理")

        # 8. 生成AI搜索映射配置
        print(f"\n=== 第3步: 生成AI搜索映射配置 ===")
        mapping_config = manager.generate_ai_search_mapping(selected_instances, group_id, config_data)

        # 9. 创建或更新Assistants
        print(f"\n=== 第4步: 创建或更新Assistants ===")
        failed_assistants = []
        assistant_errors = {}

        for instance in selected_instances:
            platform = instance.get('navigationInfo', {}).get('platform', 'Unknown')
            instance_id = instance.get('id')

            if group_id in mapping_config and platform in mapping_config[group_id]:
                assistant_name = mapping_config[group_id][platform]['assistant_name']
                dataset_names = mapping_config[group_id][platform]['dataset_names']

                print(f"🤖 处理Assistant: {assistant_name}")

                # 创建或更新assistant
                chat_id = manager.create_or_update_assistant(assistant_name, dataset_names)
                if chat_id:
                    mapping_config[group_id][platform]['chat_id'] = chat_id
                    print(f"✅ Assistant处理成功: {assistant_name}")
                else:
                    failed_assistants.append(assistant_name)
                    assistant_errors[assistant_name] = "创建或更新失败"
                    print(f"❌ Assistant处理失败: {assistant_name}")
            else:
                print(f"⚠️  未找到映射配置: {group_id}/{platform}")
                failed_assistants.append(f"{instance_id}-{platform}")
                assistant_errors[f"{instance_id}-{platform}"] = "未找到映射配置"

        if failed_assistants:
            manager.log_assistant_errors(failed_assistants, assistant_errors)
            print("⚠️  部分Assistant处理失败，但不影响其他功能的正常使用")

        print(f"\n🎉 所有步骤执行完成!")
        print(f"✅ 成功处理了 {len(selected_instances)} 个实例")

        print(f"📁 文件保存在: {manager.data_dir / group_id}")
        print(f"🔧 配置文件: {manager.static_data_dir / 'ai_search_mapping.json'}")

    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断执行")
    except Exception as e:
        print(f"\n❌ 执行过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
