"""
https_analyzer.py

Checks whether a webpage uses HTTPS.
"""


class HTTPSAnalyzer:
    """Analyzes HTTPS usage."""

    def analyze(self, page):

        if page.url.lower().startswith("https://"):
            return {
                "https": True,
                "risk": "LOW",
                "message": "Website is using HTTPS."
            }

        return {
            "https": False,
            "risk": "HIGH",
            "message": "Website is NOT using HTTPS."
        }