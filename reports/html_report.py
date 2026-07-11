"""
html_report.py

Generates an HTML report for the vulnerability scanner.
"""

from datetime import datetime


class HTMLReport:

    def generate(self, target_url, pages, filename="scan_report.html"):

        html = f"""
<!DOCTYPE html>
<html>
<head>

<title>Rule-Based Web Vulnerability Scanner</title>

<style>

body{{
font-family:Arial;
background:#f5f5f5;
margin:40px;
}}

h1{{
color:#1f4e79;
}}

.card{{
background:white;
padding:20px;
margin-bottom:20px;
border-radius:10px;
box-shadow:0 0 10px rgba(0,0,0,.1);
}}

table{{
width:100%;
border-collapse:collapse;
}}

th,td{{
padding:10px;
border:1px solid #ddd;
}}

th{{
background:#1f4e79;
color:white;
}}

.low{{color:green;font-weight:bold;}}
.medium{{color:orange;font-weight:bold;}}
.high{{color:red;font-weight:bold;}}

</style>

</head>

<body>

<h1>Rule-Based Web Vulnerability Scanner</h1>

<div class="card">

<h2>Scan Information</h2>

<p><b>Target:</b> {target_url}</p>

<p><b>Date:</b> {datetime.now()}</p>

<p><b>Pages Scanned:</b> {len(pages)}</p>

</div>

<div class="card">

<h2>Results</h2>

<table>

<tr>

<th>Page</th>
<th>Title</th>
<th>Status</th>
<th>Risk</th>

</tr>
"""

        for page in pages:

            risk = page.get("risk", "LOW")

            css = risk.lower()

            html += f"""
<tr>

<td>{page['url']}</td>

<td>{page['title']}</td>

<td>{page['status']}</td>

<td class="{css}">{risk}</td>

</tr>
"""

        html += """

</table>

</div>

</body>

</html>

"""

        with open(filename, "w", encoding="utf-8") as file:
            file.write(html)

        return filename