from __future__ import annotations

from .common import Table, _clean_html, _fmt_ts, _json_out, _paging_total, _show_empty, _type_label, console


def show_user_profile(user: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(user)
        return
    table = Table(show_header=False)
    table.add_column("Field", style="bold cyan")
    table.add_column("Value")
    table.add_row("ID", str(user.get("id", "-")))
    table.add_row("URL Token", user.get("url_token", "-"))
    table.add_row("姓名", user.get("name", "-"))
    headline = user.get("headline", "")
    if headline:
        table.add_row("签名", headline)
    avatar_url = user.get("avatar_url", "")
    if avatar_url:
        table.add_row("头像", avatar_url[:60] + "..." if len(avatar_url) > 60 else avatar_url)
    for field, label in [
        ("answer_count", "回答数"),
        ("articles_count", "文章数"),
        ("question_count", "提问数"),
        ("follower_count", "粉丝数"),
        ("following_count", "关注数"),
        ("voteup_count", "赞同数"),
        ("thanked_count", "感谢数"),
    ]:
        val = user.get(field)
        if val is not None:
            table.add_row(label, str(val))
    gender = user.get("gender")
    if gender is not None:
        gender_str = {"1": "男", "0": "女", "-1": "未知"}.get(str(gender), str(gender))
        table.add_row("性别", gender_str)
    console.print(table)


def show_user_articles(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    articles = data.get("data", [])
    if not articles:
        _show_empty("文章")
        return
    table = Table(title="用户文章", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", no_wrap=True, min_width=22)
    table.add_column("标题", min_width=40)
    table.add_column("赞同", justify="right", width=6)
    table.add_column("评论", justify="right", width=6)
    table.add_column("创建时间", width=16)
    for item in articles:
        table.add_row(
            str(item.get("id", "-")),
            item.get("title", "-")[:50],
            str(item.get("voteup_count", 0)),
            str(item.get("comment_count", 0)),
            _fmt_ts(item.get("created_time", "")),
        )
    console.print(table)
    paging = data.get("paging", {})
    _paging_total(len(articles), paging.get("totals", len(articles)), "articles")


def show_user_answers(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    answers = data.get("data", [])
    if not answers:
        _show_empty("回答")
        return
    table = Table(title="用户回答", show_header=True, header_style="bold magenta", expand=True)
    table.add_column("ID", style="dim", no_wrap=True, min_width=22)
    table.add_column("问题标题", min_width=40)
    table.add_column("赞", justify="right", width=5)
    table.add_column("评", justify="right", width=5)
    table.add_column("折", justify="center", width=5)
    table.add_column("时间", width=18)
    collapsed_count = 0
    for item in answers:
        question = item.get("question", {})
        is_collapsed = item.get("is_collapsed", False)
        if is_collapsed:
            collapsed_count += 1
            collapsed_str = "[red]是[/red]"
        else:
            collapsed_str = "[green]否[/green]"
        table.add_row(
            str(item.get("id", "-")),
            question.get("title", "-"),
            str(item.get("voteup_count", 0)),
            str(item.get("comment_count", 0)),
            collapsed_str,
            _fmt_ts(item.get("created_time", "")),
        )
    console.print(table)
    paging = data.get("paging", {})
    total = paging.get("totals", len(answers))
    if collapsed_count > 0:
        console.print(f"\nTotal: {total} answers, [red]{collapsed_count} collapsed[/red]")
    else:
        console.print(f"\nTotal: {total} answers")


def show_user_questions(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    questions = data.get("data", [])
    if not questions:
        _show_empty("提问")
        return
    table = Table(title="用户提问", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", no_wrap=True, min_width=22)
    table.add_column("标题", min_width=40)
    table.add_column("回答数", justify="right", width=8)
    table.add_column("关注者", justify="right", width=8)
    table.add_column("创建时间", width=16)
    for item in questions:
        table.add_row(
            str(item.get("id", "-")),
            item.get("title", "-")[:50],
            str(item.get("answer_count", 0)),
            str(item.get("follower_count", 0)),
            _fmt_ts(item.get("created_time", "")),
        )
    console.print(table)
    paging = data.get("paging", {})
    _paging_total(len(questions), paging.get("totals", len(questions)), "questions")


def show_user_followers(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    users = data.get("data", [])
    if not users:
        _show_empty("粉丝")
        return
    table = Table(title="粉丝列表", show_header=True, header_style="bold magenta")
    table.add_column("URL Token", min_width=15)
    table.add_column("姓名", min_width=12)
    table.add_column("签名", min_width=30, max_width=50)
    table.add_column("回答数", justify="right", width=8)
    table.add_column("文章数", justify="right", width=8)
    table.add_column("粉丝数", justify="right", width=8)
    for item in users:
        headline = item.get("headline", "")[:50]
        table.add_row(
            item.get("url_token", "-"),
            item.get("name", "-"),
            headline,
            str(item.get("answer_count", 0)),
            str(item.get("articles_count", 0)),
            str(item.get("follower_count", 0)),
        )
    console.print(table)
    paging = data.get("paging", {})
    _paging_total(len(users), paging.get("totals", len(users)), "followers")


def show_user_followees(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    users = data.get("data", [])
    if not users:
        _show_empty("关注")
        return
    table = Table(title="关注列表", show_header=True, header_style="bold magenta")
    table.add_column("URL Token", min_width=15)
    table.add_column("姓名", min_width=12)
    table.add_column("签名", min_width=30, max_width=50)
    table.add_column("回答数", justify="right", width=8)
    table.add_column("文章数", justify="right", width=8)
    table.add_column("粉丝数", justify="right", width=8)
    for item in users:
        headline = item.get("headline", "")[:50]
        table.add_row(
            item.get("url_token", "-"),
            item.get("name", "-"),
            headline,
            str(item.get("answer_count", 0)),
            str(item.get("articles_count", 0)),
            str(item.get("follower_count", 0)),
        )
    console.print(table)
    paging = data.get("paging", {})
    _paging_total(len(users), paging.get("totals", len(users)), "followees")


def show_user_collections(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    collections = data.get("data", [])
    if not collections:
        _show_empty("收藏夹")
        return
    table = Table(title="收藏夹列表", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", no_wrap=True, min_width=22)
    table.add_column("标题", min_width=30)
    table.add_column("描述", min_width=30, max_width=50)
    table.add_column("回答数", justify="right", width=8)
    table.add_column("公开", justify="center", width=6)
    for item in collections:
        is_public = "是" if not item.get("is_public", True) else "否"
        table.add_row(
            str(item.get("id", "-")),
            item.get("title", "-")[:40],
            item.get("description", "")[:50],
            str(item.get("answer_count", 0)),
            is_public,
        )
    console.print(table)
    paging = data.get("paging", {})
    _paging_total(len(collections), paging.get("totals", len(collections)), "collections")


def show_user_pins(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    pins = data.get("data", [])
    if not pins:
        _show_empty("想法")
        return
    table = Table(title="用户想法", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", no_wrap=True, min_width=22)
    table.add_column("内容", min_width=40)
    table.add_column("赞", justify="right", width=5)
    table.add_column("时间", width=16)
    for item in pins:
        raw_content = item.get("content", "")
        if isinstance(raw_content, list):
            text_parts = []
            for part in raw_content:
                if isinstance(part, dict):
                    text_parts.append(part.get("own_text", part.get("content", "")))
                else:
                    text_parts.append(str(part))
            text = " ".join(text_parts)
        else:
            text = str(raw_content)
        content = _clean_html(text, 80)
        like_count = item.get("like_count", 0)
        created_time = item.get("created_time", item.get("updated", ""))
        table.add_row(
            str(item.get("id", "-")),
            content,
            str(like_count),
            _fmt_ts(created_time) if created_time else "-",
        )
    console.print(table)
    paging = data.get("paging", {})
    _paging_total(len(pins), paging.get("totals", len(pins)), "pins")


def show_user_activities(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    activities = data.get("data", [])
    if not activities:
        _show_empty("动态")
        return
    table = Table(title="用户动态", show_header=True, header_style="bold magenta")
    table.add_column("类型", width=12)
    table.add_column("内容", min_width=40)
    table.add_column("时间", width=16)
    for item in activities:
        target = item.get("target", {})
        title = target.get("title", "")
        if not title:
            title = _clean_html(target.get("content", ""), 60)
        created = item.get("created_time", "")
        table.add_row(_type_label(item.get("type")), title[:60], _fmt_ts(created) if created else "-")
    console.print(table)
    paging = data.get("paging", {})
    _paging_total(len(activities), paging.get("totals", len(activities)), "activities")


def show_user_following_topics(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    items = data.get("data", [])
    if not items:
        _show_empty("关注话题")
        return
    table = Table(title="关注话题", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", no_wrap=True, min_width=22)
    table.add_column("名称", min_width=30)
    table.add_column("描述", min_width=30, max_width=50)
    for item in items:
        topic = item.get("topic", item)
        desc = topic.get("introduction", topic.get("excerpt", ""))[:50]
        table.add_row(
            str(topic.get("id", "-")),
            topic.get("name", "-")[:40],
            _clean_html(desc, 50),
        )
    console.print(table)
    paging = data.get("paging", {})
    _paging_total(len(items), paging.get("totals", len(items)), "topics")


def show_user_following_questions(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    questions = data.get("data", [])
    if not questions:
        _show_empty("关注问题")
        return
    table = Table(title="关注问题", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", no_wrap=True, min_width=22)
    table.add_column("标题", min_width=40)
    table.add_column("回答数", justify="right", width=8)
    table.add_column("关注者", justify="right", width=8)
    for item in questions:
        table.add_row(
            str(item.get("id", "-")),
            item.get("title", "-")[:50],
            str(item.get("answer_count", 0)),
            str(item.get("follower_count", 0)),
        )
    console.print(table)
    paging = data.get("paging", {})
    _paging_total(len(questions), paging.get("totals", len(questions)), "questions")


def show_user_following_columns(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    columns = data.get("data", [])
    if not columns:
        _show_empty("关注专栏")
        return
    table = Table(title="关注专栏", show_header=True, header_style="bold magenta")
    table.add_column("Slug", style="dim", width=20)
    table.add_column("名称", min_width=30)
    table.add_column("文章数", justify="right", width=8)
    table.add_column("关注者", justify="right", width=8)
    for item in columns:
        slug = item.get("url_token") or item.get("id", "-")
        table.add_row(
            slug,
            item.get("title", "-")[:40],
            str(item.get("articles_count") or item.get("items_count", 0)),
            str(item.get("followers", 0)),
        )
    console.print(table)
    paging = data.get("paging", {})
    _paging_total(len(columns), paging.get("totals", len(columns)), "columns")


def show_user_mutuals(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    users = data.get("data", [])
    if not users:
        _show_empty("互关好友")
        return
    table = Table(title="互关好友", show_header=True, header_style="bold magenta")
    table.add_column("URL Token", min_width=15)
    table.add_column("姓名", min_width=12)
    table.add_column("签名", min_width=30, max_width=50)
    table.add_column("回答数", justify="right", width=8)
    table.add_column("粉丝数", justify="right", width=8)
    for item in users:
        table.add_row(
            item.get("url_token", "-"),
            item.get("name", "-"),
            item.get("headline", "")[:50],
            str(item.get("answer_count", 0)),
            str(item.get("follower_count", 0)),
        )
    console.print(table)
    paging = data.get("paging", {})
    _paging_total(len(users), paging.get("totals", len(users)), "mutuals")


def show_user_zvideos(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    videos = data.get("data", [])
    if not videos:
        _show_empty("视频")
        return
    table = Table(title="用户视频", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", no_wrap=True, min_width=22)
    table.add_column("标题", min_width=40)
    table.add_column("赞", justify="right", width=5)
    table.add_column("评", justify="right", width=5)
    table.add_column("时间", width=16)
    for item in videos:
        table.add_row(
            str(item.get("id", "-")),
            item.get("title", "-")[:50],
            str(item.get("voteup_count", 0)),
            str(item.get("comment_count", 0)),
            _fmt_ts(item.get("created_time", "")),
        )
    console.print(table)
    paging = data.get("paging", {})
    _paging_total(len(videos), paging.get("totals", len(videos)), "zvideos")


def show_user_columns_direct(data: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(data)
        return
    items = data.get("data", [])
    if not items:
        _show_empty("专栏")
        return
    table = Table(title="用户专栏", show_header=True, header_style="bold magenta")
    table.add_column("Slug", style="dim", width=22)
    table.add_column("名称", min_width=30)
    table.add_column("文章数", justify="right", width=8)
    table.add_column("关注者", justify="right", width=8)
    for item in items:
        col = item.get("column", item)
        slug = col.get("url_token") or col.get("id", "-")
        title = _clean_html(col.get("title", "-"), 40)
        table.add_row(
            slug,
            title,
            str(col.get("articles_count") or col.get("items_count", 0)),
            str(col.get("followers", 0)),
        )
    console.print(table)
    paging = data.get("paging", {})
    _paging_total(len(items), paging.get("totals", len(items)), "columns")
