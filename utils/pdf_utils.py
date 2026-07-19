"""
Shared PDF generation helpers built on ReportLab. Used by
report_generator.py (session report) and roadmap_generator.py
(roadmap export).
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib import colors


def build_pdf(filepath: str, title: str, sections: list[dict]):
    """
    Generic PDF builder.

    Args:
        filepath: output path, e.g. "data/reports/session_12.pdf"
        title: document title shown at the top.
        sections: list of dicts, each either:
            {"heading": str, "paragraphs": [str, ...]}
            {"heading": str, "table": [[row1], [row2], ...]}
    """
    doc = SimpleDocTemplate(filepath, pagesize=A4,
                             topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle", parent=styles["Title"], fontSize=20, spaceAfter=20
    )
    heading_style = ParagraphStyle(
        "HeadingStyle", parent=styles["Heading2"], spaceBefore=14, spaceAfter=8
    )

    story = [Paragraph(title, title_style), Spacer(1, 0.5 * cm)]

    for section in sections:
        story.append(Paragraph(section["heading"], heading_style))

        if "paragraphs" in section:
            for p in section["paragraphs"]:
                story.append(Paragraph(p, styles["BodyText"]))
                story.append(Spacer(1, 0.2 * cm))

        if "table" in section:
            table = Table(section["table"], hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2b2b2b")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]))
            story.append(table)
            story.append(Spacer(1, 0.3 * cm))

    doc.build(story)
    return filepath