"""Markdown and template helpers for CDAM platform."""

from __future__ import annotations

import json
import re
from datetime import date, timedelta

import markdown
from markupsafe import Markup, escape


def render_markdown(text: str) -> Markup:
    html = markdown.markdown(
        text or "",
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


def chatbot_reply(message: str) -> str:
    text = message.lower().strip()
    if not text:
        return "Ask me about Python, sessions, quizzes, or your CDAM learning path."
    if "numpy" in text:
        return "NumPy powers numerical computing. Start with Session 4: NumPy Fundamentals."
    if "pandas" in text or "dataframe" in text:
        return "Pandas is ideal for tabular analysis. Check Session 5 and Session 6 for analysis and cleaning."
    if "quiz" in text or "test" in text:
        return "Each session has a Quiz tab. Submit answers to track your score on the dashboard."
    if "certificate" in text:
        return "Complete all 10 sessions to unlock your CDAM Python for Data Science certificate."
    if "login" in text or "register" in text:
        return "Use Register to create an account, then access your dashboard and track progress."
    if "cdam" in text:
        return "CDAM (Center for Data Analytics & Modelling) at Chuka University offers professional data science training."
    if "python" in text:
        return "Python is the core language here. Begin with Session 1 and follow the curriculum sequentially."
    if "help" in text or "start" in text:
        return "Click Start Learning on the homepage, open Session 1, and use the tabbed lesson interface."
    return "I can help with sessions, quizzes, certificates, and Python topics. Try asking about Pandas, NumPy, or ML."
