"""
下载资源到本地。支持下载图片、视频、音频、文档、压缩包、Github代码仓库等资源。
如果是压缩包，下载后会自动解压缩。
下载后的文件都放到 workspace 根目录的.tmp目录下，每次下载均生成一个随机文件夹名称。

参数：
- url: 资源URL

返回：
- 下载后的文件夹路径。空字符串表示下载失败。
"""

import os
import sys
import uuid
import shutil
import zipfile
import tarfile
import subprocess
from pathlib import Path
from urllib.parse import urlparse, unquote

try:
    import requests
except ImportError:
    print("错误: 需要安装 requests 库")
    print("请运行: pip install requests")
    sys.exit(1)


def _get_workspace_root() -> Path:
    """
    获取 workspace 根目录

    Returns:
        workspace 根目录路径
    """
    # 从当前脚本位置向上查找 workspace 根目录
    # 脚本位于 .docuo/scripts/，需要向上两级到 workspace 根目录
    script_dir = Path(__file__).parent.resolve()
    workspace_root = script_dir.parent.parent.resolve()

    # 尝试从环境变量获取
    workspace_path = os.environ.get("CLAUDE_CODE_WORKSPACE")
    if workspace_path:
        workspace_root = Path(workspace_path)

    return workspace_root


def _create_temp_dir() -> Path:
    """
    在 workspace 根目录的 .tmp 目录下创建随机文件夹

    Returns:
        创建的临时目录路径
    """
    workspace_root = _get_workspace_root()
    tmp_dir = workspace_root / ".tmp"
    tmp_dir.mkdir(exist_ok=True)

    # 生成随机文件夹名称（10个字符）
    random_name = uuid.uuid4().hex[:10]
    target_dir = tmp_dir / random_name
    target_dir.mkdir(exist_ok=True)

    return target_dir


def _get_filename_from_url(url: str) -> str:
    """
    从 URL 中提取文件名

    Args:
        url: 资源 URL

    Returns:
        文件名
    """
    parsed = urlparse(url)
    path = unquote(parsed.path)
    filename = os.path.basename(path)

    if not filename:
        filename = "downloaded_file"

    return filename


def _is_archive(filename: str) -> bool:
    """
    判断文件是否是压缩包

    Args:
        filename: 文件名

    Returns:
        是否是压缩包
    """
    archive_extensions = [
        '.zip', '.tar', '.tar.gz', '.tgz', '.tar.bz2', '.tbz2',
        '.tar.xz', '.txz', '.rar', '.7z', '.gz', '.bz2', '.xz'
    ]

    filename_lower = filename.lower()
    return any(filename_lower.endswith(ext) for ext in archive_extensions)


def _extract_archive(archive_path: Path, extract_to: Path) -> bool:
    """
    解压缩文件

    Args:
        archive_path: 压缩包路径
        extract_to: 解压目标目录

    Returns:
        是否解压成功
    """
    try:
        filename = archive_path.name.lower()

        # ZIP 文件
        if filename.endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            return True

        # TAR 文件
        elif any(filename.endswith(ext) for ext in ['.tar', '.tar.gz', '.tgz', '.tar.bz2', '.tbz2', '.tar.xz', '.txz']):
            with tarfile.open(archive_path, 'r:*') as tar_ref:
                tar_ref.extractall(extract_to)
            return True

        # GZ 文件（非 tar.gz）
        elif filename.endswith('.gz') and not filename.endswith('.tar.gz'):
            import gzip
            output_file = extract_to / filename[:-3]
            with gzip.open(archive_path, 'rb') as f_in:
                with open(output_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            return True

        # BZ2 文件（非 tar.bz2）
        elif filename.endswith('.bz2') and not filename.endswith('.tar.bz2'):
            import bz2
            output_file = extract_to / filename[:-4]
            with bz2.open(archive_path, 'rb') as f_in:
                with open(output_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            return True

        # XZ 文件（非 tar.xz）
        elif filename.endswith('.xz') and not filename.endswith('.tar.xz'):
            import lzma
            output_file = extract_to / filename[:-3]
            with lzma.open(archive_path, 'rb') as f_in:
                with open(output_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            return True

        # RAR 和 7Z 需要外部工具
        elif filename.endswith('.rar'):
            # 尝试使用 unrar
            result = subprocess.run(['unrar', 'x', '-y', str(archive_path), str(extract_to)],
                                    capture_output=True, text=True)
            return result.returncode == 0

        elif filename.endswith('.7z'):
            # 尝试使用 7z
            result = subprocess.run(['7z', 'x', f'-o{extract_to}', '-y', str(archive_path)],
                                    capture_output=True, text=True)
            return result.returncode == 0

        return False

    except Exception as e:
        print(f"解压缩失败: {str(e)}", file=sys.stderr)
        return False


def _is_github_url(url: str) -> bool:
    """
    判断是否是 GitHub 仓库 URL

    Args:
        url: URL

    Returns:
        是否是 GitHub 仓库 URL
    """
    parsed = urlparse(url)
    return parsed.hostname in ['github.com', 'www.github.com']


def _normalize_github_url(url: str) -> str:
    """
    将 GitHub URL 标准化为 HTTPS 格式

    Args:
        url: GitHub URL (可能是 git@github.com:user/repo.git 或 https://github.com/user/repo)

    Returns:
        标准化的 HTTPS URL
    """
    # 如果是 SSH 格式 (git@github.com:user/repo.git)
    if url.startswith('git@github.com:'):
        # 转换为 HTTPS 格式
        repo_path = url.replace('git@github.com:', '').replace('.git', '')
        return f'https://github.com/{repo_path}'

    # 如果已经是 HTTPS 格式，确保没有 .git 后缀
    if url.startswith('https://github.com/'):
        return url.replace('.git', '')

    return url


def _download_github_repo(url: str, target_dir: Path) -> tuple[bool, str]:
    """
    下载 GitHub 仓库

    Args:
        url: GitHub 仓库 URL
        target_dir: 目标目录

    Returns:
        (是否下载成功, 错误信息)
    """
    try:
        # 标准化为 HTTPS URL
        https_url = _normalize_github_url(url)

        # 设置环境变量，禁用所有交互式提示
        env = os.environ.copy()
        env['GIT_TERMINAL_PROMPT'] = '0'  # 禁用终端提示
        env['GIT_ASKPASS'] = 'echo'  # 禁用密码提示
        env['GIT_SSH_COMMAND'] = 'ssh -o BatchMode=yes'  # SSH 非交互模式

        # 使用 git clone (HTTPS 协议，非交互模式)
        result = subprocess.run(
            ['git', 'clone', '--depth', '1', '--no-single-branch', https_url, str(target_dir)],
            capture_output=True,
            text=True,
            timeout=60,  # 60秒超时
            env=env,
            stdin=subprocess.DEVNULL  # 禁用标准输入
        )

        if result.returncode == 0:
            # 删除 .git 目录以节省空间
            git_dir = target_dir / '.git'
            if git_dir.exists():
                shutil.rmtree(git_dir)
            return True, ""
        else:
            # 检查是否是仓库不存在
            error_msg = result.stderr.lower()
            if 'not found' in error_msg or 'repository not found' in error_msg or '404' in error_msg:
                return False, "仓库不存在或无法访问"
            elif 'authentication' in error_msg or 'permission denied' in error_msg or 'terminal prompts disabled' in error_msg:
                return False, "仓库需要认证或权限不足"
            else:
                return False, f"克隆失败: {result.stderr.strip()}"

    except FileNotFoundError:
        return False, "未找到 git 命令，请先安装 git"
    except subprocess.TimeoutExpired:
        return False, "克隆超时"
    except Exception as e:
        return False, f"下载失败: {str(e)}"


def _get_download_headers(url: str) -> dict:
    """
    根据 URL 获取下载所需的请求头

    Args:
        url: 文件 URL

    Returns:
        请求头字典
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    # 检查是否是 zego.im 域名的资源
    parsed = urlparse(url)
    if parsed.hostname and 'zego.im' in parsed.hostname:
        # 添加 Referer 头
        headers['Referer'] = 'https://doc-zh.zego.im'

    return headers


def _download_file(url: str, target_path: Path) -> bool:
    """
    下载文件

    Args:
        url: 文件 URL
        target_path: 目标文件路径

    Returns:
        是否下载成功
    """
    try:
        # 获取请求头
        headers = _get_download_headers(url)

        # 发送 GET 请求
        response = requests.get(url, headers=headers, stream=True, timeout=30)
        response.raise_for_status()

        # 写入文件
        with open(target_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        return True

    except requests.exceptions.RequestException as e:
        print(f"下载文件失败: {str(e)}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"保存文件失败: {str(e)}", file=sys.stderr)
        return False


def download_resource(url: str, silent: bool = False) -> str:
    """
    下载资源到本地

    支持：
    - 图片、视频、音频、文档等普通文件
    - 压缩包（自动解压）
    - GitHub 仓库（使用 git clone）

    Args:
        url: 资源 URL
        silent: 是否静默模式（不输出日志）

    Returns:
        下载后的文件夹路径。空字符串表示下载失败。
    """
    def log(msg):
        if not silent:
            print(msg, file=sys.stderr)

    try:
        # 创建临时目录
        target_dir = _create_temp_dir()

        # 判断是否是 GitHub 仓库
        if _is_github_url(url):
            log(f"检测到 GitHub 仓库，使用 git clone 下载...")
            # 为 GitHub 仓库创建子目录
            repo_name = url.rstrip('/').split('/')[-1].replace('.git', '')
            repo_dir = target_dir / repo_name

            success, error_msg = _download_github_repo(url, repo_dir)
            if success:
                log(f"GitHub 仓库下载成功: {repo_dir}")
                return str(target_dir)
            else:
                # 清理失败的下载
                shutil.rmtree(target_dir, ignore_errors=True)
                log(f"错误: {error_msg}")
                return ""

        # 普通文件下载
        filename = _get_filename_from_url(url)
        file_path = target_dir / filename

        log(f"开始下载: {url}")
        log(f"保存到: {file_path}")

        if not _download_file(url, file_path):
            # 清理失败的下载
            shutil.rmtree(target_dir, ignore_errors=True)
            return ""

        log(f"下载完成: {file_path}")

        # 判断是否是压缩包
        if _is_archive(filename):
            log(f"检测到压缩包，开始解压...")

            # 创建解压目录
            extract_dir = target_dir / "extracted"
            extract_dir.mkdir(exist_ok=True)

            if _extract_archive(file_path, extract_dir):
                log(f"解压成功: {extract_dir}")
                # 删除原始压缩包以节省空间
                file_path.unlink()
            else:
                log(f"解压失败，保留原始压缩包")

        return str(target_dir)

    except Exception as e:
        log(f"下载资源失败: {str(e)}")
        return ""


# 命令行入口
if __name__ == "__main__":
    import json

    if len(sys.argv) < 2:
        print(json.dumps({"error": "缺少 URL 参数"}))
        sys.exit(1)

    url = sys.argv[1]
    result = download_resource(url, silent=True)

    if result:
        print(json.dumps({"path": result}))
    else:
        print(json.dumps({"path": ""}))
        sys.exit(1)
