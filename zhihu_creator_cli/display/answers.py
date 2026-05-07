from __future__ import annotations

from .common import Table, _clean_html, _fmt_ts, _json_out, _show_empty, console


def show_answer_detail(answer: dict, json_mode: bool = False) -> None:
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
        table.add_row("内容预览", _clean_html(content, 200))
    console.print(table)


def show_answer_comments(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    comments = data.get("data", [])
    if not comments:
        _show_empty("评论")
        return
    table = Table(title="回答评论", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", no_wrap=True, min_width=22)
    table.add_column("作者", width=15)
    table.add_column("内容", min_width=40)
    table.add_column("赞", justify="right", width=5)
    table.add_column("时间", width=16)
    for item in comments:
        author = item.get("author", {})
        content = _clean_html(item.get("content", ""), 80)
        table.add_row(
            str(item.get("id", "-")),
            author.get("name", "-"),
            content,
            str(item.get("voteup_count", 0)),
            _fmt_ts(item.get("created_time", "")),
        )
    console.print(table)
    paging = data.get("paging", {})
    total = paging.get("totals", len(comments))
    console.print(f"\nTotal: {total} comments")


def show_answer_voters(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    voters = data.get("data", [])
    if not voters:
        _show_empty("赞同者")
        return
    table = Table(title="赞同者列表", show_header=True, header_style="bold magenta")
    table.add_column("URL Token", min_width=15)
    table.add_column("姓名", min_width=12)
    table.add_column("签名", min_width=30, max_width=50)
    table.add_column("回答数", justify="right", width=8)
    for item in voters:
        table.add_row(
            item.get("url_token", "-"),
            item.get("name", "-"),
            item.get("headline", "")[:50],
            str(item.get("answer_count", 0)),
        )
    console.print(table)
    paging = data.get("paging", {})
    total = paging.get("totals", len(voters))
    console.print(f"\nTotal: {total} voters")
