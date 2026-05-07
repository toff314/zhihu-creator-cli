"""Search commands: general, questions, answers, articles, columns,
topics, people, top, preset-words."""

import click

from ..display.common import show_error
from ..display.search import show_preset_words, show_search_results_unified, show_top_search
from ..exceptions import DataFetchError
from . import _helpers as h


@click.group(name="search")
def search_group() -> None:
    """Unified search across all content types."""
    pass


@search_group.command(name="general")
@h.common_options
@click.argument("keyword")
def search_general(keyword: str, offset: int, limit: int, json_mode: bool) -> None:
    """Search all content types (综合搜索).

    Example::

        zhihu-creator search general "Python" --limit 10
    """
    with h._get_client() as client:
        try:
            data = client.search("general", keyword, offset=offset, limit=limit)
            show_search_results_unified(data, "general", json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@search_group.command(name="questions")
@h.common_options
@click.argument("keyword")
def search_questions(keyword: str, offset: int, limit: int, json_mode: bool) -> None:
    """Search for questions (问题搜索).

    Example::

        zhihu-creator search questions "Python 学习" --limit 10
    """
    with h._get_client() as client:
        try:
            data = client.search("question", keyword, offset=offset, limit=limit)
            show_search_results_unified(data, "question", json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@search_group.command(name="answers")
@h.common_options
@click.argument("keyword")
def search_answers(keyword: str, offset: int, limit: int, json_mode: bool) -> None:
    """Search for answers (回答搜索).

    Example::

        zhihu-creator search answers "Python" --limit 10
    """
    with h._get_client() as client:
        try:
            data = client.search("answer", keyword, offset=offset, limit=limit)
            show_search_results_unified(data, "answer", json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@search_group.command(name="articles")
@h.common_options
@click.argument("keyword")
def search_articles(keyword: str, offset: int, limit: int, json_mode: bool) -> None:
    """Search for articles (文章搜索).

    Example::

        zhihu-creator search articles "深度学习" --limit 10
    """
    with h._get_client() as client:
        try:
            data = client.search("article", keyword, offset=offset, limit=limit)
            show_search_results_unified(data, "article", json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@search_group.command(name="columns")
@h.common_options
@click.argument("keyword")
def search_columns(keyword: str, offset: int, limit: int, json_mode: bool) -> None:
    """Search for columns (专栏搜索).

    Example::

        zhihu-creator search columns "Python" --limit 10
    """
    with h._get_client() as client:
        try:
            data = client.search("column", keyword, offset=offset, limit=limit)
            show_search_results_unified(data, "column", json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@search_group.command(name="topics")
@h.common_options
@click.argument("keyword")
def search_topics(keyword: str, offset: int, limit: int, json_mode: bool) -> None:
    """Search for topics (话题搜索).

    Example::

        zhihu-creator search topics "人工智能" --limit 10
    """
    with h._get_client() as client:
        try:
            data = client.search("topic", keyword, offset=offset, limit=limit)
            show_search_results_unified(data, "topic", json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@search_group.command(name="people")
@h.common_options
@click.argument("keyword")
def search_people(keyword: str, offset: int, limit: int, json_mode: bool) -> None:
    """Search for people (用户搜索).

    Example::

        zhihu-creator search people "张三" --limit 10
    """
    with h._get_client() as client:
        try:
            data = client.search("people", keyword, offset=offset, limit=limit)
            show_search_results_unified(data, "people", json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@search_group.command(name="top")
@h.json_option
def search_top(json_mode: bool) -> None:
    """Get top search terms (知乎热搜).

    Example::

        zhihu-creator search top
    """
    with h._get_client() as client:
        try:
            data = client.get_top_search()
            show_top_search(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@search_group.command(name="preset-words")
@h.json_option
def search_preset_words(json_mode: bool) -> None:
    """Get preset search words (预设搜索词).

    Example::

        zhihu-creator search preset-words
    """
    with h._get_client() as client:
        try:
            data = client.get_preset_words()
            show_preset_words(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None
