"""
sqli.py

Rule-based SQL Injection Analyzer.
"""


class SQLInjectionAnalyzer:
    """Detects potential SQL Injection points."""

    SUSPICIOUS_NAMES = {
        "id",
        "user",
        "username",
        "email",
        "login",
        "search",
        "query",
        "password",
        "pass"
    }

    def analyze(self, forms):

        findings = []

        for form in forms:

            issues = []

            # Password over GET
            if form["method"] == "GET":
                for field in form["inputs"]:
                    if field["type"] == "password":
                        issues.append(
                            "Password field submitted using GET."
                        )

            # Suspicious parameter names
            for field in form["inputs"]:

                name = field.get("name")

                if not name:
                    continue

                if name.lower() in self.SUSPICIOUS_NAMES:

                    issues.append(
                        f"Sensitive parameter detected: '{name}'"
                    )

            findings.append({
                "action": form["action"],
                "issues": issues,
                "risk": (
                    "LOW"
                    if len(issues) == 0
                    else "MEDIUM"
                )
            })

        return findings