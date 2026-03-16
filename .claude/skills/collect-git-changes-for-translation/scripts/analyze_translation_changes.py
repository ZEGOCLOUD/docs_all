#!/usr/bin/env python3
"""
分析 git commit 范围内的文档改动，生成待翻译文件列表
支持 MD/MDX/JSON/YAML 文件格式
自动排除 docuo.config.en.json 中已存在的英文文档路径
"""

import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime


# 支持的翻译文件扩展名
TRANSLATABLE_EXTENSIONS = {'.md', '.mdx', '.json', '.yaml', '.yml'}

# 排除的文件模式
EXCLUDED_PATTERNS = [
    'node_modules',
    '.docusaurus',
    'package-lock.json',
    'yarn.lock',
    'pnpm-lock.yaml',
    '.snapshot',
    '__snapshots__',
    '/en/',  # 通用英文路径
]


def get_default_base_branch():
    """
    获取默认的基准分支（origin/main 或 origin/master）
    """
    for branch in ['origin/main', 'origin/master']:
        try:
            subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                capture_output=True,
                check=True
            )
            return branch
        except subprocess.CalledProcessError:
            continue
    return 'origin/main'


def get_english_doc_paths(docs_root):
    """
    从 docuo.config.en.json 读取英文文档路径

    Args:
        docs_root: 文档根目录路径

    Returns:
        set: 英文文档路径集合（相对路径前缀）
    """
    config_path = Path(docs_root) / 'docuo.config.en.json'
    english_paths = set()

    if not config_path.exists():
        return english_paths

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        instances = config.get('instances', [])
        for instance in instances:
            path = instance.get('path', '')
            if path:
                # 标准化路径，确保以 / 结尾用于前缀匹配
                normalized = path.rstrip('/') + '/'
                english_paths.add(normalized)

        return english_paths
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Failed to read {config_path}: {e}", file=sys.stderr)
        return english_paths


def get_changed_files(repo_path, start_hash=None, end_hash=None):
    """
    获取指定 commit 范围内改动的文件

    Args:
        repo_path: 仓库路径
        start_hash: 起始 commit hash 或分支名（可选）
        end_hash: 结束 commit hash，默认为 HEAD

    Returns:
        tuple: (改动的文件列表, range_spec)
    """
    try:
        if start_hash and end_hash:
            range_spec = f"{start_hash}..{end_hash}"
        elif start_hash:
            range_spec = f"{start_hash}..HEAD"
        else:
            # 默认使用 HEAD 到 origin/main 的范围
            base_branch = get_default_base_branch()
            range_spec = f"{base_branch}..HEAD"

        result = subprocess.run(
            ["git", "diff", "--name-only", range_spec],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        files = [f for f in result.stdout.strip().split('\n') if f]
        return files, range_spec

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}", file=sys.stderr)
        return [], ""


def filter_translatable_files(files, english_doc_paths):
    """
    过滤出可翻译的文件（MD/MDX/JSON/YAML）
    排除：
    - 英文文档路径下的文件
    - node_modules、lock 文件等
    """
    result = []
    for f in files:
        # 检查扩展名
        ext = Path(f).suffix.lower()
        if ext not in TRANSLATABLE_EXTENSIONS:
            continue

        # 标准化路径用于匹配
        normalized_path = f if f.startswith('/') else '/' + f

        # 检查是否在英文文档路径下
        is_english_doc = False
        for en_path in english_doc_paths:
            if normalized_path.startswith('/' + en_path) or f.startswith(en_path):
                is_english_doc = True
                break

        if is_english_doc:
            continue

        # 检查排除模式
        should_exclude = False
        for pattern in EXCLUDED_PATTERNS:
            if pattern in f:
                should_exclude = True
                break

        if not should_exclude:
            result.append(f)

    return result


def main():
    script_name = Path(__file__).name
    if len(sys.argv) < 2:
        print(f"Usage: {script_name} <docs_root> [options] [start_commit] [end_commit]", file=sys.stderr)
        print("", file=sys.stderr)
        print("Arguments:", file=sys.stderr)
        print("  docs_root       文档根目录路径（包含 docuo.config.en.json 的目录）", file=sys.stderr)
        print("", file=sys.stderr)
        print("Options:", file=sys.stderr)
        print("  --repo PATH     git 仓库路径（如果不在仓库目录下执行时使用）", file=sys.stderr)
        print("  -o, --output    输出文件路径（默认输出到 stdout）", file=sys.stderr)
        print("  start_commit    起始 commit hash 或分支名", file=sys.stderr)
        print("  end_commit      结束 commit hash，默认为 HEAD", file=sys.stderr)
        print("", file=sys.stderr)
        print("Examples:", file=sys.stderr)
        print("", file=sys.stderr)
        print("  # 在文档目录下执行，输出到文件", file=sys.stderr)
        print(f"  {script_name} . -o /tmp/docs-git-changes.json", file=sys.stderr)
        print("", file=sys.stderr)
        print("  # 在任意目录执行，指定文档目录和输出文件", file=sys.stderr)
        print(f"  {script_name} /path/to/docs -o /tmp/docs-git-changes.json", file=sys.stderr)
        print("", file=sys.stderr)
        print("  # 指定 commit 范围", file=sys.stderr)
        print(f"  {script_name} . -o /tmp/docs-git-changes.json HEAD~10 HEAD", file=sys.stderr)
        print("", file=sys.stderr)
        print("  # 输出到 stdout（默认）", file=sys.stderr)
        print(f"  {script_name} .", file=sys.stderr)
        sys.exit(1)

    # 解析参数
    args = sys.argv[1:]
    docs_root = args[0]
    repo_path = docs_root  # 默认仓库路径等于文档路径
    output_file = None
    start_hash = None
    end_hash = None

    # 处理 --repo 参数
    if '--repo' in args:
        repo_idx = args.index('--repo')
        if repo_idx + 1 < len(args):
            repo_path = args[repo_idx + 1]
            # 从参数列表中移除 --repo 和其值
            args = args[:repo_idx] + args[repo_idx + 2:]
            docs_root = args[0] if args else docs_root

    # 处理 -o / --output 参数
    if '-o' in args:
        o_idx = args.index('-o')
        if o_idx + 1 < len(args):
            output_file = args[o_idx + 1]
            args = args[:o_idx] + args[o_idx + 2:]
            docs_root = args[0] if args else docs_root
    elif '--output' in args:
        o_idx = args.index('--output')
        if o_idx + 1 < len(args):
            output_file = args[o_idx + 1]
            args = args[:o_idx] + args[o_idx + 2:]
            docs_root = args[0] if args else docs_root

    # 剩余参数处理
    if len(args) > 1:
        start_hash = args[1]
    if len(args) > 2:
        end_hash = args[2]

    # 验证路径
    docs_root = Path(docs_root).resolve()
    repo_path = Path(repo_path).resolve()

    if not docs_root.exists():
        print(f"Error: Docs root path does not exist: {docs_root}", file=sys.stderr)
        sys.exit(1)

    # 获取英文文档路径
    english_doc_paths = get_english_doc_paths(docs_root)
    if english_doc_paths:
        print(f"Info: Found {len(english_doc_paths)} English doc paths to exclude", file=sys.stderr)

    # 获取改动的文件
    changed_files, range_spec = get_changed_files(str(repo_path), start_hash, end_hash)

    if not changed_files:
        print(json.dumps({
            "success": True,
            "range": range_spec,
            "docs_root": str(docs_root),
            "files": [],
            "categories": {"md": [], "mdx": [], "json": [], "yaml": []},
            "total_files": 0,
            "excluded_english_paths": len(english_doc_paths),
            "message": "No changes found in the specified range"
        }, indent=2, ensure_ascii=False))
        sys.exit(0)

    # 过滤可翻译文件（排除英文文档路径）
    translatable_files = filter_translatable_files(changed_files, english_doc_paths)

    # 只保留存在的文件的路径
    file_paths = []
    for file_path in translatable_files:
        full_path = docs_root / file_path
        if full_path.exists():
            file_paths.append(file_path)

    result = {
        "success": True,
        "range": range_spec,
        "docs_root": str(docs_root),
        "total_files": len(file_paths),
        "files": file_paths,
        "excluded_english_paths": len(english_doc_paths)
    }

    output_json = json.dumps(result, indent=2, ensure_ascii=False)

    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_json)
        print(f"Output written to: {output_path}", file=sys.stderr)
        print(f"Total files: {len(file_paths)}", file=sys.stderr)
    else:
        print(output_json)


if __name__ == '__main__':
    main()
