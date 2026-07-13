"""
risk_calculator.py

Calculates overall risk score for a scanned page.
"""


class RiskCalculator:

    def calculate(
        self,
        https_result,
        header_results,
        cookie_results,
        form_results,
        csrf_results,
        sqli_results,
        xss_results
    ):

        score = 0

        # HTTPS
        if https_result["risk"] == "HIGH":
            score += 3

        # Missing security headers
        for header in header_results:
            if header["status"] == "Missing":
                score += 1

        # Cookie issues
        for cookie in cookie_results:

            if not cookie["secure"]:
                score += 1

            if not cookie["httponly"]:
                score += 1

            if cookie["samesite"] == "Not Set":
                score += 1

        # Forms
        for form in form_results:

            if form["risk"] == "MEDIUM":
                score += 2
            elif form["risk"] == "HIGH":
                score += 3

        # CSRF
        for result in csrf_results:

            if result["risk"] == "MEDIUM":
                score += 2
            elif result["risk"] == "HIGH":
                score += 3

        # SQL Injection
        for result in sqli_results:

            if result["risk"] == "MEDIUM":
                score += 2

        # XSS
        for result in xss_results:

            if result["risk"] == "MEDIUM":
                score += 2
            elif result["risk"] == "HIGH":
                score += 3

        # Final risk level
        if score <= 3:
            risk = "LOW"
        elif score <= 7:
            risk = "MEDIUM"
        else:
            risk = "HIGH"

        return score, risk