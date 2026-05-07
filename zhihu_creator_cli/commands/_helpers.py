"""Shared decorators and helpers for CLI commands."""

from functools import wraps

import click

from ..auth import AuthManager
from ..client import ZhihuClient
from ..display.common import show_error


def require_login(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = AuthManager()
        if not auth.is_logged_in():
            show_error("Not logged in. Run: zhihu-creator login --qrcode")
            raise click.Abort() from None
        return f(*args, **kwargs)

    return wrapper


def json_option(f):
    return click.option(
        "--json",
        "json_mode",
        is_flag=True,
        default=False,
        help="Output raw JSON for agent consumption.",
    )(f)


def common_options(f):
    f = click.option("--offset", default=0, help="Pagination offset.")(f)
    f = click.option("--limit", default=20, help="Items per page.")(f)
    f = json_option(f)
    return f


def _get_client() -> ZhihuClient:
    auth = AuthManager()
    return ZhihuClient(auth.cookies)
