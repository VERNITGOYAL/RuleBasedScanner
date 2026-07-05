from crawler.html_parser import HTMLParser

html = """
<html>
<head><title>Demo</title></head>

<body>

<a href="/about">About</a>

<a href="/contact">Contact</a>

</body>

</html>
"""

parser = HTMLParser(html, "https://example.com")

print(parser.get_title())

print(parser.extract_links())