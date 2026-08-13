"""Command-line interface for Risk Register Automation Tool.

Usage:
    risk-register add --category "Technical" --title "SQL Injection" ...
    risk-register list [--status Open] [--level Critical]
    risk-register show RISK-20240101-0001
    risk-register export excel [--output report.xlsx]
    risk-register export pdf [--output report.pdf]
    risk-register stats
    risk-register search "SQL"
    risk-register update RISK-20240101-0001 --likelihood 5 --impact 4
    risk-register delete RISK-20240101-0001
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

from risk_register.core.register import RiskRegister
from risk_register.core.risk_model import (
    RiskLevel,
    RiskTreatment,
    Likelihood,
    Impact,
)
from risk_register.exports.excel_exporter import ExcelExporter
from risk_register.exports.pdf_exporter import PDFExporter


def main():
    parser = argparse.ArgumentParser(
        prog="risk-register",
        description="Risk Register Automation Tool - ISO 27001 Annex A compliant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  risk-register add \\
      --category "Technical" \\
      --title "SQL Injection in login form" \\
      --description "Login form vulnerable to SQL injection" \\
      --asset "Web Application" \\
      --owner "DevTeam" \\
      --likelihood 5 \\
      --impact 4

  risk-register list --level Critical

  risk-register export excel --output audit_report.xlsx

  risk-register export pdf --output audit_report.pdf

  risk-register stats
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ADD
    add_parser = subparsers.add_parser("add", help="Add a new risk")
    add_parser.add_argument("--category", required=True)
    add_parser.add_argument("--title", required=True)
    add_parser.add_argument("--description", required=True)
    add_parser.add_argument("--asset", required=True)
    add_parser.add_argument("--owner", required=True)
    add_parser.add_argument("--likelihood", type=int, default=3, choices=range(1, 6))
    add_parser.add_argument("--impact", type=int, default=3, choices=range(1, 6))
    add_parser.add_argument("--treatment", choices=["Avoid", "Transfer", "Mitigate", "Accept", "Share"], default="Mitigate")
    add_parser.add_argument("--iso-controls", nargs="*", default=[])
    add_parser.add_argument("--mitigation-plan", default="")
    add_parser.add_argument("--review-date", default=None)

    # LIST
    list_parser = subparsers.add_parser("list", help="List risks with optional filters")
    list_parser.add_argument("--status", default=None)
    list_parser.add_argument("--level", default=None)
    list_parser.add_argument("--category", default=None)
    list_parser.add_argument("--owner", default=None)
    list_parser.add_argument("--search", default=None, dest="search_query")

    # SHOW
    show_parser = subparsers.add_parser("show", help="Show detailed info about a risk")
    show_parser.add_argument("risk_id")

    # UPDATE
    update_parser = subparsers.add_parser("update", help="Update an existing risk")
    update_parser.add_argument("risk_id")
    update_parser.add_argument("--likelihood", type=int, choices=range(1, 6))
    update_parser.add_argument("--impact", type=int, choices=range(1, 6))
    update_parser.add_argument("--status", choices=["Open", "Closed", "Mitigated", "Accepted"])
    update_parser.add_argument("--treatment", choices=["Avoid", "Transfer", "Mitigate", "Accept", "Share"])
    update_parser.add_argument("--mitigation-plan", default=None)
    update_parser.add_argument("--review-date", default=None)

    # DELETE
    delete_parser = subparsers.add_parser("delete", help="Delete a risk")
    delete_parser.add_argument("risk_id")

    # EXPORT
    export_parser = subparsers.add_parser("export", help="Export risk register")
    export_sub = export_parser.add_subparsers(dest="format")

    excel_parser = export_sub.add_parser("excel", help="Export to Excel")
    excel_parser.add_argument("--output", default=None)

    pdf_parser = export_sub.add_parser("pdf", help="Export to PDF")
    pdf_parser.add_argument("--output", default=None)

    # STATS
    stats_parser = subparsers.add_parser("stats", help="Show aggregate statistics")

    # SEARCH
    search_parser = subparsers.add_parser("search", help="Search risks by keyword")
    search_parser.add_argument("query")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    register = RiskRegister()

    # ── ADD ──
    if args.command == "add":
        treatment = RiskTreatment(args.treatment)
        review_date = None
        if args.review_date:
            try:
                review_date = datetime.strptime(args.review_date, "%Y-%m-%d")
            except ValueError:
                print("Error: Invalid date format. Use YYYY-MM-DD.", file=sys.stderr)
                sys.exit(1)

        risk = register.add_risk(
            category=args.category,
            title=args.title,
            description=args.description,
            asset=args.asset,
            owner=args.owner,
            likelihood=args.likelihood,
            impact=args.impact,
            iso_controls=args.iso_controls,
            treatment=treatment,
            mitigation_plan=args.mitigation_plan,
            review_date=review_date,
        )
        print(f"[+] Risk added successfully!")
        print(f"    ID: {risk.risk_id}")
        print(f"    Level: {risk.risk_level.value} (Score: {risk.risk_score})")
        print(f"    ISO Controls: {', '.join(risk.iso_controls) or 'None assigned'}")

    # ── LIST ──
    elif args.command == "list":
        risks = register.get_all()
        if args.status:
            risks = register.filter_by_status(args.status)
        if args.level:
            level_map = {"Critical": RiskLevel.CRITICAL, "High": RiskLevel.HIGH,
                        "Medium": RiskLevel.MEDIUM, "Low": RiskLevel.LOW}
            level = level_map.get(args.level)
            if level:
                risks = register.filter_by_level(level)
            else:
                print(f"Error: Unknown risk level '{args.level}'.", file=sys.stderr)
                sys.exit(1)
        if args.category:
            risks = register.filter_by_category(args.category)
        if args.owner:
            risks = register.filter_by_owner(args.owner)
        if args.search_query:
            risks = register.search(args.search_query)

        if not risks:
            print("No risks found matching the criteria.")
        else:
            print(f"\n{'ID':<28} {'Category':<18} {'Title':<35} {'Score':>5} {'Level':<10} {'Status':<12}")
            print("-" * 110)
            for risk in risks:
                print(f"{risk.risk_id:<28} {risk.category:<18} {risk.title:<35} "
                      f"{risk.risk_score:>5} {risk.risk_level.value:<10} {risk.status:<12}")

    # ── SHOW ──
    elif args.command == "show":
        risk = register.get_risk(args.risk_id)
        if not risk:
            print(f"Error: Risk '{args.risk_id}' not found.", file=sys.stderr)
            sys.exit(1)
        print_risk_details(risk)

    # ── UPDATE ──
    elif args.command == "update":
        kwargs = {}
        if args.likelihood is not None:
            kwargs["likelihood"] = args.likelihood
        if args.impact is not None:
            kwargs["impact"] = args.impact
        if args.status is not None:
            kwargs["status"] = args.status
        if args.treatment is not None:
            kwargs["treatment"] = RiskTreatment(args.treatment)
        if args.mitigation_plan is not None:
            kwargs["mitigation_plan"] = args.mitigation_plan
        if args.review_date:
            try:
                kwargs["review_date"] = datetime.strptime(args.review_date, "%Y-%m-%d")
            except ValueError:
                print("Error: Invalid date format.", file=sys.stderr)
                sys.exit(1)

        risk = register.update_risk(args.risk_id, **kwargs)
        if not risk:
            print(f"Error: Risk '{args.risk_id}' not found.", file=sys.stderr)
            sys.exit(1)
        print(f"[+] Risk updated: {risk.risk_id} (Level: {risk.risk_level.value})")

    # ── DELETE ──
    elif args.command == "delete":
        if register.delete_risk(args.risk_id):
            print(f"[+] Risk '{args.risk_id}' deleted.")
        else:
            print(f"Error: Risk '{args.risk_id}' not found.", file=sys.stderr)
            sys.exit(1)

    # ── EXPORT ──
    elif args.command == "export":
        if args.format == "excel":
            exporter = ExcelExporter()
            path = exporter.export_risk_register(register, Path(args.output) if args.output else None)
            print(f"[+] Excel report: {path}")
        elif args.format == "pdf":
            exporter = PDFExporter()
            path = exporter.export_pdf(register, Path(args.output) if args.output else None)
            print(f"[+] PDF report: {path}")
        else:
            print("Error: Specify format: excel or pdf", file=sys.stderr)
            sys.exit(1)

    # ── STATS ──
    elif args.command == "stats":
        stats = register.get_statistics()
        print("\n" + "=" * 70)
        print("  RISK REGISTER - STATISTICS & SUMMARY")
        print("=" * 70)
        print(f"\n  Total Risks:          {stats['total_risks']}")
        print(f"  Critical Risks:       {len(stats['critical_risks'])}")
        print(f"  High Risks:           {len(stats['high_risks'])}")
        print(f"  Average Score:        {stats['average_score']}")
        print(f"\n  -- Risk Level Distribution --")
        for level, count in stats["by_level"].items():
            pct = (count / stats["total_risks"] * 100) if stats["total_risks"] else 0
            bar = "█" * int(pct / 5)
            print(f"    {level:<12} {count:>3}  ({pct:>5.1f}%)  {bar}")
        print(f"\n  -- Status Distribution --")
        for status, count in stats["status_distribution"].items():
            print(f"    {status:<12} {count:>3}")
        print(f"\n  -- By Category --")
        for cat, count in sorted(stats["by_category"].items(), key=lambda x: -x[1]):
            print(f"    {cat:<20} {count:>3}")
        print("\n" + "=" * 70 + "\n")

    # ── SEARCH ──
    elif args.command == "search":
        results = register.search(args.query)
        if not results:
            print(f"No risks found matching '{args.query}'.")
        else:
            print(f"\nFound {len(results)} risk(s) matching '{args.query}':\n")
            for risk in results:
                print_risk_details(risk)
                print()


def print_risk_details(risk):
    print(f"  Risk ID:        {risk.risk_id}")
    print(f"  Title:          {risk.title}")
    print(f"  Category:       {risk.category}")
    print(f"  Description:    {risk.description}")
    print(f"  Asset:          {risk.asset}")
    print(f"  Owner:          {risk.owner}")
    print(f"  -- Assessment --")
    print(f"  Likelihood:     {risk.likelihood} ({Likelihood(risk.likelihood).name})")
    print(f"  Impact:         {risk.impact} ({Impact(risk.impact).name})")
    print(f"  Risk Score:     {risk.risk_score} (LxI)")
    print(f"  Risk Level:     {risk.risk_level.value}")
    print(f"  -- Treatment --")
    print(f"  Treatment:      {risk.treatment.value}")
    print(f"  Mitigation:     {risk.mitigation_plan or 'Not defined'}")
    print(f"  ISO Controls:   {', '.join(risk.iso_controls) if risk.iso_controls else 'None assigned'}")
    print(f"  Status:         {risk.status}")
    print(f"  Review Date:    {risk.review_date.strftime('%Y-%m-%d') if risk.review_date else 'Not set'}")
    print(f"  Created:        {risk.created_at.strftime('%Y-%m-%d %H:%M')}")
    print(f"  Updated:        {risk.updated_at.strftime('%Y-%m-%d %H:%M')}")


if __name__ == "__main__":
    main()
