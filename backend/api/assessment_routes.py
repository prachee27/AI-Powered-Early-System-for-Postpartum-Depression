from fastapi import APIRouter

from backend.ml.epds.predictor import EPDSPredictor
from backend.ml.trend.predictor import TrendPredictor

from backend.ml.risk_engine.predictor import RiskEnginePredictor
from backend.services.recommendation.predictor import RecommendationPredictor
from backend.services.explainability.predictor import ExplainabilityPredictor

from backend.ml.trend.schemas import DailyAnalysis

from backend.ml.behavior.schemas import BehaviorPrediction

router = APIRouter(
    prefix="/assessment",
    tags=["Weekly Assessment"]
)

epds_predictor = EPDSPredictor()
trend_predictor = TrendPredictor()
risk_predictor = RiskEnginePredictor()
recommendation_predictor = RecommendationPredictor()
explainability_predictor = ExplainabilityPredictor()


@router.post("/")
def weekly_assessment():

    epds_answers = {
        1: 1,
        2: 0,
        3: 1,
        4: 2,
        5: 1,
        6: 0,
        7: 1,
        8: 0,
        9: 0,
        10: 0,
    }

    epds = epds_predictor.predict(epds_answers)

    history = [
        DailyAnalysis("Happy", "Not Depressed", 1, "Low"),
        DailyAnalysis("Happy", "Not Depressed", 1, "Low"),
        DailyAnalysis("Neutral", "Not Depressed", 2, "Low"),
        DailyAnalysis("Sad", "Depressed", 4, "Moderate"),
        DailyAnalysis("Sad", "Depressed", 5, "Moderate"),
        DailyAnalysis("Very Sad", "Depressed", 6, "High"),
        DailyAnalysis("Very Sad", "Depressed", 6, "High"),
    ]

    trend = trend_predictor.predict(history)

    behavior = BehaviorPrediction(
        sleep_disturbance=True,
        appetite_change=True,
        crying=True,
        hopelessness=False,
        bonding_issue=False,
        social_withdrawal=True,
        anxiety=True,
        self_harm_risk=False,
    )

    risk = risk_predictor.predict(
        emotion="Very Sad",
        depression="Depressed",
        behavior=behavior,
        epds=epds.risk_level,
        trend=trend.trend,
    )

    recommendation = recommendation_predictor.predict(
    risk.risk_level
    )

    explainability = explainability_predictor.predict(
    risk_level=risk.risk_level,
    reasons=risk.reasons,
    recommendations=recommendation.recommendations,
    )
    
    return {
    "epds": epds,
    "trend": trend,
    "risk": risk,
    "recommendation": recommendation,
    "explainability": explainability,
}