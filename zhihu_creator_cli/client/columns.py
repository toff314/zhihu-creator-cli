"""Column domain mixin for ZhihuClient."""

from ..config import ZHIHU_API, ZHIHU_API_V4, ZHIHU_COLUMN_API
from ..exceptions import DataFetchError


class ColumnMixin:
    def get_user_columns(self) -> dict:
        me = self._get(f"{ZHIHU_API_V4}/me")
        url_token = me.get("url_token", "")
        if not url_token:
            raise DataFetchError("Cannot get user url_token")

        url = f"{ZHIHU_API_V4}/search_v3"
        params = {
            "t": "column",
            "q": url_token,
            "correction": 1,
            "limit": 50,
            "filter_fields": "lc_idx",
            "lc_idx": 0,
            "show_all_topics": 0,
            "search_source": "Normal",
        }
        data = self._get_no_xsrf(url, params=params)

        user_columns = []
        for item in data.get("data", []):
            obj = item.get("object", item)
            if obj.get("type") != "column":
                continue
            author = obj.get("author", {})
            if author.get("url_token") == url_token:
                user_columns.append(obj)

        return {
            "data": user_columns,
            "paging": {
                "totals": len(user_columns),
                "is_end": True,
            },
        }

    def get_recommended_columns(
        self,
        classify: int = 1,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        url = f"{ZHIHU_API}/columns"
        params = {
            "classify": classify,
            "excerpt_len": 75,
            "offset": offset,
            "limit": limit,
        }
        return self._get(url, params=params)

    def search_columns(
        self,
        keyword: str,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        url = f"{ZHIHU_API_V4}/search_v3"
        params = {
            "t": "column",
            "q": keyword,
            "correction": 1,
            "offset": offset,
            "limit": limit,
            "filter_fields": "lc_idx",
            "lc_idx": 0,
            "show_all_topics": 0,
            "search_source": "Normal",
        }
        return self._get_no_xsrf(url, params=params)

    def get_column_detail(self, slug: str) -> dict:
        url = f"{ZHIHU_COLUMN_API}/{slug}"
        return self._get(url)

    def get_column_articles(
        self,
        slug: str,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        url = f"{ZHIHU_API}/columns/{slug}/articles"
        params = {
            "offset": offset,
            "limit": limit,
        }
        return self._get(url, params=params)
