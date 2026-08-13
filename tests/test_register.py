"""Unit tests for RiskRegister."""

import pytest
import json
from pathlib import Path
from datetime import datetime, timedelta
from risk_register.core.register import RiskRegister
from risk_register.core.risk_model import RiskLevel, RiskTreatment


class TestCRUD:
    def test_add(self, tmp_path):
        reg = RiskRegister(data_path=tmp_path / "test.json")
        risk = reg.add_risk("Tech", "Test Risk", "Desc", "Asset", "Owner", 3, 4)
        assert risk.risk_id.startswith("RISK-")
        assert len(reg.get_all()) == 1

    def test_update(self, tmp_path):
        reg = RiskRegister(data_path=tmp_path / "test.json")
        risk = reg.add_risk("Legal", "GDPR", "Desc", "Data", "DPO", 3, 3)
        updated = reg.update_risk(risk.risk_id, status="Mitigated")
        assert updated.status == "Mitigated"

    def test_delete(self, tmp_path):
        reg = RiskRegister(data_path=tmp_path / "test.json")
        risk = reg.add_risk("Ops", "Backup", "Desc", "Server", "Ops", 3, 3)
        assert reg.delete_risk(risk.risk_id) is True
        assert len(reg.get_all()) == 0

    def test_get_nonexistent(self, tmp_path):
        reg = RiskRegister(data_path=tmp_path / "test.json")
        assert reg.get_risk("NONEXISTENT") is None


class TestQueries:
    @pytest.fixture
    def reg(self, tmp_path):
        r = RiskRegister(data_path=tmp_path / "test.json")
        r.add_risk("Technical", "SQL Injection", "SQLi desc", "Web App", "Dev", 5, 5)
        r.add_risk("Legal", "GDPR", "GDPR desc", "DB", "DPO", 2, 4)
        r.add_risk("Operational", "Outage", "Outage desc", "Server", "Ops", 3, 4)
        r.add_risk("Technical", "XSS", "XSS desc", "Web App", "Dev", 4, 3)
        return r

    def test_filter_status(self, reg, tmp_path):
        open_risks = reg.filter_by_status("Open")
        assert len(open_risks) == 4

    def test_filter_level(self, reg):
        critical = reg.filter_by_level(RiskLevel.CRITICAL)
        assert len(critical) >= 1  # SQL Injection (5,5)

    def test_filter_category(self, reg):
        tech = reg.filter_by_category("Technical")
        assert len(tech) == 2

    def test_search(self, reg):
        results = reg.search("SQL")
        assert len(results) >= 1


class TestStatistics:
    @pytest.fixture
    def reg(self, tmp_path):
        r = RiskRegister(data_path=tmp_path / "test.json")
        r.add_risk("Tech", "Risk A", "", "A", "O", 5, 5)  # 25 - Critical
        r.add_risk("Tech", "Risk B", "", "B", "O", 4, 4)  # 16 - High
        r.add_risk("Legal", "Risk C", "", "C", "O", 2, 2)  # 4 - Low
        r.add_risk("Legal", "Risk D", "", "D", "O", 3, 3)  # 9 - Medium
        r.add_risk("Ops", "Risk E", "", "E", "O", 1, 1)    # 1 - Low
        return r

    def test_total(self, reg):
        stats = reg.get_statistics()
        assert stats["total_risks"] == 5

    def test_level_dist(self, reg):
        stats = reg.get_statistics()
        assert stats["by_level"]["Critical"] == 1
        assert stats["by_level"]["High"] == 1
        assert stats["by_level"]["Medium"] == 1
        assert stats["by_level"]["Low"] == 2

    def test_avg(self, reg):
        stats = reg.get_statistics()
        expected_avg = (25 + 16 + 4 + 9 + 1) / 5  # = 11.0
        assert abs(stats["average_score"] - expected_avg) < 0.01


class TestPersistence:
    def test_save_load(self, tmp_path):
        path = tmp_path / "persist.json"
        reg1 = RiskRegister(data_path=path)
        reg1.add_risk("Test", "Persisted", "Desc", "A", "O", 3, 3)
        reg2 = RiskRegister(data_path=path)
        assert len(reg2.get_all()) == 1
        assert reg2.get_all()[0].title == "Persisted"

    def test_export_json(self, tmp_path):
        reg = RiskRegister(data_path=tmp_path / "src.json")
        reg.add_risk("T", "Export", "", "A", "O", 4, 4)
        path = tmp_path / "out.json"
        reg.export_json(path)
        assert path.exists()
        data = json.loads(path.read_text())
        assert len(data) == 1


class TestOverdue:
    def test_overdue(self, tmp_path):
        reg = RiskRegister(data_path=tmp_path / "test.json")
        past = datetime.now() - timedelta(days=30)
        reg.add_risk("T", "Old", "", "A", "O", 3, 3, review_date=past)
        future = datetime.now() + timedelta(days=30)
        reg.add_risk("T", "New", "", "B", "O", 3, 3, review_date=future)
        overdue = reg.get_overdue_risks()
        assert len(overdue) == 1
        assert overdue[0].title == "Old"
