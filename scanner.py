"""
Rule-Based Web Vulnerability Scanner
Version 1.0
"""

from rich.console import Console
from rich.panel import Panel

from crawler.site_crawler import SiteCrawler
from analyzer.headers import HeaderAnalyzer

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

    site_crawler = SiteCrawler(max_pages=10)
    header_analyzer = HeaderAnalyzer()

    page_count = 0

    for page in site_crawler.crawl(url):

        page_count += 1

        console.rule(f"[bold blue]Page {page_count}[/bold blue]")

        console.print(f"[cyan]Title:[/cyan] {page.title}")
        console.print(f"[cyan]URL:[/cyan] {page.url}")
        console.print(f"[cyan]Status Code:[/cyan] {page.status_code}")
        console.print(
            f"[cyan]Response Time:[/cyan] {page.response_time:.2f} seconds"
        )
        console.print(f"[cyan]Links Found:[/cyan] {len(page.links)}")

        console.print("\n[bold yellow]Security Header Analysis[/bold yellow]")

        results = header_analyzer.analyze(page.headers)

        missing = 0

        for item in results:

            if item["status"] == "Present":
                console.print(f"[green]✓[/green] {item['header']}")
            else:
                console.print(f"[red]✗[/red] {item['header']}")
                missing += 1

        if missing == 0:
            risk = "LOW"
        elif missing <= 2:
            risk = "MEDIUM"
        else:
            risk = "HIGH"

        console.print(f"\n[bold magenta]Risk Level:[/bold magenta] {risk}")

    console.rule("[bold green]Scan Completed[/bold green]")
    console.print(f"Pages Scanned: {page_count}")


if __name__ == "__main__":
    main()