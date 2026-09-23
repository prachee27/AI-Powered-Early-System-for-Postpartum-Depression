from backend.services.notifications.doctor_alert import AlertResult


class _AlertService:
    def __init__(self):
        self.calls = []

    def send_critical_alert(self, **kwargs):
        self.calls.append(kwargs)
        return AlertResult(True, f"Critical alert sent to {kwargs['doctor_email']}.")


def test_critical_assessment_sends_a_doctor_alert(monkeypatch):
    from datetime import date
    from fastapi.testclient import TestClient

    from backend.api import routes
    from backend.main import app

    service = _AlertService()
    monkeypatch.setattr(routes, "_doctor_alert_service", lambda: service)
    response = TestClient(app).post("/analyze", json={
        "patient_id": "demo-patient",
        "doctor_email": "doctor@example.com",
        "doctor_alert_consent": True,
        "assessment_date": str(date.today()),
        "journal": "I feel hopeless.",
        "epds_answers": {"1": 3, "2": 3, "3": 0, "4": 3, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0},
        "history": [],
    })
    assert response.status_code == 200, response.text
    assert response.json()["critical_alert_sent"] is True
    assert service.calls[0]["doctor_email"] == "doctor@example.com"
