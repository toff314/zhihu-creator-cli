from __future__ import annotations

from .common import Table, _clean_html, _fmt_ts, _json_out, _paging_total, _show_empty, _type_label, console


def show_collection_detail(collection: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(collection)
        return
    table = Table(show_header=False)
    table.add_column("Field", style="bold cyan")
    table.add_column("Value")
    table.add_row("ID", str(collection.get("id", "-")))
    table.add_row("标题", collection.get("title", "-"))
    description = collection.get("description", "")
    if description:
        table.add_row("描述", _clean_html(description, 200))
    table.add_row("创建者", collection.get("creator", {}).get("name", "-"))
    content_count = collection.get("content_count", collection.get("answer_count", 0))
    table.add_row("内容数", str(content_count))
    followers = collection.get("followers_count", 0)
    table.add_row("关注者", str(followers))
    is_public = "是" if collection.get("is_public", True) else "否"
    table.add_row("公开", is_public)
    created = collection.get("created_time", "")
    if created:
        table.add_row("创建时间", _fmt_ts(created))
    updated = collection.get("updated_time", "")
    if updated:
        table.add_row("更新时间", _fmt_ts(updated))
    console.print(table)


def show_collection_contents(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    contents = data.get("data", [])
    if not contents:
        _show_empty("收藏内容")
        return
    table = Table(title="收藏夹内容", show_header=True, header_style="bold magenta")
    table.add_column("类型", width=10)
    table.add_column("ID", style="dim", no_wrap=True, min_width=22)
    table.add_column("标题", min_width=40)
    table.add_column("作者", width=15)
    table.add_column("赞", justify="right", width=5)
    for item in contents:
        content = item.get("content", item)
        author = content.get("author", {})
        title = content.get("title", "")
        if not title:
            q = content.get("question", {})
            title = q.get("title", "-")
        table.add_row(
            _type_label(content.get("type")),
            str(content.get("id", "-")),
            title[:50],
            author.get("name", "-"),
            str(content.get("voteup_count", 0)),
        )
    console.print(table)
    paging = data.get("paging", {})
    _paging_total(len(contents), paging.get("totals", len(contents)), "contents")
