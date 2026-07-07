"""
Rule-Based Web Vulnerability Scanner
"""

from rich.console import Console
from rich.panel import Panel

from crawler.crawler import Crawler

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

    page = crawler.fetch_page(url)

    if page is None:
        console.print("[red]✗ Failed to download page.[/red]")
        return

    console.print("[green]✓ Page downloaded successfully![/green]")

    console.print(f"\n[cyan]Page Title:[/cyan] {page.title}")

    console.print(f"[cyan]Links Found:[/cyan] {len(page.links)}")

    if page.links:
        console.print("\n[bold]Discovered Links:[/bold]")

        for link in page.links:
            console.print(f" • {link}")


if __name__ == "__main__":
    main()