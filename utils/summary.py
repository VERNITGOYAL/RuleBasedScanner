"""
summary.py

Displays the final scan summary.
"""

from rich.console import Console

console = Console()


class Summary:

    def display(
        self,
        pages_scanned,
        https_issues,
        missing_headers,
        cookie_issues,
        forms_found,
        csrf_findings,
        sqli_findings,
        xss_findings,
        overall_score,
        overall_risk
    ):

        console.rule("[bold green]SCAN SUMMARY[/bold green]")

        console.print(f"Pages Scanned      : {pages_scanned}")
        console.print(f"HTTPS Issues       : {https_issues}")
        console.print(f"Missing Headers    : {missing_headers}")
        console.print(f"Cookie Issues      : {cookie_issues}")
        console.print(f"Forms Found        : {forms_found}")
        console.print(f"CSRF Findings      : {csrf_findings}")
        console.print(f"SQLi Findings      : {sqli_findings}")
        console.print(f"XSS Findings       : {xss_findings}")
        console.print(f"Overall Score      : {overall_score}")
        console.print(f"Overall Risk       : {overall_risk}")