from __future__ import annotations
from pathlib import Path
from functools import lru_cache
import joblib
from sklearn.exceptions import NotFittedError

BASE_DIR = Path(__file__).resolve().parents[2]
CANDIDATES = [
    BASE_DIR / "text_clf_pipeline.pkl",
    BASE_DIR / "spam_clf_model_pipeline_final_second.pkl",
]

def _train_and_save(output_path):
    from machine_learning_section.train_model import train_and_save
    train_and_save(output_path)

@lru_cache(maxsize=1)
def get_pipeline():
    last_err = None
    for f in CANDIDATES:
        if f.exists():
            try:
                return joblib.load(f)
            except Exception as e:
                last_err = e
    if last_err:
        _train_and_save(CANDIDATES[0])
        return joblib.load(CANDIDATES[0])
    _train_and_save(CANDIDATES[0])
    return joblib.load(CANDIDATES[0])

def _ensure_proba(pipe, text: str) -> dict[str, float]:
    if hasattr(pipe, "predict_proba"):
        proba = pipe.predict_proba([text])[0]
        labels = [str(c) for c in getattr(pipe, "classes_", [])]
        return dict(zip(labels, map(float, proba)))
    pred = pipe.predict([text])[0]
    return {str(pred): 1.0}

def predict_proba_dict(text: str) -> dict[str, float]:
    pipe = get_pipeline()
    try:
        return _ensure_proba(pipe, text)
    except NotFittedError:
        get_pipeline.cache_clear()
        _train_and_save(CANDIDATES[0])
        pipe = get_pipeline()
        return _ensure_proba(pipe, text)
