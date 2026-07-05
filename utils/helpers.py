from urllib.parse import urlparse


def is_valid_url(url: str) -> bool:
    """
    Validate whether a URL is correctly formed.
    """
    parsed = urlparse(url)

    return all([parsed.scheme, parsed.netloc])


def get_domain(url: str) -> str:
    """
    Extract domain name.
    """
    return urlparse(url).netloc