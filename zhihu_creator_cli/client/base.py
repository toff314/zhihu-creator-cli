"""Core ZhihuClient base class with HTTP helpers and session management."""

from __future__ import annotations

import json
import logging

import requests

from ..adapters import ForceIPv4Adapter
from ..config import DEFAULT_TIMEOUT, get_browser_headers
from ..exceptions import DataFetchError, LoginError

logger = logging.getLogger(__name__)


class ZhihuClientBase:
    """Authenticated HTTP client for Zhihu (read-only).

    Usage::

        auth = AuthManager()
        client = ZhihuClient(auth.cookies)
        articles = client.get_creator_articles()
        detail = client.get_article_detail("123456")
    """

    def __init__(self, cookie_dict: dict[str, str]) -> None:
        self._session = requests.Session()
        self._session.mount("https://", ForceIPv4Adapter())
        self._session.mount("http://", ForceIPv4Adapter())
        self._session.headers.update(get_browser_headers())
        for name, value in cookie_dict.items():
            self._session.cookies.set(name, value, domain=".zhihu.com")
        xsrf = cookie_dict.get("_xsrf", "")
        if xsrf:
            self._session.headers["x-xsrftoken"] = xsrf

    def __enter__(self) -> ZhihuClientBase:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        self._session.close()

    def _get(self, url: str, **kwargs: object) -> dict:
        kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
        try:
            resp = self._session.get(url, **kwargs)
        except requests.RequestException as e:
            raise DataFetchError(f"GET {url} failed: {e}") from e
        return self._handle_response(resp, url)

    def _get_no_xsrf(self, url: str, **kwargs: object) -> dict:
        kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
        headers = dict(self._session.headers)
        headers.pop("x-requested-with", None)
        headers.pop("x-xsrftoken", None)
        try:
            resp = self._session.get(url, headers=headers, **kwargs)
        except requests.RequestException as e:
            raise DataFetchError(f"GET {url} failed: {e}") from e
        return self._handle_response(resp, url)

    def _handle_response(self, resp: requests.Response, url: str) -> dict:
        if resp.status_code == 401:
            raise LoginError("Session expired or not logged in (HTTP 401)")
        if resp.status_code != 200:
            raise DataFetchError(f"HTTP {resp.status_code} from {url}: {resp.text[:300]}")
        try:
            return resp.json()
        except json.JSONDecodeError as e:
            raise DataFetchError(f"Invalid JSON from {url}: {e}") from e

    def resolve_user_id(self, url_token: str) -> str:
        me = self._get(f"https://www.zhihu.com/api/v4/members/{url_token}")
        uid = me.get("id", "")
        if not uid:
            raise DataFetchError(f"Cannot resolve user_id for url_token={url_token}")
        return str(uid)
