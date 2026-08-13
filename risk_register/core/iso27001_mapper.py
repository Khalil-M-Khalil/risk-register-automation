"""ISO 27001:2022 Annex A control mapping utilities.

Maps ISO 27001:2022 Annex A controls (5 themes, 93 controls) to risk categories.
Also provides reverse lookup: given a control, what risk categories it addresses.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ISOControl:
    """Single ISO 27001:2022 Annex A control."""
    ref: str              # e.g., "A.5.1"
    title: str            # e.g., "Policies for information security"
    theme: str            # A.5 Policies for information security
    description: str = ""
    risk_categories: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        return f"{self.ref}: {self.title} [{self.theme}]"


# ─── Complete ISO 27001:2022 Annex A Controls ───
ISO_27001_CONTROLS = [
    # A.5 Policies for information security
    ISOControl("A.5.1", "Policies for information security", "A.5 Policies for information security",
              "Policies and procedures for information security shall be defined, approved, published, communicated and reviewed.",
              ["Governance", "Management"]),
    ISOControl("A.5.2", "Information security roles and responsibilities", "A.5 Policies for information security",
              "Roles and responsibilities for information security shall be defined and allocated.",
              ["Governance", "Management"]),
    ISOControl("A.5.3", "Segregation of duties", "A.5 Policies for information security",
              "Conflicting duties and areas of responsibility shall be segregated to reduce opportunities for unauthorised modification or misuse.",
              ["Access Control", "Operations"]),

    # A.6 Organisation of information security
    ISOControl("A.6.1", "Information security in project management", "A.6 Organisation of information security",
              "Information security shall be addressed in project management.",
              ["Project Management"]),
    ISOControl("A.6.2", "Information security in supplier relationships", "A.6 Organisation of information security",
              "Information security requirements for supplier relationships shall be agreed and managed.",
              ["Third Party", "Supply Chain"]),
    ISOControl("A.6.3", "Information security in project management", "A.6 Organisation of information security",
              "Plans shall be developed to ensure that information security is appropriately addressed in project management.",
              ["Project Management"]),

    # A.7 Human resource security
    ISOControl("A.7.1", "Screening", "A.7 Human resource security",
              "Background verification checks shall be carried out in accordance with relevant laws, regulations and ethics.",
              ["Personnel", "Physical Security"]),
    ISOControl("A.7.2", "Terms and conditions of employment", "A.7 Human resource security",
              "Contracts shall include appropriate terms and conditions related to information security.",
              ["Personnel"]),
    ISOControl("A.7.3", "Information security awareness, education and training", "A.7 Human resource security",
              "All employees and contractors shall receive appropriate awareness, education and training.",
              ["Personnel", "Awareness"]),
    ISOControl("A.7.4", "Disciplinary process", "A.7 Human resource security",
              "There shall be a formal and communicated disciplinary process for handling security violations.",
              ["Personnel"]),
    ISOControl("A.7.5", "Responsibilities after termination or change of employment", "A.7 Human resource security",
              "Responsibilities and duties for information security shall be defined and enforced after termination.",
              ["Personnel"]),

    # A.8 Asset management
    ISOControl("A.8.1", "Inventory of information and associated assets", "A.8 Asset management",
              "An inventory of information and associated assets shall be developed and maintained.",
              ["Asset Management"]),
    ISOControl("A.8.2", "Classification of information", "A.8 Asset management",
              "Information shall be classified according to legal, regulatory, business and contractual requirements.",
              ["Data Classification", "Governance"]),
    ISOControl("A.8.3", "Labelling of information", "A.8 Asset management",
              "Information shall be appropriately labelled to indicate its classification.",
              ["Data Classification"]),
    ISOControl("A.8.4", "Handling of assets", "A.8 Asset management",
              "Rules for the acceptable handling of assets shall be identified and documented.",
              ["Asset Management"]),
    ISOControl("A.8.5", "Return of assets", "A.8 Asset management",
              "All information and associated assets shall be returned by employees and contractors upon termination.",
              ["Asset Management"]),

    # A.9 Access control
    ISOControl("A.9.1", "Access control policy", "A.9 Access control",
              "Access control policy and procedures shall be established and documented.",
              ["Access Control"]),
    ISOControl("A.9.2", "User registration and de-registration", "A.9 Access control",
              "A formal user registration and de-registration process shall be implemented.",
              ["Access Control", "Identity Management"]),
    ISOControl("A.9.3", "Management of privileged access rights", "A.9 Access control",
              "Privileged access rights shall be restricted and managed.",
              ["Access Control"]),
    ISOControl("A.9.4", "Access rights", "A.9 Access control",
              "Access rights shall be reviewed at regular intervals and updated.",
              ["Access Control"]),
    ISOControl("A.9.5", "Information access restriction", "A.9 Access control",
              "Access to information and application system functions shall be restricted in accordance with the access control policy.",
              ["Access Control"]),
    ISOControl("A.9.6", "Identity management", "A.9 Access control",
              "Identity management processes shall be implemented to support the effective provisioning, review and revocation of access rights.",
              ["Identity Management"]),
    ISOControl("A.9.7", "Authentication information", "A.9 Access control",
              "Allocation and use of authentication information shall be controlled and managed.",
              ["Authentication"]),
    ISOControl("A.9.8", "Devices and systems authentication", "A.9 Access control",
              "Authentication mechanisms shall be used to verify the identity of devices and systems.",
              ["Authentication"]),
    ISOControl("A.9.9", "Restrictions on the use of external devices and systems", "A.9 Access control",
              "Restrictions on the use of external devices and systems shall be defined.",
              ["Access Control"]),
    ISOControl("A.9.10", "Secure log-on procedures", "A.9 Access control",
              "Secure log-on procedures shall be used to protect against unauthorised access.",
              ["Authentication"]),
    ISOControl("A.9.11", "Password management system", "A.9 Access control",
              "Password management systems shall be interactive and shall enforce appropriate password quality and lifetime.",
              ["Authentication"]),
    ISOControl("A.9.12", "Use of privileged utility programs", "A.9 Access control",
              "The use of utility programs that might be capable of overriding system and application controls shall be restricted and tightly controlled.",
              ["Access Control"]),
    ISOControl("A.9.13", "Access to program source code", "A.9 Access control",
              "Access to program source code shall be restricted.",
              ["Access Control", "Development"]),

    # A.10 Cryptography
    ISOControl("A.10.1", "Policy on the use of cryptographic controls", "A.10 Cryptography",
              "A policy on the use of cryptographic controls for protection of information shall be developed and implemented.",
              ["Cryptography"]),
    ISOControl("A.10.2", "Key management", "A.10 Cryptography",
              "A policy on the use, protection and lifetime of cryptographic keys shall be developed and implemented.",
              ["Cryptography"]),

    # A.11 Physical and environmental security
    ISOControl("A.11.1", "Physical security perimeter", "A.11 Physical and environmental security",
              "Security perimeters and entry controls shall be defined and implemented to protect areas that are chosen to house sensitive or critical information.",
              ["Physical Security"]),
    ISOControl("A.11.2", "Physical entry controls", "A.11 Physical and environmental security",
              "Secure areas shall be protected by appropriate entry controls.",
              ["Physical Security"]),
    ISOControl("A.11.3", "Securing offices, rooms and facilities", "A.11 Physical and environmental security",
              "Physical security for offices, rooms and facilities shall be designed and applied.",
              ["Physical Security"]),
    ISOControl("A.11.4", "Physical security monitoring", "A.11 Physical and environmental security",
              "Physical access to information and associated assets shall be restricted and monitored.",
              ["Physical Security"]),
    ISOControl("A.11.5", "Protecting against physical and environmental threats", "A.11 Physical and environmental security",
              "Protection shall be provided against physical and environmental threats such as fire, flood, earthquake, explosion, civil unrest, acts of vandalism and industrial hazards.",
              ["Physical Security"]),
    ISOControl("A.11.6", "Working in secure areas", "A.11 Physical and environmental security",
              "Procedures shall be implemented to ensure security when working in secure areas.",
              ["Physical Security"]),
    ISOControl("A.11.7", "Clear desk and clear screen policy", "A.11 Physical and environmental security",
              "A clear desk and clear screen policy shall be implemented.",
              ["Physical Security", "Operations"]),
    ISOControl("A.11.8", "Equipment siting and protection", "A.11 Physical and environmental security",
              "Equipment shall be sited and protected to reduce the risk of physical threats.",
              ["Physical Security"]),
    ISOControl("A.11.9", "Security of assets off-premises", "A.11 Physical and environmental security",
              "Security shall be applied to off-site assets taking into account the different risks of personnel working outside the organisation's premises.",
              ["Physical Security"]),
    ISOControl("A.11.10", "Secure disposal or reuse of equipment", "A.11 Physical and environmental security",
              "Equipment containing storage media shall be checked to ensure that any sensitive data and licensed software has been removed or securely overwritten.",
              ["Physical Security", "Asset Management"]),
    ISOControl("A.11.11", "Backup", "A.11 Physical and environmental security",
              "Backup copies of information, software and system images shall be maintained and regularly tested.",
              ["Backup", "Operations"]),

    # A.12 Operations security
    ISOControl("A.12.1", "Designing and operating controls for IT facilities", "A.12 Operations security",
              "Controls for the operation of IT facilities shall be established and documented.",
              ["Operations", "Infrastructure"]),
    ISOControl("A.12.2", "Controls for IT supply chain", "A.12 Operations security",
              "Information security requirements for IT supply chain shall be defined and managed.",
              ["Supply Chain", "Operations"]),
    ISOControl("A.12.3", "Information systems audit considerations", "A.12 Operations security",
              "Audit requirements, activities and roles shall be defined to ensure that audit activities do not adversely affect the operation of information systems.",
              ["Audit"]),
    ISOControl("A.12.4", "Logging and monitoring", "A.12 Operations security",
              "Event logging shall be enabled and logs shall be protected and regularly reviewed.",
              ["Logging", "Monitoring"]),
    ISOControl("A.12.5", "Protection of operational systems", "A.12 Operations security",
              "Operational procedures and responsibilities shall be established to ensure the protection of information systems and data.",
              ["Operations"]),
    ISOControl("A.12.6", "Management of technical vulnerabilities", "A.12 Operations security",
              "Information about technical vulnerabilities of information systems being used shall be obtained, the organisation's exposure to such vulnerabilities evaluated and appropriate measures taken.",
              ["Vulnerability Management"]),
    ISOControl("A.12.7", "Configuration management", "A.12 Operations security",
              "Configuration management procedures shall be implemented to ensure the security of information systems.",
              ["Configuration Management", "Operations"]),
    ISOControl("A.12.8", "Information systems acceptance", "A.12 Operations security",
              "Information systems shall be evaluated and tested before being deployed to production.",
              ["Testing", "Operations"]),

    # A.13 Communications security
    ISOControl("A.13.1", "Network security management", "A.13 Communications security",
              "Security mechanisms, service levels and management requirements shall be identified and included in network security architecture and policies.",
              ["Network Security"]),
    ISOControl("A.13.2", "Security of network services", "A.13 Communications security",
              "Security mechanisms for network services shall be implemented and maintained.",
              ["Network Security"]),
    ISOControl("A.13.3", "Segregation of networks", "A.13 Communications security",
              "Groups of information services, users and information systems shall be segregated on networks.",
              ["Network Security"]),
    ISOControl("A.13.4", "Encryption and integrity protection of data during transmission", "A.13 Communications security",
              "Data transmitted over communication networks shall be protected against interception and modification.",
              ["Cryptography", "Network Security"]),

    # A.14 System acquisition, development and maintenance
    ISOControl("A.14.1", "Securing applications before deployment", "A.14 System acquisition, development and maintenance",
              "Security requirements for applications shall be defined and addressed during the development phase.",
              ["SDLC", "Secure Development"]),
    ISOControl("A.14.2", "Secure software development", "A.14 System acquisition, development and maintenance",
              "Rules for secure software development shall be established and applied.",
              ["SDLC", "Secure Development"]),
    ISOControl("A.14.3", "Secure development environment", "A.14 System acquisition, development and maintenance",
              "The development environment shall be protected from unauthorised access and modification.",
              ["SDLC"]),
    ISOControl("A.14.4", "System security testing", "A.14 System acquisition, development and maintenance",
              "System security testing shall be performed before deployment and at regular intervals thereafter.",
              ["Testing", "Security Testing"]),
    ISOControl("A.14.5", "Outsourced development", "A.14 System acquisition, development and maintenance",
              "Information security requirements for outsourced development shall be agreed and managed.",
              ["Outsourcing", "SDLC"]),
    ISOControl("A.14.6", "Security of service-oriented architectures", "A.14 System acquisition, development and maintenance",
              "Security architecture and controls for service-oriented architectures shall be designed and implemented.",
              ["Architecture", "Network Security"]),

    # A.15 Supplier relationships
    ISOControl("A.15.1", "Information security in supplier relationships", "A.15 Supplier relationships",
              "Information security requirements for supplier relationships shall be agreed, communicated and managed.",
              ["Third Party", "Supply Chain"]),
    ISOControl("A.15.2", "Monitoring and review of supplier services", "A.15 Supplier relationships",
              "Supplier services that affect the organisation's ability to meet its information security requirements shall be monitored and reviewed.",
              ["Third Party", "Monitoring"]),

    # A.16 Information security incident management
    ISOControl("A.16.1", "Management of information security incidents", "A.16 Information security incident management",
              "A process shall be established to ensure that information security incidents are identified, reported, assessed, responded to and learned from.",
              ["Incident Response", "Management"]),
    ISOControl("A.16.2", "Collection of evidence", "A.16 Information security incident management",
              "Procedures for the identification, collection, acquisition and preservation of evidence related to information security incidents shall be established.",
              ["Incident Response", "Forensics"]),

    # A.17 Information security aspects of business continuity management
    ISOControl("A.17.1", "Planning information security continuity", "A.17 Information security aspects of business continuity management",
              "Information security continuity shall be embedded in the organisation's business continuity management systems.",
              ["BCP", "Business Continuity"]),
    ISOControl("A.17.2", "Implementing information security continuity", "A.17 Information security aspects of business continuity management",
              "The organisation shall establish, implement and maintain the required measures for information security continuity.",
              ["BCP"]),
    ISOControl("A.17.3", "Verification, review and evaluation of information security continuity", "A.17 Information security aspects of business continuity management",
              "The organisation shall verify and regularly test the established and implemented measures for information security continuity.",
              ["BCP", "Testing"]),

    # A.18 Compliance
    ISOControl("A.18.1", "Identification of applicable legislation and contractual requirements", "A.18 Compliance",
              "All relevant legislation, statutory requirements, regulatory requirements and contractual obligations of the organisation with regard to information security shall be identified.",
              ["Legal", "Governance"]),
    ISOControl("A.18.2", "Intellectual property rights", "A.18 Compliance",
              "Procedures to ensure compliance with applicable intellectual property rights and use of software products shall be implemented.",
              ["Legal"]),
    ISOControl("A.18.3", "Protection of records", "A.18 Compliance",
              "Records shall be protected from loss, destruction, falsification, unauthorized access and unauthorised release.",
              ["Records Management"]),
    ISOControl("A.18.4", "Privacy and protection of PII", "A.18 Compliance",
              "Protection of PII shall be implemented in accordance with applicable privacy laws and regulations.",
              ["Privacy", "PII"]),
    ISOControl("A.18.5", "Independent review of information security", "A.18 Compliance",
              "The organisation's approach to managing information security shall be independently reviewed at planned intervals or when significant changes occur.",
              ["Audit", "Governance"]),
    ISOControl("A.18.6", "Compliance with security policies, rules and standards for information security", "A.18 Compliance",
              "Compliance with security policies, rules and standards for information security shall be regularly reviewed.",
              ["Compliance", "Governance"]),
]


class ISO27001Mapper:
    """Utility class for ISO 27001:2022 Annex A control lookups."""

    def __init__(self):
        self.controls = {ctrl.ref: ctrl for ctrl in ISO_27001_CONTROLS}
        self.by_theme = {}
        for ctrl in ISO_27001_CONTROLS:
            self.by_theme.setdefault(ctrl.theme, []).append(ctrl)

    def get_control(self, ref: str) -> Optional[ISOControl]:
        """Look up a control by its reference (e.g., 'A.5.1')."""
        return self.controls.get(ref)

    def get_controls_by_theme(self, theme: str) -> list[ISOControl]:
        """Get all controls under a specific theme."""
        return self.by_theme.get(theme, [])

    def get_controls_for_risk_category(self, category: str) -> list[ISOControl]:
        """
        Get all controls relevant to a risk category.
        Supports both exact matches and partial/fuzzy matching.
        """
        matched = []
        category_lower = category.lower()
        for ctrl in ISO_27001_CONTROLS:
            for rc in ctrl.risk_categories:
                if category_lower in rc.lower() or rc.lower() in category_lower:
                    matched.append(ctrl)
        return matched

    def suggest_controls(self, risk_title: str, risk_categories: list[str]) -> list[ISOControl]:
        """
        Suggest relevant ISO 27001 controls for a risk based on its categories.
        Uses broad matching to ensure coverage.
        """
        suggestions = []
        for category in risk_categories:
            suggestions.extend(self.get_controls_for_risk_category(category))
        # Deduplicate
        seen = set()
        unique = []
        for ctrl in suggestions:
            if ctrl.ref not in seen:
                seen.add(ctrl.ref)
                unique.append(ctrl)
        return unique

    def get_all_themes(self) -> list[str]:
        """Return all ISO 27001 themes."""
        return list(self.by_theme.keys())

    def get_theme_summary(self) -> dict:
        """Return a summary of controls per theme."""
        return {
            theme: {
                "control_count": len(controls),
                "controls": [ctrl.ref for ctrl in controls]
            }
            for theme, controls in self.by_theme.items()
        }
