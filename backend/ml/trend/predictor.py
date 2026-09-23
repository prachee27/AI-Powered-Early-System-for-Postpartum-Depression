from backend.ml.trend.config import (
    TREND_THRESHOLD,
)

from backend.ml.trend.schemas import (
    DailyAnalysis,
    TrendPrediction,
)

from backend.ml.trend.utils import (
    calculate_daily_score,
    calculate_average,
)


class TrendPredictor:

    def predict(
        self,
        history: list[DailyAnalysis]
    ) -> TrendPrediction:

        if len(history) != 7:
            raise ValueError(
                "Trend Analysis requires exactly 7 days of history."
            )

        daily_scores = []

        for day in history:
            score = calculate_daily_score(day)
            daily_scores.append(score)

        previous_average = calculate_average(daily_scores[:3])

        recent_average = calculate_average(daily_scores[-3:])

        score_change = recent_average - previous_average

        overall_average = calculate_average(daily_scores)

        if score_change > TREND_THRESHOLD:
            trend = "Worsening"

        elif score_change < -TREND_THRESHOLD:
            trend = "Improving"

        else:
            trend = "Stable"

        return TrendPrediction(
            trend=trend,
            average_score=round(overall_average, 2),
            score_change=round(score_change, 2)
        )