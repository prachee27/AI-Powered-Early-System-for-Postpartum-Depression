from backend.ml.behavior.config import BEHAVIOR_KEYWORDS
from backend.ml.behavior.schemas import BehaviorPrediction
from backend.ml.behavior.utils import normalize_text


class BehaviorPredictor:

    def __init__(self):
        self.behavior_keywords = BEHAVIOR_KEYWORDS

    def predict(self, text: str) -> BehaviorPrediction:

        text = normalize_text(text)

        results = {}

        for behavior, keywords in self.behavior_keywords.items():

            detected = any(
                normalize_text(keyword) in text
                for keyword in keywords
            )

            results[behavior] = detected

        return BehaviorPrediction(**results)
