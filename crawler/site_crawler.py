"""
site_crawler.py

Breadth-First Search (BFS) crawler for scanning websites.
"""

from collections import deque
from urllib.parse import urljoin, urlparse

from crawler.crawler import Crawler


class SiteCrawler:
    """Crawls a website using Breadth-First Search (BFS)."""

    def __init__(self, max_pages=10):
        self.crawler = Crawler()
        self.max_pages = max_pages

    def crawl(self, start_url):
        """
        Crawl a website starting from start_url.

        Yields:
            Page objects one by one.
        """

        visited = set()
        queue = deque([start_url])

        start_domain = urlparse(start_url).netloc

        while queue and len(visited) < self.max_pages:

            current_url = queue.popleft()

            if current_url in visited:
                continue

            print(f"\nScanning: {current_url}")

            page = self.crawler.fetch_page(current_url)

            if page is None:
                continue

            visited.add(current_url)

            yield page

            print(f"Found {len(page.links)} links")

            for link in page.links:

                if not link:
                    continue

                absolute_url = urljoin(current_url, link)

                parsed = urlparse(absolute_url)

                # Ignore non-http/https links
                if parsed.scheme not in ("http", "https"):
                    continue

                # Stay inside same domain
                if parsed.netloc != start_domain:
                    continue

                # Remove URL fragment
                clean_url = absolute_url.split("#")[0]

                # Remove trailing slash (except root)
                if (
                    clean_url.endswith("/")
                    and len(clean_url)
                    > len(parsed.scheme + "://" + parsed.netloc + "/")
                ):
                    clean_url = clean_url.rstrip("/")

                if clean_url not in visited and clean_url not in queue:
                    queue.append(clean_url)