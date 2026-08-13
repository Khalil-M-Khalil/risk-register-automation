"""PDF exporter for Risk Register with professional formatting.

Generates a multi-section PDF report compliant with audit-ready formatting:
  - Executive Summary
  - Risk Register Table
  - Risk Matrix Visualization
  - ISO 27001 Annex A Coverage
  - Treatment Plan for High/Critical Risks
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable,
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.graphics.charts.textlabels import Label

from risk_register.core.register import RiskRegister
from risk_register.core.risk_model import RiskLevel


RISK_COLORS = {
    "Critical": colors.HexColor("#C00000"),
    "High": colors.HexColor("#ED7D31"),
    "Medium": colors.HexColor("#FFC000"),
    "Low": colors.HexColor("#70AD47"),
}

LEVEL_BG = {
    "Critical": colors.HexColor("#FFCCCC"),
    "High": colors.HexColor("#FFE0CC"),
    "Medium": colors.HexColor("#FFF9C4"),
    "Low": colors.HexColor("#E8F5E9"),
}

HEADER_BG = colors.HexColor("#1F4E79")
HEADER_TEXT = colors.white


class PDFExporter:
    """Generate professional PDF report for Risk Register."""

    def __init__(self, report_title: str = "Risk Register Report"):
        self.report_title = report_title
        self.styles = self._setup_styles()

    def _setup_styles(self) -> dict:
        styles = getSampleStyleSheet()

        return {
            "title": ParagraphStyle(
                "ReportTitle", parent=styles["Title"],
                fontSize=22, textColor=HEADER_BG,
                spaceAfter=6, alignment=TA_LEFT,
                fontName="Helvetica-Bold",
            ),
            "subtitle": ParagraphStyle(
                "ReportSubtitle", parent=styles["Normal"],
                fontSize=11, textColor=colors.HexColor("#2E75B6"),
                spaceAfter=4,
            ),
            "section_header": ParagraphStyle(
                "SectionHeader", parent=styles["Heading2"],
                fontSize=14, textColor=HEADER_BG,
                spaceBefore=16, spaceAfter=8,
                fontName="Helvetica-Bold",
                borderPad=4,
            ),
            "table_header": ParagraphStyle(
                "TableHeader", parent=styles["Normal"],
                fontSize=9, textColor=colors.white,
                fontName="Helvetica-Bold",
                alignment=TA_CENTER,
            ),
            "table_cell": ParagraphStyle(
                "TableCell", parent=styles["Normal"],
                fontSize=8, leading=11,
                fontName="Helvetica",
            ),
            "table_cell_center": ParagraphStyle(
                "TableCellCenter", parent=styles["Normal"],
                fontSize=8, leading=11,
                alignment=TA_CENTER,
                fontName="Helvetica",
            ),
            "footer": ParagraphStyle(
                "Footer", parent=styles["Normal"],
                fontSize=8, textColor=colors.grey,
                alignment=TA_CENTER,
            ),
            "kpi_label": ParagraphStyle(
                "KPILabel", parent=styles["Normal"],
                fontSize=9, textColor=colors.HexColor("#666666"),
                alignment=TA_CENTER,
                fontName="Helvetica",
            ),
            "kpi_value": ParagraphStyle(
                "KPIValue", parent=styles["Normal"],
                fontSize=24, textColor=HEADER_BG,
                alignment=TA_CENTER,
                fontName="Helvetica-Bold",
            ),
            "body": ParagraphStyle(
                "BodyText2", parent=styles["Normal"],
                fontSize=10, leading=14, spaceAfter=6,
            ),
            "narrative": ParagraphStyle(
                "Narrative", parent=styles["Normal"],
                fontSize=10, leading=15, spaceAfter=8,
                textColor=colors.HexColor("#333333"),
            ),
        }

    def export_pdf(
        self,
        register: RiskRegister,
        output_path: Optional[Path] = None,
    ) -> str:
        """Generate full PDF report and save to file."""
        output_path = output_path or Path.cwd() / f"risk_register_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            topMargin=25 * mm,
            bottomMargin=25 * mm,
            leftMargin=20 * mm,
            rightMargin=20 * mm,
            title=self.report_title,
            author="Risk Register Automation Tool",
            subject="ISO 27001 Risk Assessment Report",
        )

        story = []

        # ─── Cover / Header ───
        story.append(Paragraph(self.report_title, self.styles["title"]))
        story.append(Paragraph(
            f"ISO 27001:2022 Annex A Compliant Risk Assessment | "
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            self.styles["subtitle"],
        ))
        story.append(Spacer(1, 6 * mm))
        story.append(HRFlowable(width="100%", thickness=2, color=HEADER_BG))
        story.append(Spacer(1, 8 * mm))

        # ─── Executive Summary ───
        story.append(Paragraph("1. Executive Summary", self.styles["section_header"]))
        stats = register.get_statistics()
        story.append(Paragraph(
            f"This report presents the current state of the organization's risk register as of "
            f"{datetime.now().strftime('%B %d, %Y')}. A total of <b>{stats['total_risks']} risks</b> "
            f"have been identified, assessed, and tracked. The assessment methodology follows "
            f"<b>ISO 27005:2022</b> risk assessment guidelines aligned with the <b>ISO 27001:2022 "
            f"Annex A</b> control framework.",
            self.styles["narrative"],
        ))
        story.append(Spacer(1, 3 * mm))

        # KPI cards
        kpi_data = [
            ["Total Risks", str(stats["total_risks"])],
            ["Critical", str(len(stats["critical_risks"]))],
            ["High", str(len(stats["high_risks"]))],
            ["Avg Score", str(stats["average_score"])],
        ]
        kpi_table = Table(kpi_data, colWidths=[8*cm, 8*cm])
        kpi_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F5F5F5")),
            ("BACKGROUND", (1, 0), (1, -1), colors.white),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#666666")),
            ("TEXTCOLOR", (1, 0), (1, -1), HEADER_BG),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica"),
            ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (0, -1), 9),
            ("FONTSIZE", (1, 0), (1, -1), 18),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(kpi_table)
        story.append(Spacer(1, 5 * mm))

        # Methodological narrative
        story.append(Paragraph("Assessment Methodology", self.styles["section_header"]))
        story.append(Paragraph(
            "<b>Risk Scoring:</b> Each risk is evaluated on a 5×5 matrix combining "
            "Likelihood (1-5) and Impact (1-5) as defined by ISO 27005:2022. "
            "The product yields a risk score from 1 to 25, classified as: "
            "Low (1-4), Medium (5-9), High (10-16), Critical (17-25).",
            self.styles["narrative"],
        ))
        story.append(Paragraph(
            "<b>ISO 27001:2022 Mapping:</b> Each risk is mapped to relevant "
            "Annex A controls (93 controls across 14 themes). This enables "
            "audit-ready traceability between identified risks and applicable controls.",
            self.styles["narrative"],
        ))
        story.append(Paragraph(
            "<b>Risk Treatment:</b> Risks exceeding the Medium threshold require "
            "a documented treatment plan (Avoid, Transfer, Mitigate, or Accept) "
            "with assigned ownership and review timeline.",
            self.styles["narrative"],
        ))
        story.append(PageBreak())

        # ─── Risk Register Table ───
        story.append(Paragraph("2. Risk Register", self.styles["section_header"]))
        story.append(Paragraph(
            f"The following table presents all {stats['total_risks']} identified risks "
            f"with their assessment scores, levels, and ISO 27001 control mappings.",
            self.styles["body"],
        ))
        story.append(Spacer(1, 4 * mm))

        risks = register.get_all()
        if risks:
            headers = [
                Paragraph("ID", self.styles["table_header"]),
                Paragraph("Category", self.styles["table_header"]),
                Paragraph("Title", self.styles["table_header"]),
                Paragraph("L", self.styles["table_header"]),
                Paragraph("I", self.styles["table_header"]),
                Paragraph("Score", self.styles["table_header"]),
                Paragraph("Level", self.styles["table_header"]),
                Paragraph("Controls", self.styles["table_header"]),
                Paragraph("Treatment", self.styles["table_header"]),
            ]

            data = [headers]
            for risk in risks:
                data.append([
                    Paragraph(risk.risk_id, self.styles["table_cell_center"]),
                    Paragraph(risk.category, self.styles["table_cell"]),
                    Paragraph(risk.title, self.styles["table_cell"]),
                    Paragraph(str(risk.likelihood), self.styles["table_cell_center"]),
                    Paragraph(str(risk.impact), self.styles["table_cell_center"]),
                    Paragraph(str(risk.risk_score), self.styles["table_cell_center"]),
                    Paragraph(risk.risk_level.value, self.styles["table_cell_center"]),
                    Paragraph(", ".join(risk.iso_controls) if risk.iso_controls else "—", self.styles["table_cell"]),
                    Paragraph(risk.treatment.value, self.styles["table_cell_center"]),
                ])

            col_widths = [2.5*cm, 2.5*cm, 4*cm, 0.8*cm, 0.8*cm, 1.2*cm, 1.8*cm, 3.5*cm, 2*cm]

            table = Table(data, colWidths=col_widths, repeatRows=1)
            style_cmds = [
                ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]

            # Color-code level column
            for i, risk in enumerate(risks, 1):
                level = risk.risk_level.value
                style_cmds.append(("BACKGROUND", (6, i), (6, i), LEVEL_BG.get(level, colors.white)))
                style_cmds.append(("TEXTCOLOR", (6, i), (6, i), RISK_COLORS.get(level, colors.black)))
                style_cmds.append(("FONTNAME", (6, i), (6, i), "Helvetica-Bold"))

                # Highlight critical rows
                if risk.risk_level == RiskLevel.CRITICAL:
                    style_cmds.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#FFF0F0")))

            table.setStyle(TableStyle(style_cmds))
            story.append(table)
        else:
            story.append(Paragraph("No risks found in the register.", self.styles["body"]))

        story.append(PageBreak())

        # ─── Risk Matrix ───
        story.append(Paragraph("3. Risk Assessment Matrix", self.styles["section_header"]))
        story.append(Paragraph(
            "The 5×5 risk matrix below visualizes the distribution of risks across "
            "Likelihood × Impact dimensions. Each cell indicates the number of risks "
            "falling into that category.",
            self.styles["body"],
        ))
        story.append(Spacer(1, 5 * mm))

        # Draw matrix as a table with colored cells
        matrix_data = []
        impact_labels = ["1 — Negligible", "2 — Minor", "3 — Moderate", "4 — Major", "5 — Severe"]

        # Header row
        matrix_data.append([
            Paragraph("Likelihood ↓ / Impact →", self.styles["table_header"]),
        ] + [Paragraph(label, self.styles["table_header"]) for label in impact_labels])

        likelihood_labels = ["5 — Almost Certain", "4 — Likely", "3 — Possible", "2 — Unlikely", "1 — Rare"]

        for likelihood_val in range(5, 0, -1):
            row = [Paragraph(likelihood_labels[5 - likelihood_val], self.styles["table_cell_center"])]
            for impact_val in range(1, 6):
                key = (likelihood_val, impact_val)
                count = sum(1 for r in risks if r.likelihood == likelihood_val and r.impact == impact_val)

                # Determine color based on score
                score = likelihood_val * impact_val
                if score <= 4:
                    bg = colors.HexColor("#E8F5E9")
                    fg = colors.HexColor("#2E7D32")
                elif score <= 9:
                    bg = colors.HexColor("#FFF9C4")
                    fg = colors.HexColor("#F57F17")
                elif score <= 16:
                    bg = colors.HexColor("#FFEBEE")
                    fg = colors.HexColor("#C62828")
                else:
                    bg = colors.HexColor("#FFCDD2")
                    fg = colors.HexColor("#B71C1C")

                text = f"Score: {score}<br/>Level: {'Critical' if score > 16 else ('High' if score > 9 else ('Medium' if score > 4 else 'Low'))}<br/>Count: {count}"
                row.append(Paragraph(text, ParagraphStyle(
                    "MatrixCell", parent=self.styles["table_cell_center"],
                    textColor=fg, fontSize=8, leading=10,
                    backColor=bg,
                )))
            matrix_data.append(row)

        matrix_table = Table(matrix_data, colWidths=[3.5*cm] + [2.5*cm]*5)
        matrix_style = [
            ("GRID", (0, 0), (-1, -1), 1, colors.white),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]
        # Header background
        matrix_style.append(("BACKGROUND", (0, 0), (0, 0), HEADER_BG))
        matrix_style.append(("TEXTCOLOR", (0, 0), (0, 0), colors.white))
        for col in range(1, 6):
            matrix_style.append(("BACKGROUND", (col, 0), (col, 0), HEADER_BG))
            matrix_style.append(("TEXTCOLOR", (col, 0), (col, 0), colors.white))

        matrix_table.setStyle(TableStyle(matrix_style))
        story.append(matrix_table)
        story.append(Spacer(1, 6 * mm))

        # Legend
        story.append(Paragraph("<b>Risk Level Thresholds (ISO 27005:2022):</b>", self.styles["body"]))
        thresholds = [
            ("Low (1-4)", "Accept — monitor periodically", colors.HexColor("#E8F5E9")),
            ("Medium (5-9)", "Mitigate — action plan required", colors.HexColor("#FFF9C4")),
            ("High (10-16)", "Mitigate urgently — escalation required", colors.HexColor("#FFEBEE")),
            ("Critical (17-25)", "Immediate action — executive escalation", colors.HexColor("#FFCDD2")),
        ]
        for level, guidance, color in thresholds:
            story.append(Paragraph(
                f"• <b>{level}:</b> {guidance}",
                ParagraphStyle("Thr", parent=self.styles["body"], leftIndent=12),
            ))
        story.append(PageBreak())

        # ─── ISO 27001 Control Coverage ───
        story.append(Paragraph("4. ISO 27001:2022 Annex A — Control Coverage", self.styles["section_header"]))
        story.append(Paragraph(
            "This section maps identified risks to applicable ISO 27001:2022 Annex A controls. "
            "This mapping enables audit-ready traceability and demonstrates that risk management "
            "is integrated with the organization's information security control framework.",
            self.styles["body"],
        ))
        story.append(Spacer(1, 4 * mm))

        # Collect unique controls from risks
        mapped_control_refs = set()
        for risk in risks:
            for ctrl in risk.iso_controls:
                mapped_control_refs.add(ctrl)

        # Group by theme
        from risk_register.core.iso27001_mapper import ISO27001Mapper
        mapper = ISO27001Mapper()

        iso_headers = [
            Paragraph("Control Ref", self.styles["table_header"]),
            Paragraph("Control Title", self.styles["table_header"]),
            Paragraph("Theme", self.styles["table_header"]),
            Paragraph("Mapped", self.styles["table_header"]),
        ]
        iso_data = [iso_headers]

        for theme in mapper.get_all_themes():
            theme_controls = mapper.get_controls_by_theme(theme)
            first_row = True
            for ctrl in theme_controls:
                is_mapped = ctrl.ref in mapped_control_refs
                iso_data.append([
                    Paragraph(ctrl.ref, self.styles["table_cell_center"]),
                    Paragraph(ctrl.title, self.styles["table_cell"]),
                    Paragraph(theme.replace("A.", ""), self.styles["table_cell_center"]),
                    Paragraph("✓ Yes" if is_mapped else "—", self.styles["table_cell_center"]),
                ])

        iso_table = Table(iso_data, colWidths=[2*cm, 5*cm, 1.5*cm, 1.5*cm], repeatRows=1)
        iso_style = [
            ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]

        # Color mapped rows
        for i, row_data in enumerate(iso_data[1:], 1):
            is_mapped_text = row_data[3].text if hasattr(row_data[3], 'text') else ""
            if "Yes" in str(is_mapped_text):
                iso_style.append(("BACKGROUND", (3, i), (3, i), colors.HexColor("#C6EFCE")))

        iso_table.setStyle(TableStyle(iso_style))
        story.append(iso_table)

        story.append(PageBreak())

        # ─── Treatment Plan ───
        story.append(Paragraph("5. Risk Treatment Plan — High & Critical Risks", self.styles["section_header"]))
        story.append(Paragraph(
            "The following treatment plan addresses all risks classified as High or Critical. "
            "Each entry includes the selected treatment strategy, mitigation actions, "
            "assigned owner, and required timeline.",
            self.styles["body"],
        ))
        story.append(Spacer(1, 4 * mm))

        high_critical = [
            r for r in risks
            if r.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL)
        ]

        if high_critical:
            treatment_headers = [
                Paragraph("Risk ID", self.styles["table_header"]),
                Paragraph("Title", self.styles["table_header"]),
                Paragraph("Level", self.styles["table_header"]),
                Paragraph("Score", self.styles["table_header"]),
                Paragraph("Treatment", self.styles["table_header"]),
                Paragraph("Mitigation Plan", self.styles["table_header"]),
                Paragraph("Owner", self.styles["table_header"]),
                Paragraph("Review Date", self.styles["table_header"]),
            ]

            treatment_data = [treatment_headers]
            for risk in high_critical:
                review_str = risk.review_date.strftime('%Y-%m-%d') if risk.review_date else "Not Set"
                treatment_data.append([
                    Paragraph(risk.risk_id, self.styles["table_cell_center"]),
                    Paragraph(risk.title, self.styles["table_cell"]),
                    Paragraph(risk.risk_level.value, self.styles["table_cell_center"]),
                    Paragraph(str(risk.risk_score), self.styles["table_cell_center"]),
                    Paragraph(risk.treatment.value, self.styles["table_cell_center"]),
                    Paragraph(risk.mitigation_plan or "—", self.styles["table_cell"]),
                    Paragraph(risk.owner, self.styles["table_cell"]),
                    Paragraph(review_str, self.styles["table_cell_center"]),
                ])

            treatment_table = Table(treatment_data, colWidths=[2.5*cm, 3*cm, 1.5*cm, 1*cm, 1.5*cm, 4*cm, 2*cm, 1.8*cm], repeatRows=1)
            treatment_style = [
                ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]

            for i, risk in enumerate(high_critical, 1):
                level = risk.risk_level.value
                treatment_style.append(("BACKGROUND", (2, i), (2, i), LEVEL_BG.get(level, colors.white)))
                treatment_style.append(("TEXTCOLOR", (2, i), (2, i), RISK_COLORS.get(level, colors.black)))

            treatment_table.setStyle(TableStyle(treatment_style))
            story.append(treatment_table)
        else:
            story.append(Paragraph(
                "No High or Critical risks currently identified. "
                "All risks are within acceptable thresholds.",
                self.styles["body"],
            ))

        story.append(Spacer(1, 15 * mm))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CCCCCC")))
        story.append(Spacer(1, 3 * mm))
        story.append(Paragraph(
            f"<i>Report generated by Risk Register Automation Tool v1.0.0 "
            f"| {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
            f"| Classification: Internal Use Only</i>",
            self.styles["footer"],
        ))

        doc.build(story)
        return str(output_path)
