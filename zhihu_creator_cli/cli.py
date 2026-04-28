"""Click CLI command definitions (read-only).

All data commands support ``--json`` for machine-readable output.
"""

import logging
from functools import wraps
from typing import Any

import click

from .auth import AuthManager
from .client import ZhihuClient
from .config import COOKIES_FILE
from .display import (
    show_creator_articles,
    show_error,
    show_info,
    show_invite_questions,
    show_me,
    show_question_detail,
    show_recommended_questions,
    show_search_results,
)
from .exceptions import DataFetchError, LoginError

logger = logging.getLogger(__name__)


# ---- Decorators ----

def require_login(f):
    """Decorator: ensure user is logged in before command runs."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = AuthManager()
        if not auth.is_logged_in():
            show_error("Not logged in. Run: zhihu-creator login --qrcode")
            raise click.Abort()
        return f(*args, **kwargs)

    return wrapper


def json_option(f):
    """Decorator: add ``--json`` flag to command."""
    return click.option(
        "--json",
        "json_mode",
        is_flag=True,
        default=False,
        help="Output raw JSON for agent consumption.",
    )(f)


def common_options(f):
    """Add --offset, --limit, --json options."""
    f = click.option("--offset", default=0, help="Pagination offset.")(f)
    f = click.option("--limit", default=20, help="Items per page.")(f)
    f = json_option(f)
    return f


# ---- Helper ----

def _get_client() -> ZhihuClient:
    """Create a ZhihuClient from stored cookies."""
    auth = AuthManager()
    return ZhihuClient(auth.cookies)


# ---- CLI root ----

@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable debug logging.")
@click.version_option(version=__import__("zhihu_creator_cli").__version__, prog_name="zhihu-creator")
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """知乎创作助手 CLI — 创作中心、问题推荐（只读）。

    专为内容创作者和 AI Agent 设计，支持二维码/Cookie 登录，
    所有查询命令支持 ``--json`` 输出。
    """
    ctx.ensure_object(dict)
    if verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
    else:
        logging.basicConfig(level=logging.WARNING)


# ============================================================
#  Auth commands
# ============================================================

@cli.group(name="auth")
def auth_group() -> None:
    """Authentication commands."""
    pass


@auth_group.command(name="login")
@click.option("--cookie", "cookie_str", required=True, help="Login with cookie string.")
def login(cookie_str: str) -> None:
    """Login to Zhihu with Cookie string.

    Copy cookies from browser dev tools and paste them here.

    Example::

        zhihu-creator auth login --cookie "z_c0=xxx; _xsrf=yyy; d_c0=zzz"
    """
    auth = AuthManager()
    try:
        auth.login_with_cookie_string(cookie_str)
        click.echo("✓ Cookie login successful!")
    except LoginError as e:
        show_error(str(e))
        raise click.Abort()

    with _get_client() as client:
        me = client._get("https://www.zhihu.com/api/v4/me")
        show_me(me)


@auth_group.command(name="logout")
def logout() -> None:
    """Logout and clear stored cookies."""
    AuthManager().clear_cookies()
    click.echo("✓ Logged out and local cookies cleared.")


@auth_group.command(name="status")
@json_option
def status(json_mode: bool) -> None:
    """Check login status."""
    auth = AuthManager()
    if not auth.is_logged_in():
        show_info("Not logged in.")
        return

    with _get_client() as client:
        try:
            me = client._get("https://www.zhihu.com/api/v4/me")
            show_me(me, json_mode)
        except LoginError:
            show_info("Cookie exists but session expired. Please login again.")


@auth_group.command(name="whoami")
@json_option
def whoami(json_mode: bool) -> None:
    """Show current user profile."""
    with _get_client() as client:
        try:
            me = client._get("https://www.zhihu.com/api/v4/me")
            show_me(me, json_mode)
        except LoginError as e:
            show_error(str(e))
            raise click.Abort()


# ============================================================
#  Articles commands
# ============================================================

@cli.group(name="articles")
@require_login
def articles_group() -> None:
    """创作中心文章管理."""
    pass


@articles_group.command(name="list")
@common_options
@click.option("--status", default="all", type=click.Choice(["all", "published", "draft"]), help="Filter by status.")
@click.option("--sort", default="created", type=click.Choice(["created", "updated", "voteups"]), help="Sort order.")
def list_articles(offset: int, limit: int, status: str, sort: str, json_mode: bool) -> None:
    """List articles in creator center (创作中心文章列表).

    Example::

        zhihu-creator articles list --limit 10 --status published
    """
    with _get_client() as client:
        try:
            data = client.get_creator_articles(
                offset=offset, limit=limit, status=status, sort=sort
            )
            show_creator_articles(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort()


@articles_group.command(name="detail")
@json_option
@click.argument("article_id")
def article_detail(article_id: str, json_mode: bool) -> None:
    """Get article detail by ID (获取文章详情).

    Example::

        zhihu-creator articles detail 2032112310991499955
    """
    with _get_client() as client:
        try:
            data = client.get_article_detail(article_id)
            if json_mode:
                import json as _json
                show_info(_json.dumps(data, ensure_ascii=False, indent=2))
            else:
                from rich.console import Console
                console = Console()
                console.print(f"\n[bold]{data.get('title', 'No title')}[/bold]")
                console.print(f"Author: {data.get('author', {}).get('name', 'N/A')}")
                console.print(f"Status: {data.get('publish_status', '-')}")
                console.print(f"Voteups: {data.get('voteup_count', '-')}")
                console.print(f"Comments: {data.get('comment_count', '-')}")
                content = data.get('content', '')[:500]
                console.print(f"\nContent preview:\n{content}...")
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort()


# ============================================================
#  Questions commands
# ============================================================

@cli.group(name="questions")
@require_login
def questions_group() -> None:
    """Question discovery and search."""
    pass


@questions_group.command(name="recommend")
@common_options
@click.option("--topic", "topic_id", help="Filter by topic ID.")
def recommend_questions(offset: int, limit: int, topic_id: str | None, json_mode: bool) -> None:
    """Get recommended questions for you (问题推荐).

    Example::

        zhihu-creator questions recommend --limit 10
        zhihu-creator questions recommend --topic 19550517
    """
    with _get_client() as client:
        try:
            data = client.get_recommended_questions(
                offset=offset, limit=limit, topic_id=topic_id
            )
            show_recommended_questions(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort()


@questions_group.command(name="invites")
@common_options
def invite_questions(offset: int, limit: int, json_mode: bool) -> None:
    """Get questions invited to you (邀请回答列表).

    Fetches notifications of type ``邀请你回答问题`` and
    ``的提问等你来答`` from the Zhihu notification center.

    Example::

        zhihu-creator questions invites --limit 10
    """
    with _get_client() as client:
        try:
            data = client.get_invite_notifications(offset=offset, limit=limit)
            show_invite_questions(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort()


@questions_group.command(name="search")
@common_options
@click.argument("keyword")
def search_questions(keyword: str, offset: int, limit: int, json_mode: bool) -> None:
    """Search for questions by keyword.

    Example::

        zhihu-creator questions search "Python 学习" --limit 20
    """
    with _get_client() as client:
        try:
            data = client.search_questions(keyword, offset=offset, limit=limit)
            show_search_results(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort()


@questions_group.command(name="detail")
@json_option
@click.argument("question_id")
def question_detail(question_id: str, json_mode: bool) -> None:
    """Show question details (问题详情).

    Example::

        zhihu-creator questions detail 302196756
    """
    with _get_client() as client:
        try:
            data = client.get_question_detail(question_id)
            show_question_detail(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort()


@questions_group.command(name="answers")
@common_options
@click.argument("question_id")
@click.option("--sort", "sort_by", default="default", type=click.Choice(["default", "updated"]))
def question_answers(question_id: str, offset: int, limit: int, sort_by: str, json_mode: bool) -> None:
    """List answers for a question (问题回答列表).

    Example::

        zhihu-creator questions answers 656013053 --limit 5
    """
    with _get_client() as client:
        try:
            data = client.get_question_answers(question_id, offset, limit, sort_by)
            if json_mode:
                import json as _json
                show_info(_json.dumps(data, ensure_ascii=False, indent=2))
            else:
                from rich.console import Console
                answers = data.get("data") or []
                console = Console()
                console.print(f"\n[bold]Question {question_id} — {len(answers)} answers[/bold]\n")
                for i, ans in enumerate(answers[:5]):
                    author = ans.get("author", {})
                    console.print(f"{i+1}. [bold]{author.get('name', 'Anonymous')}[/bold] | "
                                  f"Voteups: {ans.get('voteup_count', 0)} | "
                                  f"Comments: {ans.get('comment_count', 0)}")
                    content = ans.get("content", "")[:300]
                    console.print(f"   {content}\n")
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort()


# ============================================================
#  Entry point
# ============================================================

def main() -> None:
    """Entry point for the CLI."""
    cli()
