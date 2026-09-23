from fastapi.testclient import TestClient

from backend.api import routes
from backend.main import app
from backend.ml.depression.schemas import DepressionPrediction
from backend.services.scheduling.epds_schedule import EPDSSchedule


class _Emotion:
    def predict(self, _text):
        return {"top_emotions": [{"label": "sadness", "score": 0.9}]}


class _Depression:
    def predict(self, _text):
        return DepressionPrediction(label="Depressed", score=0.9)


def test_analyze_runs_the_complete_pipeline(monkeypatch, tmp_path):
    monkeypatch.setattr(routes, "_emotion_predictor", lambda: _Emotion())
    monkeypatch.setattr(routes, "_depression_predictor", lambda: _Depression())
    monkeypatch.setattr(
        routes, "_epds_schedule",
        lambda: EPDSSchedule(tmp_path / "assessments.db"),
    )

    response = TestClient(app).post("/analyze", json={
        "patient_id": "demo-patient",
        "doctor_email": "doctor@example.com",
        "doctor_alert_consent": True,
        "assessment_date": "2026-08-01",
        "journal": "I cannot sleep and I have been crying. I feel hopeless.",
        "epds_answers": {
            "1": 0, "2": 0, "3": 3, "4": 0, "5": 3,
            "6": 3, "7": 3, "8": 3, "9": 3, "10": 3,
        },
        "history": [
            {"emotion": "Happy", "depression": "Not Depressed", "behavior_count": 0},
            {"emotion": "Happy", "depression": "Not Depressed", "behavior_count": 0},
            {"emotion": "Neutral", "depression": "Not Depressed", "behavior_count": 1},
            {"emotion": "Sad", "depression": "Depressed", "behavior_count": 2},
            {"emotion": "Sad", "depression": "Depressed", "behavior_count": 2},
            {"emotion": "Very Sad", "depression": "Depressed", "behavior_count": 3},
        ],
    })

    assert response.status_code == 200, response.text
    result = response.json()
    assert result["emotion"] == "Sad"
    assert result["depression"] == "Depressed"
    assert {"sleep_disturbance", "crying", "hopelessness"} <= set(result["behaviors"])
    assert result["epds"] == "Low"
    assert result["summary"].startswith("Overall Risk Level:")
    assert result["next_epds_assessment_due"] == "2026-08-08"
