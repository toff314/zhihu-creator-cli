"""Pins commands: detail."""

import click

from ..display.common import show_error
from ..display.pins import show_pin_detail
from ..exceptions import DataFetchError
from . import _helpers as h


@click.group(name="pins")
def pins_group() -> None:
    """Pin (想法) detail."""
    pass


@pins_group.command(name="detail")
@h.json_option
@click.argument("pin_id")
def pin_detail(pin_id: str, json_mode: bool) -> None:
    """Get pin detail (想法详情).

    Example::

        zhihu-creator pins detail 123456789
    """
    with h._get_client() as client:
        try:
            data = client.get_pin_detail(pin_id)
            show_pin_detail(data, json_mode)
        except DataFetchError as e:
            show_error(str(e))
            raise click.Abort() from None
