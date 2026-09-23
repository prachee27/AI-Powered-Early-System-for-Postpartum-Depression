# Run PPD-EWS

PPD-EWS is an early-warning screening-support system, not a medical diagnosis tool.

## Local run

Use Python 3.10 or newer from a VS Code terminal:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-minimal.txt
uvicorn backend.main:app --reload
```

Open <http://127.0.0.1:8000> for the assessment form, or <http://127.0.0.1:8000/docs> for Swagger API documentation.

## Docker run

```bash
docker build -t ppd-ews .
docker run --rm -p 8000:8000 ppd-ews
```

## Optional trained models

The app runs without downloaded ML models using deterministic screening fallbacks. To enable the transformer models, install `torch` and `transformers`, and place the trained depression model at `trained_model/depression_model`.

If somebody may harm themselves or is in immediate danger, contact local emergency services or a crisis service now and do not leave them alone.
