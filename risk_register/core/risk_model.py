"""Risk model with scoring and ISO 27001 Annex A mapping."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, IntEnum
from typing import Optional


class RiskLevel(Enum):
    """Risk level classification based on score thresholds."""
    LOW = "Low"         # Score 1-4
    MEDIUM = "Medium"   # Score 5-9
    HIGH = "High"       # Score 10-16
    CRITICAL = "Critical"  # Score 17-25


class RiskTreatment(Enum):
    """Risk treatment options per ISO 27001."""
    AVOID = "Avoid"
    TRANSFER = "Transfer"
    MITIGATE = "Mitigate"
    ACCEPT = "Accept"
    SHARE = "Share"


class Likelihood(IntEnum):
    """Likelihood scale 1-5 (ISO 27005 aligned)."""
    RARE = 1      # May occur only in exceptional circumstances
    UNLIKELY = 2  # Could occur at some time
    POSSIBLE = 3  # Should occur at some time
    LIKELY = 4    # Will probably occur in most circumstances
    ALMOST_CERTAIN = 5  # Expected to occur in most circumstances


class Impact(IntEnum):
    """Impact scale 1-5 (ISO 27005 aligned)."""
    NEGLIGIBLE = 1    # No significant impact
    MINOR = 2         # Minor financial/operational impact
    MODERATE = 3      # Moderate impact requiring resources
    MAJOR = 4         # Major impact on operations/reputation
    SEVERE = 5        # Catastrophic impact (business-critical)


@dataclass
class Risk:
    """
    Represents a single risk entry in the register.

    Attributes:
        risk_id: Unique identifier (auto-generated)
        category: Risk category (e.g., 'Technical', 'Legal', 'Operational')
        title: Short descriptive title
        description: Detailed risk description
        asset: Asset/process affected
        owner: Risk owner (person/role)
        likelihood: Likelihood score 1-5
        impact: Impact score 1-5
        risk_score: Computed as likelihood * impact (1-25)
        risk_level: Derived from risk_score
        iso_controls: List of ISO 27001 Annex A control references
        treatment: Selected risk treatment option
        status: Current risk status
        created_at: Timestamp of risk creation
        updated_at: Timestamp of last update
        mitigation_plan: Description of mitigation steps
        review_date: Scheduled review date
    """

    risk_id: str = field(default_factory=lambda: f"RISK-{datetime.now().strftime('%Y%m%d')}-{hash(datetime.now().timestamp()) % 10000:04d}")
    category: str = ""
    title: str = ""
    description: str = ""
    asset: str = ""
    owner: str = ""
    likelihood: int = 3  # Default: Possible
    impact: int = 3      # Default: Moderate
    risk_score: int = field(init=False)
    risk_level: RiskLevel = field(init=False)
    iso_controls: list[str] = field(default_factory=list)
    treatment: RiskTreatment = RiskTreatment.MITIGATE
    status: str = "Open"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    mitigation_plan: str = ""
    review_date: Optional[datetime] = None

    def __post_init__(self):
        """Compute risk_score and risk_level after initialization."""
        self.risk_score = self.likelihood * self.impact
        self.risk_level = self._classify_risk()

    def _classify_risk(self) -> RiskLevel:
        """Classify risk level based on score."""
        if self.risk_score <= 4:
            return RiskLevel.LOW
        elif self.risk_score <= 9:
            return RiskLevel.MEDIUM
        elif self.risk_score <= 16:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL

    def update_scores(self, likelihood: Optional[int] = None, impact: Optional[int] = None):
        """Update likelihood/impact and recompute risk metrics."""
        if likelihood is not None:
            self.likelihood = Likelihood(likelihood)
        if impact is not None:
            self.impact = Impact(impact)
        self.updated_at = datetime.now()
        self.risk_score = self.likelihood * self.impact
        self.risk_level = self._classify_risk()

    def assign_iso_control(self, control_ref: str):
        """Add an ISO 27001 Annex A control reference."""
        if control_ref not in self.iso_controls:
            self.iso_controls.append(control_ref)
            self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """Serialize risk to dictionary."""
        return {
            "risk_id": self.risk_id,
            "category": self.category,
            "title": self.title,
            "description": self.description,
            "asset": self.asset,
            "owner": self.owner,
            "likelihood": self.likelihood,
            "impact": self.impact,
            "risk_score": self.risk_score,
            "risk_level": self.risk_level.value,
            "iso_controls": self.iso_controls,
            "treatment": self.treatment.value,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "mitigation_plan": self.mitigation_plan,
            "review_date": self.review_date.isoformat() if self.review_date else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Risk":
        """Deserialize risk from dictionary."""
        risk = cls(
            risk_id=data.get("risk_id", ""),
            category=data.get("category", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            asset=data.get("asset", ""),
            owner=data.get("owner", ""),
            likelihood=data.get("likelihood", 3),
            impact=data.get("impact", 3),
            iso_controls=data.get("iso_controls", []),
            treatment=RiskTreatment(data.get("treatment", "Mitigate")),
            status=data.get("status", "Open"),
            mitigation_plan=data.get("mitigation_plan", ""),
        )
        if data.get("created_at"):
            risk.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("updated_at"):
            risk.updated_at = datetime.fromisoformat(data["updated_at"])
        if data.get("review_date"):
            risk.review_date = datetime.fromisoformat(data["review_date"])
        return risk

    def __str__(self) -> str:
        """Human-readable representation."""
        return (f"{self.risk_id}: [{self.risk_level.value}] "
                f"{self.title} (Score: {self.risk_score})")


# ─── Risk Matrix ───
RISK_MATRIX_LABELS = {
    (1, 1): "Rare × Negligible",
    (5, 5): "Almost Certain × Severe",
    # ... (full 5x5 matrix reference)
}

RISK_THRESHOLD_TABLE = [
    ("Low", 1, 4, "Accept — monitor periodically"),
    ("Medium", 5, 9, "Mitigate — action plan required"),
    ("High", 10, 16, "Mitigate urgently — escalation required"),
    ("Critical", 17, 25, "Immediate action — executive escalation"),
]
