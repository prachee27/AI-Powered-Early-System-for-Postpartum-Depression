"""Fine-tune a local text classifier from a *postpartum depression-labelled* CSV.

Expected CSV columns: ``text`` and ``label``. Labels must be 0 (not depressed)
or 1 (depression risk). This script intentionally does not train on the included
Dreaddit data because it is stress-labelled Reddit data, not postpartum
depression ground truth.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def load_examples(csv_path: Path) -> list[dict[str, int | str]]:
    with csv_path.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    if not rows or not {"text", "label"}.issubset(rows[0]):
        raise ValueError("CSV must include text and label columns.")
    examples = [{"text": row["text"], "label": int(row["label"])} for row in rows]
    if any(example["label"] not in {0, 1} for example in examples):
        raise ValueError("Labels must be 0 (not depressed) or 1 (depression risk).")
    return examples


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, type=Path)
    parser.add_argument("--output", default="trained_model/depression_model", type=Path)
    parser.add_argument("--base-model", default="distilroberta-base")
    parser.add_argument("--epochs", default=3, type=int)
    args = parser.parse_args()

    try:
        from datasets import Dataset
        from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
    except ImportError as exc:
        raise SystemExit("Install training dependencies first: pip install datasets torch transformers accelerate") from exc

    examples = load_examples(args.data)
    dataset = Dataset.from_list(examples).train_test_split(test_size=0.2, seed=42, stratify_by_column="label")
    tokenizer = AutoTokenizer.from_pretrained(args.base_model)

    def tokenize(batch):
        return tokenizer(batch["text"], truncation=True, padding="max_length", max_length=256)

    tokenized = dataset.map(tokenize, batched=True).remove_columns(["text"])
    model = AutoModelForSequenceClassification.from_pretrained(args.base_model, num_labels=2)
    args.output.mkdir(parents=True, exist_ok=True)
    training_args = TrainingArguments(
        output_dir=str(args.output / "checkpoints"),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        eval_strategy="epoch",
        save_strategy="no",
        logging_strategy="epoch",
    )
    Trainer(model=model, args=training_args, train_dataset=tokenized["train"], eval_dataset=tokenized["test"]).train()
    model.save_pretrained(args.output)
    tokenizer.save_pretrained(args.output)
    print(f"Saved trained model to {args.output}")


if __name__ == "__main__":
    main()
