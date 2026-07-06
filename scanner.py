"""
Rule-Based Web Vulnerability Scanner
"""

from rich.console import Console
from rich.panel import Panel

from crawler.crawler import Crawler
from crawler.html_parser import HTMLParser

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

    crawler = Crawler()

    html = crawler.fetch_page(url)

    if not html:
        console.print("[red]✗ Failed to download page.[/red]")
        return

    console.print("[green]✓ Page downloaded successfully![/green]")

    parser = HTMLParser(html, url)

    title = parser.get_title()

    links = parser.extract_links()

    console.print(f"\n[cyan]Page Title:[/cyan] {title}")

    console.print(f"[cyan]Links Found:[/cyan] {len(links)}")

    if links:
        console.print("\n[bold]Discovered Links:[/bold]")

        for link in links:
            console.print(f" • {link}")


if __name__ == "__main__":
    main()