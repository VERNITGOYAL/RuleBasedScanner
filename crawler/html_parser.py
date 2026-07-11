"""
html_parser.py

Parses HTML pages and extracts useful information.
"""

from bs4 import BeautifulSoup
from urllib.parse import urljoin


class HTMLParser:
    """Parses HTML content."""

    def __init__(self, html: str, base_url: str):
        self.soup = BeautifulSoup(html, "lxml")
        self.base_url = base_url

    def get_title(self) -> str:
        """Return page title."""

        if self.soup.title and self.soup.title.string:
            return self.soup.title.string.strip()

        h1 = self.soup.find("h1")

        if h1:
            return h1.get_text(strip=True)

        return "No Title"

    def extract_links(self) -> list[str]:
        """Extract all hyperlinks."""

        links = []

        for tag in self.soup.find_all("a", href=True):

            full_url = urljoin(self.base_url, tag["href"])

            if full_url not in links:
                links.append(full_url)

        return links

    def extract_forms(self):
        """Extract HTML forms."""

        forms = []

        for form in self.soup.find_all("form"):

            form_data = {
                "action": urljoin(
                    self.base_url,
                    form.get("action", "")
                ),
                "method": form.get("method", "GET").upper(),
                "inputs": []
            }

            for input_tag in form.find_all("input"):

                form_data["inputs"].append({
                    "name": input_tag.get("name"),
                    "type": input_tag.get("type", "text")
                })

            forms.append(form_data)

        return forms