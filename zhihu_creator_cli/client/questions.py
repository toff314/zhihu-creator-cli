"""Question domain mixin for ZhihuClient."""

from __future__ import annotations

from typing import Any

from ..config import ZHIHU_API_V4
from ..exceptions import DataFetchError


class QuestionMixin:
    def get_recommended_questions(
        self,
        offset: int = 0,
        limit: int = 20,
        topic_id: str | None = None,
    ) -> dict:
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
        return self._get_no_xsrf(url, params=params)

    def get_question_detail(self, question_id: str) -> dict:
        result: dict[str, Any] = {}

        url = f"{ZHIHU_API_V4}/questions/{question_id}"
        params: dict[str, str] = {
            "include": (
                "answer_count,follower_count,"
                "visit_count,comment_count,created_time,"
                "updated_time,detail,topics"
            ),
        }
        try:
            resp_data = self._get_no_xsrf(url, params=params)
            if resp_data.get("detail"):
                return resp_data
            result = resp_data
        except Exception:
            pass

        try:
            answers = self.get_question_answers(question_id, limit=1)
            first = (answers.get("data") or [{}])[0]
            q = first.get("question", {})
            if q:
                result = q.copy()
        except Exception:
            pass

        if result.get("title") and not result.get("detail"):
            try:
                title = result.get("title", "")
                search_data = self._search_question_by_title(title, question_id)
                if search_data:
                    result["detail"] = search_data.get("description", "")
                    if not result.get("follower_count"):
                        result["follower_count"] = search_data.get("follower_count", 0)
                    if not result.get("answer_count"):
                        result["answer_count"] = search_data.get("answer_count", 0)
                    if not result.get("visits_count"):
                        result["visits_count"] = search_data.get("visits_count", 0)
            except Exception:
                pass

        if result.get("id") or result.get("title"):
            return result

        raise DataFetchError(
            f"Failed to get question {question_id} detail (tried multiple methods)"
        )

    def _search_question_by_title(self, title: str, question_id: str) -> dict | None:
        url = f"{ZHIHU_API_V4}/search_v3"
        params = {
            "t": "question",
            "q": title[:50],
            "limit": 20,
            "correction": 1,
            "filter_fields": "lc_idx",
            "lc_idx": 0,
            "show_all_topics": 0,
            "search_source": "Normal",
        }
        data = self._get_no_xsrf(url, params=params)
        for item in data.get("data", []):
            obj = item.get("object", {})
            if str(obj.get("id")) == str(question_id):
                return obj
        return None

    def get_question_answers(
        self,
        question_id: str,
        offset: int = 0,
        limit: int = 20,
        sort_by: str = "default",
    ) -> dict:
        url = f"{ZHIHU_API_V4}/questions/{question_id}/answers"
        params = {
            "include": (
                "data[*].content,voteup_count,comment_count,created_time,updated_time,author"
            ),
            "offset": offset,
            "limit": limit,
            "sort_by": sort_by,
        }
        return self._get(url, params=params)
