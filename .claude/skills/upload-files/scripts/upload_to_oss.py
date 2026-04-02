#!/usr/bin/env python3
"""
Upload a local file to Zego Doc OSS.

Environment variables:
  DOCUO_USERNAME  - Dashboard login username (required)
  DOCUO_PASSWORD  - Dashboard login password (required)
  DASHBOARD_URL   - Override dashboard API URL (optional, default: https://zego-doc-dashboard.spreading.cc)

Usage:
  pip install requests oss2
  python upload_to_oss.py <file> [--path <oss_path_prefix>] [--bucket <bucket>]

File type / bucket mapping (auto-detected by extension):
  Images (.jpg .jpeg .png .gif .webp .svg .bmp)  -> zego-doc-media              -> https://doc-media.zego.im
  Videos (.mp4 .webm .ogg .mov .avi .mkv)        -> zego-doc-media              -> https://doc-media.zego.im
  Demos  (.apk .zip)                             -> zego-artifact-demonstration  -> https://artifact-demo.zego.im
  Others                                          -> zego-doc-media              -> https://doc-media.zego.im

Examples:
  # Upload an image (OSS key = filename only)
  DOCUO_USERNAME=foo DOCUO_PASSWORD=bar python upload_to_oss.py ./banner.png

  # Upload with a custom OSS path prefix
  DOCUO_USERNAME=foo DOCUO_PASSWORD=bar python upload_to_oss.py ./demo.mp4 --path en/sdk/quickstart

  # Override the target bucket
  DOCUO_USERNAME=foo DOCUO_PASSWORD=bar python upload_to_oss.py ./sdk.zip --bucket zego-artifact-demonstration
"""

import argparse
import os
import sys

import oss2
import requests

DASHBOARD_URL = os.environ.get("DASHBOARD_URL", "https://zego-doc-dashboard.spreading.cc")

BUCKET_FOR_TYPE = {
    "image": "zego-doc-media",
    "video": "zego-doc-media",
    "demo":  "zego-artifact-demonstration",
    "other": "zego-doc-media",
}

CDN_DOMAIN_MAP = {
    "zego-doc-media":              "https://doc-media.zego.im",
    "zego-artifact-sdk":           "https://artifact-sdk.zego.im",
    "zego-artifact-demonstration": "https://artifact-demo.zego.im",
}

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp"}
VIDEO_EXTS = {".mp4", ".webm", ".ogg", ".mov", ".avi", ".mkv"}
DEMO_EXTS  = {".apk", ".zip"}


def classify_file(filename):
    """Return (type_str, bucket_name) based on file extension."""
    _, ext = os.path.splitext(filename.lower())
    if ext in IMAGE_EXTS:
        return "image", BUCKET_FOR_TYPE["image"]
    if ext in VIDEO_EXTS:
        return "video", BUCKET_FOR_TYPE["video"]
    if ext in DEMO_EXTS:
        return "demo", BUCKET_FOR_TYPE["demo"]
    return "other", BUCKET_FOR_TYPE["other"]



def login(username, password):
    resp = requests.post(
        f"{DASHBOARD_URL}/api/auth/login",
        json={"username": username, "password": password},
    )
    resp.raise_for_status()
    data = resp.json()
    if not data.get("success"):
        raise RuntimeError(f"Login failed: {data.get('message', 'Unknown error')}")
    return data["token"]


def get_oss_credentials(token, bucket):
    resp = requests.get(
        f"{DASHBOARD_URL}/api/oss/credentials",
        params={"bucket": bucket},
        headers={"Authorization": f"Bearer {token}"},
    )
    resp.raise_for_status()
    data = resp.json()
    if not data.get("success"):
        raise RuntimeError(f"Failed to get OSS credentials: {data.get('message')}")
    return data["credentials"]


def upload_to_oss(credentials, bucket, oss_path, file_path):
    auth = oss2.StsAuth(
        credentials["accessKeyId"],
        credentials["accessKeySecret"],
        credentials["securityToken"],
    )
    region = credentials["region"]
    # Avoid double "oss-" if region already contains it
    if region.startswith("oss-"):
        endpoint = f"https://{region}.aliyuncs.com"
    else:
        endpoint = f"https://oss-{region}.aliyuncs.com"
    bucket_obj = oss2.Bucket(auth, endpoint, bucket)
    result = bucket_obj.put_object_from_file(oss_path, file_path)
    if result.status != 200:
        raise RuntimeError(f"OSS upload failed with status {result.status}")


def refresh_cdn(token, urls):
    try:
        resp = requests.post(
            f"{DASHBOARD_URL}/api/cdn/refresh",
            json={"urls": urls},
            headers={"Authorization": f"Bearer {token}"},
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("success"):
            print(f"CDN refresh requested: {data.get('taskId', 'OK')}")
        else:
            print(f"CDN refresh failed: {data.get('message', 'Unknown')}")
    except Exception as e:
        print(f"CDN refresh error (non-fatal): {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Upload a local file to Zego Doc OSS.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
environment variables:
  DOCUO_USERNAME   Dashboard login username (required)
  DOCUO_PASSWORD   Dashboard login password (required)
  DASHBOARD_URL    Override dashboard API URL (optional)

bucket auto-detection (by file extension):
  images (.jpg .jpeg .png .gif .webp .svg .bmp)  -> zego-doc-media            (CDN: doc-media.zego.im)
  videos (.mp4 .webm .ogg .mov .avi .mkv)        -> zego-doc-media            (CDN: doc-media.zego.im)
  demos  (.apk .zip)                             -> zego-artifact-demonstration (CDN: artifact-demo.zego.im)
  others                                          -> zego-doc-media            (CDN: doc-media.zego.im)

available buckets (use --bucket to override):
  zego-doc-media              images, videos and other docs
  zego-artifact-demonstration demo apps and sample code (.apk, .zip)
  zego-artifact-sdk           SDK build artifacts

examples:
  DOCUO_USERNAME=foo DOCUO_PASSWORD=bar python upload_to_oss.py ./banner.png
  DOCUO_USERNAME=foo DOCUO_PASSWORD=bar python upload_to_oss.py ./demo.mp4 --path en/sdk/quickstart
  DOCUO_USERNAME=foo DOCUO_PASSWORD=bar python upload_to_oss.py ./sdk.zip --bucket zego-artifact-demonstration
""",
    )
    parser.add_argument("file", help="Path to the local file to upload")
    parser.add_argument(
        "--path",
        help="OSS path prefix, e.g. 'en/sdk/quickstart'. "
             "The final OSS key will be <prefix>/<filename>. "
             "If omitted, the file is placed at the bucket root.",
    )
    parser.add_argument(
        "--bucket",
        help="Override the target bucket. Auto-detected from file extension if not specified.",
    )
    args = parser.parse_args()

    username = os.environ.get("DOCUO_USERNAME")
    password = os.environ.get("DOCUO_PASSWORD")
    if not username or not password:
        print("Error: DOCUO_USERNAME and DOCUO_PASSWORD environment variables are required")
        sys.exit(1)

    local_path = os.path.abspath(args.file)
    if not os.path.isfile(local_path):
        print(f"Error: File not found: {local_path}")
        sys.exit(1)

    filename = os.path.basename(local_path)
    file_type, bucket = classify_file(filename)
    if args.bucket:
        bucket = args.bucket

    print(f"File: {local_path} ({os.path.getsize(local_path)} bytes)")
    print(f"Type: {file_type} -> Bucket: {bucket}")

    # Login
    print("Logging in...")
    token = login(username, password)
    print("Login successful")

    # Get OSS credentials
    print(f"Fetching OSS credentials for bucket: {bucket}")
    creds = get_oss_credentials(token, bucket)

    # Determine OSS path
    oss_path = f"{args.path.rstrip('/')}/{filename}" if args.path else filename

    # Upload
    print(f"Uploading to OSS: {bucket}/{oss_path}")
    upload_to_oss(creds, bucket, oss_path, local_path)
    print("Upload successful!")

    # Construct CDN URL and refresh
    cdn_domain = CDN_DOMAIN_MAP.get(bucket, f"https://{bucket}.zego.im")
    cdn_url = f"{cdn_domain}/{oss_path}"
    refresh_cdn(token, [cdn_url])

    print(f"\n{'='*60}")
    print(f"CDN URL: {cdn_url}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
