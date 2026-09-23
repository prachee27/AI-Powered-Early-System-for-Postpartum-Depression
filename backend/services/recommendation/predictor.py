from backend.services.recommendation.schemas import (
    RecommendationPrediction,
)

from backend.services.recommendation.config import (
    RECOMMENDATIONS,
)


class RecommendationPredictor:

    def predict(
        self,
        risk_level: str,
    ) -> RecommendationPrediction:

        if risk_level not in RECOMMENDATIONS:

            raise ValueError(
                f"Unknown risk level: {risk_level}"
            )

        return RecommendationPrediction(
            risk_level=risk_level,
            recommendations=RECOMMENDATIONS[risk_level]
        )