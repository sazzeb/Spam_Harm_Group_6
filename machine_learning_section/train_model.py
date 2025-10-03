from __future__ import annotations
from pathlib import Path
import csv
from typing import List, Tuple

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import joblib

def _load_sms_data(repo_root: Path) -> tuple[list[str], list[str]]:
    """
    Load local training data ONLY from the repo.
    Preference order:
      1) machine_learning_section/spam_multiclass.csv  (labels: Not harmful, Not Spam, Spam, Harmful)
      2) machine_learning_section/spam.csv
      3) data/spam.csv
      4) machine_learning_section/SMSSpamCollection (TSV)
      5) data/SMSSpamCollection
      6) SMSSpamCollection in repo root
    No external downloads.
    """
    candidates = [
        repo_root / "machine_learning_section" / "spam_multiclass.csv",
        repo_root / "machine_learning_section" / "spam.csv",
        repo_root / "data" / "spam.csv",
        repo_root / "machine_learning_section" / "SMSSpamCollection",
        repo_root / "data" / "SMSSpamCollection",
        repo_root / "SMSSpamCollection",
    ]

    src = next((p for p in candidates if p.exists()), None)
    if not src:
        raise FileNotFoundError(
            "No local training file found. Run the generator to create "
            "machine_learning_section/spam_multiclass.csv"
        )

    # CSV path (preferred)
    if src.suffix.lower() == ".csv":
        texts, labels = [], []
        with src.open(newline="", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames or "label" not in reader.fieldnames or "text" not in reader.fieldnames:
                raise ValueError(f"{src} must have headers 'label,text'")
            for row in reader:
                labels.append(str(row["label"]))
                texts.append(str(row["text"]))
        return texts, labels

    # TSV/SMSSpamCollection
    if src.name == "SMSSpamCollection" or src.suffix.lower() == ".tsv" or src.suffix == "":
        texts, labels = [], []
        with src.open(encoding="utf-8", errors="ignore") as f:
            for line in f:
                parts = line.rstrip("\n").split("\t", 1)
                if len(parts) == 2:
                    labels.append(parts[0])
                    texts.append(parts[1])
        if texts:
            return texts, labels

    raise FileNotFoundError(f"Failed to read local dataset at: {src}")

def _build_pipeline() -> Pipeline:
    # Same classical sklearn recipe; supports multi-class out of the box
    return Pipeline(
        steps=[
            ("vect", CountVectorizer(stop_words="english")),
            ("tfidf", TfidfTransformer()),
            ("clf", MultinomialNB()),
        ]
    )

def train_and_save(output_path: Path):
    repo_root = Path(__file__).resolve().parents[1]
    X, y = _load_sms_data(repo_root)
    pipe = _build_pipeline()
    pipe.fit(X, y)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, output_path)
    print(f"Saved model to {output_path}")
    return output_path

if __name__ == "__main__":
    out = Path(__file__).resolve().parents[1] / "text_clf_pipeline.pkl"
    train_and_save(out)
