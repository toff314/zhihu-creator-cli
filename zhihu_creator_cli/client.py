"""Zhihu API client (read-only).

Encapsulates all HTTP calls to Zhihu's web API, focusing on:
- Article management (list, detail)
- Question discovery (recommend, search, detail, answers)
"""

from __future__ import annotations

import json
import logging
from typing import Any

import requests

from .adapters import ForceIPv4Adapter
from .config import (
    DEFAULT_TIMEOUT,
    ZHIHU_API_V4,
    ZHIHU_ZHUANLAN_API,
    get_browser_headers,
)
from .exceptions import DataFetchError, LoginError

logger = logging.getLogger(__name__)


class ZhihuClient:
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

    def __enter__(self) -> ZhihuClient:
        return self

    def __exit__(self, *_) -> None:
        self.close()

    def close(self) -> None:
        self._session.close()

    # ---- Low-level helpers ----

    def _get(self, url: str, **kwargs) -> dict:
        kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
        try:
            resp = self._session.get(url, **kwargs)
        except requests.RequestException as e:
            raise DataFetchError(f"GET {url} failed: {e}") from e
        return self._handle_response(resp, url)

    def _handle_response(self, resp: requests.Response, url: str) -> dict:
        if resp.status_code == 401:
            raise LoginError("Session expired or not logged in (HTTP 401)")
        if resp.status_code != 200:
            raise DataFetchError(
                f"HTTP {resp.status_code} from {url}: {resp.text[:300]}"
            )
        try:
            return resp.json()
        except json.JSONDecodeError as e:
            raise DataFetchError(f"Invalid JSON from {url}: {e}") from e

    # ============================================================
    #  1. Articles
    # ============================================================

    def get_creator_articles(
        self,
        offset: int = 0,
        limit: int = 20,
        status: str = "all",
        sort: str = "created",
    ) -> dict:
        """Fetch articles from the creator center (创作中心文章列表).

        Uses ``/api/v4/members/{url_token}/articles`` as the endpoint.

        Args:
            offset: Pagination offset.
            limit: Items per page (default 20).
            status: Filter by status - ``all``, ``published``, ``draft``.
            sort: Sort order - ``created`` (newest), ``updated``, ``voteups``.

        Returns:
            API response dict with ``data`` (list) and ``paging``.
        """
        me = self._get(f"{ZHIHU_API_V4}/me")
        url_token = me.get("url_token", "")
        if not url_token:
            raise DataFetchError("Cannot get user url_token")

        url = f"{ZHIHU_API_V4}/members/{url_token}/articles"
        params: dict[str, Any] = {
            "include": "data[*].title,excerpt,created_time,updated_time,voteup_count,comment_count",
            "offset": offset,
            "limit": limit,
            "sort_by": sort,
        }
        if status != "all":
            params["status"] = status

        return self._get(url, params=params)

    def get_article_detail(self, article_id: str) -> dict:
        """Get full detail of a single article by its ID."""
        url = f"{ZHIHU_ZHUANLAN_API}/{article_id}"
        return self._get(url)

    # ============================================================
    #  2. Question Discovery
    # ============================================================

    def get_recommended_questions(
        self,
        offset: int = 0,
        limit: int = 20,
        topic_id: str | None = None,
    ) -> dict:
        """Fetch recommended questions for the logged-in user.

        Uses ``/api/v3/feed/topstory/recommend`` (home feed) then extracts
        question entries.

        Args:
            offset: Pagination offset.
            limit: Items per page.
            topic_id: Optional topic filter.

        Returns:
            API response with question list under ``data``.
        """
        url = "https://www.zhihu.com/api/v3/feed/topstory/recommend"
        params: dict[str, Any] = {
            "offset": offset,
            "limit": limit,
        }
        if topic_id:
            params["topic_id"] = topic_id

        result = self._get(url, params=params)
        questions = []
        for item in result.get("data", []):
            target = item.get("target", {})
            if target.get("type") == "answer":
                q = target.get("question", {})
                if q:
                    questions.append(q)
            elif target.get("type") == "question":
                questions.append(target)

        return {
            "data": questions,
            "paging": result.get("paging", {}),
        }

    def search_questions(
        self,
        keyword: str,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        """Search for questions by keyword.

        Args:
            keyword: Search query.
            offset: Pagination offset.
            limit: Results per page.

        Returns:
            API response with search results.
        """
        url = f"{ZHIHU_API_V4}/search_v3"
        params = {
            "gk_version": "gz-gaokao",
            "t": "question",
            "q": keyword,
            "correction": 1,
            "offset": offset,
            "limit": limit,
            "filter_fields": "lc_idx",
            "lc_idx": 0,
            "show_all_topics": 0,
            "search_source": "Normal",
        }
        return self._get(url, params=params)

    def get_question_detail(self, question_id: str) -> dict:
        """Get question detail including metadata.

        Note:
            Direct ``/questions/{id}`` may return 403 with code 10003.
            Falls back to extracting from the answers endpoint.

        Args:
            question_id: Numeric question ID.

        Returns:
            Question dict with ``title``, ``detail``, ``answer_count``, etc.
        """
        url = f"{ZHIHU_API_V4}/questions/{question_id}"
        params: dict[str, str] = {
            "include": (
                "answer_count,follower_count,"
                "visit_count,comment_count,created_time,"
                "updated_time,detail,topics"
            ),
        }
        backup_headers = dict(self._session.headers)
        backup_headers.pop("x-requested-with", None)
        try:
            resp = self._session.get(url, params=params, headers=backup_headers, timeout=DEFAULT_TIMEOUT)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        # Fallback: get first answer's question info
        try:
            answers = self.get_question_answers(question_id, limit=1)
            first = (answers.get("data") or [{}])[0]
            q = first.get("question", {})
            if q:
                return q
        except Exception:
            pass

        raise DataFetchError(f"Failed to get question {question_id} detail (tried multiple methods)")

    def get_invite_notifications(
        self,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        """Fetch question invite notifications for the logged-in user.

        Uses ``/api/v4/notifications/v2/recent`` then filters for
        question-invite entries (verb = " 邀请你回答问题" or
        " 的提问等你来答").

        Args:
            offset: Pagination offset.
            limit: Items per page.

        Returns:
            API response with invited question list under ``data``.
            Each item contains: question, inviter_name, verb, is_read.
        """
        url = "https://www.zhihu.com/api/v4/notifications/v2/recent"
        params: dict[str, Any] = {
            "offset": offset,
            "limit": limit,
            "entry_name": "all",
        }

        result = self._get(url, params=params)
        invites = []
        INVITE_VERBS = {" 邀请你回答问题", " 的提问等你来答"}

        for item in result.get("data", []):
            content = item.get("content", {})
            verb = content.get("verb", "")
            if verb not in INVITE_VERBS:
                continue

            target = item.get("target", {})
            if target.get("type") != "question":
                continue

            actors = content.get("actors", [])
            inviter = actors[0] if actors else {}

            invites.append({
                "question": target,
                "inviter_name": inviter.get("name", ""),
                "inviter_url_token": inviter.get("url_token", ""),
                "verb": verb.strip(),
                "is_read": item.get("is_read", True),
                "merge_count": item.get("merge_count", 1),
            })

        return {
            "data": invites,
            "paging": result.get("paging", {}),
        }

    def get_question_answers(
        self,
        question_id: str,
        offset: int = 0,
        limit: int = 20,
        sort_by: str = "default",
    ) -> dict:
        """Get answers for a question.

        Args:
            question_id: The question ID.
            offset: Pagination offset.
            limit: Answers per page.
            sort_by: ``default`` or ``updated``.
        """
        url = f"{ZHIHU_API_V4}/questions/{question_id}/answers"
        params = {
            "include": (
                "data[*].content,voteup_count,comment_count,"
                "created_time,updated_time,author"
            ),
            "offset": offset,
            "limit": limit,
            "sort_by": sort_by,
        }
        return self._get(url, params=params)
