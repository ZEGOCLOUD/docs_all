#!/usr/bin/env python3
"""
扫描英文目录，检测仍包含中文字符的文件（待翻译/翻译不完整）

使用方式：
1. 传入英文目录：直接检查该目录下是否含中文字符
2. 传入中文目录：自动找到对应英文目录，检查英文目录

输出：包含中文字符的英文文件列表（即待翻译/翻译不完整的文件）
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional


# 支持检查的文件扩展名
CHECKABLE_EXTENSIONS = {'.md', '.mdx', '.json', '.yaml', '.yml'}

# 中文字符正则
CHINESE_PATTERN = re.compile(r'[\u4e00-\u9fff]+')

# 排除的文件模式
EXCLUDED_PATTERNS = [
    'node_modules',
    '.docusaurus',
    'package-lock.json',
    'yarn.lock',
    'pnpm-lock.yaml',
    '.snapshot',
    '__snapshots__',
]


def compress_line_numbers(line_numbers: List[int]) -> List[str]:
    """
    将行号列表压缩为范围表示
    例如: [1, 2, 3, 5, 8, 9, 10] -> ["1~3", "5", "8~10"]
    """
    if not line_numbers:
        return []

    line_numbers = sorted(set(line_numbers))
    result = []
    start = line_numbers[0]
    end = line_numbers[0]

    for num in line_numbers[1:]:
        if num == end + 1:
            end = num
        else:
            if start == end:
                result.append(str(start))
            else:
                result.append(f"{start}~{end}")
            start = num
            end = num

    # 处理最后一个范围
    if start == end:
        result.append(str(start))
    else:
        result.append(f"{start}~{end}")

    return result


def contains_chinese(file_path: Path) -> Tuple[bool, int, List[str]]:
    """
    检查文件是否包含中文字符

    Returns:
        Tuple[bool, int, List[str]]: (是否含中文, 中文字符数, 含中文的行号范围)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        matches = CHINESE_PATTERN.findall(content)
        if not matches:
            return False, 0, []

        # 统计中文字符数
        chinese_count = sum(len(m) for m in matches)

        # 找出含中文的行号
        line_numbers = []
        for i, line in enumerate(content.split('\n'), 1):
            if CHINESE_PATTERN.search(line):
                line_numbers.append(i)

        # 压缩为范围表示
        lines_compressed = compress_line_numbers(line_numbers)

        return True, chinese_count, lines_compressed

    except Exception as e:
        return False, 0, [f"Error: {e}"]


def is_api_doc(file_path: Path) -> bool:
    """检查是否是 API 文档（跳过）"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in list(f)[:30]:
                if 'docType: API' in line or 'docType:api' in line.lower():
                    return True
    except Exception:
        pass
    return False


def is_reuse_doc(file_path: Path) -> bool:
    """检查是否是全复用文档（跳过）"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 跳过 frontmatter
        frontmatter_end = -1
        if lines and lines[0].strip() == '---':
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    frontmatter_end = i
                    break

        content_lines = lines[frontmatter_end + 1:] if frontmatter_end > 0 else lines
        non_empty_lines = [line for line in content_lines if line.strip()]

        if len(non_empty_lines) != 2:
            return False

        line1 = non_empty_lines[0].strip()
        line2 = non_empty_lines[1].strip()

        return 'import Content from' in line1 and line2.startswith('<Content')
    except Exception:
        return False


def resolve_directories(input_dir: Path, docs_root: Path) -> Tuple[Path, Path, str]:
    """
    解析目录，返回 (要检查的目录, 源中文目录, 模式说明)

    模式1: 输入是英文目录 → 直接检查
    模式2: 输入是中文目录 → 找对应英文目录后检查
    """
    input_str = str(input_dir)

    # 判断是中文目录还是英文目录
    if '/en/' in input_str or input_str.endswith('/en'):
        # 英文目录模式
        check_dir = input_dir
        zh_dir = Path(input_str.replace('/en/', '/zh/').rstrip('/en') + '/zh')
        mode = "en_dir"
    elif '/zh/' in input_str or input_str.endswith('/zh'):
        # 中文目录模式 → 转换为英文目录
        en_dir_str = input_str.replace('/zh/', '/en/').rstrip('/zh') + '/en'
        check_dir = Path(en_dir_str)
        zh_dir = input_dir
        mode = "zh_to_en"
    else:
        # 无法判断，假设是英文目录
        check_dir = input_dir
        zh_dir = None
        mode = "unknown"

    return check_dir, zh_dir, mode


def scan_for_chinese(check_dir: Path, docs_root: Path) -> List[Dict[str, Any]]:
    """
    扫描目录，找出包含中文字符的文件

    Returns:
        List of dicts with file info
    """
    if not check_dir.exists():
        return []

    results = []

    for file_path in check_dir.rglob('*'):
        if not file_path.is_file():
            continue

        suffix = file_path.suffix.lower()
        if suffix not in CHECKABLE_EXTENSIONS:
            continue

        # 检查排除模式
        file_str = str(file_path)
        should_exclude = False
        for pattern in EXCLUDED_PATTERNS:
            if pattern in file_str:
                should_exclude = True
                break

        if should_exclude:
            continue

        # 跳过 API 文档
        if is_api_doc(file_path):
            continue

        # 跳过全复用文档
        if is_reuse_doc(file_path):
            continue

        # 检查是否含中文
        has_chinese, chinese_count, lines = contains_chinese(file_path)

        if has_chinese:
            # 计算相对路径
            try:
                rel_path = str(file_path.relative_to(docs_root))
            except ValueError:
                rel_path = str(file_path)

            results.append({
                'path': rel_path,
                'chinese_chars': chinese_count,
                'lines': lines,
            })

    return results


def main():
    script_name = Path(__file__).name

    if len(sys.argv) < 2:
        print(f"Usage: {script_name} <directory> [options]", file=sys.stderr)
        print("", file=sys.stderr)
        print("扫描英文目录，检测仍包含中文字符的文件（待翻译/翻译不完整）", file=sys.stderr)
        print("", file=sys.stderr)
        print("Arguments:", file=sys.stderr)
        print("  directory       目录路径（中文目录或英文目录）", file=sys.stderr)
        print("                  - 如果是中文目录：自动找到对应英文目录检查", file=sys.stderr)
        print("                  - 如果是英文目录：直接检查该目录", file=sys.stderr)
        print("", file=sys.stderr)
        print("Options:", file=sys.stderr)
        print("  --docs-root     文档根目录（用于计算相对路径）", file=sys.stderr)
        print("  -o, --output    输出文件路径", file=sys.stderr)
        print("", file=sys.stderr)
        print("Examples:", file=sys.stderr)
        print("", file=sys.stderr)
        print("  # 扫描中文目录 → 自动检查对应英文目录", file=sys.stderr)
        print(f"  {script_name} core_products/aiagent/zh -o /tmp/pending.json", file=sys.stderr)
        print("", file=sys.stderr)
        print("  # 直接扫描英文目录", file=sys.stderr)
        print(f"  {script_name} core_products/aiagent/en -o /tmp/pending.json", file=sys.stderr)
        sys.exit(1)

    # 解析参数
    args = sys.argv[1:]
    input_dir = None
    docs_root = None
    output_file = None

    i = 0
    while i < len(args):
        arg = args[i]
        if arg == '--docs-root' and i + 1 < len(args):
            docs_root = Path(args[i + 1])
            i += 2
        elif arg in ['-o', '--output'] and i + 1 < len(args):
            output_file = args[i + 1]
            i += 2
        elif not arg.startswith('-'):
            input_dir = Path(arg)
            i += 1
        else:
            i += 1

    if input_dir is None:
        print("Error: Directory argument is required", file=sys.stderr)
        sys.exit(1)

    # 设置默认值
    if docs_root is None:
        docs_root = Path.cwd()

    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        output_file = f'/tmp/docs-pending-translation-{timestamp}.json'

    # 解析目录
    check_dir, zh_dir, mode = resolve_directories(input_dir, docs_root)

    print(f"Input directory: {input_dir}", file=sys.stderr)
    print(f"Mode: {mode}", file=sys.stderr)
    print(f"Checking English directory: {check_dir}", file=sys.stderr)

    # 检查英文目录是否存在
    if not check_dir.exists():
        print(f"Warning: English directory does not exist: {check_dir}", file=sys.stderr)
        print("This may indicate the English docs haven't been created yet.", file=sys.stderr)

        result = {
            "success": True,
            "input_directory": str(input_dir),
            "check_directory": str(check_dir),
            "mode": mode,
            "directory_exists": False,
            "total_files": 0,
            "files": [],
            "message": "English directory does not exist - may need initial translation"
        }
    else:
        # 扫描英文目录中的中文字符
        pending_files = scan_for_chinese(check_dir, docs_root)

        result = {
            "success": True,
            "input_directory": str(input_dir),
            "check_directory": str(check_dir),
            "mode": mode,
            "directory_exists": True,
            "total_files": len(pending_files),
            "details": [
                {"path": f['path'], "chinese_chars": f['chinese_chars'], "lines": f['lines']}
                for f in pending_files
            ],
        }

        print(f"Found {len(pending_files)} files containing Chinese characters", file=sys.stderr)

    # 写入输出文件
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Output written to: {output_path}", file=sys.stderr)


if __name__ == '__main__':
    main()
