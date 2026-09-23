from backend.ml.behavior.predictor import BehaviorPredictor


predictor = BehaviorPredictor()

text = """
I haven't slept for days.
I cry every night.
I don't feel connected to my baby.
I am constantly worried.
"""

result = predictor.predict(text)

print(result)