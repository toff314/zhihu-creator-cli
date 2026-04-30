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
    show_answer_detail,
    show_creator_articles,
    show_error,
    show_hot_questions,
    show_info,
    show_invite_questions,
    show_me,
    show_question_detail,
    show_recommended_questions,
    show_search_results,
    show_user_answers,
    show_user_articles,
    show_user_collections,
    show_user_followees,
    show_user_followers,
    show_user_profile,
    show_user_questions,
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
@click.version_option(
    version=__import__("zhihu_creator_cli").__version__, prog_name="zhihu-creator"
)
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
    with _get_client() as client:
        try:
            data = client.get_creator_articles(offset=offset, limit=limit, status=status, sort=sort)
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
                content = data.get("content", "")[:500]
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
            data = client.get_recommended_questions(offset=offset, limit=limit, topic_id=topic_id)
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
def question_answers(
    question_id: str, offset: int, limit: int, sort_by: str, json_mode: bool
) -> None:
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
                    console.print(
                        f"{i + 1}. [bold]{author.get('name', 'Anonymous')}[/bold] | "
                        f"Voteups: {ans.get('voteup_count', 0)} | "
                        f"Comments: {ans.get('comment_count', 0)}"
                    )
                    content = ans.get("content", "")[:300]
                    console.print(f"   {content}\n")
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort()


# ============================================================
#  4. Users commands
# ============================================================


@cli.group(name="users")
def users_group() -> None:
    """User profile and content."""
    pass


@users_group.command(name="profile")
@json_option
@click.argument("url_token")
def user_profile(url_token: str, json_mode: bool) -> None:
    """Get user profile by url_token.

    Example::

        zhihu-creator users profile toff314
    """
    with _get_client() as client:
        try:
            data = client.get_user_profile(url_token)
            show_user_profile(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort()


@users_group.command(name="articles")
@common_options
@click.option(
    "--sort", "sort_by", default="created", type=click.Choice(["created", "updated", "voteups"])
)
@click.argument("url_token")
def user_articles(url_token: str, offset: int, limit: int, sort_by: str, json_mode: bool) -> None:
    """Get articles by a user.

    Example::

        zhihu-creator users articles toff314 --limit 10
    """
    with _get_client() as client:
        try:
            data = client.get_user_articles(url_token, offset, limit, sort_by)
            show_user_articles(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort()


@users_group.command(name="answers")
@common_options
@click.option(
    "--sort", "sort_by", default="created", type=click.Choice(["created", "updated", "voteups"])
)
@click.option("--collapsed", is_flag=True, help="Filter collapsed answers only.")
@click.argument("url_token")
def user_answers(
    url_token: str, offset: int, limit: int, sort_by: str, collapsed: bool, json_mode: bool
) -> None:
    """Get answers by a user.

    Example::

        zhihu-creator users answers toff314 --limit 10
        zhihu-creator users answers toff314 --collapsed  # Only collapsed
    """
    with _get_client() as client:
        try:
            data = client.get_user_answers(url_token, offset, limit, sort_by)
            if collapsed and not json_mode:
                answers = data.get("data", [])
                filtered = [a for a in answers if a.get("is_collapsed", False)]
                data["data"] = filtered
                data["paging"]["totals"] = len(filtered)
            show_user_answers(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort()


@users_group.command(name="questions")
@common_options
@click.argument("url_token")
def user_questions(url_token: str, offset: int, limit: int, json_mode: bool) -> None:
    """Get questions asked by a user.

    Example::

        zhihu-creator users questions toff314 --limit 10
    """
    with _get_client() as client:
        try:
            data = client.get_user_questions(url_token, offset, limit)
            show_user_questions(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort()


@users_group.command(name="followers")
@common_options
@click.argument("url_token")
def user_followers(url_token: str, offset: int, limit: int, json_mode: bool) -> None:
    """Get user's followers (粉丝列表).

    Example::

        zhihu-creator users followers toff314 --limit 20
    """
    with _get_client() as client:
        try:
            data = client.get_user_followers(url_token, offset, limit)
            show_user_followers(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort()


@users_group.command(name="followees")
@common_options
@click.argument("url_token")
def user_followees(url_token: str, offset: int, limit: int, json_mode: bool) -> None:
    """Get users that a user follows (关注列表).

    Example::

        zhihu-creator users followees toff314 --limit 20
    """
    with _get_client() as client:
        try:
            data = client.get_user_followees(url_token, offset, limit)
            show_user_followees(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort()


@users_group.command(name="collections")
@common_options
@click.argument("user_id")
def user_collections(user_id: str, offset: int, limit: int, json_mode: bool) -> None:
    """Get user's collections (收藏夹列表).

    Note: Uses user_id (numeric), not url_token.

    Example::

        zhihu-creator users collections 19ff584816895caaa1d68fbf187a29fd --limit 10
    """
    with _get_client() as client:
        try:
            data = client.get_user_collections(user_id, offset, limit)
            show_user_collections(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort()


# ============================================================
#  5. Answers commands
# ============================================================


@cli.group(name="answers")
def answers_group() -> None:
    """Answer detail."""
    pass


@answers_group.command(name="detail")
@json_option
@click.argument("answer_id")
def answer_detail(answer_id: str, json_mode: bool) -> None:
    """Get answer detail by ID.

    Example::

        zhihu-creator answers detail 29960616
    """
    with _get_client() as client:
        try:
            data = client.get_answer_detail(answer_id)
            show_answer_detail(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort()


# ============================================================
#  6. Hot commands
# ============================================================


@cli.group(name="hot")
def hot_group() -> None:
    """Hot questions list (热榜)."""
    pass


@hot_group.command(name="list")
@json_option
@click.option("--limit", default=50, help="Number of hot questions.")
def hot_list(limit: int, json_mode: bool) -> None:
    """Get hot questions list (知乎热榜).

    Example::

        zhihu-creator hot list --limit 20
    """
    with _get_client() as client:
        try:
            data = client.get_hot_questions(limit)
            show_hot_questions(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort()


# ============================================================
#  Entry point
# ============================================================


def main() -> None:
    """Entry point for the CLI."""
    cli()
