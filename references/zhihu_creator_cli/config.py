"""Central configuration for Zhihu Creator CLI."""

import os
from pathlib import Path

# Base paths
HOME_DIR = Path.home()
CONFIG_DIR = HOME_DIR / ".zhihu-creator-cli"
COOKIES_FILE = CONFIG_DIR / "cookies.json"
CREDENTIALS_FILE = CONFIG_DIR / "credentials.json"

# Ensure config dir exists with secure permissions
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
# 0o700 = rwx------ (owner only)
os.chmod(CONFIG_DIR, 0o700)

# API Endpoints
ZHIHU_API_V4 = "https://www.zhihu.com/api/v4"
ZHIHU_CONTENT_DRAFTS_URL = "https://www.zhihu.com/api/content/drafts"
ZHIHU_CONTENT_PUBLISH_URL = "https://www.zhihu.com/api/content/publish"
ZHIHU_IMAGE_API = "https://www.zhihu.com/api/v4/images"
ZHIHU_OSS_UPLOAD_URL = "https://picx.galgamer.eu.org"
ZHIHU_ZHUANLAN_API = "https://zhuanlan.zhihu.com/api/articles"
ZHIHU_CREATOR_API = "https://www.zhihu.com/api/v4/creator"
ZHIHU_CREATOR_HOME_API = "https://www.zhihu.com/creator/api/v1"
ZHIHU_ANSWER_API = "https://www.zhihu.com/api/v4/answers"

# Request settings
DEFAULT_TIMEOUT = 15
CHROME_VERSION = "124"

# Browser fingerprint headers (consistent across all requests)
def get_browser_headers() -> dict[str, str]:
    """Return headers that mimic Chrome browser.

    Reduces risk-control / anti-crawl triggers by presenting
    a uniform, modern browser fingerprint.
    """
    return {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            f"Chrome/{CHROME_VERSION}.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "sec-ch-ua": f'"Chromium";v="{CHROME_VERSION}", "Google Chrome";v="{CHROME_VERSION}"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Referer": "https://www.zhihu.com/",
    }
