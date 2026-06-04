"""Markdown and template helpers for CDAM platform."""

from __future__ import annotations

import json
import re
from datetime import date, timedelta

import markdown
from markupsafe import Markup, escape


def render_markdown(text: str) -> Markup:
    if not text:
        return Markup("")
    # Standardize escaped newlines from raw seed/db inputs
    processed_text = text.replace("\\n", "\n")
    html = markdown.markdown(
        processed_text,
        extensions=["extra", "nl2br", "sane_lists", "tables"],
    )
    return Markup(html)


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^\w\s-]", "", value)
    return re.sub(r"[-\s]+", "-", value).strip("-")


def parse_quiz(raw: str | None) -> list[dict]:
    if not raw:
        return []
    try:
        data = json.loads(raw)
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def compute_streak(completed_dates: list[date]) -> int:
    if not completed_dates:
        return 0
    unique_days = sorted(set(completed_dates), reverse=True)
    streak = 1
    for idx in range(1, len(unique_days)):
        if unique_days[idx - 1] - unique_days[idx] == timedelta(days=1):
            streak += 1
        else:
            break
    today = date.today()
    if unique_days[0] not in {today, today - timedelta(days=1)}:
        return 0
    return streak

