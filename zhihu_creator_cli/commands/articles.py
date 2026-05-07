"""Articles commands: list, detail."""

import json as _json

import click
from rich.console import Console

from ..display.articles import show_creator_articles
from ..display.common import show_error
from ..exceptions import DataFetchError
from . import _helpers as h


@click.group(name="articles")
@h.require_login
def articles_group() -> None:
    """创作中心文章管理."""
    pass


@articles_group.command(name="list")
@h.common_options
@click.option(
    "--status",
    default="all",
    type=click.Choice(["all", "published", "draft"]),
    help="Filter by status.",
)
@click.option(
    "--sort",
    default="created",
    type=click.Choice(["created", "updated", "voteups"]),
    help="Sort order.",
)
def list_articles(offset: int, limit: int, status: str, sort: str, json_mode: bool) -> None:
    """List articles in creator center (创作中心文章列表).

    Example::

        zhihu-creator articles list --limit 10 --status published
    """
    with h._get_client() as client:
        try:
            data = client.get_creator_articles(offset=offset, limit=limit, status=status, sort=sort)
            show_creator_articles(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@articles_group.command(name="detail")
@h.json_option
@click.argument("article_id")
def article_detail(article_id: str, json_mode: bool) -> None:
    """Get article detail by ID (获取文章详情).

    Example::

        zhihu-creator articles detail 2032112310991499955
    """
    with h._get_client() as client:
        try:
            data = client.get_article_detail(article_id)
            if json_mode:
                click.echo(_json.dumps(data, ensure_ascii=False))
            else:
                console = Console()
                console.print(f"\n[bold]{data.get('title', 'No title')}[/bold]")
                console.print(f"Author: {data.get('author', {}).get('name', 'N/A')}")
                console.print(f"Status: {data.get('publish_status', '-')}")
                console.print(f"Voteups: {data.get('voteup_count', '-')}")
                console.print(f"Comments: {data.get('comment_count', '-')}")
                content = data.get("content", "")[:500]
                console.print(f"\nContent preview:\n{content}...")
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None
