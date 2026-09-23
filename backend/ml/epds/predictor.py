from backend.ml.epds.config import (
    EPDS_CONFIG,
    TOTAL_EPDS_QUESTIONS,
    LOW_RISK_MAX,
    MODERATE_RISK_MAX,
)

from backend.ml.epds.schemas import EPDSPrediction


class EPDSPredictor:

    def predict(self, answers: dict[int, int]) -> EPDSPrediction:

        if len(answers) != TOTAL_EPDS_QUESTIONS:
            raise ValueError(
                f"EPDS requires exactly {TOTAL_EPDS_QUESTIONS} answers."
            )

        total_score = 0

        for question_number, selected_option in answers.items():

            if question_number not in EPDS_CONFIG:
                raise ValueError(
                    f"Invalid question number: {question_number}"
                )

            question = EPDS_CONFIG[question_number]

            if selected_option not in question["score_map"]:
                raise ValueError(
                    f"Invalid option selected for Question {question_number}"
                )

            total_score += question["score_map"][selected_option]

        if total_score <= LOW_RISK_MAX:
            risk_level = "Low"

        elif total_score <= MODERATE_RISK_MAX:
            risk_level = "Moderate"

        else:
            risk_level = "High"

        return EPDSPrediction(
            score=total_score,
            risk_level=risk_level,
            # Question 10 is the EPDS self-harm item. Option 3 is "Never";
            # every other response requires the risk-engine safety override.
            self_harm_risk=answers[10] != 3,
        )
