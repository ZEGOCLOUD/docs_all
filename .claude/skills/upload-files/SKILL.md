---
name: upload-files
description: This skill should be used when the user asks to "upload an image", "upload a video", "upload a file", "insert an image", "insert a video", "add an attachment", "upload to OSS", "上传图片", "上传视频", "上传文件", "插入图片", "插入视频", "添加附件", or any task that requires uploading local files (images, videos, demos, attachments) to ZEGO Doc OSS and obtaining a CDN URL for use in documentation.
---

# Upload Files to ZEGO Doc OSS

Upload local files (images, videos, demos, other attachments) to ZEGO Doc OSS and obtain a CDN URL for embedding in MDX documentation.

## Upload Script

The upload script is located at `scripts/upload_to_oss.py`. It uploads a local file to ZEGO Doc OSS, auto-detects the target bucket by file extension, and prints the CDN URL.

### Prerequisites

The Python packages `requests` and `oss2` must be installed. Install if missing:

```bash
pip3 install requests oss2
```

Environment variables `DOCUO_USERNAME` and `DOCUO_PASSWORD` must be set in the user's shell. Do not prompt for these values.

### Usage

```bash
python3 scripts/upload_to_oss.py <file> [--path <oss_path_prefix>] [--bucket <bucket>]
```

- `file` — Path to the local file to upload.
- `--path` — OSS path prefix. The final OSS key becomes `<prefix>/<filename>`. Omit to place at bucket root.
- `--bucket` — Override the target bucket. Auto-detected from file extension when omitted.

### Bucket Auto-Detection

| File Type | Extensions | Bucket | CDN Domain |
|-----------|-----------|--------|------------|
| Image | .jpg .jpeg .png .gif .webp .svg .bmp | zego-doc-media | doc-media.zego.im |
| Video | .mp4 .webm .ogg .mov .avi .mkv | zego-doc-media | doc-media.zego.im |
| Demo | .apk .zip | zego-artifact-demonstration | artifact-demo.zego.im |
| Other | * | zego-doc-media | doc-media.zego.im |

## Workflow

### Uploading an Image or Video

1. Determine the local file path to upload.
2. Determine the OSS path prefix based on the document's location in the docs structure. For example, a file used in `core_products/aiagent/zh/android/introduction` should use `--path core_products/aiagent/zh/android/introduction`.
3. Run the upload script:

```bash
python3 scripts/upload_to_oss.py /path/to/local/file.png --path core_products/aiagent/zh/android/introduction
```

4. The script outputs a CDN URL (e.g. `https://doc-media.zego.im/core_products/aiagent/zh/android/introduction/file.png`). Use this URL in the MDX document.

### Inserting into MDX

After obtaining the CDN URL, insert it using the appropriate MDX component

## Examples

Upload an image to a specific path:

```bash
python3 scripts/upload_to_oss.py ./banner.png --path en/sdk/quickstart
# Output: CDN URL: https://doc-media.zego.im/en/sdk/quickstart/banner.png
```

Upload a video to the bucket root:

```bash
python3 scripts/upload_to_oss.py ./tutorial.mp4
# Output: CDN URL: https://doc-media.zego.im/tutorial.mp4
```

Upload a demo APK with explicit bucket:

```bash
python3 scripts/upload_to_oss.py ./app.apk --path demos/android --bucket zego-artifact-demonstration
# Output: CDN URL: https://artifact-demo.zego.im/demos/android/app.apk
```
