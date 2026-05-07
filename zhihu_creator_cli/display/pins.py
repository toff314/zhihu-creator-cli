from __future__ import annotations

from .common import Table, _clean_html, _fmt_ts, _json_out, console


def show_pin_detail(pin: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(pin)
        return
    table = Table(show_header=False)
    table.add_column("Field", style="bold cyan")
    table.add_column("Value")
    table.add_row("ID", str(pin.get("id", "-")))
    author = pin.get("author", {})
    table.add_row("作者", author.get("name", "-"))
    content = pin.get("content", "")
    if content:
        table.add_row("内容", _clean_html(content, 200))
    for field, label in [
        ("voteup_count", "赞同数"),
        ("comment_count", "评论数"),
    ]:
        val = pin.get(field)
        if val is not None:
            table.add_row(label, str(val))
    created = pin.get("created_time", "")
    if created:
        table.add_row("创建时间", _fmt_ts(created))
    url = pin.get("url", "")
    if url:
        table.add_row("链接", url)
    console.print(table)
