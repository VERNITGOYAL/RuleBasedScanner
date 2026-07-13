"""
Rule-Based Web Vulnerability Scanner
Version 1.0
"""

from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from analyzer.cookies import CookieAnalyzer
from analyzer.csrf import CSRFAnalyzer
from analyzer.forms import FormAnalyzer
from analyzer.headers import HeaderAnalyzer
from analyzer.https_analyzer import HTTPSAnalyzer
from analyzer.sqli import SQLInjectionAnalyzer
from analyzer.xss import XSSAnalyzer
from crawler.site_crawler import SiteCrawler
from database.database import Database
from reports.html_report import HTMLReport
from reports.pdf_report import PDFReport
from utils.risk_calculator import RiskCalculator
from utils.summary import Summary

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

    if not url:
        console.print("[red]No target URL provided.[/red]")
        return

    site_crawler = SiteCrawler(max_pages=10)
    header_analyzer = HeaderAnalyzer()
    cookie_analyzer = CookieAnalyzer()
    https_analyzer = HTTPSAnalyzer()
    form_analyzer = FormAnalyzer()
    csrf_analyzer = CSRFAnalyzer()
    sqli_analyzer = SQLInjectionAnalyzer()
    xss_analyzer = XSSAnalyzer()
    risk_calculator = RiskCalculator()
    summary = Summary()
    html_report = HTMLReport()
    pdf_report = PDFReport()
    database = Database()

    page_count = 0
    report_pages = []

    https_issues = 0
    missing_headers = 0
    cookie_issues = 0
    forms_found = 0
    csrf_findings = 0
    sqli_findings = 0
    xss_findings = 0
    overall_score = 0

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
            https_issues += 1

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

        missing_headers += missing

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

                if (
                    not cookie["secure"]
                    or not cookie["httponly"]
                    or cookie["samesite"] == "Not Set"
                ):
                    cookie_issues += 1

        # ==========================
        # Form Analysis
        # ==========================

        console.print("\n[bold yellow]Form Analysis[/bold yellow]")

        form_results = form_analyzer.analyze(page.forms)
        forms_found += len(form_results)

        if not form_results:
            console.print("[yellow]No forms found.[/yellow]")
        else:
            for form in form_results:
                console.print(
                    f"Form Action: {form['action']} | Risk: {form['risk']}"
                )
                if form["issues"]:
                    console.print(f"Issues: {', '.join(form['issues'])}")

        # ==========================
        # SQL Injection Analysis
        # ==========================

        console.print("\n[bold yellow]SQL Injection Analysis[/bold yellow]")

        sqli_results = sqli_analyzer.analyze(page.forms)
        page_sqli_findings = sum(1 for result in sqli_results if result["issues"])
        sqli_findings += page_sqli_findings

        if page_sqli_findings == 0:
            console.print("[green]No SQLi issues found.[/green]")
        else:
            for result in sqli_results:
                if result["issues"]:
                    console.print(
                        f"Action: {result['action']} | Risk: {result['risk']}"
                    )
                    console.print(f"Issues: {', '.join(result['issues'])}")

        # ==========================
        # CSRF Analysis
        # ==========================

        console.print("\n[bold yellow]CSRF Analysis[/bold yellow]")

        csrf_results = csrf_analyzer.analyze(page.forms)
        page_csrf_findings = sum(1 for result in csrf_results if result["issues"])
        csrf_findings += page_csrf_findings

        if page_csrf_findings == 0:
            console.print("[green]No CSRF issues found.[/green]")
        else:
            for result in csrf_results:
                if result["issues"]:
                    console.print(
                        f"Action: {result['action']} | Risk: {result['risk']}"
                    )
                    console.print(f"Issues: {', '.join(result['issues'])}")

        # ==========================
        # XSS Analysis
        # ==========================

        console.print("\n[bold yellow]XSS Analysis[/bold yellow]")

        xss_results = xss_analyzer.analyze(page.forms, page.headers)
        page_xss_findings = sum(1 for result in xss_results if result["issues"])
        xss_findings += page_xss_findings

        if page_xss_findings == 0:
            console.print("[green]No XSS issues found.[/green]")
        else:
            for result in xss_results:
                if result["issues"]:
                    console.print(
                        f"Action: {result['action']} | Risk: {result['risk']}"
                    )
                    console.print(f"Issues: {', '.join(result['issues'])}")

        # ==========================
        # Overall Risk
        # ==========================

        page_score, page_risk = risk_calculator.calculate(
            https_result,
            header_results,
            cookie_results,
            form_results,
            csrf_results,
            sqli_results,
            xss_results,
        )

        overall_score += page_score

        report_pages.append(
            {
                "url": page.url,
                "title": page.title,
                "status": str(page.status_code),
                "risk": page_risk,
            }
        )

        console.print(f"\n[bold red]Page Risk: {page_risk}[/bold red]")
        console.print(f"[bold red]Page Score: {page_score}[/bold red]")

    if overall_score <= 3:
        overall_risk = "LOW"
    elif overall_score <= 7:
        overall_risk = "MEDIUM"
    else:
        overall_risk = "HIGH"

    summary.display(
        pages_scanned=page_count,
        https_issues=https_issues,
        missing_headers=missing_headers,
        cookie_issues=cookie_issues,
        forms_found=forms_found,
        csrf_findings=csrf_findings,
        sqli_findings=sqli_findings,
        xss_findings=xss_findings,
        overall_score=overall_score,
        overall_risk=overall_risk,
    )

    base_dir = Path(__file__).resolve().parent
    report_dir = base_dir / "output" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    html_report_path = html_report.generate(
        url,
        report_pages,
        filename=str(report_dir / "scan_report.html"),
    )

    summary_payload = {
        "Pages Scanned": page_count,
        "HTTPS Issues": https_issues,
        "Missing Headers": missing_headers,
        "Cookie Issues": cookie_issues,
        "Forms Found": forms_found,
        "CSRF Findings": csrf_findings,
        "SQLi Findings": sqli_findings,
        "XSS Findings": xss_findings,
        "Overall Score": overall_score,
        "Overall Risk": overall_risk,
    }

    pdf_report_path = pdf_report.generate(
        url,
        report_pages,
        summary_payload,
        filename=str(report_dir / "scan_report.pdf"),
    )

    database.save_scan(
        url,
        page_count,
        overall_score,
        overall_risk,
    )

    console.print(f"\n[green]HTML report generated: {html_report_path}[/green]")
    console.print(f"[green]PDF report generated: {pdf_report_path}[/green]")
    console.print("[green]Scan result saved to the database.[/green]")

    table = Table(title="Recent Scan History")
    table.add_column("ID", style="cyan")
    table.add_column("Target URL", style="green")
    table.add_column("Pages")
    table.add_column("Risk", style="red")

    history = database.get_history()

    for row in history[:5]:
        table.add_row(str(row[0]), row[1], str(row[3]), row[5])

    console.print(table)

    database.close()

    console.rule("[bold green]Scan Completed[/bold green]")
    console.print(f"Pages Scanned: {page_count}")


if __name__ == "__main__":
    main()