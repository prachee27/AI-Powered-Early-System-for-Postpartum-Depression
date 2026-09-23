from backend.ml.trend.predictor import TrendPredictor
from backend.ml.trend.schemas import DailyAnalysis


predictor = TrendPredictor()


# ----------------------------------------
# Test Case 1 : Worsening Trend
# ----------------------------------------

history = [

    DailyAnalysis("Happy", "Not Depressed", 0, None),

    DailyAnalysis("Neutral", "Not Depressed", 1, None),

    DailyAnalysis("Sad", "Not Depressed", 1, None),

    DailyAnalysis("Sad", "Depressed", 2, None),

    DailyAnalysis("Very Sad", "Depressed", 3, "Moderate"),

    DailyAnalysis("Very Sad", "Depressed", 4, "High"),

    DailyAnalysis("Very Sad", "Depressed", 5, "High"),

]

result = predictor.predict(history)

print("Worsening Trend Test")
print(result)


# ----------------------------------------
# Test Case 2 : Improving Trend
# ----------------------------------------

history = [

    DailyAnalysis("Very Sad", "Depressed", 5, "High"),

    DailyAnalysis("Very Sad", "Depressed", 4, "High"),

    DailyAnalysis("Sad", "Depressed", 3, "Moderate"),

    DailyAnalysis("Sad", "Depressed", 2, None),

    DailyAnalysis("Neutral", "Not Depressed", 1, None),

    DailyAnalysis("Happy", "Not Depressed", 0, None),

    DailyAnalysis("Happy", "Not Depressed", 0, None),

]

result = predictor.predict(history)

print("\nImproving Trend Test")
print(result)


# ----------------------------------------
# Test Case 3 : Stable Trend
# ----------------------------------------

history = [

    DailyAnalysis("Neutral", "Not Depressed", 2, None),

    DailyAnalysis("Sad", "Not Depressed", 2, None),

    DailyAnalysis("Neutral", "Depressed", 2, None),

    DailyAnalysis("Sad", "Depressed", 2, None),

    DailyAnalysis("Neutral", "Depressed", 2, None),

    DailyAnalysis("Sad", "Not Depressed", 2, None),

    DailyAnalysis("Neutral", "Not Depressed", 2, None),

]

result = predictor.predict(history)

print("\nStable Trend Test")
print(result)


# ----------------------------------------
# Test Case 4 : Less than 7 Days
# ----------------------------------------

try:

    history = [

        DailyAnalysis("Happy", "Not Depressed", 0, None),

        DailyAnalysis("Happy", "Not Depressed", 0, None),

        DailyAnalysis("Happy", "Not Depressed", 0, None),

    ]

    predictor.predict(history)

except Exception as e:

    print("\nInvalid History Test")
    print(e)