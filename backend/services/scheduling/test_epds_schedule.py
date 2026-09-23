from datetime import date

import pytest

from backend.services.scheduling.epds_schedule import EPDSSchedule


def test_epds_can_only_be_submitted_once_per_week(tmp_path):
    schedule = EPDSSchedule(tmp_path / "assessment.db")

    assert schedule.submit("patient-1", date(2026, 8, 1)) == date(2026, 8, 8)
    assert schedule.next_due_date("patient-1") == date(2026, 8, 8)

    with pytest.raises(ValueError, match="2026-08-08"):
        schedule.submit("patient-1", date(2026, 8, 7))

    assert schedule.submit("patient-1", date(2026, 8, 8)) == date(2026, 8, 15)
