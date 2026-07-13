"""
csrf.py

Rule-based CSRF analysis for HTML forms.
"""

class CSRFAnalyzer:
    """Detects potential CSRF weaknesses."""

    TOKEN_NAMES = {
        "csrf",
        "csrf_token",
        "authenticity_token",
        "requesttoken",
        "__requestverificationtoken",
        "xsrf_token",
        "token",
    }

    def analyze(self, forms):

        findings = []

        for form in forms:
            issues = []

            hidden_names = {
                input_field.get("name", "").lower()
                for input_field in form["inputs"]
                if input_field.get("type", "").lower() == "hidden"
                and input_field.get("name")
            }

            if form["method"] == "POST":
                if not any(token in hidden_names for token in self.TOKEN_NAMES):
                    issues.append("Missing anti-CSRF token in form.")
            else:
                issues.append("Form uses non-POST method; CSRF protection may be incomplete.")

            if form["action"].startswith("http://"):
                issues.append("Form action uses HTTP instead of HTTPS.")

            if len(issues) == 0:
                risk = "LOW"
            elif len(issues) == 1:
                risk = "MEDIUM"
            else:
                risk = "HIGH"

            findings.append({
                "action": form["action"],
                "issues": issues,
                "risk": risk,
            })

        return findings
