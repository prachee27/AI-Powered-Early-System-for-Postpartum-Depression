from backend.services.explainability.predictor import (
    ExplainabilityPredictor,
)

predictor = ExplainabilityPredictor()

risk = "High"

reasons = [
    "Depression detected",
    "High EPDS risk",
    "Symptoms worsening over the last week",
    "Sleep disturbance detected",
]

recommendations = [
    "Consult a mental health professional.",
    "Continue daily monitoring.",
    "Inform a trusted family member.",
]

result = predictor.predict(
    risk_level=risk,
    reasons=reasons,
    recommendations=recommendations,
)

print(result.summary)
print()
print(result.explanation)