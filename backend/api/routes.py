"""End-to-end analysis endpoint for the PPD early-warning system."""

from functools import lru_cache
from datetime import date, timedelta
import logging

from fastapi import APIRouter, HTTPException

from backend.ml.emotion.utils import EMOTION_MAPPING
from backend.schemas.request import AnalyzeRequest, DailyCheckInRequest
from backend.schemas.response import AnalyzeResponse
from backend.services.scheduling.epds_schedule import EPDSSchedule
from backend.services.notifications.doctor_alert import DoctorAlertService, AlertResult
from backend.ml.trend.schemas import DailyAnalysis

router = APIRouter(tags=["Analysis"])
logger = logging.getLogger(__name__)


@lru_cache
def _emotion_predictor():
    """Load the optional transformer only when an analysis is requested."""
    from backend.ml.emotion.predictor import EmotionPredictor
    return EmotionPredictor()


@lru_cache
def _depression_predictor():
    from backend.ml.depression.predictor import DepressionPredictor
    return DepressionPredictor()


@lru_cache
def _behavior_predictor():
    from backend.ml.behavior.predictor import BehaviorPredictor
    return BehaviorPredictor()


@lru_cache
def _epds_predictor():
    from backend.ml.epds.predictor import EPDSPredictor
    return EPDSPredictor()


@lru_cache
def _trend_predictor():
    from backend.ml.trend.predictor import TrendPredictor
    return TrendPredictor()


@lru_cache
def _risk_predictor():
    from backend.ml.risk_engine.predictor import RiskEnginePredictor
    return RiskEnginePredictor()


@lru_cache
def _recommendation_predictor():
    from backend.services.recommendation.predictor import RecommendationPredictor
    return RecommendationPredictor()


@lru_cache
def _explainability_predictor():
    from backend.services.explainability.predictor import ExplainabilityPredictor
    return ExplainabilityPredictor()


@lru_cache
def _epds_schedule():
    return EPDSSchedule()


@lru_cache
def _doctor_alert_service():
    return DoctorAlertService()


def _normalize_emotion(raw_result: dict) -> str:
    """Map GoEmotions labels onto the four public API labels."""
    top_emotions = raw_result.get("top_emotions", [])
    if not top_emotions:
        raise ValueError("Emotion model returned no labels.")

    raw_label = str(top_emotions[0].get("label", "")).strip()
    if raw_label in {"Happy", "Neutral", "Sad", "Very Sad"}:
        return raw_label
    normalized_label = raw_label.lower()
    if normalized_label in EMOTION_MAPPING:
        return EMOTION_MAPPING[normalized_label]

    # A model update must never prevent a safety report from being generated.
    # Unknown labels are kept neutral rather than being interpreted as distress.
    logger.warning("Unsupported emotion label '%s'; treating it as Neutral.", raw_label)
    return "Neutral"


def _detected_behaviors(behavior) -> list[str]:
    return [name for name, detected in vars(behavior).items() if detected]


def _build_daily_analysis(emotion: str, depression: str, behavior, epds_risk: str) -> DailyAnalysis:
    return DailyAnalysis(
        emotion=emotion,
        depression=depression,
        behavior_count=len(_detected_behaviors(behavior)),
        epds_risk=epds_risk,
    )


def _apply_assessment_context(emotion: str, depression: str, epds_risk: str, epds_self_harm_risk: bool = False) -> str:
    """Prevent a positive model label from masking severe screening signals."""
    if epds_self_harm_risk:
        return "Very Sad"
    if epds_risk == "High" and emotion in {"Happy", "Neutral"}:
        return "Sad"
    if depression == "Depressed" and emotion == "Happy":
        return "Sad"
    return emotion


def _critical_alert(doctor_email: str, patient_id: str, risk_level: str) -> AlertResult:
    if risk_level != "Critical":
        return AlertResult(False, "No doctor alert required for this risk level.")
    return _doctor_alert_service().send_critical_alert(
        doctor_email=doctor_email, patient_id=patient_id, risk_level=risk_level
    )


@router.get("/epds-status/{patient_id}")
def epds_status(patient_id: str):
    """Return whether the weekly EPDS questionnaire is due for this browser user."""
    next_due_date = _epds_schedule().next_due_date(patient_id)
    return {
        "epds_due": next_due_date is None or date.today() >= next_due_date,
        "next_epds_assessment_due": next_due_date.isoformat() if next_due_date else None,
    }


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """Run the weekly EPDS assessment (available once every seven days)."""
    try:
        emotion = _normalize_emotion(_emotion_predictor().predict(request.journal))
        depression = _depression_predictor().predict(request.journal).label
        behavior = _behavior_predictor().predict(request.journal)
        epds = _epds_predictor().predict(request.epds_answers)
        emotion = _apply_assessment_context(
            emotion, depression, epds.risk_level, epds.self_harm_risk
        )
        today = _build_daily_analysis(emotion, depression, behavior, epds.risk_level)
        # A combined weekly trend is calculated only when there are six real
        # preceding daily check-ins. A first-time assessment still receives a
        # journal-and-EPDS report without inventing seven days of history.
        trend = _trend_predictor().predict([*request.history, today]).trend if len(request.history) == 6 else "Stable"
        risk = _risk_predictor().predict(
            emotion=emotion, depression=depression, behavior=behavior,
            epds=epds.risk_level, trend=trend,
            epds_self_harm_risk=epds.self_harm_risk,
        )
        recommendation = _recommendation_predictor().predict(risk.risk_level)
        explainability = _explainability_predictor().predict(
            risk_level=risk.risk_level,
            reasons=risk.reasons,
            recommendations=recommendation.recommendations,
        )
        # Persist only a completed assessment.  A failed model call must not
        # make a patient wait seven days before retrying.
        next_epds_assessment_due = (
            _epds_schedule().submit(request.patient_id, request.assessment_date)
            if request.enforce_weekly_schedule
            else request.assessment_date + timedelta(days=7)
        )
        alert = _critical_alert(request.doctor_email, request.patient_id, risk.risk_level)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Analysis pipeline could not complete")
        raise HTTPException(
            status_code=503,
            detail="Analysis service is temporarily unavailable. Please try again.",
        ) from exc

    return AnalyzeResponse(
        emotion=emotion,
        depression=depression,
        behaviors=_detected_behaviors(behavior),
        epds=epds.risk_level,
        overall_risk=risk.risk_level,
        confidence=risk.confidence,
        recommendations=recommendation.recommendations,
        summary=explainability.summary,
        explanation=explainability.explanation,
        next_epds_assessment_due=next_epds_assessment_due,
        critical_alert_sent=alert.sent,
        critical_alert_message=alert.message,
    )


@router.post("/daily-check-in", response_model=AnalyzeResponse)
def daily_check_in(request: DailyCheckInRequest) -> AnalyzeResponse:
    """Analyse a daily journal entry without presenting EPDS questions.

    If the caller provides six preceding daily summaries, the current entry
    completes the seven-day window and receives a calculated trend. Before
    that, the trend is reported as Stable instead of inventing a trend from
    insufficient data.
    """
    try:
        emotion = _normalize_emotion(_emotion_predictor().predict(request.journal))
        depression = _depression_predictor().predict(request.journal).label
        behavior = _behavior_predictor().predict(request.journal)
        emotion = _apply_assessment_context(
            emotion, depression, request.latest_epds_risk
        )

        today = _build_daily_analysis(
            emotion, depression, behavior, request.latest_epds_risk
        )
        if len(request.history) == 6:
            trend = _trend_predictor().predict([*request.history, today]).trend
        else:
            trend = "Stable"

        risk = _risk_predictor().predict(
            emotion=emotion,
            depression=depression,
            behavior=behavior,
            epds=request.latest_epds_risk,
            trend=trend,
        )
        recommendation = _recommendation_predictor().predict(risk.risk_level)
        explainability = _explainability_predictor().predict(
            risk_level=risk.risk_level,
            reasons=risk.reasons,
            recommendations=recommendation.recommendations,
        )
        next_epds_assessment_due = _epds_schedule().next_due_date(request.patient_id)
        alert = _critical_alert(request.doctor_email, request.patient_id, risk.risk_level)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Daily check-in pipeline could not complete")
        raise HTTPException(
            status_code=503,
            detail="Analysis service is temporarily unavailable. Please try again.",
        ) from exc

    return AnalyzeResponse(
        emotion=emotion,
        depression=depression,
        behaviors=_detected_behaviors(behavior),
        epds=request.latest_epds_risk,
        overall_risk=risk.risk_level,
        confidence=risk.confidence,
        recommendations=recommendation.recommendations,
        summary=explainability.summary,
        explanation=explainability.explanation,
        # If an initial EPDS has not been completed, it is due now.
        next_epds_assessment_due=next_epds_assessment_due or request.check_in_date,
        critical_alert_sent=alert.sent,
        critical_alert_message=alert.message,
    )
