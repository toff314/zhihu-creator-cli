from __future__ import annotations

from .common import Table, _clean_html, _json_out, _paging_total, _show_empty, _type_label, console


def show_topic_detail(topic: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(topic)
        return
    table = Table(show_header=False)
    table.add_column("Field", style="bold cyan")
    table.add_column("Value")
    table.add_row("ID", str(topic.get("id", "-")))
    table.add_row("名称", topic.get("name", "-"))
    description = topic.get("description", "")
    if description:
        table.add_row("描述", _clean_html(description, 200))
    followers = topic.get("followers_count", 0)
    table.add_row("关注者", str(followers))
    questions_count = topic.get("questions_count", 0)
    table.add_row("问题数", str(questions_count))
    best_answers_count = topic.get("best_answers_count", 0)
    table.add_row("精华回答", str(best_answers_count))
    url = topic.get("url", "")
    if url:
        table.add_row("链接", url)
    console.print(table)


def show_topic_unanswered(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    questions = data.get("data", [])
    if not questions:
        _show_empty("待回答问题")
        return
    table = Table(title="话题待回答问题", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", no_wrap=True, min_width=22)
    table.add_column("标题", min_width=40)
    table.add_column("回答数", justify="right", width=8)
    table.add_column("关注者", justify="right", width=8)
    for item in questions:
        target = item.get("target", item)
        table.add_row(
            str(target.get("id", "-")),
            target.get("title", "-")[:50],
            str(target.get("answer_count", 0)),
            str(target.get("follower_count", 0)),
        )
    console.print(table)
    paging = data.get("paging", {})
    _paging_total(len(questions), paging.get("totals", len(questions)), "questions")


def show_topic_essence(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    items = data.get("data", [])
    if not items:
        _show_empty("话题精华")
        return
    table = Table(title="话题精华内容", show_header=True, header_style="bold magenta")
    table.add_column("类型", width=6)
    table.add_column("ID", style="dim", no_wrap=True, min_width=22)
    table.add_column("标题", min_width=40)
    table.add_column("赞同", justify="right", width=6)
    table.add_column("评论", justify="right", width=6)
    for item in items:
        target = item.get("target", item)
        table.add_row(
            _type_label(target.get("type")),
            str(target.get("id", "-")),
            target.get("title", "-")[:50],
            str(target.get("voteup_count", 0)),
            str(target.get("comment_count", 0)),
        )
    console.print(table)
    paging = data.get("paging", {})
    _paging_total(len(items), paging.get("totals", len(items)), "精华内容")
