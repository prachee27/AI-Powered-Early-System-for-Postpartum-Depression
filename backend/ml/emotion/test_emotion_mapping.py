from backend.api.routes import _normalize_emotion


def test_every_go_emotions_label_has_a_safe_public_label():
    labels = {
        "admiration", "amusement", "anger", "annoyance", "approval", "caring",
        "confusion", "curiosity", "desire", "disappointment", "disapproval",
        "disgust", "embarrassment", "excitement", "fear", "gratitude", "grief",
        "joy", "love", "nervousness", "optimism", "pride", "realization", "relief",
        "remorse", "sadness", "surprise", "neutral",
    }
    results = {
        _normalize_emotion({"top_emotions": [{"label": label}]})
        for label in labels
    }
    assert results <= {"Happy", "Neutral", "Sad", "Very Sad"}


def test_unknown_emotion_still_generates_a_safe_label():
    assert _normalize_emotion({"top_emotions": [{"label": "new_model_label"}]}) == "Neutral"
