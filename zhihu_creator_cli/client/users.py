"""User domain mixin for ZhihuClient."""

from __future__ import annotations

from ..config import ZHIHU_API_V4


class UserMixin:
    def get_user_profile(self, url_token: str) -> dict:
        url = f"{ZHIHU_API_V4}/members/{url_token}"
        return self._get(url)

    def get_user_articles(
        self,
        url_token: str,
        offset: int = 0,
        limit: int = 20,
        sort_by: str = "created",
    ) -> dict:
        url = f"{ZHIHU_API_V4}/members/{url_token}/articles"
        params = {
            "include": "data[*].title,excerpt,created_time,updated_time,voteup_count,comment_count",
            "offset": offset,
            "limit": limit,
            "sort_by": sort_by,
        }
        return self._get(url, params=params)

    def get_user_answers(
        self,
        url_token: str,
        offset: int = 0,
        limit: int = 20,
        sort_by: str = "created",
    ) -> dict:
        url = f"{ZHIHU_API_V4}/members/{url_token}/answers"
        params = {
            "include": "data[*].content,voteup_count,comment_count,created_time,question.title",
            "offset": offset,
            "limit": limit,
            "sort_by": sort_by,
        }
        return self._get(url, params=params)

    def get_user_questions(
        self,
        url_token: str,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        url = f"{ZHIHU_API_V4}/members/{url_token}/questions"
        params = {
            "include": "data[*].title,answer_count,follower_count,created_time",
            "offset": offset,
            "limit": limit,
        }
        return self._get(url, params=params)

    def get_user_followers(
        self,
        url_token: str,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        url = f"{ZHIHU_API_V4}/members/{url_token}/followers"
        params = {
            "include": "data[*].answer_count,articles_count,follower_count,name,headline",
            "offset": offset,
            "limit": limit,
        }
        return self._get(url, params=params)

    def get_user_followees(
        self,
        url_token: str,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        url = f"{ZHIHU_API_V4}/members/{url_token}/followees"
        params = {
            "include": "data[*].answer_count,articles_count,follower_count,name,headline",
            "offset": offset,
            "limit": limit,
        }
        return self._get_no_xsrf(url, params=params)

    def get_user_collections(
        self,
        user_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        url = f"{ZHIHU_API_V4}/people/{user_id}/collections"
        params = {
            "offset": offset,
            "limit": limit,
        }
        return self._get(url, params=params)

    def get_user_pins(
        self,
        url_token: str,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        url = f"{ZHIHU_API_V4}/members/{url_token}/pins"
        params = {
            "offset": offset,
            "limit": limit,
        }
        return self._get(url, params=params)

    def get_user_zvideos(
        self,
        url_token: str,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        url = f"{ZHIHU_API_V4}/members/{url_token}/zvideos"
        params = {
            "offset": offset,
            "limit": limit,
        }
        return self._get(url, params=params)

    def get_user_columns_direct(
        self,
        url_token: str,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        url = f"{ZHIHU_API_V4}/members/{url_token}/column-contributions"
        params = {
            "offset": offset,
            "limit": limit,
        }
        return self._get(url, params=params)

    def get_user_following_topics(
        self,
        url_token: str,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        url = f"{ZHIHU_API_V4}/members/{url_token}/following-topic-contributions"
        params = {
            "offset": offset,
            "limit": limit,
        }
        return self._get_no_xsrf(url, params=params)

    def get_user_following_questions(
        self,
        url_token: str,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        url = f"{ZHIHU_API_V4}/members/{url_token}/following-questions"
        params = {
            "offset": offset,
            "limit": limit,
        }
        return self._get(url, params=params)

    def get_user_following_columns(
        self,
        url_token: str,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        url = f"{ZHIHU_API_V4}/members/{url_token}/following-columns"
        params = {
            "offset": offset,
            "limit": limit,
        }
        return self._get(url, params=params)

    def get_user_mutuals(
        self,
        url_token: str,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        url = f"{ZHIHU_API_V4}/members/{url_token}/relations/mutuals"
        params = {
            "include": "data[*].answer_count,articles_count,follower_count,name,headline",
            "offset": offset,
            "limit": limit,
        }
        return self._get(url, params=params)

    def get_user_activities(
        self,
        url_token: str,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        url = f"{ZHIHU_API_V4}/members/{url_token}/activities"
        params = {
            "offset": offset,
            "limit": limit,
        }
        return self._get_no_xsrf(url, params=params)
