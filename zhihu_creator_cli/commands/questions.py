"""Questions commands: recommend, invites, search, detail, answers."""

import json as _json

import click
from rich.console import Console

from ..display.common import show_error
from ..display.questions import (
    show_invite_questions,
    show_question_detail,
    show_recommended_questions,
    show_search_results,
)
from ..exceptions import DataFetchError
from . import _helpers as h


@click.group(name="questions")
@h.require_login
def questions_group() -> None:
    """Question discovery and search."""
    pass


@questions_group.command(name="recommend")
@h.common_options
@click.option("--topic", "topic_id", help="Filter by topic ID.")
def recommend_questions(offset: int, limit: int, topic_id: str | None, json_mode: bool) -> None:
    """Get recommended questions for you (问题推荐).

    Example::

        zhihu-creator questions recommend --limit 10
        zhihu-creator questions recommend --topic 19550517
    """
    with h._get_client() as client:
        try:
            data = client.get_recommended_questions(offset=offset, limit=limit, topic_id=topic_id)
            show_recommended_questions(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@questions_group.command(name="invites")
@h.common_options
@click.option(
    "--answered",
    "answered_filter",
    default="all",
    type=click.Choice(["all", "yes", "no"]),
    help="Filter by answered status: all, yes (已回答), no (未回答).",
)
def invite_questions(offset: int, limit: int, answered_filter: str, json_mode: bool) -> None:
    """Get questions invited to you (邀请回答列表).

    Fetches notifications of type ``邀请你回答问题`` and
    ``的提问等你来答`` from the Zhihu notification center.

    Example::

        zhihu-creator questions invites --limit 10
        zhihu-creator questions invites --answered no  # Only unanswered
        zhihu-creator questions invites --answered yes  # Only answered
    """
    with h._get_client() as client:
        try:
            check_answered = answered_filter != "all"
            data = client.get_invite_notifications(
                offset=offset, limit=limit, check_answered=check_answered
            )
            if answered_filter != "all":
                invites = data.get("data", [])
                if answered_filter == "yes":
                    filtered = [i for i in invites if i.get("is_answered", False)]
                else:
                    filtered = [i for i in invites if not i.get("is_answered", False)]
                data["data"] = filtered
                data["paging"]["totals"] = len(filtered)
            show_invite_questions(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@questions_group.command(name="search")
@h.common_options
@click.argument("keyword")
def search_questions(keyword: str, offset: int, limit: int, json_mode: bool) -> None:
    """Search for questions by keyword.

    Example::

        zhihu-creator questions search "Python 学习" --limit 20
    """
    with h._get_client() as client:
        try:
            data = client.search("question", keyword, offset=offset, limit=limit)
            show_search_results(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@questions_group.command(name="detail")
@h.json_option
@click.argument("question_id")
def question_detail(question_id: str, json_mode: bool) -> None:
    """Show question details (问题详情).

    Example::

        zhihu-creator questions detail 302196756
    """
    with h._get_client() as client:
        try:
            data = client.get_question_detail(question_id)
            show_question_detail(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@questions_group.command(name="answers")
@h.common_options
@click.argument("question_id")
@click.option("--sort", "sort_by", default="default", type=click.Choice(["default", "updated"]))
def question_answers(
    question_id: str, offset: int, limit: int, sort_by: str, json_mode: bool
) -> None:
    """List answers for a question (问题回答列表).

    Example::

        zhihu-creator questions answers 656013053 --limit 5
    """
    with h._get_client() as client:
        try:
            data = client.get_question_answers(question_id, offset, limit, sort_by)
            if json_mode:
                click.echo(_json.dumps(data, ensure_ascii=False))
            else:
                answers = data.get("data") or []
                console = Console()
                console.print(f"\n[bold]Question {question_id} — {len(answers)} answers[/bold]\n")
                for i, ans in enumerate(answers[:5]):
                    author = ans.get("author", {})
                    console.print(
                        f"{i + 1}. [dim]{ans.get('id', '-')}[/dim] | "
                        f"[bold]{author.get('name', 'Anonymous')}[/bold] | "
                        f"Voteups: {ans.get('voteup_count', 0)} | "
                        f"Comments: {ans.get('comment_count', 0)}"
                    )
                    content = ans.get("content", "")[:300]
                    console.print(f"   {content}\n")
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None
