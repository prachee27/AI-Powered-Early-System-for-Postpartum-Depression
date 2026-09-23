from datetime import date
from typing import Dict

from pydantic import BaseModel, Field, field_validator

from backend.ml.trend.schemas import DailyAnalysis


class AnalyzeRequest(BaseModel):
    """Weekly check-in: journal plus the full ten-question EPDS form.

    ``history`` holds up to six preceding daily check-ins. The API adds today's
    analysis as the seventh point when enough history is available.
    """
    patient_id: str = Field(min_length=1, max_length=128)
    doctor_email: str = Field(min_length=5, max_length=254, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    doctor_alert_consent: bool
    assessment_date: date
    journal: str = Field(min_length=1, max_length=10_000)
    epds_answers: Dict[int, int]
    history: list[DailyAnalysis] = Field(default_factory=list, max_length=6)
    # Demo mode allows repeatable presentation/testing without modifying the
    # seven-day production schedule.
    enforce_weekly_schedule: bool = False

    @field_validator("doctor_alert_consent")
    @classmethod
    def require_doctor_alert_consent(cls, consent: bool) -> bool:
        if not consent:
            raise ValueError("Consent is required before a critical alert can be sent to the doctor.")
        return consent

    @field_validator("epds_answers")
    @classmethod
    def validate_epds_answers(cls, answers: Dict[int, int]) -> Dict[int, int]:
        if set(answers) != set(range(1, 11)):
            raise ValueError("EPDS answers must include questions 1 through 10 exactly once.")
        if any(answer not in range(4) for answer in answers.values()):
            raise ValueError("Each EPDS answer must be an integer from 0 to 3.")
        return answers

    @field_validator("history")
    @classmethod
    def validate_history(cls, history: list[DailyAnalysis]) -> list[DailyAnalysis]:
        if len(history) > 6:
            raise ValueError("History can contain at most 6 previous daily assessments.")
        valid_emotions = {"Happy", "Neutral", "Sad", "Very Sad"}
        valid_depression = {"Depressed", "Not Depressed"}
        valid_epds_risks = {None, "Low", "Moderate", "High"}
        for index, day in enumerate(history, start=1):
            if day.emotion not in valid_emotions:
                raise ValueError(f"History day {index} has an invalid emotion label.")
            if day.depression not in valid_depression:
                raise ValueError(f"History day {index} has an invalid depression label.")
            if not 0 <= day.behavior_count <= 7:
                raise ValueError(f"History day {index} behavior_count must be from 0 to 7.")
            if day.epds_risk not in valid_epds_risks:
                raise ValueError(f"History day {index} has an invalid EPDS risk label.")
        return history


class DailyCheckInRequest(BaseModel):
    """Daily journal/voice check-in. It deliberately has no EPDS answers."""

    patient_id: str = Field(min_length=1, max_length=128)
    doctor_email: str = Field(min_length=5, max_length=254, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    doctor_alert_consent: bool
    check_in_date: date
    journal: str = Field(min_length=1, max_length=10_000)
    latest_epds_risk: str = "Low"
    # The client sends up to the previous six daily summaries. Together with
    # today's result they form the seven-day trend window.
    history: list[DailyAnalysis] = Field(default_factory=list, max_length=6)

    @field_validator("doctor_alert_consent")
    @classmethod
    def require_doctor_alert_consent(cls, consent: bool) -> bool:
        if not consent:
            raise ValueError("Consent is required before a critical alert can be sent to the doctor.")
        return consent

    @field_validator("latest_epds_risk")
    @classmethod
    def validate_latest_epds_risk(cls, risk: str) -> str:
        if risk not in {"Low", "Moderate", "High"}:
            raise ValueError("latest_epds_risk must be Low, Moderate, or High.")
        return risk
