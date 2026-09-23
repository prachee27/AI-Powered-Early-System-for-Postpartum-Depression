from backend.api.routes import _apply_assessment_context


def test_self_harm_epds_never_displays_happy_emotion():
    assert _apply_assessment_context("Happy", "Not Depressed", "High", True) == "Very Sad"


def test_high_epds_never_displays_happy_or_neutral_emotion():
    assert _apply_assessment_context("Happy", "Not Depressed", "High") == "Sad"
    assert _apply_assessment_context("Neutral", "Not Depressed", "High") == "Sad"
