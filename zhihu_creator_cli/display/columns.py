from __future__ import annotations

from .common import Table, _clean_html, _fmt_ts, _json_out, _paging_total, _show_empty, console


def show_recommended_columns(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    columns = data.get("data", [])
    if not columns:
        _show_empty("专栏")
        return
    tablist = data.get("tablist", [])
    tab_name = tablist[0].get("name", "") if tablist else ""
    title = f"专栏推荐 - {tab_name}" if tab_name else "专栏推荐"
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("ID/Slug", style="dim", no_wrap=True, min_width=22)
    table.add_column("名称", min_width=30)
    table.add_column("描述", min_width=30, max_width=50)
    table.add_column("文章数", justify="right", width=8)
    table.add_column("关注者", justify="right", width=8)
    table.add_column("作者", width=15)
    for item in columns:
        if item.get("type") != "column":
            continue
        id_or_slug = item.get("url_token") or item.get("id", "-")
        excerpt = item.get("excerpt") or item.get("description", "")
        if excerpt:
            excerpt = excerpt[:50]
        author = item.get("author", {})
        author_name = author.get("name", "-")
        table.add_row(
            id_or_slug,
            item.get("title", "-")[:40],
            excerpt,
            str(item.get("articles_count") or item.get("items_count", 0)),
            str(item.get("followers", 0)),
            author_name,
        )
    console.print(table)
    console.print(f"\nShowing {len(columns)} columns")


def show_user_columns(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    columns = data.get("data", [])
    if not columns:
        _show_empty("专栏")
        return
    table = Table(title="我的专栏", show_header=True, header_style="bold magenta")
    table.add_column("ID/Slug", style="dim", no_wrap=True, min_width=22)
    table.add_column("名称", min_width=30)
    table.add_column("文章数", justify="right", width=8)
    table.add_column("关注者", justify="right", width=8)
    table.add_column("赞同", justify="right", width=8)
    for item in columns:
        id_or_slug = item.get("url_token") or item.get("id", "-")
        title = _clean_html(item.get("title", "-"), 40)
        table.add_row(
            id_or_slug,
            title,
            str(item.get("articles_count") or item.get("items_count", 0)),
            str(item.get("followers", 0)),
            str(item.get("voteup_count", 0)),
        )
    console.print(table)
    total = data.get("paging", {}).get("totals", len(columns))
    _paging_total(len(columns), total, "columns")


def show_search_columns(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    results = data.get("data", [])
    if not results:
        _show_empty("搜索专栏结果")
        return
    table = Table(title="专栏搜索结果", show_header=True, header_style="bold magenta")
    table.add_column("ID/Slug", style="dim", no_wrap=True, min_width=22)
    table.add_column("名称", min_width=30)
    table.add_column("作者", width=15)
    table.add_column("文章数", justify="right", width=8)
    table.add_column("关注者", justify="right", width=8)
    for item in results:
        obj = item.get("object", item)
        if obj.get("type") != "column":
            continue
        id_or_slug = obj.get("url_token") or obj.get("id", "-")
        author = obj.get("author", {})
        author_name = author.get("name", "-")
        title = _clean_html(obj.get("title", "-"), 40)
        table.add_row(
            id_or_slug,
            title,
            author_name,
            str(obj.get("articles_count") or obj.get("items_count", 0)),
            str(obj.get("followers", 0)),
        )
    console.print(table)
    paging = data.get("paging", {})
    total = paging.get("totals", len(results))
    _paging_total(len(results), total, "columns")


def show_column_detail(column: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(column)
        return
    table = Table(show_header=False)
    table.add_column("Field", style="bold cyan")
    table.add_column("Value")
    slug = column.get("url_token") or column.get("slug") or column.get("id", "-")
    table.add_row("Slug/ID", slug)
    table.add_row("名称", column.get("title") or column.get("name", "-"))
    description = column.get("intro") or column.get("description", "")
    if description:
        table.add_row("描述", _clean_html(description, 200))
    followers = column.get("followers") or column.get("followersCount", 0)
    articles_count = (
        column.get("articles_count") or column.get("items_count") or column.get("postsCount", 0)
    )
    table.add_row("关注者", str(followers))
    table.add_row("文章数", str(articles_count))
    author = column.get("author") or column.get("creator", {})
    if author:
        table.add_row("创建者", author.get("name", "-"))
        author_slug = author.get("url_token") or author.get("slug", "-")
        table.add_row("创建者Slug", author_slug)
    created = column.get("created", "")
    if created:
        table.add_row("创建时间", _fmt_ts(created))
    updated = column.get("updated", "")
    if updated:
        table.add_row("更新时间", _fmt_ts(updated))
    console.print(table)


def show_column_articles(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    articles = data.get("data", [])
    if not articles:
        _show_empty("文章")
        return
    table = Table(title="专栏文章", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", no_wrap=True, min_width=22)
    table.add_column("标题", min_width=40)
    table.add_column("赞", justify="right", width=5)
    table.add_column("评", justify="right", width=5)
    table.add_column("时间", width=16)
    for item in articles:
        table.add_row(
            str(item.get("id", "-")),
            item.get("title", "-")[:50],
            str(item.get("voteup_count", 0)),
            str(item.get("comment_count", 0)),
            _fmt_ts(item.get("created", item.get("created_time", ""))),
        )
    console.print(table)
    paging = data.get("paging", {})
    total = paging.get("totals", len(articles))
    _paging_total(len(articles), total, "articles")
