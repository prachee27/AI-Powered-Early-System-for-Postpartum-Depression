from pathlib import Path

# Project root (PPD/)
PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = PROJECT_ROOT / "trained_model" / "depression_model"

MAX_LENGTH = 512
