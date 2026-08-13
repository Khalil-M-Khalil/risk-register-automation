"""Excel exporter for Risk Register with professional formatting.

Generates multi-sheet Excel workbook:
  - Sheet 1: Risk Register (all risks with full details)
  - Sheet 2: Risk Matrix (5x5 heatmap)
  - Sheet 3: Statistics & Summary
  - Sheet 4: ISO 27001 Annex A Control Mapping
  - Sheet 5: Risk Treatment Plan
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

from openpyxl import Workbook
from openpyxl.styles import (
    Font, PatternFill, Alignment, Border, Side
)
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.utils import get_column_letter

from risk_register.core.register import RiskRegister
from risk_register.core.risk_model import RiskLevel
from risk_register.core.iso27001_mapper import ISO_27001_CONTROLS


# ─── ISO 27001 Theme Colors ───
THEME_COLORS = {
    "A.5 Policies for information security": "1F4E79",
    "A.6 Organisation of information security": "2E75B6",
    "A.7 Human resource security": "548235",
    "A.8 Asset management": "BF8F00",
    "A.9 Access control": "C55A11",
    "A.10 Cryptography": "7030A0",
    "A.11 Physical and environmental security": "375623",
    "A.12 Operations security": "843C0C",
    "A.13 Communications security": "00B0F0",
    "A.14 System acquisition, development and maintenance": "002060",
    "A.15 Supplier relationships": "A5A5A5",
    "A.16 Information security incident management": "FF0000",
    "A.17 Information security aspects of business continuity management": "4472C4",
    "A.18 Compliance": "70AD47",
}

RISK_LEVEL_COLORS = {
    "Critical": "C00000",
    "High": "ED7D31",
    "Medium": "FFC000",
    "Low": "70AD47",
}

RISK_LEVEL_FILLS = {
    "Critical": PatternFill(start_color="C00000", end_color="C00000", fill_type="solid"),
    "High": PatternFill(start_color="ED7D31", end_color="ED7D31", fill_type="solid"),
    "Medium": PatternFill(start_color="FFC000", end_color="FFC000", fill_type="solid"),
    "Low": PatternFill(start_color="70AD47", end_color="70AD47", fill_type="solid"),
}


class ExcelExporter:
    """Professional Excel exporter for Risk Register."""

    def __init__(self, workbook_title: str = "Risk Register"):
        self.workbook = Workbook()
        self.workbook.title = workbook_title
        self._styles = self._setup_styles()

    def _setup_styles(self) -> dict:
        """Set up reusable cell styles."""
        return {
            "header_font": Font(name="Calibri", size=11, bold=True, color="FFFFFF"),
            "header_fill": PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid"),
            "title_font": Font(name="Calibri", size=14, bold=True, color="1F4E79"),
            "subtitle_font": Font(name="Calibri", size=11, bold=True, color="2E75B6"),
            "normal_font": Font(name="Calibri", size=10),
            "bold_font": Font(name="Calibri", size=10, bold=True),
            "thin_border": Border(
                left=Side(style="thin", color="B0B0B0"),
                right=Side(style="thin", color="B0B0B0"),
                top=Side(style="thin", color="B0B0B0"),
                bottom=Side(style="thin", color="B0B0B0"),
            ),
            "center_align": Alignment(horizontal="center", vertical="center", wrap_text=True),
            "left_align": Alignment(horizontal="left", vertical="center", wrap_text=True),
        }

    def _style_header_row(self, ws, row: int, num_cols: int):
        """Apply header styling to a row."""
        style = self._styles
        for col in range(1, num_cols + 1):
            cell = ws.cell(row=row, column=col)
            cell.font = style["header_font"]
            cell.fill = style["header_fill"]
            cell.alignment = style["center_align"]
            cell.border = style["thin_border"]

    def _auto_width(self, ws, min_width: int = 10, max_width: int = 50):
        """Auto-fit column widths."""
        for col_cells in ws.columns:
            max_len = min_width
            col_letter = get_column_letter(col_cells[0].column)
            for cell in col_cells:
                if cell.value:
                    lines = str(cell.value).split("\n")
                    for line in lines:
                        max_len = max(max_len, len(line))
            ws.column_dimensions[col_letter].width = min(max_len + 2, max_width)

    def export_risk_register(
        self,
        register: RiskRegister,
        output_path: Optional[Path] = None,
    ) -> str:
        """Generate full Excel report and save to file."""
        # Sheet 1: Risk Register
        ws1 = self.workbook.active
        ws1.title = "Risk Register"
        self._write_risk_register_sheet(ws1, register)

        # Sheet 2: Risk Matrix
        ws2 = self.workbook.create_sheet("Risk Matrix")
        self._write_risk_matrix_sheet(ws2, register)

        # Sheet 3: Statistics
        ws3 = self.workbook.create_sheet("Statistics")
        self._write_statistics_sheet(ws3, register)

        # Sheet 4: ISO Controls
        ws4 = self.workbook.create_sheet("ISO 27001 Controls")
        self._write_iso_controls_sheet(ws4, register)

        # Sheet 5: Treatment Plan
        ws5 = self.workbook.create_sheet("Treatment Plan")
        self._write_treatment_plan_sheet(ws5, register)

        # Freeze panes
        ws1.freeze_panes = "A2"
        ws2.freeze_panes = "B2"
        ws3.freeze_panes = "A2"

        output_path = output_path or Path.cwd() / f"risk_register_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        self.workbook.save(str(output_path))
        return str(output_path)

    def _write_risk_register_sheet(self, ws, register: RiskRegister):
        """Write full risk register data."""
        styles = self._styles

        # Title
        ws.merge_cells("A1:L1")
        ws["A1"] = "RISK REGISTER"
        ws["A1"].font = styles["title_font"]
        ws["A1"].alignment = Alignment(horizontal="left", vertical="center")

        ws.merge_cells("A2:L2")
        ws["A2"] = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  Total Risks: {len(register.get_all())}"
        ws["A2"].font = styles["subtitle_font"]

        # Headers
        headers = [
            "Risk ID", "Category", "Title", "Description", "Asset",
            "Owner", "Likelihood (1-5)", "Impact (1-5)", "Risk Score (LxI)",
            "Risk Level", "ISO 27001 Controls", "Treatment",
        ]
        header_row = 4
        for col, header in enumerate(headers, 1):
            ws.cell(row=header_row, column=col, value=header)
        self._style_header_row(ws, header_row, len(headers))

        # Data
        row = header_row + 1
        for risk in register.get_all():
            ws.cell(row=row, column=1, value=risk.risk_id)
            ws.cell(row=row, column=2, value=risk.category)
            ws.cell(row=row, column=3, value=risk.title)
            ws.cell(row=row, column=4, value=risk.description)
            ws.cell(row=row, column=5, value=risk.asset)
            ws.cell(row=row, column=6, value=risk.owner)
            ws.cell(row=row, column=7, value=risk.likelihood)
            ws.cell(row=row, column=8, value=risk.impact)
            ws.cell(row=row, column=9, value=risk.risk_score)
            ws.cell(row=row, column=10, value=risk.risk_level.value)
            ws.cell(row=row, column=11, value=", ".join(risk.iso_controls))
            ws.cell(row=row, column=12, value=risk.treatment.value)

            # Style cells
            for col in range(1, len(headers) + 1):
                cell = ws.cell(row=row, column=col)
                cell.font = styles["normal_font"]
                cell.border = styles["thin_border"]
                cell.alignment = styles["left_align"]

            # Color-code risk level
            level_cell = ws.cell(row=row, column=10)
            level_fill = RISK_LEVEL_FILLS.get(risk.risk_level.value)
            if level_fill:
                level_cell.fill = level_fill
                level_cell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")

            # Color-score cell
            score_cell = ws.cell(row=row, column=9)
            if risk.risk_level == RiskLevel.CRITICAL:
                score_cell.fill = PatternFill(start_color="FFCCCC", end_color="FFCCCC", fill_type="solid")
            elif risk.risk_level == RiskLevel.HIGH:
                score_cell.fill = PatternFill(start_color="FFE0CC", end_color="FFE0CC", fill_type="solid")

            row += 1

        self._auto_width(ws, min_width=12, max_width=40)
        ws.column_dimensions["D"].width = 50
        ws.column_dimensions["K"].width = 45

    def _write_risk_matrix_sheet(self, ws, register: RiskRegister):
        """Write 5x5 risk matrix heatmap."""
        styles = self._styles

        ws.merge_cells("A1:G1")
        ws["A1"] = "RISK ASSESSMENT MATRIX (Likelihood x Impact)"
        ws["A1"].font = styles["title_font"]

        ws.merge_cells("A2:G2")
        ws["A2"] = "ISO 27005 / ISO 31000 aligned risk matrix"
        ws["A2"].font = styles["subtitle_font"]

        impact_labels = ["Negligible (1)", "Minor (2)", "Moderate (3)", "Major (4)", "Severe (5)"]
        likelihood_labels = [
            "Almost Certain (5)", "Likely (4)", "Possible (3)", "Unlikely (2)", "Rare (1)"
        ]

        start_row = 5
        ws.cell(row=start_row - 1, column=1, value="Likelihood / Impact")
        ws.cell(row=start_row - 1, column=1).font = styles["bold_font"]
        ws.cell(row=start_row - 1, column=1).alignment = styles["center_align"]

        for col, label in enumerate(impact_labels, 2):
            ws.cell(row=start_row - 1, column=col, value=label)
            ws.cell(row=start_row - 1, column=col).font = styles["header_font"]
            ws.cell(row=start_row - 1, column=col).fill = styles["header_fill"]
            ws.cell(row=start_row - 1, column=col).alignment = styles["center_align"]
            ws.cell(row=start_row - 1, column=col).border = styles["thin_border"]

        # Matrix data
        risks = register.get_all()
        matrix = {}
        for risk in risks:
            key = (risk.likelihood, risk.impact)
            matrix[key] = matrix.get(key, 0) + 1

        for row_idx, likelihood_val in enumerate(range(5, 0, -1)):
            row = start_row + row_idx
            ws.cell(row=row, column=1, value=likelihood_labels[row_idx])
            ws.cell(row=row, column=1).font = styles["bold_font"]
            ws.cell(row=row, column=1).fill = PatternFill(start_color="D9E2F3", end_color="D9E2F3", fill_type="solid")
            ws.cell(row=row, column=1).border = styles["thin_border"]
            ws.cell(row=row, column=1).alignment = styles["center_align"]

            for col_idx, impact_val in enumerate(range(1, 6)):
                col = col_idx + 2
                key = (likelihood_val, impact_val)
                count = matrix.get(key, 0)

                score = likelihood_val * impact_val
                if score <= 4:
                    level = "Low"
                    color = "C6EFCE"
                    font_color = "006100"
                elif score <= 9:
                    level = "Medium"
                    color = "FFEB9C"
                    font_color = "9C6500"
                elif score <= 16:
                    level = "High"
                    color = "FFC7CE"
                    font_color = "9C0006"
                else:
                    level = "Critical"
                    color = "FF9999"
                    font_color = "7C0000"

                cell = ws.cell(row=row, column=col, value=f"Score: {score}\nLevel: {level}\nRisks: {count}")
                cell.fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
                cell.font = Font(name="Calibri", size=9, color=font_color)
                cell.alignment = styles["center_align"]
                cell.border = styles["thin_border"]

        # Legend
        legend_row = start_row + 7
        ws.merge_cells(f"A{legend_row}:G{legend_row}")
        ws.cell(row=legend_row, column=1, value="LEGEND").font = styles["subtitle_font"]

        legend_items = [
            ("Low (1-4)", "C6EFCE", "006100", "Accept - monitor periodically"),
            ("Medium (5-9)", "FFEB9C", "9C6500", "Mitigate - action plan required"),
            ("High (10-16)", "FFC7CE", "9C0006", "Mitigate urgently - escalation required"),
            ("Critical (17-25)", "FF9999", "7C0000", "Immediate action - executive escalation"),
        ]
        for i, (label, bg, fg, desc) in enumerate(legend_items):
            r = legend_row + 1 + i
            ws.cell(row=r, column=1, value=label)
            ws.cell(row=r, column=1).fill = PatternFill(start_color=bg, end_color=bg, fill_type="solid")
            ws.cell(row=r, column=1).font = Font(name="Calibri", size=10, color=fg, bold=True)
            ws.cell(row=r, column=1).alignment = styles["center_align"]
            ws.cell(row=r, column=1).border = styles["thin_border"]
            ws.merge_cells(f"B{r}:G{r}")
            ws.cell(row=r, column=2, value=desc).font = styles["normal_font"]

        self._auto_width(ws, min_width=15, max_width=30)

    def _write_statistics_sheet(self, ws, register: RiskRegister):
        """Write statistics and summary dashboard."""
        styles = self._styles
        stats = register.get_statistics()

        ws.merge_cells("A1:F1")
        ws["A1"] = "RISK REGISTER - STATISTICS & SUMMARY"
        ws["A1"].font = styles["title_font"]

        ws.merge_cells("A2:F2")
        ws["A2"] = f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        ws["A2"].font = styles["subtitle_font"]

        # KPIs
        kpi_start = 4
        kpis = [
            ("Total Risks", stats["total_risks"], "1F4E79"),
            ("Critical Risks", len(stats["critical_risks"]), "C00000"),
            ("High Risks", len(stats["high_risks"]), "ED7D31"),
            ("Average Risk Score", stats["average_score"], "2E75B6"),
            ("Open Risks", stats["status_distribution"]["Open"], "70AD47"),
        ]

        for i, (label, value, color) in enumerate(kpis):
            col = i * 2 + 1
            ws.cell(row=kpi_start, column=col, value=label)
            ws.cell(row=kpi_start, column=col).font = Font(name="Calibri", size=10, color=color, bold=True)
            ws.cell(row=kpi_start, column=col).alignment = styles["center_align"]
            ws.cell(row=kpi_start, column=col).border = styles["thin_border"]

            ws.cell(row=kpi_start + 1, column=col, value=value)
            ws.cell(row=kpi_start + 1, column=col).font = Font(name="Calibri", size=20, bold=True, color=color)
            ws.cell(row=kpi_start + 1, column=col).alignment = styles["center_align"]
            ws.cell(row=kpi_start + 1, column=col).border = styles["thin_border"]

        # Level distribution table
        level_row = kpi_start + 4
        ws.merge_cells(f"A{level_row}:F{level_row}")
        ws.cell(row=level_row, column=1, value="Risk Distribution by Level").font = styles["subtitle_font"]

        level_headers = ["Risk Level", "Count", "Percentage", "Action Required"]
        for col, h in enumerate(level_headers, 1):
            ws.cell(row=level_row + 1, column=col, value=h)
        self._style_header_row(ws, level_row + 1, len(level_headers))

        level_actions = {
            "Critical": "Immediate executive escalation",
            "High": "Urgent mitigation plan required",
            "Medium": "Action plan with timeline",
            "Low": "Monitor and accept",
        }

        # Write level data
        level_data_start = level_row + 2
        levels_ordered = ["Critical", "High", "Medium", "Low"]
        level_data_end = level_data_start + len(levels_ordered) - 1

        for i, level in enumerate(levels_ordered):
            row = level_data_start + i
            count = stats["by_level"].get(level, 0)
            pct = (count / stats["total_risks"] * 100) if stats["total_risks"] else 0

            ws.cell(row=row, column=1, value=level)
            ws.cell(row=row, column=1).font = Font(name="Calibri", size=10, bold=True)
            ws.cell(row=row, column=1).fill = RISK_LEVEL_FILLS.get(level, PatternFill())
            ws.cell(row=row, column=1).font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
            ws.cell(row=row, column=1).alignment = styles["center_align"]
            ws.cell(row=row, column=1).border = styles["thin_border"]

            ws.cell(row=row, column=2, value=count)
            ws.cell(row=row, column=2).alignment = styles["center_align"]
            ws.cell(row=row, column=2).border = styles["thin_border"]

            ws.cell(row=row, column=3, value=f"{pct:.1f}%")
            ws.cell(row=row, column=3).alignment = styles["center_align"]
            ws.cell(row=row, column=3).border = styles["thin_border"]

            ws.cell(row=row, column=4, value=level_actions.get(level, ""))
            ws.cell(row=row, column=4).font = styles["normal_font"]
            ws.cell(row=row, column=4).border = styles["thin_border"]

        # Add chart for level distribution
        chart = BarChart()
        chart.type = "col"
        chart.title = "Risk Level Distribution"
        chart.y_axis.title = "Number of Risks"
        chart.style = 10

        # Data for chart: column 2 (Count) from header to last data row
        data_ref = Reference(ws, min_col=2, min_row=level_row + 1, max_row=level_data_end)
        cats_ref = Reference(ws, min_col=1, min_row=level_data_start, max_row=level_data_end)

        chart.add_data(data_ref, titles_from_data=True)
        chart.set_categories(cats_ref)
        chart.legend = None

        # Set chart series color
        if chart.series:
            chart.series[0].graphicalProperties.solidFill = "1F4E79"

        ws.add_chart(chart, "B" + str(level_row - 2))

        # Category distribution
        cat_row = level_row + 10
        ws.merge_cells(f"A{cat_row}:F{cat_row}")
        ws.cell(row=cat_row, column=1, value="Risk Distribution by Category").font = styles["subtitle_font"]

        cat_headers = ["Category", "Count", "Avg Score"]
        for col, h in enumerate(cat_headers, 1):
            ws.cell(row=cat_row + 1, column=col, value=h)
        self._style_header_row(ws, cat_row + 1, len(cat_headers))

        row = cat_row + 2
        for cat, count in sorted(stats["by_category"].items(), key=lambda x: -x[1]):
            risks_in_cat = [r for r in register.get_all() if r.category == cat]
            avg = sum(r.risk_score for r in risks_in_cat) / len(risks_in_cat) if risks_in_cat else 0

            ws.cell(row=row, column=1, value=cat).font = styles["normal_font"]
            ws.cell(row=row, column=1).border = styles["thin_border"]
            ws.cell(row=row, column=2, value=count).alignment = styles["center_align"]
            ws.cell(row=row, column=2).border = styles["thin_border"]
            ws.cell(row=row, column=3, value=round(avg, 1)).alignment = styles["center_align"]
            ws.cell(row=row, column=3).border = styles["thin_border"]
            row += 1

        # Status distribution
        status_row = cat_row + 10
        ws.merge_cells(f"A{status_row}:F{status_row}")
        ws.cell(row=status_row, column=1, value="Status Distribution").font = styles["subtitle_font"]

        status_headers = ["Status", "Count", "Percentage"]
        for col, h in enumerate(status_headers, 1):
            ws.cell(row=status_row + 1, column=col, value=h)
        self._style_header_row(ws, status_row + 1, len(status_headers))

        total = stats["total_risks"]
        row = status_row + 2
        for status, count in stats["status_distribution"].items():
            pct = (count / total * 100) if total else 0
            ws.cell(row=row, column=1, value=status).font = styles["normal_font"]
            ws.cell(row=row, column=1).border = styles["thin_border"]
            ws.cell(row=row, column=2, value=count).alignment = styles["center_align"]
            ws.cell(row=row, column=2).border = styles["thin_border"]
            ws.cell(row=row, column=3, value=f"{pct:.1f}%").alignment = styles["center_align"]
            ws.cell(row=row, column=3).border = styles["thin_border"]
            row += 1

        self._auto_width(ws, min_width=15, max_width=40)

    def _write_iso_controls_sheet(self, ws, register: RiskRegister):
        """Write ISO 27001 Annex A controls and their coverage."""
        from risk_register.core.iso27001_mapper import ISO27001Mapper

        styles = self._styles
        mapper = ISO27001Mapper()

        ws.merge_cells("A1:F1")
        ws["A1"] = "ISO 27001:2022 Annex A - Control Coverage Map"
        ws["A1"].font = styles["title_font"]

        ws.merge_cells("A2:F2")
        ws["A2"] = f"Total Annex A controls: {len(mapper.controls)}"
        ws["A2"].font = styles["subtitle_font"]

        # Collect mapped controls
        mapped_controls = set()
        for risk in register.get_all():
            for ctrl in risk.iso_controls:
                mapped_controls.add(ctrl)

        headers = ["Control Ref", "Title", "Theme", "Description", "Mapped to Risks", "Status"]
        header_row = 4
        for col, h in enumerate(headers, 1):
            ws.cell(row=header_row, column=col, value=h)
        self._style_header_row(ws, header_row, len(headers))

        row = header_row + 1
        for ctrl in ISO_27001_CONTROLS:
            is_mapped = ctrl.ref in mapped_controls
            ws.cell(row=row, column=1, value=ctrl.ref)
            ws.cell(row=row, column=2, value=ctrl.title)
            ws.cell(row=row, column=3, value=ctrl.theme)
            ws.cell(row=row, column=4, value=ctrl.description[:80] + "..." if len(ctrl.description) > 80 else ctrl.description)
            ws.cell(row=row, column=5, value="Yes" if is_mapped else "-")
            ws.cell(row=row, column=6, value="Covered" if is_mapped else "Not Covered")

            for col in range(1, len(headers) + 1):
                cell = ws.cell(row=row, column=col)
                cell.font = styles["normal_font"]
                cell.border = styles["thin_border"]
                cell.alignment = styles["left_align"]

            if is_mapped:
                ws.cell(row=row, column=5).font = Font(name="Calibri", size=10, color="006100", bold=True)
                ws.cell(row=row, column=6).font = Font(name="Calibri", size=10, color="006100", bold=True)
                ws.cell(row=row, column=5).fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
                ws.cell(row=row, column=6).fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")

            # Theme coloring
            theme_color = THEME_COLORS.get(ctrl.theme, "FFFFFF")
            ws.cell(row=row, column=3).fill = PatternFill(start_color=theme_color, end_color=theme_color, fill_type="solid")
            ws.cell(row=row, column=3).font = Font(name="Calibri", size=9, color="FFFFFF" if theme_color not in ["A5A5A5", "000000"] else "000000")

            row += 1

        self._auto_width(ws, min_width=12, max_width=45)
        ws.column_dimensions["B"].width = 45
        ws.column_dimensions["D"].width = 60

    def _write_treatment_plan_sheet(self, ws, register: RiskRegister):
        """Write risk treatment plan for high/critical risks."""
        styles = self._styles

        high_critical = [
            r for r in register.get_all()
            if r.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL)
        ]

        ws.merge_cells("A1:G1")
        ws["A1"] = "RISK TREATMENT PLAN - High & Critical Risks"
        ws["A1"].font = styles["title_font"]

        ws.merge_cells("A2:G2")
        ws["A2"] = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  Count: {len(high_critical)}"
        ws["A2"].font = styles["subtitle_font"]

        headers = [
            "Risk ID", "Title", "Risk Level", "Risk Score",
            "Treatment Option", "Mitigation Plan", "Owner / Deadline"
        ]
        header_row = 4
        for col, h in enumerate(headers, 1):
            ws.cell(row=header_row, column=col, value=h)
        self._style_header_row(ws, header_row, len(headers))

        row = header_row + 1
        for risk in high_critical:
            ws.cell(row=row, column=1, value=risk.risk_id)
            ws.cell(row=row, column=2, value=risk.title)
            ws.cell(row=row, column=3, value=risk.risk_level.value)
            ws.cell(row=row, column=4, value=risk.risk_score)
            ws.cell(row=row, column=5, value=risk.treatment.value)
            ws.cell(row=row, column=6, value=risk.mitigation_plan)
            ws.cell(row=row, column=7, value=f"{risk.owner}  |  Review: {risk.review_date.strftime('%Y-%m-%d') if risk.review_date else 'N/A'}")

            for col in range(1, len(headers) + 1):
                cell = ws.cell(row=row, column=col)
                cell.font = styles["normal_font"]
                cell.border = styles["thin_border"]
                cell.alignment = styles["left_align"]

            # Level coloring
            level_fill = RISK_LEVEL_FILLS.get(risk.risk_level.value)
            if level_fill:
                ws.cell(row=row, column=3).fill = level_fill
                ws.cell(row=row, column=3).font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")

            row += 1

        self._auto_width(ws, min_width=12, max_width=50)
        ws.column_dimensions["F"].width = 60
        ws.column_dimensions["G"].width = 35
