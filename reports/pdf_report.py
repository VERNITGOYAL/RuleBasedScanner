"""
pdf_report.py

Generates a PDF report for the vulnerability scanner.
"""

from datetime import datetime
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib import colors


class PDFReport:

    def generate(
        self,
        target_url,
        pages,
        summary,
        filename="scan_report.pdf",
    ):

        doc = SimpleDocTemplate(filename)

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph(
                "<b>Rule-Based Web Vulnerability Scanner</b>",
                styles["Title"],
            )
        )

        elements.append(
            Paragraph(
                f"Target URL: {target_url}",
                styles["Normal"],
            )
        )

        elements.append(
            Paragraph(
                f"Scan Date: {datetime.now()}",
                styles["Normal"],
            )
        )

        elements.append(Spacer(1, 20))

        data = [
            ["URL", "Title", "Status", "Risk"]
        ]

        for page in pages:

            data.append(
                [
                    page["url"],
                    page["title"],
                    str(page["status"]),
                    page["risk"],
                ]
            )

        table = Table(data)

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                    ("GRID", (0, 0), (-1, -1), 1, colors.black),

                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ]
            )
        )

        elements.append(table)

        elements.append(Spacer(1, 20))

        elements.append(
            Paragraph(
                "<b>Scan Summary</b>",
                styles["Heading2"],
            )
        )

        for key, value in summary.items():

            elements.append(
                Paragraph(
                    f"{key}: {value}",
                    styles["Normal"],
                )
            )

        doc.build(elements)

        return filename