from dataclasses import dataclass


@dataclass
class ExplainabilityPrediction:
    summary: str
    explanation: str