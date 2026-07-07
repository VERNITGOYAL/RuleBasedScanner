"""
crawler.py

Handles downloading web pages.
"""

import requests
from requests.exceptions import RequestException

from config import REQUEST_TIMEOUT
from utils.constants import DEFAULT_HEADERS

from crawler.html_parser import HTMLParser
from crawler.page import Page


class Crawler:
    """Downloads and parses web pages."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)

    def fetch_page(self, url: str):
        """
        Download a webpage and return a Page object.
        """

        try:
            response = self.session.get(
                url,
                timeout=REQUEST_TIMEOUT
            )

            response.raise_for_status()

            html = response.text

            parser = HTMLParser(html, url)

            page = Page(
                url=url,
                html=html,
                title=parser.get_title(),
                links=parser.extract_links()
            )

            return page

        except RequestException as error:
            print(f"Error: {error}")
            return None