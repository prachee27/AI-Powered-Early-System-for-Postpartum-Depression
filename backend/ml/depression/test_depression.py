from predictor import DepressionPredictor

print(DepressionPredictor)
print(dir(DepressionPredictor))

predictor = DepressionPredictor()

text = """
I feel hopeless.
Nothing makes me happy anymore.
I cry almost every day.
I don't enjoy spending time with my baby.
"""

result = predictor.predict(text)

print(result)