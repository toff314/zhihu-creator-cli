from __future__ import annotations

from .common import Table, _clean_html, _json_out, _paging_total, _show_empty, console

_SEARCH_COLUMNS = {
    "general": ["ID", "标题", "类型", "回答数", "关注者", "赞"],
    "question": ["ID", "标题", "回答数", "关注者"],
    "answer": ["ID", "问题", "作者", "赞", "评"],
    "article": ["ID", "标题", "作者", "赞", "评"],
    "column": ["Slug", "名称", "作者", "文章数", "关注者"],
    "topic": ["ID", "名称", "描述", "关注者"],
    "people": ["URL Token", "姓名", "签名", "回答数", "粉丝数"],
}


def show_search_results_unified(data: dict, kind: str, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    results = data.get("data", [])
    if not results:
        _show_empty("搜索结果")
        return
    col_defs = _SEARCH_COLUMNS.get(kind, _SEARCH_COLUMNS["general"])
    table = Table(title=f"搜索结果 ({kind})", show_header=True, header_style="bold magenta")
    for col in col_defs:
        style = "dim" if col in ("ID", "Slug", "URL Token") else None
        justify = "right" if col in ("回答数", "关注者", "赞", "评", "文章数", "粉丝数") else "left"
        width = 8 if justify == "right" else None
        min_w = 40 if col in ("标题", "问题", "名称", "内容", "描述") else None
        table.add_column(col, style=style, justify=justify, width=width, min_width=min_w)
    for item in results:
        obj = item
        for key in ("object", "target"):
            if key in item:
                obj = item[key]
                break
        row: list[str] = []
        for col in col_defs:
            if col == "ID":
                row.append(str(obj.get("id", "-")))
            elif col == "Slug":
                row.append(obj.get("url_token") or str(obj.get("id", "-")))
            elif col == "标题":
                row.append(_clean_html(obj.get("title", obj.get("name", "-")), 60))
            elif col == "问题":
                q = obj.get("question", {})
                row.append(q.get("title", "-")[:60])
            elif col == "作者":
                a = obj.get("author", {})
                row.append(a.get("name", "-"))
            elif col == "类型":
                row.append(obj.get("type", "-"))
            elif col == "回答数":
                row.append(str(obj.get("answer_count", "-")))
            elif col == "关注者":
                row.append(str(obj.get("follower_count", obj.get("followers", "-"))))
            elif col == "赞":
                row.append(str(obj.get("voteup_count", 0)))
            elif col == "评":
                row.append(str(obj.get("comment_count", 0)))
            elif col == "文章数":
                row.append(str(obj.get("articles_count") or obj.get("items_count", 0)))
            elif col == "名称":
                row.append(_clean_html(obj.get("name", obj.get("title", "-")), 50))
            elif col == "描述":
                row.append(_clean_html(obj.get("description", ""), 50))
            elif col == "URL Token":
                row.append(obj.get("url_token", "-"))
            elif col == "姓名":
                row.append(obj.get("name", "-"))
            elif col == "签名":
                row.append(obj.get("headline", "")[:50])
            elif col == "粉丝数":
                row.append(str(obj.get("follower_count", 0)))
            else:
                row.append(str(obj.get(col, "-")))
        table.add_row(*row)
    console.print(table)
    paging = data.get("paging", {})
    total = paging.get("totals", len(results))
    _paging_total(len(results), total, "results")


def show_top_search(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    items = data.get("data", [])
    if not items:
        _show_empty("热搜")
        return
    table = Table(title="知乎热搜", show_header=True, header_style="bold magenta")
    table.add_column("排名", style="bold yellow", justify="right", width=6)
    table.add_column("热搜词", min_width=30)
    table.add_column("类型", width=10)
    for idx, item in enumerate(items, 1):
        query = item.get("query", item.get("search_text", "-"))
        item_type = item.get("type", "-")
        table.add_row(str(idx), query[:40], item_type)
    console.print(table)
    console.print(f"\nTotal: {len(items)} hot searches")


def show_preset_words(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    words = data.get("preset_words", data.get("data", []))
    if not words:
        _show_empty("预设词")
        return
    table = Table(title="搜索预设词", show_header=True, header_style="bold magenta")
    table.add_column("序号", style="bold yellow", justify="right", width=6)
    table.add_column("关键词", min_width=30)
    for idx, word in enumerate(words, 1):
        if isinstance(word, dict):
            text = word.get("query", word.get("search_text", word.get("word", "-")))
        else:
            text = str(word)
        table.add_row(str(idx), text[:40])
    console.print(table)
    console.print(f"\nTotal: {len(words)} preset words")
