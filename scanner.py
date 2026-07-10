"""
Rule-Based Web Vulnerability Scanner
Version 1.0
"""

from rich.console import Console
from rich.panel import Panel

from crawler.site_crawler import SiteCrawler
from analyzer.headers import HeaderAnalyzer
from analyzer.cookies import CookieAnalyzer
from analyzer.https_analyzer import HTTPSAnalyzer

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
    cookie_analyzer = CookieAnalyzer()
    https_analyzer = HTTPSAnalyzer()

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

        # ==========================
        # HTTPS Analysis
        # ==========================

        console.print("\n[bold yellow]HTTPS Analysis[/bold yellow]")

        https_result = https_analyzer.analyze(page)

        if https_result["https"]:
            console.print("[green]✓ HTTPS Enabled[/green]")
        else:
            console.print("[red]✗ HTTPS Not Enabled[/red]")

        console.print(f"Risk: {https_result['risk']}")
        console.print(f"Message: {https_result['message']}")

        # ==========================
        # Security Header Analysis
        # ==========================

        console.print("\n[bold yellow]Security Header Analysis[/bold yellow]")

        header_results = header_analyzer.analyze(page.headers)

        missing = 0

        for item in header_results:

            if item["status"] == "Present":
                console.print(f"[green]✓[/green] {item['header']}")
            else:
                console.print(f"[red]✗[/red] {item['header']}")
                missing += 1

        if missing == 0:
            header_risk = "LOW"
        elif missing <= 2:
            header_risk = "MEDIUM"
        else:
            header_risk = "HIGH"

        console.print(f"\nHeader Risk: {header_risk}")

        # ==========================
        # Cookie Analysis
        # ==========================

        console.print("\n[bold yellow]Cookie Analysis[/bold yellow]")

        cookie_results = cookie_analyzer.analyze(page.cookies)

        if not cookie_results:
            console.print("[yellow]No cookies found.[/yellow]")
        else:

            for cookie in cookie_results:

                console.print(f"\nCookie: {cookie['name']}")

                console.print(
                    "[green]✓ Secure[/green]"
                    if cookie["secure"]
                    else "[red]✗ Secure[/red]"
                )

                console.print(
                    "[green]✓ HttpOnly[/green]"
                    if cookie["httponly"]
                    else "[red]✗ HttpOnly[/red]"
                )

                console.print(f"SameSite: {cookie['samesite']}")

        # ==========================
        # Overall Risk
        # ==========================

        overall_score = 0

        if https_result["risk"] == "HIGH":
            overall_score += 3

        if header_risk == "HIGH":
            overall_score += 3
        elif header_risk == "MEDIUM":
            overall_score += 2
        else:
            overall_score += 1

        if overall_score <= 2:
            overall_risk = "LOW"
        elif overall_score <= 4:
            overall_risk = "MEDIUM"
        else:
            overall_risk = "HIGH"

        console.print(f"\n[bold red]Overall Risk: {overall_risk}[/bold red]")

    console.rule("[bold green]Scan Completed[/bold green]")
    console.print(f"Pages Scanned: {page_count}")


if __name__ == "__main__":
    main()