"""Columns commands: list, recommend, search, detail, articles."""

import click

from ..display.columns import (
    show_column_articles,
    show_column_detail,
    show_recommended_columns,
    show_search_columns,
    show_user_columns,
)
from ..display.common import show_error
from ..exceptions import DataFetchError
from . import _helpers as h


@click.group(name="columns")
def columns_group() -> None:
    """Column (专栏) discovery and detail."""
    pass


@columns_group.command(name="list")
@h.require_login
@h.common_options
def list_columns(offset: int, limit: int, json_mode: bool) -> None:
    """List your columns (我的专栏列表).

    Uses search API and filters by author.

    Example::

        zhihu-creator columns list --limit 10
    """
    with h._get_client() as client:
        try:
            data = client.get_user_columns()
            show_user_columns(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@columns_group.command(name="recommend")
@h.common_options
@click.option(
    "--classify",
    default=1,
    type=click.INT,
    help="Category ID (1=推荐, 2=生活方式, 4=影视, 5=心理, 7=互联网, etc.)",
)
def recommend_columns(offset: int, limit: int, classify: int, json_mode: bool) -> None:
    """Get recommended columns by category (专栏推荐).

    Classify categories:
    1=新鲜推荐, 2=生活方式, 4=影视娱乐, 5=心理学,
    7=互联网, 8=文学, 9=商业, 12=音乐, 13=科学, 16=金融

    Example::

        zhihu-creator columns recommend --classify 7 --limit 10
    """
    with h._get_client() as client:
        try:
            data = client.get_recommended_columns(classify, offset, limit)
            show_recommended_columns(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@columns_group.command(name="search")
@h.common_options
@click.argument("keyword")
def search_columns(keyword: str, offset: int, limit: int, json_mode: bool) -> None:
    """Search for columns by keyword (搜索专栏).

    Example::

        zhihu-creator columns search toff314
        zhihu-creator columns search Python --limit 10
    """
    with h._get_client() as client:
        try:
            data = client.search("column", keyword, offset=offset, limit=limit)
            show_search_columns(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@columns_group.command(name="detail")
@h.json_option
@click.argument("slug_or_id")
def column_detail(slug_or_id: str, json_mode: bool) -> None:
    """Get column detail (获取专栏详情).

    SLUG_OR_ID can be either:
    - slug: the string after https://zhuanlan.zhihu.com/ (e.g., 'pythoneer')
    - id: column ID from API (e.g., 'c_2032794954242769616')

    Example::

        zhihu-creator columns detail pythoneer
        zhihu-creator columns detail c_2032794954242769616
    """
    with h._get_client() as client:
        try:
            data = client.get_column_detail(slug_or_id)
            show_column_detail(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@columns_group.command(name="articles")
@h.common_options
@click.argument("slug_or_id")
def column_articles(slug_or_id: str, offset: int, limit: int, json_mode: bool) -> None:
    """Get articles in a column (获取专栏文章列表).

    SLUG_OR_ID can be either slug (e.g., 'pythoneer') or ID (e.g., 'c_xxx').

    Example::

        zhihu-creator columns articles pythoneer --limit 10
        zhihu-creator columns articles c_2032794954242769616
    """
    with h._get_client() as client:
        try:
            data = client.get_column_articles(slug_or_id, offset, limit)
            show_column_articles(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None
