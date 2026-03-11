#!/usr/bin/env python3
"""Find local .mdx file by documentation URL.
Usage: python find_mdx.py <docs_root> <url>
  docs_root: repo root containing docuo.config.*.json
  url: page URL or path like /real-time-video-ios-oc/introduction/overview
"""

import sys
import json
import re
from pathlib import Path
from urllib.parse import urlparse

CONFIG_FILE_PRIORITY = [
    "docuo.config.zh.json",
    "docuo.config.en.json",
    "docuo.config.json",
]


def get_config_file_by_domain(url):
    try:
        hostname = urlparse(url).hostname or ""
        if hostname == "doc-zh.zego.im":
            return "docuo.config.zh.json"
        elif hostname.endswith("zegocloud.com"):
            return "docuo.config.en.json"
    except Exception:
        pass
    return "docuo.config.json"


def is_zegocloud_domain(url):
    """Check if URL belongs to www.zegocloud.com domain."""
    try:
        hostname = urlparse(url).hostname or ""
        return hostname == "zegocloud.com" or  hostname == "www.zegocloud.com" or hostname.endswith(".zegocloud.com")
    except Exception:
        return False


def process_url_path(url, parsed_path):
    """Process URL path based on domain.

    For www.zegocloud.com, URLs have /docs prefix that needs to be stripped.
    E.g., /docs/uikit/live-streaming-kit-android -> uikit/live-streaming-kit-android
    """
    if is_zegocloud_domain(url):
        # Strip /docs prefix for zegocloud.com URLs
        path = parsed_path.lstrip("/")
        if path.startswith("docs/"):
            return "/" + path[5:]
        return parsed_path
    return parsed_path


def read_config_by_priority(docs_root):
    for name in CONFIG_FILE_PRIORITY:
        p = Path(docs_root) / name
        if p.exists():
            try:
                return json.loads(p.read_text("utf-8"))
            except Exception:
                pass
    return None


def path_to_file_id(file_path):
    """Convert relative file path to fileId for URL matching."""
    no_ext = re.sub(r"\.(md|mdx)$", "", file_path, flags=re.IGNORECASE)
    parts = no_ext.split("/")
    result = []
    for seg in parts:
        s = re.sub(r"^[0-9]+-", "", seg)   # remove numeric prefix like "01-"
        s = s.lower()
        s = re.sub(r"\s+", "-", s)         # spaces to hyphens
        result.append(s)
    file_id = "/".join(result)
    if file_id.endswith("/index"):
        file_id = file_id[: -len("/index")]
    return file_id


def find_best_match_instance(url_path, instances):
    """Greedy match: find instance with longest matching routeBasePath."""
    segments = [s for s in url_path.lstrip("/").split("/") if s]
    best = None
    for inst in instances:
        route = (inst.get("routeBasePath") or "").strip("/")
        if not route:
            continue
        route_segs = [s for s in route.split("/") if s]
        if len(route_segs) > len(segments):
            continue
        if segments[: len(route_segs)] == route_segs:
            if best is None or len(route_segs) > best[2]:
                remaining = "/".join(segments[len(route_segs) :])
                best = (inst, remaining, len(route_segs))
    if best:
        return best[0], best[1]
    return None


def find_file_by_file_id(instance_path, target_file_id):
    """Recursively search instance dir for file matching fileId."""
    base = Path(instance_path)
    for ext in ("*.mdx", "*.md"):
        for f in base.rglob(ext):
            rel = f.relative_to(base).as_posix()
            if path_to_file_id(rel) == target_file_id:
                return str(f)
    return None


def main():
    if len(sys.argv) < 3:
        print("Usage: python find_mdx.py <docs_root> <url>", file=sys.stderr)
        sys.exit(1)

    docs_root = sys.argv[1]
    url = sys.argv[2]

    trimmed = url.strip()
    if trimmed.startswith("/") and not trimmed.startswith("//"):
        url_path = trimmed
        config_file_name = "docuo.config.zh.json"
    else:
        parsed = urlparse(trimmed)
        url_path = process_url_path(trimmed, parsed.path)
        config_file_name = get_config_file_by_domain(trimmed)

    config = None
    specific = Path(docs_root) / config_file_name
    if specific.exists():
        try:
            config = json.loads(specific.read_text("utf-8"))
        except Exception:
            pass
    if not config:
        config = read_config_by_priority(docs_root)
    if not config:
        print(f"Error: no docuo config found in {docs_root}", file=sys.stderr)
        sys.exit(1)

    instances = config.get("instances", [])
    if not instances:
        print("Error: no instances in config", file=sys.stderr)
        sys.exit(1)

    result = find_best_match_instance(url_path, instances)
    if not result:
        print(f"Error: no matching instance for {url_path}", file=sys.stderr)
        sys.exit(1)

    instance, remaining_path = result
    instance_dir = Path(docs_root) / (instance.get("path") or "").strip("/")
    target_file_id = remaining_path.lower()

    file_path = find_file_by_file_id(str(instance_dir), target_file_id)
    if file_path:
        print(file_path)
    else:
        print(
            f"Error: no file for fileId={target_file_id} in {instance_dir}",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
