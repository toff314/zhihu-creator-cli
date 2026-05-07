"""Topics commands: detail, unanswered."""

import click

from ..display.common import show_error
from ..display.topics import show_topic_detail, show_topic_unanswered
from ..exceptions import DataFetchError
from . import _helpers as h


@click.group(name="topics")
def topics_group() -> None:
    """Topic discovery and detail."""
    pass


@topics_group.command(name="detail")
@h.json_option
@click.argument("topic_id")
def topic_detail(topic_id: str, json_mode: bool) -> None:
    """Get topic detail (话题详情).

    Example::

        zhihu-creator topics detail 19550517
    """
    with h._get_client() as client:
        try:
            data = client.get_topic_detail(topic_id)
            show_topic_detail(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@topics_group.command(name="unanswered")
@h.common_options
@click.argument("topic_id")
def topic_unanswered(topic_id: str, offset: int, limit: int, json_mode: bool) -> None:
    """Get unanswered questions in a topic (话题下未回答问题).

    Example::

        zhihu-creator topics unanswered 19550517 --limit 10
    """
    with h._get_client() as client:
        try:
            data = client.get_topic_unanswered(topic_id, offset=offset, limit=limit)
            show_topic_unanswered(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None
