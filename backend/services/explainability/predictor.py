from backend.services.explainability.schemas import (
    ExplainabilityPrediction,
)


class ExplainabilityPredictor:

    def predict(
        self,
        risk_level: str,
        reasons: list[str],
        recommendations: list[str],
    ) -> ExplainabilityPrediction:

        summary = f"Overall Risk Level: {risk_level}"

        explanation = (
            f"The assessment indicates a {risk_level.lower()} risk of "
            f"postpartum depression.\n\n"
        )

        if reasons:

            explanation += "Reasons:\n"

            for reason in reasons:
                explanation += f"- {reason}\n"

        if recommendations:

            explanation += "\nRecommended Actions:\n"

            for recommendation in recommendations:
                explanation += f"- {recommendation}\n"

        return ExplainabilityPrediction(
            summary=summary,
            explanation=explanation,
        )