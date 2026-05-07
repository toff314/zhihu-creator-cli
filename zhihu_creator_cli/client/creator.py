"""Creator center domain mixin for ZhihuClient."""

from ..config import ZHIHU_CREATOR_HOME_API


class CreatorMixin:
    def get_creator_home(self) -> dict:
        url = f"{ZHIHU_CREATOR_HOME_API}/home"
        return self._get(url)

    def get_creator_stats(self) -> dict:
        url = f"{ZHIHU_CREATOR_HOME_API}/stats/overview"
        return self._get(url)
