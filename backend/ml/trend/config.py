# Emotion severity scores
EMOTION_SCORES = {
    "Happy": 0,
    "Neutral": 1,
    "Sad": 2,
    "Very Sad": 3
}


# Depression severity scores
DEPRESSION_SCORES = {
    "Not Depressed": 0,
    "Depressed": 3
}


# Weekly EPDS risk contribution
EPDS_RISK_SCORES = {
    None: 0,
    "Low": 0,
    "Moderate": 2,
    "High": 4
}


# Minimum score difference required
# to consider the trend as improving
# or worsening.
TREND_THRESHOLD = 1.0