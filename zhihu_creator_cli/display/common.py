from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from typing import Any

from rich.console import Console
from rich.table import Table  # noqa: F401 — re-exported for sub-modules

console = Console(width=160, force_terminal=True)


def _fmt_ts(raw: Any) -> str:
    if isinstance(raw, (int, float)) and raw > 1000000000:
        return datetime.fromtimestamp(raw).strftime("%Y-%m-%d %H:%M")
    return str(raw)[:16]


def _json_out(data: Any) -> None:
    sys.stdout.write(json.dumps(data, ensure_ascii=False, indent=None))
    sys.stdout.write("\n")


def _clean_html(text: str, max_len: int = 200) -> str:
    cleaned = re.sub(r"<[^>]+>", "", text).strip()
    if len(cleaned) > max_len:
        cleaned = cleaned[:max_len] + "..."
    return cleaned


def _show_empty(label: str = "数据") -> None:
    console.print(f"[yellow]暂无{label}[/yellow]")


def _paging_total(count: int, total: Any, label: str = "items") -> None:
    console.print(f"\nTotal: {total} {label}")


def show_error(message: str) -> None:
    console.print(f"[bold red]Error:[/bold red] {message}")


def show_info(message: str) -> None:
    console.print(f"[blue]{message}[/blue]")


def show_me(me: dict, json_mode: bool = False) -> None:
    if json_mode:
        _json_out(me)
        return
    name = me.get("name", "Unknown")
    headline = me.get("headline", "")
    console.print(f"\n[bold green]Logged in as:[/bold green] {name}")
    if headline:
        console.print(f"  Headline: {headline}")
    console.print(f"  ID: {me.get('id', '-')}")
    console.print(f"  URL Token: {me.get('url_token', '-')}")
