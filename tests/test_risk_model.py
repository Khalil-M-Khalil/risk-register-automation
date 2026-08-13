"""Unit tests for risk model core logic."""

import pytest
from datetime import datetime
from risk_register.core.risk_model import (
    Risk, RiskLevel, RiskTreatment, Likelihood, Impact
)


class TestRiskScoring:
    def test_low_risk(self):
        for s in [1, 2]:
            risk = Risk(likelihood=s, impact=s)
            assert risk.risk_score == s * s
            assert risk.risk_level == RiskLevel.LOW

    def test_medium_risk(self):
        for l, i in [(2, 3), (3, 2), (3, 3), (4, 2)]:
            risk = Risk(likelihood=l, impact=i)
            assert 5 <= risk.risk_score <= 9
            assert risk.risk_level == RiskLevel.MEDIUM

    def test_high_risk(self):
        for l, i in [(3, 4), (4, 3), (4, 4)]:
            risk = Risk(likelihood=l, impact=i)
            assert 10 <= risk.risk_score <= 16
            assert risk.risk_level == RiskLevel.HIGH

    def test_critical_risk(self):
        risk = Risk(likelihood=5, impact=5)
        assert risk.risk_score == 25
        assert risk.risk_level == RiskLevel.CRITICAL


class TestRiskSerialization:
    def test_to_dict(self):
        risk = Risk(
            risk_id="TEST-001", category="Technical", title="Test",
            description="Desc", asset="Server", owner="Admin",
            likelihood=4, impact=3, iso_controls=["A.9.1"],
            treatment=RiskTreatment.MITIGATE, status="Open",
        )
        data = risk.to_dict()
        assert data["risk_id"] == "TEST-001"
        assert data["risk_score"] == 12
        assert data["risk_level"] == "High"

    def test_roundtrip(self):
        original = Risk(
            risk_id="RT-001", category="Legal", title="GDPR Gap",
            description="Missing GDPR", asset="Data", owner="DPO",
            likelihood=3, impact=4, iso_controls=["A.18.4"],
            treatment=RiskTreatment.TRANSFER, status="Open",
            mitigation_plan="Engage counsel",
            review_date=datetime(2024, 12, 31),
        )
        restored = Risk.from_dict(original.to_dict())
        assert restored.risk_id == original.risk_id
        assert restored.iso_controls == original.iso_controls
        assert restored.review_date == original.review_date


class TestRiskUpdate:
    def test_update_likelihood(self):
        risk = Risk(likelihood=2, impact=4)
        risk.update_scores(likelihood=5)
        assert risk.risk_score == 20
        assert risk.risk_level == RiskLevel.CRITICAL

    def test_update_both(self):
        risk = Risk(likelihood=1, impact=1)
        risk.update_scores(likelihood=5, impact=5)
        assert risk.risk_score == 25


class TestISOControls:
    def test_assign(self):
        risk = Risk(title="Test")
        risk.assign_iso_control("A.9.1")
        assert "A.9.1" in risk.iso_controls

    def test_no_duplicates(self):
        risk = Risk(title="Test")
        risk.assign_iso_control("A.9.1")
        risk.assign_iso_control("A.9.1")
        assert risk.iso_controls.count("A.9.1") == 1
