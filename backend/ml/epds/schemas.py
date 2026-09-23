from dataclasses import dataclass


@dataclass
class EPDSPrediction:
    score: int
    risk_level: str
    self_harm_risk: bool = False
