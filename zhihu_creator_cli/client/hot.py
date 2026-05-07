"""Hot questions domain mixin for ZhihuClient."""


class HotMixin:
    def get_hot_questions(self, limit: int = 50) -> dict:
        url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
        params = {
            "limit": limit,
        }
        return self._get_no_xsrf(url, params=params)
