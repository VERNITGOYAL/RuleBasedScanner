"""
cookies.py

Analyzes cookies for security attributes.
"""


class CookieAnalyzer:
    """Analyzes HTTP cookies."""

    def analyze(self, cookies):

        results = []

        if not cookies:
            return results

        for cookie in cookies:

            httponly = False

            if hasattr(cookie, "_rest"):
                httponly = "HttpOnly" in cookie._rest

            samesite = "Not Set"

            if hasattr(cookie, "_rest"):
                samesite = cookie._rest.get("SameSite", "Not Set")

            results.append({
                "name": cookie.name,
                "secure": cookie.secure,
                "httponly": httponly,
                "samesite": samesite
            })

        return results