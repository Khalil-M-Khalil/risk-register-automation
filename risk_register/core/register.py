"""Risk Register — CRUD operations, filtering, aggregation & persistence."""

import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from risk_register.core.risk_model import (
    Risk,
    RiskLevel,
    RiskTreatment,
    Likelihood,
    Impact,
)


class RiskRegister:
    """
    Central registry for managing risks.

    Provides:
    - Add/update/delete risks
    - Filter by status, level, category, owner
    - Aggregate statistics
    - Export to JSON/Excel/PDF
    """

    def __init__(self, data_path: Optional[Path] = None):
        self._risks: dict[str, Risk] = {}
        self._data_path = data_path or Path.home() / ".risk_register_data.json"
        self._load()

    # ─── CRUD ───
    def add_risk(
        self,
        category: str,
        title: str,
        description: str,
        asset: str,
        owner: str,
        likelihood: int = 3,
        impact: int = 3,
        iso_controls: Optional[list] = None,
        treatment: RiskTreatment = RiskTreatment.MITIGATE,
        mitigation_plan: str = "",
        review_date: Optional[datetime] = None,
    ) -> Risk:
        """Create and register a new risk."""
        risk = Risk(
            category=category,
            title=title,
            description=description,
            asset=asset,
            owner=owner,
            likelihood=likelihood,
            impact=impact,
            iso_controls=iso_controls or [],
            treatment=treatment,
            mitigation_plan=mitigation_plan,
            review_date=review_date,
        )
        self._risks[risk.risk_id] = risk
        self._save()
        return risk

    def update_risk(self, risk_id: str, **kwargs) -> Optional[Risk]:
        """Update an existing risk and keep derived metrics consistent."""
        risk = self._risks.get(risk_id)
        if not risk:
            return None

        if "likelihood" in kwargs or "impact" in kwargs:
            risk.update_scores(
                likelihood=kwargs.pop("likelihood", None),
                impact=kwargs.pop("impact", None),
            )

        for key, value in kwargs.items():
            if not hasattr(risk, key) or key in {"risk_score", "risk_level", "created_at", "updated_at"}:
                continue
            if key == "treatment" and isinstance(value, str):
                value = RiskTreatment(value)
            if key == "iso_controls":
                value = list(dict.fromkeys(value))
            setattr(risk, key, value)

        risk.updated_at = datetime.now()
        self._save()
        return risk

    def delete_risk(self, risk_id: str) -> bool:
        """Delete a risk from the register."""
        if risk_id in self._risks:
            del self._risks[risk_id]
            self._save()
            return True
        return False

    def get_risk(self, risk_id: str) -> Optional[Risk]:
        """Retrieve a single risk."""
        return self._risks.get(risk_id)

    # ─── Queries ───
    def get_all(self) -> list[Risk]:
        """Return all risks."""
        return list(self._risks.values())

    def filter_by_status(self, status: str) -> list[Risk]:
        """Filter risks by status (Open, Closed, Mitigated, Accepted)."""
        return [r for r in self._risks.values() if r.status == status]

    def filter_by_level(self, level: RiskLevel) -> list[Risk]:
        """Filter risks by risk level."""
        return [r for r in self._risks.values() if r.risk_level == level]

    def filter_by_category(self, category: str) -> list[Risk]:
        """Filter risks by category."""
        return [r for r in self._risks.values() if r.category.lower() == category.lower()]

    def filter_by_owner(self, owner: str) -> list[Risk]:
        """Filter risks by owner."""
        return [r for r in self._risks.values() if owner.lower() in r.owner.lower()]

    def search(self, query: str) -> list[Risk]:
        """Full-text search across all text fields."""
        q = query.lower()
        results = []
        for risk in self._risks.values():
            fields = [
                risk.title, risk.description, risk.category,
                risk.asset, risk.owner, str(risk.risk_level.value),
                " ".join(risk.iso_controls), risk.mitigation_plan,
            ]
            if any(q in field.lower() for field in fields):
                results.append(risk)
        return results

    # ─── Statistics ───
    def get_statistics(self) -> dict:
        """Generate aggregate statistics for the register."""
        risks = self._risks.values()
        total = len(risks)

        by_level = {}
        for level in RiskLevel:
            by_level[level.value] = len([r for r in risks if r.risk_level == level])

        by_category = {}
        for r in risks:
            by_category.setdefault(r.category, 0)
            by_category[r.category] += 1

        open_count = len([r for r in risks if r.status == "Open"])
        closed_count = len([r for r in risks if r.status == "Closed"])
        mitigated_count = len([r for r in risks if r.status == "Mitigated"])
        accepted_count = len([r for r in risks if r.status == "Accepted"])

        avg_score = sum(r.risk_score for r in risks) / total if total else 0

        critical_risks = [r for r in risks if r.risk_level == RiskLevel.CRITICAL]
        high_risks = [r for r in risks if r.risk_level == RiskLevel.HIGH]

        return {
            "total_risks": total,
            "by_level": by_level,
            "by_category": by_category,
            "status_distribution": {
                "Open": open_count,
                "Closed": closed_count,
                "Mitigated": mitigated_count,
                "Accepted": accepted_count,
            },
            "average_score": round(avg_score, 2),
            "critical_risks": critical_risks,
            "high_risks": high_risks,
            "generated_at": datetime.now().isoformat(),
        }

    def get_overdue_risks(self) -> list[Risk]:
        """Return risks whose review_date has passed."""
        today = datetime.now()
        return [r for r in self._risks.values()
                if r.review_date and r.review_date < today]

    # ─── Persistence ───
    def _save(self):
        """Save register to JSON file."""
        data = {rid: risk.to_dict() for rid, risk in self._risks.items()}
        Path(self._data_path).parent.mkdir(parents=True, exist_ok=True)
        with open(self._data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)

    def _load(self):
        """Load register from JSON file."""
        if not Path(self._data_path).exists():
            return
        try:
            with open(self._data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for rid, risk_data in data.items():
                self._risks[rid] = Risk.from_dict(risk_data)
        except (json.JSONDecodeError, KeyError):
            self._risks = {}

    def export_json(self, path: Path) -> str:
        """Export full register to JSON file."""
        data = {rid: risk.to_dict() for rid, risk in self._risks.items()}
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
        return str(path)

    def import_json(self, path: Path) -> int:
        """Import risks from JSON file. Returns count of imported risks."""
        data = json.loads(path.read_text(encoding="utf-8"))
        count = 0
        for rid, risk_data in data.items():
            risk = Risk.from_dict(risk_data)
            self._risks[risk.risk_id if risk.risk_id else f"RISK-IMPORT-{uuid.uuid4().hex[:8]}" ] = risk
            count += 1
        self._save()
        return count
