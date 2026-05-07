"""Notifications commands: invites, messages."""

import click

from ..display.common import show_error
from ..display.notifications import show_invite_notifications, show_message_notifications
from ..exceptions import DataFetchError
from . import _helpers as h


@click.group(name="notifications")
@h.require_login
def notifications_group() -> None:
    """Notification center (通知中心)."""
    pass


@notifications_group.command(name="invites")
@h.common_options
def notification_invites(offset: int, limit: int, json_mode: bool) -> None:
    """Get invite notifications (邀请回答通知).

    Example::

        zhihu-creator notifications invites --limit 10
    """
    with h._get_client() as client:
        try:
            data = client.get_invite_notifications_only(offset=offset, limit=limit)
            show_invite_notifications(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None


@notifications_group.command(name="messages")
@h.common_options
def notification_messages(offset: int, limit: int, json_mode: bool) -> None:
    """Get message notifications (消息通知).

    Example::

        zhihu-creator notifications messages --limit 10
    """
    with h._get_client() as client:
        try:
            data = client.get_message_notifications(offset=offset, limit=limit)
            show_message_notifications(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None
