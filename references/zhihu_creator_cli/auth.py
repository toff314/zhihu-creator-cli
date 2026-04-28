"""Authentication manager: cookie storage and session validation."""

import json
import logging
import os
from pathlib import Path

import requests

from .adapters import ForceIPv4Adapter
from .config import CONFIG_DIR, COOKIES_FILE, CREDENTIALS_FILE, DEFAULT_TIMEOUT, get_browser_headers
from .exceptions import LoginError

logger = logging.getLogger(__name__)


def _ipv4_session() -> requests.Session:
    """Create a requests.Session that forces IPv4 connections."""
    s = requests.Session()
    s.mount("https://", ForceIPv4Adapter())
    s.mount("http://", ForceIPv4Adapter())
    return s


class AuthManager:
    """Handles Zhihu login state via Cookie."""

    def __init__(self) -> None:
        self.cookies: dict[str, str] = {}
        self._load_cookies()

    def _load_cookies(self) -> None:
        """Load cookies from local file if present."""
        if COOKIES_FILE.exists():
            try:
                data = json.loads(COOKIES_FILE.read_text(encoding="utf-8"))
                self.cookies = data if isinstance(data, dict) else {}
            except (json.JSONDecodeError, OSError) as e:
                logger.warning("Failed to load cookies: %s", e)
                self.cookies = {}

    def save_cookies(self) -> None:
        """Persist current cookies to local file with secure permissions."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        COOKIES_FILE.write_text(
            json.dumps(self.cookies, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        os.chmod(COOKIES_FILE, 0o600)

    def clear_cookies(self) -> None:
        """Remove stored credentials."""
        self.cookies = {}
        for f in (COOKIES_FILE, CREDENTIALS_FILE):
            if f.exists():
                f.unlink()

    def login_with_cookie_string(self, cookie_str: str) -> dict[str, str]:
        """Parse and store a raw cookie string.

        Expected format: ``z_c0=xxx; _xsrf=yyy; d_c0=zzz``
        """
        cookies: dict[str, str] = {}
        for part in cookie_str.split(";"):
            part = part.strip()
            if "=" in part:
                k, v = part.split("=", 1)
                cookies[k.strip()] = v.strip()

        required = {"z_c0", "_xsrf", "d_c0"}
        missing = required - set(cookies.keys())
        if missing:
            raise LoginError(f"Missing required cookies: {missing}")

        self.cookies = cookies
        self.save_cookies()
        return cookies

    def is_logged_in(self) -> bool:
        """Check whether stored cookies look like a valid session (local only)."""
        return bool(self.cookies.get("z_c0") and self.cookies.get("_xsrf"))

    def validate_online(self) -> bool:
        """Hit ``/api/v4/me`` to verify the current session is accepted by Zhihu."""
        if not self.is_logged_in():
            return False
        url = "https://www.zhihu.com/api/v4/me"
        headers = get_browser_headers()
        headers["cookie"] = "; ".join(f"{k}={v}" for k, v in self.cookies.items())
        try:
            resp = _ipv4_session().get(url, headers=headers, timeout=DEFAULT_TIMEOUT)
            return resp.status_code == 200 and resp.json().get("name") is not None
        except Exception:
            return False
