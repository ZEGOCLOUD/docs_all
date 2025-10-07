#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAGFlow 知识库清理脚本

功能：
- 默认：删除 document_count 为 0 的知识库
- 选项：--all 删除所有知识库

接口文档：
- 列举知识库：GET /api/v1/datasets?page=&page_size=&...
- 删除知识库：DELETE /api/v1/datasets  (body: {"ids": null} 删除全部；或 [id,...])

环境变量（或 .scripts/ai_data/.env）：
- RAGFLOW_BASE_URL，例如：https://your-host/api/v1
- RAGFLOW_API_KEY，例如：ragflow-xxxx
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import List, Optional

try:
    import requests
except ImportError:
    print("需要安装 requests：pip install requests")
    sys.exit(1)


class Config:
    def __init__(self) -> None:
        self.ragflow_base_url: Optional[str] = None
        self.api_key: str = ""
        self._load_env()
        self._normalize_base_url()
        self.api_key = os.getenv("RAGFLOW_API_KEY", "").strip()

    def _load_env(self) -> None:
        """加载同目录下 .env（仅填充未在环境中的键）。"""
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

    def _normalize_base_url(self) -> None:
        base = os.getenv("RAGFLOW_BASE_URL", "").strip().rstrip("/")
        if base:
            if not (base.startswith("http://") or base.startswith("https://")):
                base = "https://" + base
            # 确保包含 /api/v{n}
            if not re.search(r"/api/v\d+($|/)", base):
                base = base + "/api/v1"
        self.ragflow_base_url = base


def list_datasets(cfg: Config) -> List[dict]:
    if not cfg.ragflow_base_url:
        print("❌ RAGFLOW_BASE_URL 未设置或无效。请设置为 http(s)://<host>:<port>/api/v1")
        return []
    if not cfg.api_key:
        print("❌ RAGFLOW_API_KEY 未设置。")
        return []

    headers = {"Authorization": f"Bearer {cfg.api_key}"}
    url = f"{cfg.ragflow_base_url}/datasets"

    all_items: List[dict] = []
    page = 1
    page_size = 200
    while True:
        params = {"page": page, "page_size": page_size}
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=30)
        except Exception as e:
            print(f"❌ 列举知识库请求异常: {e}")
            break
        text_preview = (resp.text or "")[:400]
        print(f"🔎 列举 Datasets: page={page}, status={resp.status_code}, body={text_preview}")
        try:
            data = resp.json()
        except Exception:
            print("❌ 无法解析 JSON 响应")
            break
        if data.get("code") != 0:
            print(f"❌ 列举知识库失败: code={data.get('code')}, message={data.get('message')}")
            break
        batch = data.get("data", [])
        if not isinstance(batch, list):
            # 有些版本可能返回对象，尽量兼容
            print("⚠️ 返回 data 非列表，尝试从对象中提取 items/records ...")
            if isinstance(batch, dict):
                if isinstance(batch.get("items"), list):
                    batch = batch["items"]
                elif isinstance(batch.get("records"), list):
                    batch = batch["records"]
                else:
                    batch = []
        all_items.extend(batch)
        if len(batch) < page_size:
            break
        page += 1
    print(f"📦 共获取知识库: {len(all_items)} 条")
    return all_items


def delete_datasets(cfg: Config, ids: Optional[List[str]]) -> bool:
    if not cfg.ragflow_base_url:
        print("❌ RAGFLOW_BASE_URL 未设置或无效。")
        return False
    if not cfg.api_key:
        print("❌ RAGFLOW_API_KEY 未设置。")
        return False

    headers = {"Authorization": f"Bearer {cfg.api_key}", "Content-Type": "application/json"}
    url = f"{cfg.ragflow_base_url}/datasets"

    # 若 ids 为 None，按文档表示删除全部；否则分批删除指定 ids（避免一次性删除过多导致 504）
    if ids is None:
        body = {"ids": None}
        print(f"🗑️  删除知识库请求: url={url}, body={body}")
        try:
            resp = requests.delete(url, headers=headers, json=body, timeout=120)
        except Exception as e:
            print(f"❌ 删除知识库请求异常: {e}")
            return False
        preview = (resp.text or "")[:400]
        print(f"🗑️  删除知识库响应: status={resp.status_code}, body={preview}")
        try:
            data = resp.json()
        except Exception:
            print("❌ 无法解析删除响应 JSON")
            return False
        if data.get("code") == 0:
            print("✅ 删除成功")
            return True
        print(f"❌ 删除失败: code={data.get('code')}, message={data.get('message')}")
        return False

    # 分批删除指定 ids
    batch_size = 100
    total = len(ids)
    ok_all = True
    for i in range(0, total, batch_size):
        batch = ids[i:i+batch_size]
        body = {"ids": batch}
        print(f"🗑️  删除知识库批次: {i//batch_size+1} / {((total-1)//batch_size)+1}, 数量={len(batch)}")
        print(f"🗑️  删除知识库请求: url={url}, body长度={len(json.dumps(body))} 字节")
        try:
            resp = requests.delete(url, headers=headers, json=body, timeout=120)
        except Exception as e:
            print(f"❌ 删除批次请求异常: {e}")
            ok_all = False
            continue
        preview = (resp.text or "")[:400]
        print(f"🗑️  删除知识库响应: status={resp.status_code}, body={preview}")
        try:
            data = resp.json()
        except Exception:
            print("❌ 无法解析删除响应 JSON")
            ok_all = False
            continue
        if data.get("code") == 0:
            print("✅ 批次删除成功")
        else:
            print(f"❌ 批次删除失败: code={data.get('code')}, message={data.get('message')}")
            ok_all = False
    return ok_all


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="RAGFlow 知识库清理工具")
    parser.add_argument("--all", action="store_true", help="删除所有知识库（危险）")
    parser.add_argument("--dry-run", action="store_true", help="仅打印将要删除的知识库，不执行删除")
    args = parser.parse_args(argv)

    cfg = Config()

    datasets = list_datasets(cfg)
    if not datasets:
        print("⚠️ 未获取到任何知识库")
        return 1

    if args.all:
        ids = [d.get("id") for d in datasets if isinstance(d, dict) and d.get("id")]
        print(f"📋 计划删除全部知识库，共 {len(ids)} 个")
        if args.dry_run:
            print(json.dumps(ids, ensure_ascii=False, indent=2))
            return 0
        return 0 if delete_datasets(cfg, ids) else 2

    # 默认：仅删除 document_count==0 的知识库
    empty_ids: List[str] = []
    for d in datasets:
        if not isinstance(d, dict):
            continue
        did = d.get("id")
        if not did:
            continue
        doc_cnt = d.get("document_count")
        if doc_cnt is None:
            # 兼容其他可能字段名
            doc_cnt = d.get("docs_count", 0)
        try:
            doc_cnt_int = int(doc_cnt)
        except Exception:
            doc_cnt_int = 0
        if doc_cnt_int == 0:
            empty_ids.append(did)
    print(f"📋 计划删除空知识库（document_count=0）: {len(empty_ids)} 个")
    if not empty_ids:
        print("✅ 没有空知识库需要删除")
        return 0

    if args.dry_run:
        print(json.dumps(empty_ids, ensure_ascii=False, indent=2))
        return 0

    ok = delete_datasets(cfg, empty_ids)
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())

