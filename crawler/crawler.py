"""
crawler.py

Handles downloading web pages.
"""

from typing import Optional

import requests
from requests.exceptions import RequestException

from config import REQUEST_TIMEOUT
from utils.constants import DEFAULT_HEADERS


class Crawler:
    """Downloads HTML from a webpage."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)

    def fetch_page(self, url: str) -> Optional[str]:
        """
        Download a webpage.

        Args:
            url: Target URL

        Returns:
            HTML content if successful, otherwise None.
        """

        try:
            response = self.session.get(
                url,
                timeout=REQUEST_TIMEOUT
            )

            response.raise_for_status()

            return response.text

        except RequestException as error:
            print(f"Error: {error}")
            return None