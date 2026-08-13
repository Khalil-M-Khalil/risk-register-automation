# Risk Register Automation Tool

> **Automated ISO 27001:2022 Annex A Compliant Risk Management System**
>
> A professional-grade Python tool for creating, managing, scoring, and reporting enterprise risk registers. Aligned with **ISO 27005:2022** risk assessment methodology and fully mapped to **ISO 27001:2022 Annex A** (93 controls across 14 themes).

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [CLI Reference](#cli-reference)
- [Risk Scoring Methodology](#risk-scoring-methodology)
- [ISO 27001:2022 Annex A Mapping](#iso-270012022-annex-a-mapping)
- [Excel Export](#excel-export)
- [PDF Export](#pdf-export)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Compliance Alignment](#compliance-alignment)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This tool provides a complete risk register management system for information security professionals, auditors, and GRC practitioners. It enables:

- **Structured risk capture** with standardized fields (category, likelihood, impact, treatment, owner)
- **Automated risk scoring** using the ISO 27005:2022 5x5 matrix (Likelihood × Impact)
- **ISO 27001:2022 control mapping** — every risk can be linked to specific Annex A controls for audit traceability
- **Professional reporting** — export to Excel (5-sheet workbook with charts and conditional formatting) or PDF (audit-ready document)
- **CLI-first workflow** — manage risks from the command line with full CRUD, search, filtering, and statistics

---

## Architecture

```
risk-register-automation/
├── risk_register/
│   ├── core/
│   │   ├── risk_model.py       # Data model (Risk, RiskLevel, Likelihood, Impact, RiskTreatment)
│   │   ├── register.py         # CRUD register with persistence (JSON)
│   │   └── iso27001_mapper.py  # ISO 27001:2022 Annex A control definitions (93 controls)
│   ├── exports/
│   │   ├── excel_exporter.py   # 5-sheet Excel workbook with charts
│   │   └── pdf_exporter.py     # Audit-ready PDF report
│   └── cli.py                  # Command-line interface (argparse)
├── scripts/
│   └── generate_sample_data.py # Populate register with realistic sample data
├── tests/
│   ├── test_risk_model.py      # Model unit tests (scoring, serialization)
│   └── test_register.py        # Register unit tests (CRUD, queries, stats, persistence)
├── pyproject.toml              # Modern Python packaging (PEP 621)
├── requirements.txt            # Runtime dependencies
└── README.md                   # This file
```

---

## Features

### Core Risk Management

| Feature | Description |
|---------|-------------|
| **Risk Scoring** | 5×5 matrix: Likelihood (1-5) × Impact (1-5) = Score (1-25) |
| **Risk Classification** | Low (1-4), Medium (5-9), High (10-16), Critical (17-25) — ISO 27005 aligned |
| **Risk Treatment** | Avoid, Transfer, Mitigate, Accept, Share |
| **ISO 27001 Mapping** | Link risks to Annex A controls (A.5.1 through A.18.6) |
| **Full CRUD** | Add, update, delete, list, show, search |
| **Filtering** | By status, level, category, owner |
| **Full-text search** | Across all text fields (title, description, category, asset, owner, controls) |
| **Statistics** | Total counts, level distribution, category breakdown, average score |
| **Overdue tracking** | Identify risks with passed review dates |
| **JSON persistence** | Auto-saved to `~/.risk_register_data.json` |

### Professional Excel Export (5 Sheets)

| Sheet | Contents |
|-------|----------|
| **Risk Register** | All risks with full details, color-coded risk levels, ISO control references |
| **Risk Matrix** | 5×5 heatmap showing risk distribution by Likelihood × Impact with legend |
| **Statistics** | KPI cards, level distribution table, category breakdown, status tracking, bar chart |
| **ISO 27001 Controls** | Complete Annex A control list with coverage status, theme-based coloring |
| **Treatment Plan** | High & Critical risks with treatment strategy, mitigation plans, owners |

### Audit-Ready PDF Export

| Section | Contents |
|---------|----------|
| **Cover Page** | Title, generation date, classification |
| **Executive Summary** | KPI dashboard, methodology narrative (ISO 27005/31000) |
| **Risk Register** | Full table with color-coded risk levels |
| **Risk Matrix** | Visual 5×5 matrix with thresholds legend |
| **ISO 27001 Coverage** | Control mapping with coverage status |
| **Treatment Plan** | High/Critical risks with detailed treatment strategies |

---

## Installation

### Requirements

- Python 3.8+
- pip (or pip3)

### Install from Source

```bash
# Clone the repository
git clone https://github.com/Khalil-M-Khalil/risk-register-automation.git
cd risk-register-automation

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Or install runtime only
pip install -r requirements.txt
```

### Install via pip (when published)

```bash
pip install risk-register-automation
```

---

## Quick Start

### 1. Generate Sample Data

Populate the register with 11 realistic, ISO 27001-aligned risks:

```bash
python3 scripts/generate_sample_data.py
```

This creates `~/.risk_register_data.json` with risks covering:
- Technical (SQL Injection, Unpatched CVE)
- Legal (GDPR Compliance)
- Operational (Single Point of Failure)
- Personnel (Insider Threat)
- Third Party (Cloud Provider Risk)
- Access Control (Shared Admin Accounts)
- Data Classification (Unencrypted PII)
- Physical Security (Server Room Access)
- Cryptography (Weak Algorithms)
- Incident Response (No IR Plan)

### 2. View Statistics

```bash
risk-register stats
```

Output:
```
======================================================================
  RISK REGISTER - STATISTICS & SUMMARY
======================================================================

  Total Risks:          11
  Critical Risks:       0
  High Risks:           11
  Average Score:        12.82

  -- Risk Level Distribution --
    High          11  (100.0%)  ████████████████████

  -- By Category --
    Technical              2
    Legal                  1
    ...
```

### 3. List All Risks

```bash
risk-register list
```

### 4. Filter by Level

```bash
risk-register list --level High
```

### 5. Search

```bash
risk-register search "SQL"
```

### 6. Export to Excel

```bash
risk-register export excel --output audit_report.xlsx
```

Generates a 5-sheet Excel workbook with:
- Color-coded risk register
- 5×5 risk matrix heatmap
- Statistics dashboard with chart
- ISO 27001 control coverage map
- Treatment plan for high/critical risks

### 7. Export to PDF

```bash
risk-register export pdf --output audit_report.pdf
```

Generates an audit-ready PDF report with:
- Executive summary with methodology
- Full risk register table
- Risk matrix visualization
- ISO 27001 control coverage
- Treatment plan

---

## CLI Reference

```
risk-register <command> [options]

Commands:
  add         Add a new risk to the register
  list        List risks with optional filters
  show        Show detailed information about a specific risk
  update      Update an existing risk
  delete      Delete a risk from the register
  export      Export risk register (excel | pdf)
  stats       Show aggregate statistics
  search      Search risks by keyword
```

### add

```bash
risk-register add \
    --category "Technical" \
    --title "SQL Injection in login form" \
    --description "Login form vulnerable to SQL injection attacks" \
    --asset "Web Application" \
    --owner "DevTeam" \
    --likelihood 5 \
    --impact 4 \
    --treatment Mitigate \
    --iso-controls A.9.1 A.9.3 A.14.1 \
    --mitigation-plan "Implement parameterized queries and deploy WAF"
```

### list

```bash
risk-register list                          # All risks
risk-register list --status Open            # Filter by status
risk-register list --level Critical         # Filter by level
risk-register list --category Technical     # Filter by category
risk-register list --owner DevTeam          # Filter by owner
```

### show

```bash
risk-register show RISK-20240101-0001
```

### update

```bash
risk-register update RISK-20240101-0001 \
    --likelihood 5 \
    --impact 4 \
    --status Mitigated \
    --mitigation-plan "Patched and tested"
```

### delete

```bash
risk-register delete RISK-20240101-0001
```

### export

```bash
risk-register export excel --output report.xlsx
risk-register export pdf --output report.pdf
```

### stats

```bash
risk-register stats
```

### search

```bash
risk-register search "database"
```

---

## Risk Scoring Methodology

This tool implements the **ISO 27005:2022** risk assessment methodology using a 5×5 matrix.

### Likelihood Scale (1-5)

| Level | Value | Definition |
|-------|-------|------------|
| Rare | 1 | May occur only in exceptional circumstances |
| Unlikely | 2 | Could occur at some time |
| Possible | 3 | Should occur at some time |
| Likely | 4 | Will probably occur in most circumstances |
| Almost Certain | 5 | Expected to occur in most circumstances |

### Impact Scale (1-5)

| Level | Value | Definition |
|-------|-------|------------|
| Negligible | 1 | No significant impact on operations, finances, or reputation |
| Minor | 2 | Minor financial or operational impact, easily absorbed |
| Moderate | 3 | Moderate impact requiring dedicated resources to remediate |
| Major | 4 | Major impact on operations, finances, or reputation |
| Severe | 5 | Catastrophic impact — business-critical or existential threat |

### Risk Score = Likelihood × Impact

| Score Range | Risk Level | Recommended Action |
|-------------|------------|-------------------|
| 1-4 | **Low** | Accept — monitor periodically |
| 5-9 | **Medium** | Mitigate — action plan required with timeline |
| 10-16 | **High** | Mitigate urgently — escalation to management required |
| 17-25 | **Critical** | Immediate action — executive escalation required |

---

## ISO 27001:2022 Annex A Mapping

The tool includes the complete set of **93 Annex A controls** from ISO 27001:2022, organized into 14 themes:

| Theme | Controls | Description |
|-------|----------|-------------|
| **A.5** Policies for information security | A.5.1 - A.5.3 | Policy framework and roles |
| **A.6** Organisation of information security | A.6.1 - A.6.3 | Project management and supplier relationships |
| **A.7** Human resource security | A.7.1 - A.7.5 | Screening, training, termination |
| **A.8** Asset management | A.8.1 - A.8.5 | Inventory, classification, handling |
| **A.9** Access control | A.9.1 - A.9.13 | Authentication, authorization, identity management |
| **A.10** Cryptography | A.10.1 - A.10.2 | Cryptographic controls and key management |
| **A.11** Physical & environmental security | A.11.1 - A.11.11 | Perimeters, entry controls, equipment |
| **A.12** Operations security | A.12.1 - A.12.8 | Logging, vulnerability management, configuration |
| **A.13** Communications security | A.13.1 - A.13.4 | Network security, encryption in transit |
| **A.14** System acquisition, development & maintenance | A.14.1 - A.14.6 | Secure development, testing, outsourcing |
| **A.15** Supplier relationships | A.15.1 - A.15.2 | Supplier security requirements and monitoring |
| **A.16** Information security incident management | A.16.1 - A.16.2 | Incident response and evidence handling |
| **A.17** Business continuity management | A.17.1 - A.17.3 | Continuity planning, implementation, testing |
| **A.18** Compliance | A.18.1 - A.18.6 | Legal, IP, records, privacy, independent review |

Each control is fully defined with:
- **Reference** (e.g., "A.9.1")
- **Title** (e.g., "Access control policy")
- **Theme** (e.g., "A.9 Access control")
- **Description** (full control statement from the standard)
- **Risk categories** (tags for matching to risk types)

---

## Excel Export

The Excel exporter generates a 5-sheet workbook designed for auditor review and management reporting.

### Sheet 1: Risk Register

Full listing of all risks with:
- Color-coded risk level cells (red=Critical, orange=High, yellow=Medium, green=Low)
- Highlighted score cells for High/Critical risks
- ISO control references in dedicated column
- Treatment, owner, status fields

### Sheet 2: Risk Matrix

Interactive 5×5 heatmap:
- Each cell shows: Score, Level, Count of risks in that cell
- Color gradient: green (Low) → yellow (Medium) → red (High/Critical)
- Legend with threshold definitions and recommended actions

### Sheet 3: Statistics

Executive dashboard with:
- **KPI cards**: Total, Critical, High, Average Score, Open risks
- **Level distribution table** with percentages and action guidance
- **Bar chart**: Visual representation of risk level distribution
- **Category breakdown**: Count and average score per category
- **Status tracking**: Open, Closed, Mitigated, Accepted counts

### Sheet 4: ISO 27001 Controls

Complete Annex A listing with:
- All 93 controls with references, titles, themes, and descriptions
- Coverage status column (Yes/No) showing which controls are mapped to risks
- Color-coded theme column using standardized color palette
- Green highlighting for covered controls

### Sheet 5: Treatment Plan

Focused view of High and Critical risks:
- Full details including mitigation plans
- Treatment strategy (Avoid/Transfer/Mitigate/Accept/Share)
- Owner and review date
- Color-coded level column for quick prioritization

---

## PDF Export

The PDF exporter generates an audit-ready report suitable for:
- Internal audit presentations
- Management review meetings
- External auditor evidence packages
- ISO 27001 certification audit documentation

### Sections

1. **Title Page** — Report title, generation timestamp, classification
2. **Executive Summary** — KPI cards, methodology narrative citing ISO 27005:2022 and ISO 31000
3. **Risk Register Table** — Full listing with color-coded levels
4. **Risk Assessment Matrix** — 5×5 visual matrix with threshold legend
5. **ISO 27001 Annex A Coverage** — Control mapping table
6. **Treatment Plan** — High/Critical risks with detailed strategies
7. **Footer** — Generation timestamp, tool version, classification marking

---

## Project Structure

```
risk-register-automation/
├── pyproject.toml              # PEP 621 packaging configuration
├── requirements.txt            # Runtime dependencies
├── .gitignore                  # Git ignore patterns
├── risk_register/
│   ├── __init__.py             # Package metadata (version, author)
│   ├── cli.py                  # Command-line interface (argparse-based)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── risk_model.py       # Risk dataclass, enums, scoring logic
│   │   ├── register.py         # RiskRegister class with CRUD + persistence
│   │   └── iso27001_mapper.py  # ISO_27001_CONTROLS list + ISO27001Mapper class
│   └── exports/
│       ├── __init__.py
│       ├── excel_exporter.py   # ExcelExporter class (5-sheet workbook)
│       └── pdf_exporter.py     # PDFExporter class (audit-ready PDF)
├── scripts/
│   └── generate_sample_data.py # CLI tool to populate sample risks
├── tests/
│   ├── __init__.py
│   ├── test_risk_model.py      # 10 tests: scoring, serialization, updates, controls
│   └── test_register.py        # 14 tests: CRUD, queries, stats, persistence, overdue
└── examples/
    └── sample_risk_register.json # Example JSON export format
```

---

## Testing

### Run All Tests

```bash
python3 -m pytest tests/ -v
```

**Test Coverage:**

| Module | Tests | Coverage |
|--------|-------|----------|
| `test_risk_model.py` | 10 tests | Scoring logic, serialization, updates, ISO controls |
| `test_register.py` | 14 tests | CRUD, queries, statistics, persistence, overdue detection |

**Total: 24 tests, all passing**

### Run Specific Test File

```bash
python3 -m pytest tests/test_risk_model.py -v
python3 -m pytest tests/test_register.py -v
```

### Run with Coverage Report

```bash
python3 -m pytest tests/ -v --cov=risk_register --cov-report=term-missing
```

---

## Compliance Alignment

### ISO 27001:2022

| Clause | Alignment |
|--------|-----------|
| **6.1.2** Information security risk assessment | Risk scoring methodology, likelihood/impact scales |
| **6.1.3** Information security risk treatment | Risk treatment options (Avoid, Transfer, Mitigate, Accept, Share) |
| **6.1.4** Information security risk treatment plan | Treatment plan sheet/report for High & Critical risks |
| **6.1.5** Risk acceptance | Status tracking (Accepted, Mitigated, Closed) |
| **6.1.6** Risk reporting | Excel/PDF exports suitable for management review |
| **Annex A** Control mapping | Each risk can be linked to specific Annex A controls |
| **9.1** Monitoring, measurement, analysis | Statistics dashboard, overdue tracking |

### ISO 27005:2022

| Section | Alignment |
|---------|-----------|
| **7.2** Risk assessment process | Structured approach with identified risks, likelihood, impact |
| **7.3** Risk identification | Risk categories, assets, owners, descriptions |
| **7.4** Risk analysis | Quantitative scoring (L×I), risk level classification |
| **7.5** Risk evaluation | Threshold-based prioritization, action guidance |

### NIST SP 800-30

| Section | Alignment |
|---------|-----------|
| **3.1** Identify threats and vulnerabilities | Risk descriptions, asset identification |
| **3.2** Assess likelihood | 5-level likelihood scale |
| **3.3** Assess impact | 5-level impact scale |
| **3.4** Determine risk level | L×I matrix with classification thresholds |

---

## Roadmap

### v1.0.0 (Current)

- ✅ Risk model with ISO 27005-aligned scoring
- ✅ ISO 27001:2022 Annex A complete control mapping (93 controls)
- ✅ CLI with full CRUD, search, filtering, statistics
- ✅ Excel export (5 sheets, charts, conditional formatting)
- ✅ PDF export (audit-ready report)
- ✅ 24 unit tests (100% passing)
- ✅ Sample data generator (11 realistic risks)
- ✅ JSON persistence

### v1.1.0 (Planned)

- [ ] NIST CSF mapping (Identify, Protect, Detect, Respond, Recover)
- [ ] COBIT 2019 process mapping
- [ ] Risk owner assignment notifications (email reminders for upcoming reviews)
- [ ] Multi-user support with role-based access
- [ ] API backend (FastAPI) for web dashboard integration
- [ ] Risk trend analysis over time (versioned snapshots)
- [ ] Risk appetite / tolerance configuration

### v2.0.0 (Future)

- [ ] Web dashboard (Streamlit / Dash) for interactive risk management
- [ ] Import/export from GRC platforms (ServiceNow, RSA Archer, MetricStream)
- [ ] Automated control testing evidence linking
- [ ] Integration with vulnerability scanners (Nessus, Qualys)
- [ ] Audit trail logging for all register changes

---

## Contributing

Contributions are welcome! Please read our contributing guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/my-feature`)
3. **Commit** your changes (`git commit -m 'feat: Add my feature'`)
4. **Push** to the branch (`git push origin feature/my-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Clone and install dev dependencies
git clone https://github.com/Khalil-M-Khalil/risk-register-automation.git
cd risk-register-automation
pip install -e ".[dev]"

# Run tests
python3 -m pytest tests/ -v

# Format code
black risk_register/ tests/

# Lint
flake8 risk_register/ tests/
```

### Coding Standards

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write unit tests for new features
- Update README.md if adding new functionality
- Keep commit messages informative (conventional commits preferred)

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Khalil M. Khalil

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Author

**Khalil M. Khalil**
- GitHub: [@Khalil-M-Khalil](https://github.com/Khalil-M-Khalil)
- Email: khalil@example.com

---

## Acknowledgments

- **ISO/IEC 27001:2022** — Information security management systems requirements
- **ISO/IEC 27005:2022** — Information security risk management guidance
- **ISO/IEC 31000:2018** — Risk management guidelines
- **NIST SP 800-30 Rev. 1** — Guide for Conducting Risk Assessments
- **COBIT 2019** — Governance and Management of Enterprise IT

---

*Built with Python, openpyxl, and reportlab for the GRC community.*
