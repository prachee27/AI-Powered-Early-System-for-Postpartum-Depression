from predictor import EmotionPredictor

predictor = EmotionPredictor()

text = """
I love my boyfriend. But I cheated on him twice. Now I want to go to the second guy.
"""

result = predictor.predict(text)

print(result)