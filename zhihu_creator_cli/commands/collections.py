"""Collections commands: detail, contents."""

import click

from ..display.collections import show_collection_contents, show_collection_detail
from ..display.common import show_error
from ..exceptions import DataFetchError
from . import _helpers as h


@click.group(name="collections")
def collections_group() -> None:
    """Collection (收藏夹) detail."""
    pass


@collections_group.command(name="detail")
@h.json_option
@click.argument("collection_id")
def collection_detail(collection_id: str, json_mode: bool) -> None:
    """Get collection detail (收藏夹详情).

    Example::

        zhihu-creator collections detail 123456789
    """
    with h._get_client() as client:
        try:
            data = client.get_collection_detail(collection_id)
            show_collection_detail(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@collections_group.command(name="contents")
@h.common_options
@click.argument("collection_id")
def collection_contents(collection_id: str, offset: int, limit: int, json_mode: bool) -> None:
    """Get collection contents (收藏夹内容列表).

    Example::

        zhihu-creator collections contents 123456789 --limit 10
    """
    with h._get_client() as client:
        try:
            data = client.get_collection_contents(collection_id, offset=offset, limit=limit)
            show_collection_contents(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None
