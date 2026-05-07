"""Auth commands: login, logout, status, whoami."""

import click

from ..auth import AuthManager
from ..display.common import show_error, show_info, show_me
from ..exceptions import LoginError
from . import _helpers as h


@click.group(name="auth")
def auth_group() -> None:
    """Authentication commands."""
    pass


@auth_group.command(name="login")
@click.option("--cookie", "cookie_str", required=True, help="Login with cookie string.")
def login(cookie_str: str) -> None:
    """Login to Zhihu with Cookie string.

    Copy cookies from browser dev tools and paste them here.

    Example::

        zhihu-creator auth login --cookie "z_c0=xxx; _xsrf=yyy; d_c0=zzz"
    """
    auth = AuthManager()
    try:
        auth.login_with_cookie_string(cookie_str)
        click.echo("✓ Cookie login successful!")
    except LoginError as e:
        show_error(str(e))
        raise click.Abort() from None

    with h._get_client() as client:
        me = client._get("https://www.zhihu.com/api/v4/me")
        show_me(me)


@auth_group.command(name="logout")
def logout() -> None:
    """Logout and clear stored cookies."""
    AuthManager().clear_cookies()
    click.echo("✓ Logged out and local cookies cleared.")


@auth_group.command(name="status")
@h.json_option
def status(json_mode: bool) -> None:
    """Check login status."""
    auth = AuthManager()
    if not auth.is_logged_in():
        show_info("Not logged in.")
        return

    with h._get_client() as client:
        try:
            me = client._get("https://www.zhihu.com/api/v4/me")
            show_me(me, json_mode)
        except LoginError:
            show_info("Cookie exists but session expired. Please login again.")


@auth_group.command(name="whoami")
@h.json_option
def whoami(json_mode: bool) -> None:
    """Show current user profile."""
    with h._get_client() as client:
        try:
            me = client._get("https://www.zhihu.com/api/v4/me")
            show_me(me, json_mode)
        except LoginError as e:
            show_error(str(e))
            raise click.Abort() from None
