"""
forms.py

Analyzes HTML forms for basic security issues.
"""


class FormAnalyzer:
    """Analyzes HTML forms."""

    def analyze(self, forms):

        results = []

        for form in forms:

            has_password = False

            for input_field in form["inputs"]:

                if input_field["type"].lower() == "password":
                    has_password = True

            action = form["action"]

            method = form["method"]

            issues = []

            if has_password and method == "GET":
                issues.append("Password submitted using GET method.")

            if action.startswith("http://"):
                issues.append("Form submits over HTTP.")

            if not action:
                issues.append("Form action not specified.")

            if len(issues) == 0:
                risk = "LOW"
            elif len(issues) == 1:
                risk = "MEDIUM"
            else:
                risk = "HIGH"

            results.append({
                "action": action,
                "method": method,
                "password": has_password,
                "issues": issues,
                "risk": risk
            })

        return results