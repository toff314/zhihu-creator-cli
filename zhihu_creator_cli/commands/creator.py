"""Creator commands — currently no available endpoints."""

import click

from . import _helpers as h


@click.group(name="creator")
@h.require_login
def creator_group() -> None:
    """Creator center (创作中心) — 暂无可用 API."""
    pass
