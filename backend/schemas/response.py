from datetime import date

from pydantic import BaseModel


class AnalyzeResponse(BaseModel):

    emotion: str

    depression: str

    behaviors: list[str]

    epds: str

    overall_risk: str

    confidence: float

    recommendations: list[str]

    summary: str

    explanation: str

    next_epds_assessment_due: date

    critical_alert_sent: bool = False
    critical_alert_message: str | None = None
