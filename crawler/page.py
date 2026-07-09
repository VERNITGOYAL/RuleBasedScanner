"""
page.py

Represents a downloaded webpage.
"""

from dataclasses import dataclass, field


@dataclass
class Page:
    url: str
    html: str
    title: str
    links: list[str] = field(default_factory=list)

    status_code: int = 0
    headers: dict = field(default_factory=dict)
    cookies: dict = field(default_factory=dict)
    response_time: float = 0.0