"""
xss.py

Rule-based Cross-Site Scripting (XSS) Analyzer.
"""


class XSSAnalyzer:
    """Detects potential XSS points."""

    def analyze(self, forms, headers):

        findings = []

        csp_present = "Content-Security-Policy" in headers

        for form in forms:

            issues = []

            # Check text/search inputs
            for field in form["inputs"]:

                field_type = field.get("type", "text").lower()

                if field_type in [
                    "text",
                    "search",
                    "email",
                    "url",
                    "textarea"
                ]:
                    issues.append(
                        f"User input field detected ({field_type})"
                    )

            # Missing CSP increases XSS risk
            if not csp_present:
                issues.append(
                    "Missing Content-Security-Policy header."
                )

            # Calculate risk
            if len(issues) == 0:
                risk = "LOW"
            elif len(issues) <= 2:
                risk = "MEDIUM"
            else:
                risk = "HIGH"

            findings.append({
                "action": form["action"],
                "issues": issues,
                "risk": risk
            })

        return findings