from backend.ml.behavior.schemas import BehaviorPrediction
from backend.ml.risk_engine.config import (
    EMOTION_WEIGHTS,
    DEPRESSION_WEIGHTS,
    EPDS_WEIGHTS,
    TREND_WEIGHTS,
)


def calculate_risk_score(
    emotion: str,
    depression: str,
    behavior: BehaviorPrediction,
    epds: str,
    trend: str,
) -> int:
    """
    Calculate the total weighted risk score.
    """

    score = 0

    score += EMOTION_WEIGHTS[emotion]

    score += DEPRESSION_WEIGHTS[depression]

    score += EPDS_WEIGHTS[epds]

    score += TREND_WEIGHTS[trend]

    behavior_count = sum([
        behavior.sleep_disturbance,
        behavior.appetite_change,
        behavior.crying,
        behavior.hopelessness,
        behavior.bonding_issue,
        behavior.social_withdrawal,
        behavior.anxiety,
    ])

    score += behavior_count

    return score


def generate_reasons(
    emotion: str,
    depression: str,
    behavior: BehaviorPrediction,
    epds: str,
    trend: str,
) -> list[str]:

    reasons = []

    if emotion in ("Sad", "Very Sad"):
        reasons.append(f"Emotion detected: {emotion}")

    if depression == "Depressed":
        reasons.append("Depression detected")

    if behavior.sleep_disturbance:
        reasons.append("Sleep disturbance detected")

    if behavior.appetite_change:
        reasons.append("Appetite change detected")

    if behavior.crying:
        reasons.append("Frequent crying detected")

    if behavior.hopelessness:
        reasons.append("Hopelessness detected")

    if behavior.bonding_issue:
        reasons.append("Mother-infant bonding issue detected")

    if behavior.social_withdrawal:
        reasons.append("Social withdrawal detected")

    if behavior.anxiety:
        reasons.append("Anxiety symptoms detected")

    if behavior.self_harm_risk:
        reasons.append("Self-harm risk detected")

    if epds == "Moderate":
        reasons.append("Moderate EPDS risk")

    elif epds == "High":
        reasons.append("High EPDS risk")

    if trend == "Worsening":
        reasons.append("Symptoms worsening over the last week")

    return reasons


def calculate_confidence(score: int) -> float:
    """
    Convert the weighted score into a confidence value.
    """

    confidence = min(score / 21, 1.0)

    return round(confidence, 2)