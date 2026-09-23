# Postpartum Depression Early-Warning System

This project is an early-warning system that helps track possible signs of postpartum depression using daily journal entries and weekly EPDS assessments.

> This is only a prototype and screening tool. It is not a medical diagnosis or emergency service.

## How It Works

Users can submit a journal entry every day using:

```text
POST /daily-check-in
```

The journal can be typed or entered using voice-to-text. The system analyzes the text and looks for emotional signals such as stress, anxiety, sadness, sleep problems, or negative thoughts.

The app also keeps the previous six daily summaries so it can compare patterns over a seven-day period.

The EPDS questionnaire is **not asked every day**.

## Weekly EPDS Assessment

The 10 EPDS questions are shown during the first assessment and then once every seven days.

The weekly assessment is submitted through:

```text
POST /analyze
```

After completing it, the system saves the assessment date and returns:

```text
next_epds_assessment_due
```

If the user tries to submit another EPDS assessment before the due date, the server returns an HTTP `422` error.

## Example Request

```json
{
  "patient_id": "patient-123",
  "assessment_date": "2026-08-21",
  "journal": "I have been feeling anxious and cannot sleep.",
  "epds_answers": {
    "1": 0,
    "2": 0,
    "3": 3,
    "4": 0,
    "5": 3,
    "6": 3,
    "7": 3,
    "8": 3,
    "9": 3,
    "10": 3
  },
  "history": []
}
```

For the actual `/analyze` request, `history` should contain exactly seven daily summaries.

## Text Analysis Model

The project works by default using a simple keyword-based screening system.

If a trained transformer model is added inside:

```text
trained_model/depression_model/
```

the application automatically starts using it after the server is restarted.

The included Dreaddit dataset is meant for stress detection, so it should not be treated as a postpartum-depression dataset.

To train a custom model, use a reviewed dataset with:

```text
text
label
```

where:

```text
0 = no depression risk
1 = possible depression risk
```

Run:

```bash
pip install -r requirements.txt
python scripts/train_postpartum_depression_model.py --data path/to/postpartum_labelled_data.csv
```

## Privacy

Assessment history is stored in:

```text
data/assessments.db
```

This file may contain sensitive health-related information, so it should remain private and should never be uploaded to a public repository.
