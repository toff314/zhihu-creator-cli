"""Search domain mixin for ZhihuClient."""

from ..config import ZHIHU_API_V4

_SEARCH_TYPE_MAP: dict[str, str] = {
    "general": "",
    "question": "question",
    "answer": "answer",
    "article": "article",
    "column": "column",
    "topic": "topic",
    "people": "people",
}


class SearchMixin:
    def search(
        self,
        kind: str,
        keyword: str,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        t = _SEARCH_TYPE_MAP.get(kind, "")
        url = f"{ZHIHU_API_V4}/search_v3"
        params: dict[str, str | int] = {
            "q": keyword,
            "correction": 1,
            "offset": offset,
            "limit": limit,
            "filter_fields": "lc_idx",
            "lc_idx": 0,
            "show_all_topics": 0,
            "search_source": "Normal",
        }
        if t:
            params["t"] = t
        return self._get_no_xsrf(url, params=params)

    def get_top_search(self) -> dict:
        url = "https://www.zhihu.com/api/v4/search/top_search"
        return self._get_no_xsrf(url)

    def get_preset_words(self) -> dict:
        url = "https://www.zhihu.com/api/v4/search/preset_words"
        return self._get_no_xsrf(url)
