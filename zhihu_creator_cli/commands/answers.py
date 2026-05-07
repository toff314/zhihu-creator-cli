"""Answers commands: detail, comments, voters."""

import click

from ..display.answers import show_answer_comments, show_answer_detail, show_answer_voters
from ..display.common import show_error
from ..exceptions import DataFetchError
from . import _helpers as h


@click.group(name="answers")
def answers_group() -> None:
    """Answer detail."""
    pass


@answers_group.command(name="detail")
@h.json_option
@click.argument("answer_id")
def answer_detail(answer_id: str, json_mode: bool) -> None:
    """Get answer detail by ID.

    Example::

        zhihu-creator answers detail 29960616
    """
    with h._get_client() as client:
        try:
            data = client.get_answer_detail(answer_id)
            show_answer_detail(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@answers_group.command(name="comments")
@h.common_options
@click.argument("answer_id")
def answer_comments(answer_id: str, offset: int, limit: int, json_mode: bool) -> None:
    """Get comments on an answer (回答评论列表).

    Example::

        zhihu-creator answers comments 29960616 --limit 10
    """
    with h._get_client() as client:
        try:
            data = client.get_answer_comments(answer_id, offset, limit)
            show_answer_comments(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@answers_group.command(name="voters")
@h.common_options
@click.argument("answer_id")
def answer_voters(answer_id: str, offset: int, limit: int, json_mode: bool) -> None:
    """Get voters on an answer (回答投票者列表).

    Example::

        zhihu-creator answers voters 29960616 --limit 10
    """
    with h._get_client() as client:
        try:
            data = client.get_answer_voters(answer_id, offset, limit)
            show_answer_voters(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None
