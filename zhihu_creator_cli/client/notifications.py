"""Notification domain mixin for ZhihuClient."""

from __future__ import annotations

from typing import Any

from ..config import ZHIHU_API_V4


class NotificationMixin:
    def get_invite_notifications(
        self,
        offset: int = 0,
        limit: int = 20,
        check_answered: bool = False,
    ) -> dict:
        url = "https://www.zhihu.com/api/v4/notifications/v2/recent"
        params: dict[str, Any] = {
            "offset": offset,
            "limit": limit,
            "entry_name": "all",
        }

        result = self._get(url, params=params)
        invites = []
        invite_verbs = {" 邀请你回答问题", " 的提问等你来答"}

        answered_ids: set[str] = set()
        if check_answered:
            me = self._get(f"{ZHIHU_API_V4}/me")
            my_url_token = me.get("url_token", "")
            if my_url_token:
                user_answers = self.get_user_answers(my_url_token, limit=100)
                answered_ids = {
                    str(a.get("question", {}).get("id", "")) for a in user_answers.get("data", [])
                }

        for item in result.get("data", []):
            content = item.get("content", {})
            verb = content.get("verb", "")
            if verb not in invite_verbs:
                continue

            target = item.get("target", {})
            if target.get("type") != "question":
                continue

            actors = content.get("actors", [])
            inviter = actors[0] if actors else {}

            invite_item = {
                "question": target,
                "inviter_name": inviter.get("name", ""),
                "inviter_url_token": inviter.get("url_token", ""),
                "verb": verb.strip(),
                "is_read": item.get("is_read", True),
                "merge_count": item.get("merge_count", 1),
                "invite_time": item.get("create_time", 0),
            }

            if check_answered:
                question_id = str(target.get("id", ""))
                invite_item["is_answered"] = question_id in answered_ids

            invites.append(invite_item)

        return {
            "data": invites,
            "paging": result.get("paging", {}),
        }

    def get_invite_notifications_only(
        self,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        url = "https://www.zhihu.com/api/v4/notifications/v2/recent"
        params = {
            "offset": offset,
            "limit": limit,
            "entry_name": "invite",
        }
        return self._get(url, params=params)

    def get_message_notifications(
        self,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:
        url = "https://www.zhihu.com/api/v4/notifications/v2/recent"
        params = {
            "offset": offset,
            "limit": limit,
            "entry_name": "message",
        }
        return self._get(url, params=params)
