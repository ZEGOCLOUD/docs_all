#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import re
import shutil
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
from datetime import datetime
import urllib.parse

class PathResolver:
    """路径解析工具类"""

    def __init__(self, workspace_root: str):
        self.workspace_root = os.path.abspath(workspace_root).replace('\\', '/')

    def normalize_path(self, file_path: str) -> str:
        """标准化路径（统一使用正斜杠）"""
        return file_path.replace('\\', '/')

    def get_relative_to_workspace(self, file_path: str) -> str:
        """获取相对于工作区的路径"""
        normalized = self.normalize_path(os.path.abspath(file_path))
        workspace_normalized = self.normalize_path(self.workspace_root)

        if normalized.startswith(workspace_normalized):
            return normalized[len(workspace_normalized):].lstrip('/')
        return normalized

    def get_absolute_path(self, relative_path: str) -> str:
        """获取绝对路径"""
        if os.path.isabs(relative_path):
            return self.normalize_path(relative_path)
        return self.normalize_path(os.path.join(self.workspace_root, relative_path))

    def get_relative_path(self, from_file: str, to_file: str) -> str:
        """计算相对路径"""
        from_dir = os.path.dirname(from_file)
        relative_path = os.path.relpath(to_file, from_dir)
        return self.normalize_path(relative_path)

    def decode_url_path(self, url_path: str) -> str:
        """解码URL编码的路径"""
        try:
            return urllib.parse.unquote(url_path)
        except Exception as e:
            print(f"警告：解码URL路径失败: {url_path}, {e}")
            return url_path

    def encode_url_path(self, file_path: str) -> str:
        """编码路径为URL编码格式"""
        try:
            # 编码特殊字符，但保留正斜杠作为路径分隔符
            return urllib.parse.quote(file_path, safe='/')
        except Exception as e:
            print(f"警告：编码URL路径失败: {file_path}, {e}")
            return file_path

class FileReference:
    """文件引用信息"""

    def __init__(self, file_path: str, line: int, column: int, text: str, ref_type: str):
        self.file_path = file_path
        self.line = line
        self.column = column
        self.text = text
        self.type = ref_type  # 'import', 'link', 'internal-link'

class LinkUpdater:
    """链接更新器"""

    def __init__(self, path_resolver: PathResolver, workspace_root: str):
        self.path_resolver = path_resolver
        self.workspace_root = workspace_root
        self.docuo_config = self._load_docuo_config()

    def _load_docuo_config(self) -> Optional[Dict]:
        """加载 docuo.config.json 配置"""
        config_path = os.path.join(self.workspace_root, 'docuo.config.json')
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"警告：无法加载 docuo.config.json: {e}")
        return None

    def find_instance_by_file_path(self, file_path: str) -> Optional[Dict]:
        """根据文件路径找到对应的实例"""
        if not self.docuo_config or 'instances' not in self.docuo_config:
            return None

        relative_path = self.path_resolver.get_relative_to_workspace(file_path)

        for instance in self.docuo_config['instances']:
            instance_path = self.path_resolver.normalize_path(instance['path'])
            if relative_path.startswith(instance_path):
                return instance

        return None

    def get_file_id(self, file_path: str, instance_root_path: str) -> str:
        """将文件路径转换为文件ID"""
        relative_path = os.path.relpath(file_path, instance_root_path)
        file_path_without_extension = os.path.splitext(relative_path)[0]
        id_path = file_path_without_extension.lower().replace(' ', '-')

        # 处理路径段，移除数字前缀
        segments = id_path.split('/')
        sanitized_segments = [self._sanitize_path_segment(segment) for segment in segments]

        return '/'.join(sanitized_segments)

    def _sanitize_path_segment(self, segment: str) -> str:
        """清理路径段（移除数字前缀）"""
        return re.sub(r'^\d+-', '', segment)

    def parse_imports(self, file_path: str) -> List[FileReference]:
        """解析文件中的导入语句"""
        references = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line_index, line in enumerate(lines):
                # 匹配 import 语句: import Content from '/path/to/file.mdx'
                import_pattern = r'import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]'
                matches = re.finditer(import_pattern, line)

                for match in matches:
                    import_path = match.group(1)
                    # 只处理以 / 开头的路径（相对于工作区根目录）
                    if import_path.startswith('/'):
                        references.append(FileReference(
                            file_path, line_index, match.start(), match.group(0), 'import'
                        ))
        except Exception as e:
            print(f"警告：解析导入语句失败 {file_path}: {e}")

        return references

    def parse_links(self, file_path: str) -> List[FileReference]:
        """解析文件中的链接语句"""
        references = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line_index, line in enumerate(lines):
                # 匹配 Markdown 链接: [text](./path/to/file.mdx)
                link_pattern = r'\[([^\]]*)\]\((\.[^)]+)\)'
                matches = re.finditer(link_pattern, line)

                for match in matches:
                    link_path = match.group(2)
                    # 只处理以 ./ 开头的相对路径
                    if link_path.startswith('./'):
                        references.append(FileReference(
                            file_path, line_index, match.start(), match.group(0), 'link'
                        ))
        except Exception as e:
            print(f"警告：解析链接语句失败 {file_path}: {e}")

        return references

    def parse_internal_links(self, file_path: str) -> List[FileReference]:
        """解析文件中的站内链接语句"""
        references = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line_index, line in enumerate(lines):
                # 匹配站内链接: [text](/route-base-path/file-id)
                internal_link_pattern = r'\[([^\]]*)\]\(\/([^)]+)\)'
                matches = re.finditer(internal_link_pattern, line)

                for match in matches:
                    link_path = match.group(2)
                    # 确保这不是一个import路径（import路径通常指向文件扩展名）
                    if not re.match(r'.*\.(md|mdx)$', link_path, re.IGNORECASE):
                        references.append(FileReference(
                            file_path, line_index, match.start(), match.group(0), 'internal-link'
                        ))
        except Exception as e:
            print(f"警告：解析站内链接语句失败 {file_path}: {e}")

        return references

    def find_all_references(self, target_file_path: str) -> Tuple[List[FileReference], List[FileReference], List[FileReference]]:
        """查找所有引用指定文件的链接"""
        import_refs = []
        link_refs = []
        internal_link_refs = []

        target_relative_path = '/' + self.path_resolver.get_relative_to_workspace(target_file_path)

        # 查找目标文件所在的实例
        target_instance = self.find_instance_by_file_path(target_file_path)

        # 遍历工作区中的所有 md/mdx 文件
        for root, dirs, files in os.walk(self.workspace_root):
            # 跳过 node_modules 等目录
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '__pycache__']]

            for file in files:
                if file.endswith(('.md', '.mdx')):
                    file_path = os.path.join(root, file)

                    # 解析导入引用
                    imports = self.parse_imports(file_path)
                    for import_ref in imports:
                        try:
                            with open(import_ref.file_path, 'r', encoding='utf-8') as f:
                                lines = f.readlines()
                            line = lines[import_ref.line]
                            match = re.search(r'import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]', line)
                            if match and match.group(1) == target_relative_path:
                                import_refs.append(import_ref)
                        except Exception:
                            continue

                    # 解析链接引用（仅在同实例内）
                    if target_instance:
                        file_instance = self.find_instance_by_file_path(file_path)
                        if file_instance and file_instance['id'] == target_instance['id']:
                            links = self.parse_links(file_path)
                            for link_ref in links:
                                try:
                                    with open(link_ref.file_path, 'r', encoding='utf-8') as f:
                                        lines = f.readlines()
                                    line = lines[link_ref.line]
                                    match = re.search(r'\[([^\]]*)\]\((\.[^)]+)\)', line)
                                    if match:
                                        link_path = match.group(2)
                                        resolved_path = self._resolve_link_path(link_path, link_ref.file_path)
                                        if self.path_resolver.normalize_path(resolved_path) == self.path_resolver.normalize_path(target_file_path):
                                            link_refs.append(link_ref)
                                except Exception:
                                    continue

                    # 解析站内链接引用（整个工作区范围内）
                    if target_instance:
                        internal_links = self.parse_internal_links(file_path)
                        for internal_link_ref in internal_links:
                            try:
                                with open(internal_link_ref.file_path, 'r', encoding='utf-8') as f:
                                    lines = f.readlines()
                                line = lines[internal_link_ref.line]
                                match = re.search(r'\[([^\]]*)\]\(\/([^)]+)\)', line)
                                if match:
                                    link_path = f"/{match.group(2)}"
                                    # 计算目标文件的站内URL
                                    instance_abs_path = self.path_resolver.get_absolute_path(target_instance['path'])
                                    target_file_id = self.get_file_id(target_file_path, instance_abs_path)
                                    target_internal_url = f"/{target_instance['routeBasePath']}/{target_file_id}"

                                    if link_path == target_internal_url:
                                        internal_link_refs.append(internal_link_ref)
                            except Exception:
                                continue

        return import_refs, link_refs, internal_link_refs

    def _resolve_link_path(self, link_path: str, from_file: str) -> str:
        """解析链接路径为绝对路径"""
        if link_path.startswith('./'):
            from_dir = os.path.dirname(from_file)
            # 对URL编码的路径进行解码
            decoded_path = self.path_resolver.decode_url_path(link_path)
            return self.path_resolver.normalize_path(os.path.abspath(os.path.join(from_dir, decoded_path)))
        return link_path

    def _is_url_encoded(self, path: str) -> bool:
        """检查路径是否使用了URL编码"""
        return bool(re.search(r'%[0-9A-Fa-f]{2}', path))

    def update_file_references(self, old_path: str, new_path: str) -> Dict[str, List[str]]:
        """更新文件引用，返回更新的文件列表"""
        updated_files = {
            'import': [],
            'link': [],
            'internal-link': [],
            'sidebar': []
        }

        # 查找所有引用
        import_refs, link_refs, internal_link_refs = self.find_all_references(old_path)

        # 更新导入引用
        for ref in import_refs:
            if self._update_import_reference(ref, old_path, new_path):
                updated_files['import'].append(ref.file_path)

        # 更新链接引用
        for ref in link_refs:
            if self._update_link_reference(ref, old_path, new_path):
                updated_files['link'].append(ref.file_path)

        # 更新站内链接引用
        for ref in internal_link_refs:
            if self._update_internal_link_reference(ref, old_path, new_path):
                updated_files['internal-link'].append(ref.file_path)

        # 更新 sidebars.json
        if self._update_sidebar_references(old_path, new_path):
            updated_files['sidebar'].append('sidebars.json')

        return updated_files

    def _update_import_reference(self, ref: FileReference, old_path: str, new_path: str) -> bool:
        """更新导入引用"""
        try:
            with open(ref.file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            old_relative_path = '/' + self.path_resolver.get_relative_to_workspace(old_path)
            new_relative_path = '/' + self.path_resolver.get_relative_to_workspace(new_path)

            new_content = content.replace(old_relative_path, new_relative_path)

            if new_content != content:
                with open(ref.file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                return True
        except Exception as e:
            print(f"警告：更新导入引用失败 {ref.file_path}: {e}")

        return False

    def _update_link_reference(self, ref: FileReference, old_path: str, new_path: str) -> bool:
        """更新链接引用"""
        try:
            with open(ref.file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            line = lines[ref.line]
            match = re.search(r'\[([^\]]*)\]\((\.[^)]+)\)', line)
            if not match:
                return False

            link_text = match.group(1)
            old_link_path = match.group(2)

            # 计算新的相对路径
            new_relative_path = './' + self.path_resolver.get_relative_path(ref.file_path, new_path)

            # 检查原链接是否使用了URL编码
            if self._is_url_encoded(old_link_path):
                path_without_prefix = new_relative_path[2:]  # 移除 ./
                encoded_path = self.path_resolver.encode_url_path(path_without_prefix)
                new_relative_path = './' + encoded_path

            new_link_text = f"[{link_text}]({new_relative_path})"
            new_line = line.replace(match.group(0), new_link_text)
            lines[ref.line] = new_line

            with open(ref.file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)

            return True
        except Exception as e:
            print(f"警告：更新链接引用失败 {ref.file_path}: {e}")

        return False

    def _update_internal_link_reference(self, ref: FileReference, old_path: str, new_path: str) -> bool:
        """更新站内链接引用"""
        try:
            with open(ref.file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            line = lines[ref.line]
            match = re.search(r'\[([^\]]*)\]\(\/([^)]+)\)', line)
            if not match:
                return False

            link_text = match.group(1)

            # 获取新文件所在的实例
            new_instance = self.find_instance_by_file_path(new_path)
            if not new_instance:
                return False

            # 计算新的文件ID和站内URL
            instance_abs_path = self.path_resolver.get_absolute_path(new_instance['path'])
            new_file_id = self.get_file_id(new_path, instance_abs_path)
            new_internal_url = f"/{new_instance['routeBasePath']}/{new_file_id}"

            new_link_text = f"[{link_text}]({new_internal_url})"
            new_line = line.replace(match.group(0), new_link_text)
            lines[ref.line] = new_line

            with open(ref.file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)

            return True
        except Exception as e:
            print(f"警告：更新站内链接引用失败 {ref.file_path}: {e}")

        return False

    def _update_sidebar_references(self, old_path: str, new_path: str) -> bool:
        """更新 sidebars.json 文件中的ID引用"""
        try:
            # 查找实例根目录
            instance_root_dir = self._find_instance_root_dir(old_path)
            if not instance_root_dir:
                return False

            sidebar_path = os.path.join(instance_root_dir, 'sidebars.json')
            if not os.path.exists(sidebar_path):
                return False

            # 计算旧的和新的ID
            old_id = self.get_file_id(old_path, instance_root_dir)
            new_id = self.get_file_id(new_path, instance_root_dir)

            if old_id == new_id:
                return False

            # 读取sidebars.json文件
            with open(sidebar_path, 'r', encoding='utf-8') as f:
                content = f.read()

            sidebar_data = json.loads(content)

            # 递归更新ID引用
            updated = self._update_sidebar_ids(sidebar_data, old_id, new_id)

            if updated:
                # 写回文件
                with open(sidebar_path, 'w', encoding='utf-8') as f:
                    json.dump(sidebar_data, f, indent=2, ensure_ascii=False)
                return True

            return False
        except Exception as e:
            print(f"警告：更新sidebars.json失败: {e}")
            return False

    def _find_instance_root_dir(self, file_path: str) -> Optional[str]:
        """查找实例根目录（包含sidebars.json的目录）"""
        current_dir = os.path.dirname(file_path)
        while current_dir != os.path.dirname(current_dir):
            if os.path.exists(os.path.join(current_dir, 'sidebars.json')):
                return current_dir
            current_dir = os.path.dirname(current_dir)
        return None

    def _update_sidebar_ids(self, obj, old_id: str, new_id: str) -> bool:
        """递归更新sidebars.json中的ID引用"""
        updated = False

        if isinstance(obj, list):
            for item in obj:
                if self._update_sidebar_ids(item, old_id, new_id):
                    updated = True
        elif isinstance(obj, dict):
            if obj.get('id') == old_id:
                obj['id'] = new_id
                updated = True
                print(f"更新 sidebar ID: {old_id} -> {new_id}")

            for value in obj.values():
                if self._update_sidebar_ids(value, old_id, new_id):
                    updated = True

        return updated

class RenameLogger:
    """重命名操作日志记录器"""

    def __init__(self, log_file: str = 'rename.log'):
        self.log_file = log_file
        self.logs = {}
        self.start_time = datetime.now()

    def add_target(self, target: str):
        """添加目标目录"""
        if target not in self.logs:
            self.logs[target] = {
                'success': [],
                'failed': [],
                'skipped': []
            }

    def log_success(self, target: str, action: str, details: str = ''):
        """记录成功操作"""
        self.add_target(target)
        self.logs[target]['success'].append({
            'action': action,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })

    def log_failure(self, target: str, action: str, error: str):
        """记录失败操作"""
        self.add_target(target)
        self.logs[target]['failed'].append({
            'action': action,
            'error': error,
            'timestamp': datetime.now().isoformat()
        })

    def log_skip(self, target: str, action: str, reason: str):
        """记录跳过操作"""
        self.add_target(target)
        self.logs[target]['skipped'].append({
            'action': action,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        })

    def write_log(self):
        """写入日志文件"""
        log_data = {
            'summary': {
                'start_time': self.start_time.isoformat(),
                'end_time': datetime.now().isoformat(),
                'total_targets': len(self.logs),
                'total_success': sum(len(target_log['success']) for target_log in self.logs.values()),
                'total_failed': sum(len(target_log['failed']) for target_log in self.logs.values()),
                'total_skipped': sum(len(target_log['skipped']) for target_log in self.logs.values())
            },
            'details': self.logs
        }

        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
            print(f"日志已写入: {self.log_file}")
        except Exception as e:
            print(f"警告：写入日志文件失败: {e}")

class RenameScript:
    """重命名脚本主类"""

    def __init__(self, workspace_root: str, config_file: str = None):
        self.workspace_root = os.path.abspath(workspace_root)
        self.config_file = config_file or os.path.join(self.workspace_root, 'rename.json')
        self.path_resolver = PathResolver(self.workspace_root)
        self.link_updater = LinkUpdater(self.path_resolver, self.workspace_root)
        self.logger = RenameLogger()

        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"配置文件不存在: {self.config_file}")

    def load_config(self) -> Dict:
        """加载配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            if 'target' not in config or 'action' not in config:
                raise ValueError("配置文件必须包含 'target' 和 'action' 字段")

            return config
        except Exception as e:
            raise Exception(f"加载配置文件失败: {e}")

    def parse_action(self, action: str) -> Tuple[str, str, str]:
        """解析操作指令"""
        parts = action.split(' ', 2)
        if len(parts) < 2:
            raise ValueError(f"无效的操作指令: {action}")

        cmd = parts[0]
        if cmd == 'mv-dir':
            if len(parts) != 3:
                raise ValueError(f"mv-dir 指令需要两个参数: {action}")
            return cmd, parts[1], parts[2]
        elif cmd == 'mv':
            if len(parts) != 3:
                raise ValueError(f"mv 指令需要两个参数: {action}")
            return cmd, parts[1], parts[2]
        elif cmd == 'mkdir':
            if len(parts) != 2:
                raise ValueError(f"mkdir 指令需要一个参数: {action}")
            return cmd, parts[1], ''
        else:
            raise ValueError(f"不支持的操作指令: {cmd}")

    def execute_action(self, target_dir: str, action: str) -> bool:
        """执行单个操作"""
        try:
            cmd, src, dst = self.parse_action(action)

            # 构建完整路径
            target_abs = self.path_resolver.get_absolute_path(target_dir)
            src_path = os.path.join(target_abs, src) if src else ''
            dst_path = os.path.join(target_abs, dst) if dst else ''

            if cmd == 'mkdir':
                if os.path.exists(src_path):
                    self.logger.log_skip(target_dir, action, f"目录已存在: {src}")
                    return False

                os.makedirs(src_path, exist_ok=True)
                self.logger.log_success(target_dir, action, f"创建目录: {src}")
                return True

            elif cmd == 'mv-dir':
                if not os.path.exists(src_path):
                    self.logger.log_skip(target_dir, action, f"源目录不存在: {src}")
                    return False

                if not os.path.isdir(src_path):
                    self.logger.log_skip(target_dir, action, f"源路径不是目录: {src}")
                    return False

                # 确保目标目录的父目录存在
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)

                # 移动目录
                shutil.move(src_path, dst_path)

                # 更新目录内所有文件的引用
                self._update_directory_references(src_path, dst_path)

                self.logger.log_success(target_dir, action, f"移动目录: {src} -> {dst}")
                return True

            elif cmd == 'mv':
                if not os.path.exists(src_path):
                    self.logger.log_skip(target_dir, action, f"源文件不存在: {src}")
                    return False

                # 确保目标文件的父目录存在
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)

                # 移动文件
                shutil.move(src_path, dst_path)

                # 更新文件引用
                if src_path.endswith(('.md', '.mdx')):
                    updated_files = self.link_updater.update_file_references(src_path, dst_path)
                    details = f"移动文件: {src} -> {dst}"
                    if any(updated_files.values()):
                        update_count = sum(len(files) for files in updated_files.values())
                        details += f", 更新了 {update_count} 个引用"
                    self.logger.log_success(target_dir, action, details)
                else:
                    self.logger.log_success(target_dir, action, f"移动文件: {src} -> {dst}")

                return True

        except Exception as e:
            self.logger.log_failure(target_dir, action, str(e))
            return False

    def _update_directory_references(self, old_dir: str, new_dir: str):
        """更新目录内所有文件的引用"""
        try:
            # 获取目录中所有的md/mdx文件
            md_files = []
            for root, dirs, files in os.walk(new_dir):
                for file in files:
                    if file.endswith(('.md', '.mdx')):
                        new_file_path = os.path.join(root, file)
                        # 计算对应的旧文件路径
                        relative_path = os.path.relpath(new_file_path, new_dir)
                        old_file_path = os.path.join(old_dir, relative_path)
                        md_files.append((old_file_path, new_file_path))

            # 更新每个文件的引用
            for old_file_path, new_file_path in md_files:
                self.link_updater.update_file_references(old_file_path, new_file_path)

        except Exception as e:
            print(f"警告：更新目录引用失败: {e}")

    def run(self):
        """运行重命名脚本"""
        try:
            print("开始执行重命名操作...")
            config = self.load_config()

            targets = config['target']
            actions = config['action']

            print(f"目标目录数量: {len(targets)}")
            print(f"操作数量: {len(actions)}")

            for target in targets:
                print(f"\n处理目标目录: {target}")
                target_abs = self.path_resolver.get_absolute_path(target)

                if not os.path.exists(target_abs):
                    self.logger.log_skip(target, "all", f"目标目录不存在: {target}")
                    print(f"  跳过：目标目录不存在")
                    continue

                success_count = 0
                for action in actions:
                    print(f"  执行操作: {action}")
                    if self.execute_action(target, action):
                        success_count += 1

                print(f"  完成：{success_count}/{len(actions)} 个操作成功")

            # 写入日志
            self.logger.write_log()

            # 输出汇总
            print(f"\n操作完成！")
            print(f"总成功: {self.logger.logs}")

        except Exception as e:
            print(f"执行失败: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='批量重命名/移动文件和目录工具')
    parser.add_argument('config', nargs='?', default=None, help='配置文件路径（默认：工作区根目录的rename.json）')
    parser.add_argument('--workspace', '-w', default='.', help='工作区根目录路径（默认：当前目录）')

    args = parser.parse_args()

    try:
        script = RenameScript(args.workspace, args.config)
        script.run()
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()