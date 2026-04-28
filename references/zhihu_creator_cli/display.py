"""Terminal display utilities: tables for humans, JSON for agents.

All output functions accept a ``json_mode`` flag. When True, raw dict/list
is printed as compact JSON for machine consumption.
"""

from __future__ import annotations

import json
from typing import Any

from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()


def _fmt_ts(raw: Any) -> str:
    """Format a timestamp (int/float) to human-readable string."""
    if isinstance(raw, (int, float)) and raw > 1000000000:
        return datetime.fromtimestamp(raw).strftime("%Y-%m-%d %H:%M")
    return str(raw)[:16]


def _json_out(data: Any) -> None:
    """Print compact JSON for --json mode."""
    console.print(json.dumps(data, ensure_ascii=False, indent=None))


def show_creator_articles(data: dict, json_mode: bool = False) -> None:
    """Display creator articles as a table or JSON."""
    if json_mode:
        _json_out(data)
        return

    articles = data.get("data", [])
    if not articles:
        console.print("[yellow]No articles found.[/yellow]")
        return

    table = Table(
        title="创作中心文章",
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("ID", style="dim", no_wrap=True, width=20)
    table.add_column("标题", min_width=30)
    table.add_column("状态", width=8)
    table.add_column("赞同", justify="right", width=6)
    table.add_column("评论", justify="right", width=6)
    table.add_column("阅读", justify="right", width=8)
    table.add_column("更新时间", width=16)

    for item in articles:
        article = item if isinstance(item, dict) else item.get("content", item)
        # API returns "state" (published/draft), not "publish_status"
        status = article.get("state", article.get("publish_status", "unknown"))
        status_style = {"published": "green", "draft": "yellow"}.get(status, "white")

        # Format Unix timestamp from "updated" field
        updated_raw = article.get("updated", article.get("updated_time", ""))
        updated_str = _fmt_ts(updated_raw) if updated_raw else ""

        # visit_count may not exist in this endpoint
        visit_count = article.get("visit_count")
        visit_str = str(visit_count) if visit_count is not None else "-"

        table.add_row(
            str(article.get("id", "-")),
            article.get("title", "Untitled")[:50],
            f"[{status_style}]{status}[/{status_style}]",
            str(article.get("voteup_count", "-")),
            str(article.get("comment_count", "-")),
            visit_str,
            updated_str,
        )

    console.print(table)
    paging = data.get("paging", {})
    total = paging.get("totals", "?")
    console.print(f"\nTotal: {total} articles")


def show_creator_stats(data: dict, json_mode: bool = False) -> None:
    """Display creator dashboard statistics."""
    if json_mode:
        _json_out(data)
        return

    table = Table(title="创作数据概览", show_header=False)
    table.add_column("Metric", style="bold")
    table.add_column("Value", justify="right")

    metrics = [
        ("总阅读量", data.get("total_read_count", "-")),
        ("总赞同数", data.get("total_upvote_count", "-")),
        ("总评论数", data.get("total_comment_count", "-")),
        ("总收藏数", data.get("total_fav_count", "-")),
        ("关注者", data.get("follower_count", "-")),
        ("新增关注", data.get("new_follower_count", "-")),
    ]
    for label, value in metrics:
        table.add_row(label, str(value))

    console.print(table)


def show_question_detail(question: dict, json_mode: bool = False) -> None:
    """Display question details — only fields with actual values."""
    if json_mode:
        _json_out(question)
        return

    table = Table(show_header=False)
    table.add_column("Field", style="bold cyan")
    table.add_column("Value")

    table.add_row("ID", str(question.get("id", "-")))
    table.add_row("标题", question.get("title", "-"))

    # Optional metrics: only show if present
    for field_key, label in [
        ("answer_count", "回答数"),
        ("follower_count", "关注者"),
        ("visit_count", "浏览量"),
        ("comment_count", "评论数"),
    ]:
        val = question.get(field_key)
        if val is not None:
            table.add_row(label, str(val))

    # Topics
    topics = question.get("topics", [])
    if topics:
        topic_names = ", ".join(t.get("name", "") for t in topics[:5])
        table.add_row("话题", topic_names)

    # Timestamps
    created_raw = question.get("created", question.get("created_time"))
    if created_raw:
        table.add_row("创建时间", _fmt_ts(created_raw))

    updated_raw = question.get("updated_time", question.get("updated"))
    if updated_raw:
        table.add_row("更新时间", _fmt_ts(updated_raw))

    # URL
    url = question.get("url")
    if url:
        table.add_row("链接", url)

    # Question type
    qtype = question.get("question_type")
    if qtype:
        table.add_row("类型", qtype)

    console.print(table)


def show_recommended_questions(data: dict, json_mode: bool = False) -> None:
    """Display recommended questions as table or JSON."""
    if json_mode:
        _json_out(data)
        return

    questions = data.get("data", [])
    if not questions:
        console.print("[yellow]No recommended questions found.[/yellow]")
        return

    table = Table(
        title="问题推荐",
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("ID", style="dim", no_wrap=True, width=20)
    table.add_column("标题", min_width=40)
    table.add_column("回答数", justify="right", width=8)
    table.add_column("关注者", justify="right", width=8)
    table.add_column("话题", min_width=20)

    for item in questions:
        q = item if isinstance(item, dict) else item.get("target", item)
        topics = q.get("topics", [])
        topic_str = ", ".join(t.get("name", "") for t in topics[:3])

        table.add_row(
            str(q.get("id", "-")),
            q.get("title", "Untitled")[:60],
            str(q.get("answer_count", "-")),
            str(q.get("follower_count", "-")),
            topic_str[:30],
        )

    console.print(table)
    paging = data.get("paging", {})
    total = paging.get("totals", len(questions))
    console.print(f"\nShowing {len(questions)} of {total} questions")


def show_invite_questions(data: dict, json_mode: bool = False) -> None:
    """Display invited questions as table or JSON."""
    if json_mode:
        _json_out(data)
        return

    invites = data.get("data", [])
    if not invites:
        console.print("[yellow]No invite notifications found.[/yellow]")
        return

    table = Table(
        title="邀请回答",
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("问题ID", style="dim", no_wrap=True, width=20)
    table.add_column("标题", min_width=40)
    table.add_column("邀请者", width=16)
    table.add_column("类型", width=12)
    table.add_column("状态", width=6)

    for item in invites:
        q = item.get("question", {})
        is_read = item.get("is_read", True)
        status = "[dim]已读[/dim]" if is_read else "[bold green]未读[/bold green]"

        table.add_row(
            str(q.get("id", "-")),
            q.get("title", "Untitled")[:60],
            item.get("inviter_name", "-"),
            item.get("verb", "-"),
            status,
        )

    console.print(table)
    console.print(f"\nTotal: {len(invites)} invites")


def show_search_results(data: dict, json_mode: bool = False) -> None:
    """Display question search results."""
    if json_mode:
        _json_out(data)
        return

    results = data.get("data", [])
    if not results:
        console.print("[yellow]No results found.[/yellow]")
        return

    table = Table(
        title="搜索结果",
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("ID", style="dim", no_wrap=True, width=20)
    table.add_column("标题", min_width=40)
    table.add_column("回答数", justify="right", width=8)
    table.add_column("关注者", justify="right", width=8)

    for item in results:
        # Search results nest under 'object' or 'target'
        obj = item
        for key in ("object", "target"):
            if key in item:
                obj = item[key]
                break

        table.add_row(
            str(obj.get("id", "-")),
            obj.get("title", "-")[:60],
            str(obj.get("answer_count", "-")),
            str(obj.get("follower_count", "-")),
        )

    console.print(table)


def show_me(me: dict, json_mode: bool = False) -> None:
    """Display current user profile."""
    if json_mode:
        _json_out(me)
        return

    name = me.get("name", "Unknown")
    headline = me.get("headline", "")
    console.print(f"\n[bold green]Logged in as:[/bold green] {name}")
    if headline:
        console.print(f"  Headline: {headline}")
    console.print(f"  ID: {me.get('id', '-')}")
    console.print(f"  URL Token: {me.get('url_token', '-')}")


def show_error(message: str) -> None:
    """Print error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def show_info(message: str) -> None:
    """Print informational message."""
    console.print(f"[blue]{message}[/blue]")
