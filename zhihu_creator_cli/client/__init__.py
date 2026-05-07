"""Zhihu API client (read-only).

Re-exports ``ZhihuClient`` so ``from zhihu_creator_cli.client import ZhihuClient``
still works after the module-to-package refactor.
"""

from .answers import AnswerMixin
from .articles import ArticleMixin
from .base import ZhihuClientBase
from .collections import CollectionMixin
from .columns import ColumnMixin
from .creator import CreatorMixin
from .hot import HotMixin
from .notifications import NotificationMixin
from .pins import PinMixin
from .questions import QuestionMixin
from .search import SearchMixin
from .topics import TopicMixin
from .users import UserMixin


class ZhihuClient(
    ArticleMixin,
    QuestionMixin,
    UserMixin,
    AnswerMixin,
    HotMixin,
    ColumnMixin,
    SearchMixin,
    CreatorMixin,
    TopicMixin,
    CollectionMixin,
    PinMixin,
    NotificationMixin,
    ZhihuClientBase,
):
    pass


__all__ = ["ZhihuClient"]
