from backend.ml.trend.schemas import DailyAnalysis

from backend.ml.trend.config import (
    EMOTION_SCORES,
    DEPRESSION_SCORES,
    EPDS_RISK_SCORES,
)


def calculate_daily_score(day: DailyAnalysis) -> int:
    """
    Calculate the severity score for a single day's analysis.
    """

    emotion_score = EMOTION_SCORES[day.emotion]

    depression_score = DEPRESSION_SCORES[day.depression]

    behavior_score = day.behavior_count

    epds_score = EPDS_RISK_SCORES[day.epds_risk]

    total_score = (
        emotion_score
        + depression_score
        + behavior_score
        + epds_score
    )

    return total_score


def calculate_average(scores: list[int]) -> float:
    """
    Calculate the average of a list of scores.
    """

    return sum(scores) / len(scores)