"""Users commands: profile, articles, answers, questions, followers, followees,
collections, pins, activities, mutuals, following-topics, following-questions,
following-columns, zvideos, columns."""

import re

import click

from ..display.common import show_error
from ..display.users import (
    show_user_activities,
    show_user_answers,
    show_user_articles,
    show_user_collections,
    show_user_columns_direct,
    show_user_followees,
    show_user_followers,
    show_user_following_columns,
    show_user_following_questions,
    show_user_following_topics,
    show_user_mutuals,
    show_user_pins,
    show_user_profile,
    show_user_questions,
    show_user_zvideos,
)
from ..exceptions import DataFetchError
from . import _helpers as h

_HEX_PATTERN = re.compile(r"^[0-9a-fA-F]+$")


def _resolve_user_id_if_needed(client, user_input: str) -> str:
    if _HEX_PATTERN.match(user_input):
        return user_input
    return client.resolve_user_id(user_input)


@click.group(name="users")
def users_group() -> None:
    """User profile and content."""
    pass


@users_group.command(name="profile")
@h.json_option
@click.argument("url_token")
def user_profile(url_token: str, json_mode: bool) -> None:
    """Get user profile by url_token.

    Example::

        zhihu-creator users profile toff314
    """
    with h._get_client() as client:
        try:
            data = client.get_user_profile(url_token)
            show_user_profile(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@users_group.command(name="articles")
@h.common_options
@click.option(
    "--sort", "sort_by", default="created", type=click.Choice(["created", "updated", "voteups"])
)
@click.argument("url_token")
def user_articles(url_token: str, offset: int, limit: int, sort_by: str, json_mode: bool) -> None:
    """Get articles by a user.

    Example::

        zhihu-creator users articles toff314 --limit 10
    """
    with h._get_client() as client:
        try:
            data = client.get_user_articles(url_token, offset, limit, sort_by)
            show_user_articles(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@users_group.command(name="answers")
@h.common_options
@click.option(
    "--sort", "sort_by", default="created", type=click.Choice(["created", "updated", "voteups"])
)
@click.option("--collapsed", is_flag=True, help="Filter collapsed answers only.")
@click.argument("url_token")
def user_answers(
    url_token: str, offset: int, limit: int, sort_by: str, collapsed: bool, json_mode: bool
) -> None:
    """Get answers by a user.

    Example::

        zhihu-creator users answers toff314 --limit 10
        zhihu-creator users answers toff314 --collapsed  # Only collapsed
    """
    with h._get_client() as client:
        try:
            data = client.get_user_answers(url_token, offset, limit, sort_by)
            if collapsed and not json_mode:
                answers = data.get("data", [])
                filtered = [a for a in answers if a.get("is_collapsed", False)]
                data["data"] = filtered
                data["paging"]["totals"] = len(filtered)
            show_user_answers(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@users_group.command(name="questions")
@h.common_options
@click.argument("url_token")
def user_questions(url_token: str, offset: int, limit: int, json_mode: bool) -> None:
    """Get questions asked by a user.

    Example::

        zhihu-creator users questions toff314 --limit 10
    """
    with h._get_client() as client:
        try:
            data = client.get_user_questions(url_token, offset, limit)
            show_user_questions(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@users_group.command(name="followers")
@h.common_options
@click.argument("url_token")
def user_followers(url_token: str, offset: int, limit: int, json_mode: bool) -> None:
    """Get user's followers (粉丝列表).

    Example::

        zhihu-creator users followers toff314 --limit 20
    """
    with h._get_client() as client:
        try:
            data = client.get_user_followers(url_token, offset, limit)
            show_user_followers(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@users_group.command(name="followees")
@h.common_options
@click.argument("url_token")
def user_followees(url_token: str, offset: int, limit: int, json_mode: bool) -> None:
    """Get users that a user follows (关注列表).

    Example::

        zhihu-creator users followees toff314 --limit 20
    """
    with h._get_client() as client:
        try:
            data = client.get_user_followees(url_token, offset, limit)
            show_user_followees(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@users_group.command(name="collections")
@h.common_options
@click.argument("user_input")
def user_collections(user_input: str, offset: int, limit: int, json_mode: bool) -> None:
    """Get user's collections (收藏夹列表).

    Accepts url_token or hex user_id. If a url_token is given,
    it will be resolved to user_id automatically.

    Example::

        zhihu-creator users collections toff314 --limit 10
        zhihu-creator users collections 19ff584816895caaa1d68fbf187a29fd --limit 10
    """
    with h._get_client() as client:
        try:
            resolved_id = _resolve_user_id_if_needed(client, user_input)
            data = client.get_user_collections(resolved_id, offset, limit)
            show_user_collections(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@users_group.command(name="pins")
@h.common_options
@click.argument("url_token")
def user_pins(url_token: str, offset: int, limit: int, json_mode: bool) -> None:
    """Get user's pins (想法列表).

    Example::

        zhihu-creator users pins toff314 --limit 10
    """
    with h._get_client() as client:
        try:
            data = client.get_user_pins(url_token, offset, limit)
            show_user_pins(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@users_group.command(name="activities")
@h.common_options
@click.argument("url_token")
def user_activities(url_token: str, offset: int, limit: int, json_mode: bool) -> None:
    """Get user's recent activities (动态).

    Example::

        zhihu-creator users activities toff314 --limit 10
    """
    with h._get_client() as client:
        try:
            data = client.get_user_activities(url_token, offset, limit)
            show_user_activities(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@users_group.command(name="mutuals")
@h.common_options
@click.argument("url_token")
def user_mutuals(url_token: str, offset: int, limit: int, json_mode: bool) -> None:
    """Get user's mutual followers (互关列表).

    Example::

        zhihu-creator users mutuals toff314 --limit 20
    """
    with h._get_client() as client:
        try:
            data = client.get_user_mutuals(url_token, offset, limit)
            show_user_mutuals(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@users_group.command(name="following-topics")
@h.common_options
@click.argument("url_token")
def user_following_topics(url_token: str, offset: int, limit: int, json_mode: bool) -> None:
    """Get topics a user follows (关注话题列表).

    Example::

        zhihu-creator users following-topics toff314 --limit 20
    """
    with h._get_client() as client:
        try:
            data = client.get_user_following_topics(url_token, offset, limit)
            show_user_following_topics(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@users_group.command(name="following-questions")
@h.common_options
@click.argument("url_token")
def user_following_questions(url_token: str, offset: int, limit: int, json_mode: bool) -> None:
    """Get questions a user follows (关注问题列表).

    Example::

        zhihu-creator users following-questions toff314 --limit 20
    """
    with h._get_client() as client:
        try:
            data = client.get_user_following_questions(url_token, offset, limit)
            show_user_following_questions(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@users_group.command(name="following-columns")
@h.common_options
@click.argument("url_token")
def user_following_columns(url_token: str, offset: int, limit: int, json_mode: bool) -> None:
    """Get columns a user follows (关注专栏列表).

    Example::

        zhihu-creator users following-columns toff314 --limit 20
    """
    with h._get_client() as client:
        try:
            data = client.get_user_following_columns(url_token, offset, limit)
            show_user_following_columns(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@users_group.command(name="zvideos")
@h.common_options
@click.argument("url_token")
def user_zvideos(url_token: str, offset: int, limit: int, json_mode: bool) -> None:
    """Get user's videos (视频列表).

    Example::

        zhihu-creator users zvideos toff314 --limit 10
    """
    with h._get_client() as client:
        try:
            data = client.get_user_zvideos(url_token, offset, limit)
            show_user_zvideos(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@users_group.command(name="columns")
@h.common_options
@click.argument("url_token")
def user_columns(url_token: str, offset: int, limit: int, json_mode: bool) -> None:
    """Get user's subscribed columns (用户订阅专栏列表).

    Example::

        zhihu-creator users columns toff314 --limit 10
    """
    with h._get_client() as client:
        try:
            data = client.get_user_columns_direct(url_token, offset, limit)
            show_user_columns_direct(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None
