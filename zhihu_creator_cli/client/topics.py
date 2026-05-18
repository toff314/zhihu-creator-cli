"""Topic domain mixin for ZhihuClient."""


class TopicMixin:
    def get_topic_detail(self, topic_id: str) -> dict:
        url = f"https://api.zhihu.com/topics/{topic_id}/basic"
        return self._get_no_xsrf(url)

    def get_topic_unanswered(
        self,
        topic_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        url = f"https://api.zhihu.com/topics/{topic_id}/unanswered_questions"
        params = {
            "offset": offset,
            "limit": limit,
        }
        return self._get_no_xsrf(url, params=params)

    def get_topic_essence(
        self,
        topic_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        url = f"https://api.zhihu.com/topics/{topic_id}/best_answers"
        params = {
            "offset": offset,
            "limit": limit,
        }
        return self._get_no_xsrf(url, params=params)
