from dataclasses import dataclass


@dataclass
class DepressionPrediction:

    label: str

    score: float