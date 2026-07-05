from bs4 import BeautifulSoup
from urllib.parse import urljoin


class HTMLParser:
    """Parses HTML content."""

    def __init__(self, html: str, base_url: str):
        self.soup = BeautifulSoup(html, "lxml")
        self.base_url = base_url

    def get_title(self) -> str:
        """Return page title."""
        if self.soup.title:
            return self.soup.title.text.strip()
        return "No Title"

    def extract_links(self) -> list[str]:
        """Extract all links from the page."""

        links = []

        for tag in self.soup.find_all("a", href=True):
            full_url = urljoin(self.base_url, tag["href"])

            if full_url not in links:
                links.append(full_url)

        return links