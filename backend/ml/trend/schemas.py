from dataclasses import dataclass


@dataclass
class DailyAnalysis:
    emotion: str
    depression: str
    behavior_count: int
    epds_risk: str | None = None


@dataclass
class TrendPrediction:
    trend: str
    average_score: float
    score_change: float