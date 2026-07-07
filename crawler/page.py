"""
page.py

Represents a downloaded webpage.
"""

from dataclasses import dataclass


@dataclass
class Page:
    url: str
    html: str
    title: str
    links: list[str]