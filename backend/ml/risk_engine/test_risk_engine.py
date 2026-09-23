from backend.ml.behavior.schemas import BehaviorPrediction

from backend.ml.risk_engine.predictor import RiskEnginePredictor

predictor = RiskEnginePredictor()


print("---------- LOW ----------")

behavior = BehaviorPrediction(
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
)

print(
    predictor.predict(
        emotion="Happy",
        depression="Not Depressed",
        behavior=behavior,
        epds="Low",
        trend="Improving",
    )
)


print("\n---------- HIGH ----------")

behavior = BehaviorPrediction(
    True,
    True,
    True,
    True,
    False,
    True,
    True,
    False,
)

print(
    predictor.predict(
        emotion="Very Sad",
        depression="Depressed",
        behavior=behavior,
        epds="High",
        trend="Worsening",
    )
)


print("\n---------- SELF HARM OVERRIDE ----------")

behavior = BehaviorPrediction(
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    True,
)

print(
    predictor.predict(
        emotion="Happy",
        depression="Not Depressed",
        behavior=behavior,
        epds="Low",
        trend="Improving",
    )
)