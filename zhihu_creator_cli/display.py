"""Terminal display utilities: tables for humans, JSON for agents.

All output functions accept a ``json_mode`` flag. When True, raw dict/list
is printed as compact JSON for machine consumption.
"""

from __future__ import annotations

import json
import re
from typing import Any

from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()


def _fmt_ts(raw: Any) -> str:
    """Format a timestamp (int/float) to human-readable string."""
    if isinstance(raw, (int, float)) and raw > 1000000000:
        return datetime.fromtimestamp(raw).strftime("%m-%d %H:%M")
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
    table.add_column("ID", style="dim", width=18)
    table.add_column("标题", width=25)
    table.add_column("赞", justify="right", width=4)
    table.add_column("评", justify="right", width=4)
    table.add_column("藏", justify="right", width=4)
    table.add_column("时间", width=12)

    for item in articles:
        article = item if isinstance(item, dict) else item.get("content", item)

        updated_raw = article.get("updated", article.get("updated_time", ""))
        updated_str = _fmt_ts(updated_raw) if updated_raw else ""

        reaction = article.get("reaction", {})
        stats = reaction.get("statistics", {})
        fav_count = stats.get("favorites", 0)

        table.add_row(
            str(article.get("id", "-"))[:18],
            article.get("title", "Untitled")[:25],
            str(article.get("voteup_count", 0)),
            str(article.get("comment_count", 0)),
            str(fav_count),
            updated_str[:12],
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

    detail = question.get("detail", "")
    if detail:
        clean_detail = re.sub(r"<[^>]+>", "", detail).strip()
        if len(clean_detail) > 200:
            clean_detail = clean_detail[:200] + "..."
        table.add_row("内容", clean_detail)

    for field_key, label in [
        ("answer_count", "回答数"),
        ("follower_count", "关注者"),
        ("visits_count", "浏览量"),
        ("visit_count", "浏览量"),
        ("comment_count", "评论数"),
    ]:
        val = question.get(field_key)
        if val is not None:
            table.add_row(label, str(val))

    topics = question.get("topics", [])
    if topics:
        topic_names = ", ".join(t.get("name", "") for t in topics[:5])
        table.add_row("话题", topic_names)

    created_raw = question.get("created", question.get("created_time"))
    if created_raw:
        table.add_row("创建时间", _fmt_ts(created_raw))

    updated_raw = question.get("updated_time", question.get("updated"))
    if updated_raw:
        table.add_row("更新时间", _fmt_ts(updated_raw))

    url = question.get("url")
    if url:
        table.add_row("链接", url)

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


# ============================================================
#  4. User Profile
# ============================================================


def show_user_profile(user: dict, json_mode: bool = False) -> None:
    """Display user profile."""
    if json_mode:
        _json_out(user)
        return

    table = Table(show_header=False)
    table.add_column("Field", style="bold cyan")
    table.add_column("Value")

    table.add_row("ID", str(user.get("id", "-")))
    table.add_row("URL Token", user.get("url_token", "-"))
    table.add_row("姓名", user.get("name", "-"))

    headline = user.get("headline", "")
    if headline:
        table.add_row("签名", headline)

    avatar_url = user.get("avatar_url", "")
    if avatar_url:
        table.add_row("头像", avatar_url[:60] + "..." if len(avatar_url) > 60 else avatar_url)

    for field, label in [
        ("answer_count", "回答数"),
        ("articles_count", "文章数"),
        ("question_count", "提问数"),
        ("follower_count", "粉丝数"),
        ("following_count", "关注数"),
        ("voteup_count", "赞同数"),
        ("thanked_count", "感谢数"),
    ]:
        val = user.get(field)
        if val is not None:
            table.add_row(label, str(val))

    gender = user.get("gender")
    if gender is not None:
        gender_str = {"1": "男", "0": "女", "-1": "未知"}.get(str(gender), str(gender))
        table.add_row("性别", gender_str)

    console.print(table)


def show_user_articles(data: dict, json_mode: bool = False) -> None:
    """Display user articles."""
    if json_mode:
        _json_out(data)
        return

    articles = data.get("data", [])
    if not articles:
        console.print("[yellow]暂无文章[/yellow]")
        return

    table = Table(title="用户文章", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=20)
    table.add_column("标题", min_width=40)
    table.add_column("赞同", justify="right", width=6)
    table.add_column("评论", justify="right", width=6)
    table.add_column("创建时间", width=16)

    for item in articles:
        table.add_row(
            str(item.get("id", "-")),
            item.get("title", "-")[:50],
            str(item.get("voteup_count", 0)),
            str(item.get("comment_count", 0)),
            _fmt_ts(item.get("created_time", "")),
        )

    console.print(table)
    paging = data.get("paging", {})
    console.print(f"\nTotal: {paging.get('totals', len(articles))} articles")


def show_user_answers(data: dict, json_mode: bool = False) -> None:
    """Display user answers."""
    if json_mode:
        _json_out(data)
        return

    answers = data.get("data", [])
    if not answers:
        console.print("[yellow]暂无回答[/yellow]")
        return

    table = Table(title="用户回答", show_header=True, header_style="bold magenta", expand=False)
    table.add_column("ID", style="dim", width=18)
    table.add_column("问题标题", width=25)
    table.add_column("赞", justify="right", width=4)
    table.add_column("评", justify="right", width=4)
    table.add_column("折", justify="center", width=4)
    table.add_column("时间", width=12)

    collapsed_count = 0
    for item in answers:
        question = item.get("question", {})
        is_collapsed = item.get("is_collapsed", False)
        if is_collapsed:
            collapsed_count += 1
            collapsed_str = "[red]是[/red]"
        else:
            collapsed_str = "[green]否[/green]"
        table.add_row(
            str(item.get("id", "-")),
            question.get("title", "-")[:25],
            str(item.get("voteup_count", 0)),
            str(item.get("comment_count", 0)),
            collapsed_str,
            _fmt_ts(item.get("created_time", ""))[:12],
        )

    console.print(table)
    paging = data.get("paging", {})
    total = paging.get("totals", len(answers))
    if collapsed_count > 0:
        console.print(f"\nTotal: {total} answers, [red]{collapsed_count} collapsed[/red]")
    else:
        console.print(f"\nTotal: {total} answers")


def show_user_questions(data: dict, json_mode: bool = False) -> None:
    """Display user questions."""
    if json_mode:
        _json_out(data)
        return

    questions = data.get("data", [])
    if not questions:
        console.print("[yellow]暂无提问[/yellow]")
        return

    table = Table(title="用户提问", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=20)
    table.add_column("标题", min_width=40)
    table.add_column("回答数", justify="right", width=8)
    table.add_column("关注者", justify="right", width=8)
    table.add_column("创建时间", width=16)

    for item in questions:
        table.add_row(
            str(item.get("id", "-")),
            item.get("title", "-")[:50],
            str(item.get("answer_count", 0)),
            str(item.get("follower_count", 0)),
            _fmt_ts(item.get("created_time", "")),
        )

    console.print(table)
    paging = data.get("paging", {})
    console.print(f"\nTotal: {paging.get('totals', len(questions))} questions")


def show_user_followers(data: dict, json_mode: bool = False) -> None:
    """Display user followers."""
    if json_mode:
        _json_out(data)
        return

    users = data.get("data", [])
    if not users:
        console.print("[yellow]暂无粉丝[/yellow]")
        return

    table = Table(title="粉丝列表", show_header=True, header_style="bold magenta")
    table.add_column("URL Token", min_width=15)
    table.add_column("姓名", min_width=12)
    table.add_column("签名", min_width=30, max_width=50)
    table.add_column("回答数", justify="right", width=8)
    table.add_column("文章数", justify="right", width=8)
    table.add_column("粉丝数", justify="right", width=8)

    for item in users:
        headline = item.get("headline", "")[:50]
        table.add_row(
            item.get("url_token", "-"),
            item.get("name", "-"),
            headline,
            str(item.get("answer_count", 0)),
            str(item.get("articles_count", 0)),
            str(item.get("follower_count", 0)),
        )

    console.print(table)
    paging = data.get("paging", {})
    console.print(f"\nTotal: {paging.get('totals', len(users))} followers")


def show_user_followees(data: dict, json_mode: bool = False) -> None:
    """Display user followees (关注列表)."""
    if json_mode:
        _json_out(data)
        return

    users = data.get("data", [])
    if not users:
        console.print("[yellow]暂无关注[/yellow]")
        return

    table = Table(title="关注列表", show_header=True, header_style="bold magenta")
    table.add_column("URL Token", min_width=15)
    table.add_column("姓名", min_width=12)
    table.add_column("签名", min_width=30, max_width=50)
    table.add_column("回答数", justify="right", width=8)
    table.add_column("文章数", justify="right", width=8)
    table.add_column("粉丝数", justify="right", width=8)

    for item in users:
        headline = item.get("headline", "")[:50]
        table.add_row(
            item.get("url_token", "-"),
            item.get("name", "-"),
            headline,
            str(item.get("answer_count", 0)),
            str(item.get("articles_count", 0)),
            str(item.get("follower_count", 0)),
        )

    console.print(table)
    paging = data.get("paging", {})
    console.print(f"\nTotal: {paging.get('totals', len(users))} followees")


def show_user_collections(data: dict, json_mode: bool = False) -> None:
    """Display user collections."""
    if json_mode:
        _json_out(data)
        return

    collections = data.get("data", [])
    if not collections:
        console.print("[yellow]暂无收藏夹[/yellow]")
        return

    table = Table(title="收藏夹列表", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=20)
    table.add_column("标题", min_width=30)
    table.add_column("描述", min_width=30, max_width=50)
    table.add_column("回答数", justify="right", width=8)
    table.add_column("公开", justify="center", width=6)

    for item in collections:
        is_public = "是" if not item.get("is_public", True) else "否"
        table.add_row(
            str(item.get("id", "-")),
            item.get("title", "-")[:40],
            item.get("description", "")[:50],
            str(item.get("answer_count", 0)),
            is_public,
        )

    console.print(table)
    paging = data.get("paging", {})
    console.print(f"\nTotal: {paging.get('totals', len(collections))} collections")


# ============================================================
#  5. Answer Detail
# ============================================================


def show_answer_detail(answer: dict, json_mode: bool = False) -> None:
    """Display answer detail."""
    if json_mode:
        _json_out(answer)
        return

    table = Table(show_header=False)
    table.add_column("Field", style="bold cyan")
    table.add_column("Value")

    table.add_row("ID", str(answer.get("id", "-")))

    question = answer.get("question", {})
    table.add_row("问题", question.get("title", "-")[:60])

    author = answer.get("author", {})
    table.add_row("作者", author.get("name", "-"))

    for field, label in [
        ("voteup_count", "赞同数"),
        ("comment_count", "评论数"),
    ]:
        val = answer.get(field)
        if val is not None:
            table.add_row(label, str(val))

    created = answer.get("created_time", "")
    if created:
        table.add_row("创建时间", _fmt_ts(created))

    updated = answer.get("updated_time", "")
    if updated:
        table.add_row("更新时间", _fmt_ts(updated))

    content = answer.get("content", "")
    if content:
        # Strip HTML tags and truncate
        content_text = re.sub(r"<[^>]+>", "", content).strip()
        if len(content_text) > 200:
            content_text = content_text[:200] + "..."
        table.add_row("内容预览", content_text)

    console.print(table)


# ============================================================
#  6. Hot Questions
# ============================================================


def show_hot_questions(data: dict, json_mode: bool = False) -> None:
    """Display hot questions list."""
    if json_mode:
        _json_out(data)
        return

    items = data.get("data", [])
    if not items:
        console.print("[yellow]暂无热榜数据[/yellow]")
        return

    table = Table(title="知乎热榜", show_header=True, header_style="bold magenta")
    table.add_column("排名", style="bold yellow", justify="right", width=6)
    table.add_column("热度", justify="right", width=10)
    table.add_column("标题", min_width=50)
    table.add_column("回答数", justify="right", width=8)

    rank = 0
    for item in items:
        item_type = item.get("type", "")

        if item_type == "hot_list_feed":
            target = item.get("target", {})
            target_type = target.get("type", "")

            if target_type == "question":
                rank += 1
                title = target.get("title", "-")
                answer_count = target.get("answer_count", 0)

                hot_val = "-"
                detail_text = item.get("detail_text", "")
                if detail_text:
                    hot_val = detail_text.replace("热度", "").strip()
                else:
                    hot_score = item.get("score", 0)
                    if hot_score:
                        hot_val = str(hot_score)

                table.add_row(
                    str(rank),
                    hot_val,
                    title[:60],
                    str(answer_count),
                )
        elif item_type in ("feed_advert", "hot_list_feed_advert"):
            continue

    console.print(table)
    console.print(f"\nTotal: {rank} hot questions")
