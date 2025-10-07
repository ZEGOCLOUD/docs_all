#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 docuo.config.zh.json 中 themeConfig.instanceGroups 的数组原样通过 PUT 发送到 UPDATE_PRODUCT_INTRODUCTION_ENDPOINT。
- Endpoint 从环境变量 UPDATE_PRODUCT_INTRODUCTION_ENDPOINT 读取，或用 --endpoint 覆盖
- 必须携带管理口令：请求头 X-Admin-Token: $ADMIN_API_TOKEN（从环境变量读取）
- 配置文件默认 ../../docuo.config.zh.json，可用 --config 覆盖
用法：
  ADMIN_API_TOKEN=xxxx python .scripts/ai_data/update_product_introductions.py [--config ../../docuo.config.zh.json] [--endpoint https://...]
"""
from __future__ import annotations
import os
import sys
import json
import argparse
from pathlib import Path
from typing import Any, Optional

try:
    import requests  # type: ignore
except ImportError:
    print("需要安装 requests: pip install requests", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = REPO_ROOT / "docuo.config.zh.json"


def _load_local_env() -> None:
    """加载同目录 .env（仅填充未在环境中的键）。"""
    try:
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            for raw in env_path.read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k and k not in os.environ:
                        os.environ[k] = v
    except Exception:
        pass


def read_instance_groups(config_path: Path) -> list[Any]:
    data = json.loads(config_path.read_text(encoding="utf-8"))
    theme = data.get("themeConfig") or {}
    groups = theme.get("instanceGroups")
    if not isinstance(groups, list):
        raise ValueError("themeConfig.instanceGroups 不是数组或不存在")
    return groups


def put_instance_groups(endpoint: str, groups: list[Any], token: Optional[str] = None, admin_token: Optional[str] = None) -> requests.Response:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    # 必需：X-Admin-Token（从环境变量 ADMIN_API_TOKEN 或入参传入）
    if admin_token is None:
        admin_token = os.getenv("ADMIN_API_TOKEN", "").strip()
    if admin_token:
        headers["X-Admin-Token"] = admin_token

    # 可选：Authorization（兼容旧用法）
    auth = os.getenv("UPDATE_PRODUCT_INTRODUCTION_AUTH", "").strip()
    if token:
        headers["Authorization"] = token
    elif auth:
        headers["Authorization"] = auth

    resp = requests.put(endpoint, json=groups, headers=headers, timeout=30)
    return resp


def main() -> int:
    _load_local_env()

    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="配置文件路径，默认 ../../docuo.config.zh.json")
    parser.add_argument("--endpoint", default=os.getenv("UPDATE_PRODUCT_INTRODUCTION_ENDPOINT", "").strip(), help="PUT 接口地址，优先使用该参数，其次读取环境变量")
    parser.add_argument("--auth", default=os.getenv("UPDATE_PRODUCT_INTRODUCTION_AUTH", "").strip(), help="可选：Authorization 头的值，例如 Bearer xxx")
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    if not config_path.exists():
        print(f"配置文件不存在: {config_path}", file=sys.stderr)
        return 2

    endpoint = args.endpoint
    if not endpoint:
        print("未提供 endpoint，请通过 --endpoint 或环境变量 UPDATE_PRODUCT_INTRODUCTION_ENDPOINT 指定", file=sys.stderr)
        return 2

    try:
        groups = read_instance_groups(config_path)
    except Exception as e:
        print(f"读取 instanceGroups 失败: {e}", file=sys.stderr)
        return 3

    # 校验 ADMIN_API_TOKEN
    admin_token = os.getenv("ADMIN_API_TOKEN", "").strip()
    if not admin_token:
        print("缺少 ADMIN_API_TOKEN 环境变量，无法进行鉴权。请设置后重试。", file=sys.stderr)
        return 6

    try:
        resp = put_instance_groups(endpoint, groups, token=args.auth or None, admin_token=admin_token)
        ok = 200 <= resp.status_code < 300
        print(f"PUT {endpoint} -> {resp.status_code}")
        text = (resp.text or "")[:500]
        if text:
            print(text)
        return 0 if ok else 4
    except requests.RequestException as e:
        print(f"请求失败: {e}", file=sys.stderr)
        return 5


if __name__ == "__main__":
    sys.exit(main())

