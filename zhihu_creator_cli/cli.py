"""知乎创作助手 CLI — Agent-native, --json 输出."""

import logging

import click

from .commands.answers import answers_group
from .commands.articles import articles_group
from .commands.auth import auth_group
from .commands.collections import collections_group
from .commands.columns import columns_group
from .commands.creator import creator_group
from .commands.hot import hot_group
from .commands.notifications import notifications_group
from .commands.pins import pins_group
from .commands.questions import questions_group
from .commands.search import search_group
from .commands.topics import topics_group
from .commands.users import users_group


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable debug logging.")
@click.version_option(
    version=__import__("zhihu_creator_cli").__version__, prog_name="zhihu-creator"
)
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """知乎创作助手 CLI — 创作中心、问题推荐（只读）。

    专为内容创作者和 AI Agent 设计，支持 Cookie 登录，
    所有查询命令支持 ``--json`` 输出。
    """
    ctx.ensure_object(dict)
    if verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
    else:
        logging.basicConfig(level=logging.WARNING)


cli.add_command(auth_group)
cli.add_command(articles_group)
cli.add_command(questions_group)
cli.add_command(users_group)
cli.add_command(answers_group)
cli.add_command(hot_group)
cli.add_command(columns_group)
cli.add_command(search_group)
cli.add_command(creator_group)
cli.add_command(topics_group)
cli.add_command(collections_group)
cli.add_command(pins_group)
cli.add_command(notifications_group)


def main() -> None:
    """Entry point for the CLI."""
    cli()
