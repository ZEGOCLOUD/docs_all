#!/usr/bin/env python3
"""
分析 git commit 范围内的中文文档改动
用于生成翻译任务列表
"""

import subprocess
import sys
import json
from pathlib import Path


def get_changed_files(repo_path, start_hash=None, end_hash=None):
    """
    获取指定 commit 范围内改动的文件

    Args:
        repo_path: 仓库路径
        start_hash: 起始 commit hash（可选）
        end_hash: 结束 commit hash，默认为 HEAD

    Returns:
        list: 改动的文件列表
    """
    try:
        if start_hash and end_hash:
            range_spec = f"{start_hash}..{end_hash}"
        elif start_hash:
            range_spec = f"{start_hash}..HEAD"
        else:
            # 如果没有指定范围，获取未提交的改动
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            files = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    status = line[:2]
                    filepath = line[3:]
                    if status.strip() and not filepath.startswith('???'):
                        files.append(filepath)
            return files

        result = subprocess.run(
            ["git", "diff", "--name-only", range_spec],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        files = [f for f in result.stdout.strip().split('\n') if f]
        return files

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}", file=sys.stderr)
        return []


def filter_md_files(files):
    """过滤出 Markdown 文件"""
    return [f for f in files if f.endswith('.md')]


def get_file_stats(repo_path, file_path, start_hash=None, end_hash=None):
    """
    获取文件的改动统计信息

    Args:
        repo_path: 仓库路径
        file_path: 文件路径
        start_hash: 起始 commit hash
        end_hash: 结束 commit hash

    Returns:
        dict: 包含改动统计的字典
    """
    try:
        if start_hash and end_hash:
            range_spec = f"{start_hash}..{end_hash}"
        elif start_hash:
            range_spec = f"{start_hash}..HEAD"
        else:
            # 未提交的改动
            result = subprocess.run(
                ["git", "diff", "--numstat", "--", file_path],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True
            )

        if start_hash or end_hash:
            result = subprocess.run(
                ["git", "diff", "--numstat", range_spec, "--", file_path],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True
            )

        lines = result.stdout.strip().split('\n')
        if lines and lines[0]:
            parts = lines[0].split('\t')
            if len(parts) >= 2:
                additions = parts[0]
                deletions = parts[1]
                return {
                    'additions': int(additions) if additions.isdigit() else 0,
                    'deletions': int(deletions) if deletions.isdigit() else 0
                }
    except subprocess.CalledProcessError:
        pass

    return {'additions': 0, 'deletions': 0}


def main():
    if len(sys.argv) < 2:
        print("Usage: analyze_changes.py <repo_path> [start_hash] [end_hash]", file=sys.stderr)
        print("Example: analyze_changes.py . abc123 def456", file=sys.stderr)
        print("Example: analyze_changes.py . abc123", file=sys.stderr)
        sys.exit(1)

    repo_path = sys.argv[1]
    start_hash = sys.argv[2] if len(sys.argv) > 2 else None
    end_hash = sys.argv[3] if len(sys.argv) > 3 else None

    # 获取改动的文件
    changed_files = get_changed_files(repo_path, start_hash, end_hash)

    if not changed_files:
        print(json.dumps({"files": [], "message": "No changes found in the specified range"}))
        sys.exit(0)

    # 过滤 Markdown 文件
    md_files = filter_md_files(changed_files)

    # 获取每个文件的统计信息
    files_with_stats = []
    for file_path in md_files:
        full_path = Path(repo_path) / file_path
        if full_path.exists():
            stats = get_file_stats(repo_path, file_path, start_hash, end_hash)
            files_with_stats.append({
                'path': file_path,
                'additions': stats['additions'],
                'deletions': stats['deletions']
            })

    result = {
        'range': f"{start_hash or 'working_dir'}..{end_hash or 'HEAD'}" if start_hash or end_hash else "working directory",
        'total_files': len(files_with_stats),
        'files': files_with_stats
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
