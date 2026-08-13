#!/usr/bin/env python3
"""Generate sample risk register data for testing and demo purposes."""

import sys
from datetime import datetime, date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from risk_register.core.register import RiskRegister
from risk_register.core.risk_model import RiskTreatment


def parse_date(date_str):
    """Convert YYYY-MM-DD string to datetime object."""
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%d")
    return None


def generate_sample_register(output_path=None):
    register = RiskRegister(data_path=output_path or Path.home() / ".risk_register_data.json")

    risks = [
        {
            "category": "Technical",
            "title": "SQL Injection in Customer Portal",
            "description": "The customer portal login field is vulnerable to SQL injection attacks.",
            "asset": "Customer Web Portal",
            "owner": "Web Development Team",
            "likelihood": 4, "impact": 4,
            "iso_controls": ["A.9.1", "A.9.3", "A.14.1", "A.14.2"],
            "treatment": RiskTreatment.MITIGATE,
            "mitigation_plan": "1. Implement parameterized queries\n2. Conduct pentesting\n3. Deploy WAF",
            "review_date": "2024-06-15",
        },
        {
            "category": "Technical",
            "title": "Unpatched Critical CVE",
            "description": "A critical RCE vulnerability (CVSS 9.8) in production web server.",
            "asset": "Production Web Server",
            "owner": "Infrastructure Team",
            "likelihood": 3, "impact": 5,
            "iso_controls": ["A.12.6", "A.12.4", "A.9.12"],
            "treatment": RiskTreatment.MITIGATE,
            "mitigation_plan": "1. Apply patch within 48 hours\n2. Network mitigations\n3. SIEM monitoring",
            "review_date": "2024-03-01",
        },
        {
            "category": "Legal",
            "title": "GDPR Compliance - Missing DPIAs",
            "description": "Organization processes EU personal data without required DPIAs.",
            "asset": "Customer Personal Data",
            "owner": "Data Protection Officer",
            "likelihood": 2, "impact": 5,
            "iso_controls": ["A.18.4", "A.18.1", "A.8.2"],
            "treatment": RiskTreatment.MITIGATE,
            "mitigation_plan": "1. Conduct DPIAs\n2. Engage DPO\n3. Privacy-by-design",
            "review_date": "2024-04-01",
        },
        {
            "category": "Operational",
            "title": "Single Point of Failure - Database",
            "description": "Primary database has no redundancy or failover.",
            "asset": "Primary Database Server",
            "owner": "Infrastructure Team",
            "likelihood": 3, "impact": 5,
            "iso_controls": ["A.11.11", "A.12.1", "A.17.1"],
            "treatment": RiskTreatment.MITIGATE,
            "mitigation_plan": "1. DB replication\n2. Auto failover\n3. Backup procedures",
            "review_date": "2024-04-15",
        },
        {
            "category": "Personnel",
            "title": "Insider Threat - Unmonitored Privileged Access",
            "description": "Admins have unrestricted access without monitoring or SoD.",
            "asset": "Production Systems",
            "owner": "IT Security Team",
            "likelihood": 3, "impact": 4,
            "iso_controls": ["A.9.3", "A.9.4", "A.12.4", "A.7.3"],
            "treatment": RiskTreatment.MITIGATE,
            "mitigation_plan": "1. PAM solution\n2. Audit logging\n3. Quarterly access reviews",
            "review_date": "2024-05-01",
        },
        {
            "category": "Third Party",
            "title": "Cloud Provider Data Breach Risk",
            "description": "Sensitive data stored in cloud - provider breach could expose data.",
            "asset": "Cloud Storage",
            "owner": "Cloud Infrastructure Team",
            "likelihood": 2, "impact": 5,
            "iso_controls": ["A.6.2", "A.15.1", "A.15.2", "A.13.4"],
            "treatment": RiskTreatment.TRANSFER,
            "mitigation_plan": "1. Review SLA\n2. Customer-managed encryption keys\n3. Annual assessment",
            "review_date": "2024-05-15",
        },
        {
            "category": "Access Control",
            "title": "Shared Generic Admin Accounts",
            "description": "Shared admin accounts prevent accountability and audit trail.",
            "asset": "System Admin Accounts",
            "owner": "IT Security Team",
            "likelihood": 4, "impact": 3,
            "iso_controls": ["A.9.2", "A.9.3", "A.9.4", "A.9.6"],
            "treatment": RiskTreatment.MITIGATE,
            "mitigation_plan": "1. Document shared accounts\n2. Create named accounts\n3. Implement RBAC",
            "review_date": "2024-06-01",
        },
        {
            "category": "Data Classification",
            "title": "Sensitive Data Without Encryption",
            "description": "Customer PII stored in dev/test databases without encryption at rest.",
            "asset": "Dev & Test Databases",
            "owner": "DB Administration Team",
            "likelihood": 3, "impact": 4,
            "iso_controls": ["A.8.2", "A.8.3", "A.10.1", "A.10.2"],
            "treatment": RiskTreatment.MITIGATE,
            "mitigation_plan": "1. TDE on all DBs\n2. Data classification policy\n3. Anonymize non-prod PII",
            "review_date": "2024-05-20",
        },
        {
            "category": "Physical Security",
            "title": "Unauthorized Physical Access to Server Room",
            "description": "Server room lacks access control - simple lock, no logging.",
            "asset": "Server Room",
            "owner": "Facilities Management",
            "likelihood": 3, "impact": 4,
            "iso_controls": ["A.11.1", "A.11.2", "A.11.3", "A.11.4"],
            "treatment": RiskTreatment.MITIGATE,
            "mitigation_plan": "1. Electronic access control\n2. Access logging\n3. CCTV",
            "review_date": "2024-06-01",
        },
        {
            "category": "Cryptography",
            "title": "Weak Crypto in Legacy Systems",
            "description": "Legacy apps still use MD5, SHA-1, RC4 - vulnerable to attacks.",
            "asset": "Legacy Applications",
            "owner": "Application Dev Team",
            "likelihood": 4, "impact": 3,
            "iso_controls": ["A.10.1", "A.10.2", "A.14.2"],
            "treatment": RiskTreatment.MITIGATE,
            "mitigation_plan": "1. Crypto inventory\n2. Replace with SHA-256/AES-256\n3. Update standards",
            "review_date": "2024-09-15",
        },
        {
            "category": "Incident Response",
            "title": "No Documented Incident Response Plan",
            "description": "No formal IR plan - response would be ad-hoc during incidents.",
            "asset": "Organizational Operations",
            "owner": "IT Security Team",
            "likelihood": 3, "impact": 5,
            "iso_controls": ["A.16.1", "A.16.2"],
            "treatment": RiskTreatment.MITIGATE,
            "mitigation_plan": "1. Develop IR plan (NIST SP 800-61)\n2. Severity classification\n3. Tabletop exercise",
            "review_date": "2024-06-20",
        },
    ]

    added = []
    for rd in risks:
        risk = register.add_risk(
            category=rd["category"],
            title=rd["title"],
            description=rd["description"],
            asset=rd["asset"],
            owner=rd["owner"],
            likelihood=rd["likelihood"],
            impact=rd["impact"],
            iso_controls=rd["iso_controls"],
            treatment=rd["treatment"],
            mitigation_plan=rd["mitigation_plan"],
            review_date=parse_date(rd["review_date"]),
        )
        added.append(risk.risk_id)

    print(f"[+] Generated {len(added)} sample risks")
    for rid in added:
        print(f"    - {rid}")

    stats = register.get_statistics()
    print(f"\n[=] Summary: Total={stats['total_risks']}, Critical={len(stats['critical_risks'])}, High={len(stats['high_risks'])}, Avg={stats['average_score']}")

    return output_path or register._data_path


if __name__ == "__main__":
    output = generate_sample_register()
    print(f"\n[OK] Risk register saved to: {output}")
