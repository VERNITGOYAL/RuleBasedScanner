"""
Rule-Based Web Vulnerability Scanner
"""

from rich.console import Console
from rich.panel import Panel

from crawler.site_crawler import SiteCrawler

console = Console()


def main():
    console.print(
        Panel.fit(
            "[bold cyan]Rule-Based Web Vulnerability Scanner[/bold cyan]\n"
            "[green]Version 1.0[/green]",
            title="Welcome",
        )
    )

    url = input("Enter target URL: ").strip()

    site_crawler = SiteCrawler()

    count = 0

    for page in site_crawler.crawl(url):

        count += 1

        console.print(f"\n[bold green]Page {count}[/bold green]")
        console.print(f"[cyan]Title:[/cyan] {page.title}")
        console.print(f"[cyan]URL:[/cyan] {page.url}")
        console.print(f"[cyan]Status Code:[/cyan] {page.status_code}")
        console.print(f"[cyan]Response Time:[/cyan] {page.response_time:.2f} sec")
        console.print(f"[cyan]Links Found:[/cyan] {len(page.links)}")



if __name__ == "__main__":
    main()