# Postpartum Depression Early-Warning System

This backend is an early-warning prototype. It is not a clinical diagnosis or
an emergency service.

## Assessment cadence

- A user submits a daily journal or voice-to-text journal to
  `POST /daily-check-in`. This endpoint does **not** ask EPDS questions.
- The ten EPDS questions appear only in the weekly `POST /analyze` check-in.
- After a successful weekly request, the system stores the completion
  date for that `patient_id` in `data/assessments.db` and returns
  `next_epds_assessment_due`.
- A second submission before that date is rejected with HTTP 422. A new
  submission is accepted on the due date or later.

For a daily check-in, send up to six previous daily summaries in `history`.
When the current entry makes seven days in total, the system calculates the
weekly trend. This does not mean that the EPDS questionnaire is filled seven
times.

Example fields required by `POST /analyze`:

```json
{
  "patient_id": "patient-123",
  "assessment_date": "2026-08-21",
  "journal": "I have been feeling anxious and cannot sleep.",
  "epds_answers": {"1": 0, "2": 0, "3": 3, "4": 0, "5": 3, "6": 3, "7": 3, "8": 3, "9": 3, "10": 3},
  "history": []
}
```

`history` must contain exactly seven daily summaries in an actual API request.
Keep the generated `data/assessments.db` private: it can contain health-related
screening history and is intentionally excluded from version control.

## Web-app flow

- A journal entry may be submitted every day, by typing or voice-to-text.
- The app stores only the six most recent daily summary signals in the current
  browser so that the next report can compare today with the prior week.
- The 10 EPDS questions appear on the first check-in and then only when the
  next seven-day due date is reached. A daily journal still receives a report
  when the EPDS questionnaire is not due or is declined.

## Depression text model

The application runs immediately with a transparent keyword-based screening
fallback. It automatically switches to a trained local transformer when its
files are placed in `trained_model/depression_model/`.

The repository does not include a clinical postpartum-depression model or
patient data. The included Dreaddit dataset is labelled for stress, so it must
not be repurposed as a postpartum-depression model. To train a model ethically,
use a reviewed, consented postpartum-depression-labelled CSV with `text` and
`label` columns (`0` = not depressed, `1` = depression risk):

```bash
pip install -r requirements.txt
python scripts/train_postpartum_depression_model.py --data path/to/postpartum_labelled_data.csv
```

The saved model will be used automatically after restarting the server. It is
still a screening aid rather than a diagnostic tool and requires clinical
validation before real-world medical use.
