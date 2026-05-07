from __future__ import annotations

from .common import Table, _clean_html, _fmt_ts, _json_out, _show_empty, console


def show_question_detail(question: dict, json_mode: bool = False) -> None:
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
        table.add_row("内容", _clean_html(detail, 200))
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
    if json_mode:
        _json_out(data)
        return
    questions = data.get("data", [])
    if not questions:
        _show_empty("推荐问题")
        return
    table = Table(title="问题推荐", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", no_wrap=True, min_width=22)
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
    if json_mode:
        _json_out(data)
        return
    invites = data.get("data", [])
    if not invites:
        _show_empty("邀请回答")
        return
    has_answered_field = any(i.get("is_answered") is not None for i in invites)
    table = Table(title="邀请回答", show_header=True, header_style="bold magenta")
    table.add_column("问题ID", style="dim", no_wrap=True, min_width=22)
    table.add_column("标题", min_width=40)
    table.add_column("邀请者", width=16)
    table.add_column("邀请时间", width=18)
    if has_answered_field:
        table.add_column("已回答", width=6)
    table.add_column("类型", width=12)
    table.add_column("状态", width=6)
    for item in invites:
        q = item.get("question", {})
        is_read = item.get("is_read", True)
        status = "[dim]已读[/dim]" if is_read else "[bold green]未读[/bold green]"
        invite_time = item.get("invite_time", 0)
        time_str = _fmt_ts(invite_time) if invite_time else "-"
        row = [
            str(q.get("id", "-")),
            q.get("title", "Untitled")[:60],
            item.get("inviter_name", "-"),
            time_str,
        ]
        if has_answered_field:
            is_answered = item.get("is_answered", False)
            answered_str = "[green]是[/green]" if is_answered else "[yellow]否[/yellow]"
            row.append(answered_str)
        row.extend([item.get("verb", "-"), status])
        table.add_row(*row)
    console.print(table)
    console.print(f"\nTotal: {len(invites)} invites")


def show_search_results(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    results = data.get("data", [])
    if not results:
        _show_empty("搜索结果")
        return
    table = Table(title="搜索结果", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", no_wrap=True, min_width=22)
    table.add_column("标题", min_width=40)
    table.add_column("回答数", justify="right", width=8)
    table.add_column("关注者", justify="right", width=8)
    for item in results:
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
