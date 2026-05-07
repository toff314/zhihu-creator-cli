from __future__ import annotations

from .common import Table, _json_out, _show_empty, console


def show_hot_questions(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    items = data.get("data", [])
    if not items:
        _show_empty("热榜数据")
        return
    table = Table(title="知乎热榜", show_header=True, header_style="bold magenta")
    table.add_column("排名", style="bold yellow", justify="right", width=6)
    table.add_column("ID", style="dim", no_wrap=True, min_width=22)
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
                    str(rank), str(target.get("id", "-")), hot_val, title[:60], str(answer_count)
                )
        elif item_type in ("feed_advert", "hot_list_feed_advert"):
            continue
    console.print(table)
    console.print(f"\nTotal: {rank} hot questions")
