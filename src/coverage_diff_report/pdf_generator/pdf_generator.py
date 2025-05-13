
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from src.coverage_diff_report.diff_analyzer.diff_analyzer import DiffCoverageResult


def generate_pdf_report(results: list[DiffCoverageResult], output_path: str) -> None:
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    title = Paragraph("PR Diff Coverage Report", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    if not results:
        elements.append(Paragraph("✅ No changes found in diff.", styles["Normal"]))
    else:
        data = [["File", "Line", "Before", "After"]]
        for entry in results:
            row = [
                entry["file"],
                str(entry["line"]),
                entry["before"],
                entry["after"],
            ]
            data.append(row)

        table = Table(data, colWidths=[200, 50, 100, 100])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ],
            ),
        )
        elements.append(table)

    doc.build(elements)
