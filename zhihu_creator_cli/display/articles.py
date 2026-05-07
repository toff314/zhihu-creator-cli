from __future__ import annotations

from .common import Table, _fmt_ts, _json_out, _paging_total, _show_empty, console


def show_creator_articles(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    articles = data.get("data", [])
    if not articles:
        _show_empty("文章")
        return
    table = Table(title="创作中心文章", show_header=True, header_style="bold magenta", expand=True)
    table.add_column("ID", style="dim", no_wrap=True, min_width=22)
    table.add_column("标题", min_width=40)
    table.add_column("赞", justify="right", width=5)
    table.add_column("评", justify="right", width=5)
    table.add_column("藏", justify="right", width=5)
    table.add_column("时间", width=18)
    for item in articles:
        article = item if isinstance(item, dict) else item.get("content", item)
        updated_raw = article.get("updated", article.get("updated_time", ""))
        updated_str = _fmt_ts(updated_raw) if updated_raw else ""
        reaction = article.get("reaction", {})
        stats = reaction.get("statistics", {})
        fav_count = stats.get("favorites", 0)
        table.add_row(
            str(article.get("id", "-")),
            article.get("title", "Untitled"),
            str(article.get("voteup_count", 0)),
            str(article.get("comment_count", 0)),
            str(fav_count),
            updated_str,
        )
    console.print(table)
    paging = data.get("paging", {})
    total = paging.get("totals", "?")
    _paging_total(len(articles), total, "articles")


def show_creator_stats(data: dict, json_mode: bool = False) -> None:
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
