from __future__ import annotations

from .common import Table, _json_out, console


def show_creator_home(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    table = Table(title="创作中心概览", show_header=False)
    table.add_column("Metric", style="bold")
    table.add_column("Value", justify="right")
    metrics = [
        ("总阅读量", data.get("total_read_count", "-")),
        ("总赞同数", data.get("total_upvote_count", "-")),
        ("总评论数", data.get("total_comment_count", "-")),
        ("总收藏数", data.get("total_fav_count", "-")),
        ("关注者", data.get("follower_count", "-")),
        ("新增关注", data.get("new_follower_count", "-")),
        ("昨日阅读", data.get("yesterday_read_count", "-")),
        ("昨日赞同", data.get("yesterday_upvote_count", "-")),
    ]
    for label, value in metrics:
        table.add_row(label, str(value))
    console.print(table)


def show_creator_stats_detail(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    table = Table(title="创作数据详情", show_header=False)
    table.add_column("Metric", style="bold")
    table.add_column("Value", justify="right")
    for key, value in data.items():
        if isinstance(value, (int, float, str)):
            table.add_row(key, str(value))
    console.print(table)
