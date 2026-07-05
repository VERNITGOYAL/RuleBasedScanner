SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",
]

SEVERITY = {
    "LOW": "Low",
    "MEDIUM": "Medium",
    "HIGH": "High",
}

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "RuleBasedScanner/1.0 "
        "(Educational Project)"
    )
}