"""Article domain mixin for ZhihuClient."""

from __future__ import annotations

from typing import Any

from ..config import ZHIHU_API_V4, ZHIHU_ZHUANLAN_API
from ..exceptions import DataFetchError


class ArticleMixin:
    def get_creator_articles(
        self,
        offset: int = 0,
        limit: int = 20,
        status: str = "all",
        sort: str = "created",
    ) -> dict:
        me = self._get(f"{ZHIHU_API_V4}/me")
        url_token = me.get("url_token", "")
        if not url_token:
            raise DataFetchError("Cannot get user url_token")

        url = f"{ZHIHU_API_V4}/members/{url_token}/articles"
        params: dict[str, Any] = {
            "include": (
                "data[*].title,excerpt,created_time,updated_time,"
                "voteup_count,comment_count,reaction.statistics"
            ),
            "offset": offset,
            "limit": limit,
            "sort_by": sort,
        }
        if status != "all":
            params["status"] = status

        return self._get(url, params=params)

    def get_article_detail(self, article_id: str) -> dict:
        url = f"{ZHIHU_ZHUANLAN_API}/{article_id}"
        return self._get(url)
