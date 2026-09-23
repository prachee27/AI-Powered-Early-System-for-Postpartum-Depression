from dataclasses import dataclass


@dataclass
class RecommendationPrediction:
    risk_level: str
    recommendations: list[str]