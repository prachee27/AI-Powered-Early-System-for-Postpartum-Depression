from backend.ml.behavior.schemas import BehaviorPrediction

from backend.ml.risk_engine.config import (
    LOW_RISK_MAX,
    MODERATE_RISK_MAX,
    HIGH_RISK_MAX,
)

from backend.ml.risk_engine.schemas import OverallRiskPrediction

from backend.ml.risk_engine.utils import (
    calculate_risk_score,
    calculate_confidence,
    generate_reasons,
)


class RiskEnginePredictor:

    def predict(
        self,
        emotion: str,
        depression: str,
        behavior: BehaviorPrediction,
        epds: str,
        trend: str,
        epds_self_harm_risk: bool = False,
    ) -> OverallRiskPrediction:

        if behavior.self_harm_risk or epds_self_harm_risk:
            reasons = generate_reasons(emotion, depression, behavior, epds, trend)
            if "Self-harm risk detected" not in reasons:
                reasons.insert(0, "Self-harm risk detected")

            return OverallRiskPrediction(
                risk_level="Critical",
                risk_score=21,
                confidence=1.0,
                override_triggered=True,
                reasons=reasons,
            )

        score = calculate_risk_score(
            emotion,
            depression,
            behavior,
            epds,
            trend,
        )

        if score <= LOW_RISK_MAX:
            risk = "Low"

        elif score <= MODERATE_RISK_MAX:
            risk = "Moderate"

        elif score <= HIGH_RISK_MAX:
            risk = "High"

        else:
            risk = "Critical"

        # A high EPDS screening result must never be shown as Low or Moderate.
        # A journal-based depression signal should likewise not be shown as Low.
        risk_rank = {"Low": 0, "Moderate": 1, "High": 2, "Critical": 3}
        minimum_risk = "High" if epds == "High" else "Moderate" if depression == "Depressed" else "Low"
        if risk_rank[risk] < risk_rank[minimum_risk]:
            risk = minimum_risk

        return OverallRiskPrediction(
            risk_level=risk,
            risk_score=score,
            confidence=calculate_confidence(score),
            override_triggered=False,
            reasons=generate_reasons(
                emotion,
                depression,
                behavior,
                epds,
                trend,
            ),
        )
