"""Hot commands: list."""

import click

from ..display.common import show_error
from ..display.hot import show_hot_questions
from ..exceptions import DataFetchError
from . import _helpers as h


@click.group(name="hot")
def hot_group() -> None:
    """Hot questions list (热榜)."""
    pass


@hot_group.command(name="list")
@h.json_option
@click.option("--limit", default=50, help="Number of hot questions.")
def hot_list(limit: int, json_mode: bool) -> None:
    """Get hot questions list (知乎热榜).

    Example::

        zhihu-creator hot list --limit 20
    """
    with h._get_client() as client:
        try:
            data = client.get_hot_questions(limit)
            show_hot_questions(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None
