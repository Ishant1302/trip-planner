"""
Evaluation and Metrics Module
Loads and returns all model evaluation results for the ML Dashboard.
"""

import joblib
import json
from pathlib import Path
from typing import Dict, Any

MODELS_DIR = Path(__file__).parent.parent.parent / "saved_models"
DATASETS_DIR = Path(__file__).parent.parent.parent / "datasets"


def get_training_status() -> dict:
    status_path = MODELS_DIR / "training_status.json"
    if status_path.exists():
        with open(status_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"trained": False, "trained_at": None}


def get_classification_results() -> dict:
    path = MODELS_DIR / "classification_results.pkl"
    if path.exists():
        return joblib.load(path)
    return {"error": "Models not trained yet. Run /api/ml/train first."}


def get_clustering_results() -> dict:
    path = MODELS_DIR / "clustering_results.pkl"
    if path.exists():
        return joblib.load(path)
    return {"error": "Models not trained yet."}


def get_regression_results() -> dict:
    path = MODELS_DIR / "regression_results.pkl"
    if path.exists():
        return joblib.load(path)
    return {"error": "Models not trained yet."}


def get_dataset_stats() -> dict:
    metadata_path = DATASETS_DIR / "metadata.json"
    if metadata_path.exists():
        with open(metadata_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        records = meta.get("records", {})
        return {
            "places": records.get("places", 0),
            "destinations": records.get("destinations", 0),
            "users": records.get("users", 0),
            "interactions": records.get("interactions", 0),
            "past_trips": records.get("past_trips", 0),
            "note": meta.get("data_note", "Synthetic data"),
            "train_size": int(records.get("interactions", 0) * 0.8),
            "test_size": int(records.get("interactions", 0) * 0.2),
        }
    return {}


def get_all_metrics() -> dict:
    return {
        "training_status": get_training_status(),
        "classification": get_classification_results(),
        "clustering": get_clustering_results(),
        "regression": get_regression_results(),
        "dataset_stats": get_dataset_stats(),
    }

