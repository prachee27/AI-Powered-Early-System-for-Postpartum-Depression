from dataclasses import dataclass
from backend.ml.behavior.schemas import BehaviorPrediction


@dataclass
class RiskEngineInput:
    emotion: str
    depression: str
    behavior: BehaviorPrediction
    epds: str
    trend: str


@dataclass
class OverallRiskPrediction:
    risk_level: str
    risk_score: int
    confidence: float
    override_triggered: bool
    reasons: list[str]