"""Creator commands: home, stats."""

import click

from ..display.common import show_error
from ..display.creator import show_creator_home, show_creator_stats_detail
from ..exceptions import DataFetchError
from . import _helpers as h


@click.group(name="creator")
@h.require_login
def creator_group() -> None:
    """Creator center (创作中心)."""
    pass


@creator_group.command(name="home")
@h.json_option
def creator_home(json_mode: bool) -> None:
    """Get creator center home overview (创作中心首页).

    Example::

        zhihu-creator creator home
        zhihu-creator creator home --json
    """
    with h._get_client() as client:
        try:
            data = client.get_creator_home()
            show_creator_home(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@creator_group.command(name="stats")
@h.json_option
def creator_stats(json_mode: bool) -> None:
    """Get creator center stats (创作中心数据统计).

    Example::

        zhihu-creator creator stats
        zhihu-creator creator stats --json
    """
    with h._get_client() as client:
        try:
            data = client.get_creator_stats()
            show_creator_stats_detail(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None
