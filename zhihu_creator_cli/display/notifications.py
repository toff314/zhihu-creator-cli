from __future__ import annotations

from .common import Table, _fmt_ts, _json_out, _show_empty, console


def show_invite_notifications(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    invites = data.get("data", [])
    if not invites:
        _show_empty("邀请回答通知")
        return
    table = Table(title="邀请回答通知", show_header=True, header_style="bold magenta")
    table.add_column("问题ID", style="dim", no_wrap=True, min_width=22)
    table.add_column("标题", min_width=40)
    table.add_column("邀请者", width=16)
    table.add_column("邀请时间", width=18)
    table.add_column("状态", width=6)
    for item in invites:
        target = item.get("target", {})
        q = item.get("question", target)
        question_id = q.get("id", "-")
        title = q.get("title", "Untitled")[:60]
        content = item.get("content", {})
        actors = content.get("actors", [])
        inviter_name = actors[0].get("name", "-") if actors else "-"
        invite_time = item.get("invite_time", item.get("create_time", 0))
        time_str = _fmt_ts(invite_time) if invite_time else "-"
        is_read = item.get("is_read", True)
        status = "[dim]已读[/dim]" if is_read else "[bold green]未读[/bold green]"
        table.add_row(str(question_id), title, inviter_name, time_str, status)
    console.print(table)
    paging = data.get("paging", {})
    total = paging.get("totals", len(invites))
    console.print(f"\nTotal: {total} invite notifications")


def show_message_notifications(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    messages = data.get("data", [])
    if not messages:
        _show_empty("消息通知")
        return
    table = Table(title="消息通知", show_header=True, header_style="bold magenta")
    table.add_column("类型", width=12)
    table.add_column("内容", min_width=40)
    table.add_column("时间", width=16)
    table.add_column("状态", width=6)
    for item in messages:
        content = item.get("content", item.get("text", "-"))
        is_read = item.get("is_read", True)
        status = "[dim]已读[/dim]" if is_read else "[bold green]未读[/bold green]"
        created = item.get("created_time", item.get("created", ""))
        table.add_row(
            item.get("type", "-")[:12],
            str(content)[:60],
            _fmt_ts(created) if created else "-",
            status,
        )
    console.print(table)
    total = data.get("paging", {}).get("totals", len(messages))
    console.print(f"\nTotal: {total} notifications")
