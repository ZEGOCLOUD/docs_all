#!/usr/bin/env python3
"""
Generate nginx rewrite rules mapping old numeric article pages to new routes,
and verify the generated destination pages locally.

Rules format example:

    # 项目名称
    rewrite ^/article/11344$ https://doc-zh.zego.im/some-route/path? permanent;

How it works:
- Read instances from docuo.config.zh.json
- For each instance, open its `path`/sidebars.json (skip if `path` is a URL or missing)
- Traverse all nodes and collect those where `type` == `doc` and contains `articleID`
- Build destination URL:
  - If node has `href` and starts with "/", use https://doc-zh.zego.im{href}?
  - Else if node has absolute `href` (http/https), use it as-is (append ?)
  - Else if node has `id`, use https://doc-zh.zego.im/{routeBasePath}/{id}?
  - Else fallback to https://doc-zh.zego.im/{routeBasePath}?

Verification after generation:
- Collect all destination URLs, convert the domain to http://localhost:3000
- Prefer HEAD requests to avoid downloading content; if HEAD not supported, fallback to GET without reading body
- Print progress to stderr periodically while checking
- If HTTP 200, treat as OK; otherwise, record into redirect_error.txt
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib.parse import urlparse, urlunparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


BASE_DOMAIN = "https://doc-zh.zego.im"
CONFIG_FILENAME = "docuo.config.zh.json"
SIDEBARS_FILENAME = "sidebars.json"
OUTPUT_FILENAME = "transfer.conf"
ERROR_LOG_FILENAME = "redirect_error.txt"


def is_url(path: Optional[str]) -> bool:
    if not path or not isinstance(path, str):
        return False
    return path.startswith("http://") or path.startswith("https://")


def load_json_file(file_path: str) -> Any:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def traverse_collect_article_nodes(obj: Any) -> List[Dict[str, Any]]:
    """Traverse arbitrary JSON-like structure and return nodes (dicts) where type==doc and contain `articleID`."""
    collected: List[Dict[str, Any]] = []

    def _walk(node: Any) -> None:
        if isinstance(node, dict):
            if node.get("type") == "doc" and "articleID" in node:
                collected.append(node)
            for value in node.values():
                _walk(value)
        elif isinstance(node, list):
            for item in node:
                _walk(item)

    _walk(obj)
    return collected


def build_destination_url(route_base_path: str, node: Dict[str, Any]) -> str:
    href = node.get("href")
    doc_id = node.get("id")

    if isinstance(href, str) and href:
        if href.startswith("/"):
            return f"{BASE_DOMAIN}{href}?"
        if href.startswith("http://") or href.startswith("https://"):
            return f"{href}?"

    if isinstance(doc_id, str) and doc_id:
        cleaned = doc_id.strip("/")
        return f"{BASE_DOMAIN}/{route_base_path}/{cleaned}?"

    return f"{BASE_DOMAIN}/{route_base_path}?"


def generate_for_instance(root_dir: str, instance: Dict[str, Any]) -> Tuple[Optional[str], List[str]]:
    label = instance.get("label") or instance.get("id") or ""
    path = instance.get("path")
    route_base_path = instance.get("routeBasePath")

    if not path or not route_base_path:
        return None, []

    # Skip instances whose path is an URL or non-existent directory
    if is_url(path):
        return None, []

    abs_sidebar_path = os.path.join(root_dir, path, SIDEBARS_FILENAME)
    if not os.path.isfile(abs_sidebar_path):
        return None, []

    try:
        sidebar_json = load_json_file(abs_sidebar_path)
    except Exception as e:
        print(f"[WARN] Failed to read {abs_sidebar_path}: {e}", file=sys.stderr)
        return None, []

    nodes = traverse_collect_article_nodes(sidebar_json)
    if not nodes:
        return None, []

    # Build rewrite lines per instance
    lines: List[str] = []
    dest_urls: List[str] = []
    lines.append(f"# {label}")

    seen_ids: set = set()
    # Try stable order: sort by numeric articleID if possible
    def _article_id_value(n: Dict[str, Any]) -> Tuple[int, str]:
        raw = n.get("articleID")
        try:
            return (int(raw), str(raw))
        except Exception:
            return (2**31 - 1, str(raw))

    for node in sorted(nodes, key=_article_id_value):
        article_id = node.get("articleID")
        if article_id is None:
            continue
        article_id_str = str(article_id).strip()
        if not article_id_str or article_id_str in seen_ids:
            continue
        seen_ids.add(article_id_str)

        dest = build_destination_url(route_base_path, node)
        dest_urls.append(dest)
        lines.append(
            f"rewrite ^/article/{article_id_str}$ {dest} permanent;"
        )

    if len(lines) <= 1:
        return None, []
    return "\n".join(lines), dest_urls


def convert_to_local_url(remote_url: str) -> str:
    """Replace remote domain with http://localhost:3000 and drop trailing '?' if no query."""
    try:
        parsed = urlparse(remote_url)
        path = parsed.path or "/"
        query = parsed.query
        base = "http://localhost:3000"
        if query:
            return f"{base}{path}?{query}"
        return f"{base}{path}"
    except Exception:
        # Fallback: naive replace
        if remote_url.endswith("?"):
            remote_url = remote_url[:-1]
        # Ensure we only keep path
        try:
            parsed = urlparse(remote_url)
            return f"http://localhost:3000{parsed.path}"
        except Exception:
            return "http://localhost:3000/"


def check_urls_and_log(root_dir: str, dest_urls: List[str]) -> None:
    failures: List[str] = []
    seen: set = set()

    # Deduplicate while preserving order
    unique_remotes: List[str] = []
    for remote in dest_urls:
        if not isinstance(remote, str) or not remote:
            continue
        if remote in seen:
            continue
        seen.add(remote)
        unique_remotes.append(remote)

    total = len(unique_remotes)
    checked = 0
    if total:
        print(f"[INFO] Checking {total} URLs...", file=sys.stderr)

    def _try_status(url: str) -> int:
        # Try HEAD first
        try:
            req = Request(url, method="HEAD")
            with urlopen(req, timeout=5) as resp:
                return getattr(resp, "status", None) or resp.getcode()
        except HTTPError as he:
            # Some servers return 405 for HEAD; fallback to GET in that case
            if he.code in (400, 401, 403, 404, 405, 500, 501, 502, 503, 504):
                # propagate for logging unless 405 where we will retry GET
                if he.code != 405:
                    raise
            else:
                raise
        except URLError:
            # fallback to GET
            pass
        except Exception:
            # fallback to GET
            pass
        # Fallback GET without reading body
        req = Request(url, method="GET")
        with urlopen(req, timeout=5) as resp:
            return getattr(resp, "status", None) or resp.getcode()

    for remote in unique_remotes:
        local_url = convert_to_local_url(remote)
        try:
            code = int(_try_status(local_url))
            if code != 200:
                failures.append(f"{local_url}\tHTTP {code}\tfrom {remote}")
        except HTTPError as he:
            failures.append(f"{local_url}\tHTTP {he.code}\tfrom {remote}")
        except URLError as ue:
            failures.append(f"{local_url}\tURLERR {ue.reason}\tfrom {remote}")
        except Exception as e:
            failures.append(f"{local_url}\tERROR {e}\tfrom {remote}")

        checked += 1
        if checked == 1 or checked % 50 == 0 or checked == total:
            print(f"[INFO] Progress: {checked}/{total}", file=sys.stderr)

    # Always write the error file (empty if no failures)
    error_path = os.path.join(root_dir, ERROR_LOG_FILENAME)
    try:
        with open(error_path, "w", encoding="utf-8") as f:
            if failures:
                f.write("\n".join(failures) + "\n")
            else:
                f.write("")
    except Exception as e:
        print(f"[ERROR] Failed to write {error_path}: {e}", file=sys.stderr)


def main(argv: List[str]) -> int:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, CONFIG_FILENAME)

    try:
        config = load_json_file(config_path)
    except Exception as e:
        print(f"[ERROR] Failed to load {config_path}: {e}", file=sys.stderr)
        return 1

    instances = config.get("instances", [])
    if not isinstance(instances, list) or not instances:
        print("[ERROR] No instances found in configuration.", file=sys.stderr)
        return 1

    # Optional: filter by instance id if provided via CLI args
    filter_ids = set(argv[1:]) if len(argv) > 1 else set()

    outputs: List[str] = []
    all_dests: List[str] = []
    for instance in instances:
        instance_id = instance.get("id")
        if filter_ids and instance_id not in filter_ids:
            continue

        block, dests = generate_for_instance(script_dir, instance)
        if block:
            outputs.append(block)
        if dests:
            all_dests.extend(dests)

    # Write results to transfer.conf in project root
    out_path = os.path.join(script_dir, OUTPUT_FILENAME)
    content = ("\n\n".join(outputs) + "\n") if outputs else ""
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"[ERROR] Failed to write {out_path}: {e}", file=sys.stderr)
        return 1

    # After writing, verify local URLs and log failures
    try:
        check_urls_and_log(script_dir, all_dests)
    except Exception as e:
        print(f"[ERROR] URL verification failed: {e}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))


