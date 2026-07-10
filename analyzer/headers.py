"""
headers.py

Analyzes HTTP Security Headers.
"""


class HeaderAnalyzer:
    """Checks important HTTP security headers."""

    REQUIRED_HEADERS = {
        "Content-Security-Policy":
            "Helps prevent Cross-Site Scripting (XSS).",

        "Strict-Transport-Security":
            "Forces HTTPS connections.",

        "X-Frame-Options":
            "Protects against Clickjacking.",

        "X-Content-Type-Options":
            "Prevents MIME type sniffing.",

        "Referrer-Policy":
            "Controls referrer information.",

        "Permissions-Policy":
            "Restricts browser features."
    }

    def analyze(self, headers: dict):

        results = []

        for header, description in self.REQUIRED_HEADERS.items():

            if header in headers:
                status = "Present"
            else:
                status = "Missing"

            results.append({
                "header": header,
                "status": status,
                "description": description
            })

        return results