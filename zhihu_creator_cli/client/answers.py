"""Answer domain mixin for ZhihuClient."""

from ..config import ZHIHU_API_V4


class AnswerMixin:
    def get_answer_detail(self, answer_id: str) -> dict:
        url = f"{ZHIHU_API_V4}/answers/{answer_id}"
        params = {
            "include": (
                "content,voteup_count,comment_count,created_time,updated_time,author,question.title"
            ),
        }
        return self._get(url, params=params)

    def get_answer_comments(
        self,
        answer_id: str,
        offset: int = 0,
        limit: int = 20,
        sort_by: str = "created",
    ) -> dict:
        url = f"{ZHIHU_API_V4}/answers/{answer_id}/comments"
        params = {
            "offset": offset,
            "limit": limit,
            "sort_by": sort_by,
        }
        return self._get(url, params=params)

    def get_answer_voters(
        self,
        answer_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        url = f"{ZHIHU_API_V4}/answers/{answer_id}/voters"
        params = {
            "offset": offset,
            "limit": limit,
        }
        return self._get(url, params=params)
