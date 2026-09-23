from backend.ml.epds.predictor import EPDSPredictor


predictor = EPDSPredictor()


# -----------------------------
# Test Case 1: Low Risk
# -----------------------------

answers = {
    1: 0,
    2: 0,
    3: 3,
    4: 0,
    5: 3,
    6: 3,
    7: 3,
    8: 3,
    9: 3,
    10: 3
}

result = predictor.predict(answers)

print("Low Risk Test")
print(result)


# -----------------------------
# Test Case 2: Moderate Risk
# -----------------------------

answers = {
    1: 1,
    2: 1,
    3: 2,
    4: 1,
    5: 2,
    6: 2,
    7: 2,
    8: 2,
    9: 2,
    10: 2
}

result = predictor.predict(answers)

print("\nModerate Risk Test")
print(result)


# -----------------------------
# Test Case 3: High Risk
# -----------------------------

answers = {
    1: 3,
    2: 3,
    3: 0,
    4: 3,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
    10: 0
}

result = predictor.predict(answers)

print("\nHigh Risk Test")
print(result)


# -----------------------------
# Test Case 4: Invalid Question
# -----------------------------

try:

    answers = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        11: 0
    }

    predictor.predict(answers)

except Exception as e:
    print("\nInvalid Question Test")
    print(e)


# -----------------------------
# Test Case 5: Invalid Option
# -----------------------------

try:

    answers = {
        1: 5,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0
    }

    predictor.predict(answers)

except Exception as e:
    print("\nInvalid Option Test")
    print(e)


# -----------------------------
# Test Case 6: Missing Answers
# -----------------------------

try:

    answers = {
        1: 0,
        2: 0,
        3: 0
    }

    predictor.predict(answers)

except Exception as e:
    print("\nMissing Answers Test")
    print(e)