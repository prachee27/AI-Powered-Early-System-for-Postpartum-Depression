from backend.services.recommendation.predictor import (
    RecommendationPredictor
)

predictor = RecommendationPredictor()


print("---------- LOW ----------")

print(
    predictor.predict("Low")
)

print("\n---------- MODERATE ----------")

print(
    predictor.predict("Moderate")
)

print("\n---------- HIGH ----------")

print(
    predictor.predict("High")
)

print("\n---------- CRITICAL ----------")

print(
    predictor.predict("Critical")
)

print("\n---------- INVALID ----------")

try:

    print(
        predictor.predict("Very High")
    )

except Exception as e:

    print(e)