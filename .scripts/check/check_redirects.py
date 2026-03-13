#!/usr/bin/env python3
"""
检查旧文档链接的重定向情况。

读取 check_link_result.json 中的 old-doc 链接，
通过 HTTP HEAD 请求获取重定向后的最终 URL。
"""

import json
import requests
from typing import Optional
from pathlib import Path
from urllib.parse import urlparse


def get_final_url(url: str, timeout: int = 10) -> dict:
    """
    获取 URL 重定向后的最终地址。

    Args:
        url: 原始 URL
        timeout: 请求超时时间（秒）

    Returns:
        包含重定向信息的字典
    """
    result = {
        "original_url": url,
        "final_url": url,
        "status_code": None,
        "redirected": False,
        "redirect_chain": [],
        "error": None
    }

    try:
        # 使用 HEAD 请求，跟随重定向
        response = requests.head(
            url,
            timeout=timeout,
            allow_redirects=True
        )

        result["status_code"] = response.status_code
        result["final_url"] = response.url

        # 提取 path 部分（不含域名）
        parsed = urlparse(response.url)
        result["url_path"] = parsed.path
        if parsed.fragment:  # 如果有锚点，加上锚点
            result["url_path"] += f"#{parsed.fragment}"

        result["redirected"] = len(response.history) > 0
        result["redirect_chain"] = [r.url for r in response.history]

    except requests.exceptions.RequestException as e:
        result["error"] = str(e)

    return result


def check_redirects(
    result_file: str = None,
    output_file: str = None
) -> dict:
    """
    检查所有 old-doc 链接的重定向情况。

    Args:
        result_file: check_link_result.json 文件路径
        output_file: 输出文件路径（可选）

    Returns:
        重定向检查结果
    """
    if result_file is None:
        result_file = Path(__file__).parent / "check_link_result.json"

    result_file = Path(result_file)

    # 读取链接检查结果
    with open(result_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 获取 old-doc 链接列表
    old_doc_urls = data.get("urls_by_category", {}).get("external", {}).get("old-doc", [])

    if not old_doc_urls:
        print("未找到 old-doc 链接")
        return {"urls": []}

    print(f"共找到 {len(old_doc_urls)} 个旧文档链接，开始检查重定向...\n")

    redirect_results = []

    for item in old_doc_urls:
        url = item["url"]
        count = item["count"]

        print(f"检查：{url}")
        result = get_final_url(url)
        result["count"] = count

        # 简化输出
        if result["redirected"]:
            print(f"  → 重定向 ({len(result['redirect_chain'])} 次)")
            for redirect_url in result["redirect_chain"]:
                print(f"    → {redirect_url}")
            print(f"  → 最终：{result['final_url']}")
        elif result["error"]:
            print(f"  ✗ 错误：{result['error']}")
        else:
            print(f"  ✓ 无重定向 (状态码：{result['status_code']})")

        redirect_results.append(result)
        print()

    # 构建输出结果
    output = {
        "summary": {
            "total": len(redirect_results),
            "redirected": sum(1 for r in redirect_results if r["redirected"]),
            "no_redirect": sum(1 for r in redirect_results if not r["redirected"] and not r["error"]),
            "error": sum(1 for r in redirect_results if r["error"])
        },
        "urls": redirect_results
    }

    # 保存结果
    if output_file is None:
        output_file = result_file.parent / "check_redirect_result.json"

    output_file = Path(output_file)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"结果已保存到：{output_file}")
    print(f"\n汇总:")
    print(f"  总链接数：{output['summary']['total']}")
    print(f"  发生重定向：{output['summary']['redirected']}")
    print(f"  无重定向：{output['summary']['no_redirect']}")
    print(f"  请求错误：{output['summary']['error']}")

    return output


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="检查旧文档链接的重定向情况")
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help="check_link_result.json 文件路径（默认：当前目录下的 check_link_result.json）"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="输出文件路径（默认：check_redirect_result.json）"
    )

    args = parser.parse_args()

    check_redirects(result_file=args.input, output_file=args.output)
