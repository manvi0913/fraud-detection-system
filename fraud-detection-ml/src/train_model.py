from pathlib import Path
import json

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score
from sklearn.model_selection import train_test_split

from features import prepare_features


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = BASE_DIR / "data" / "generated_transactions.csv"
FALLBACK_DATASET = BASE_DIR / "data" / "sample_transactions.csv"
MODEL_PATH = BASE_DIR / "models" / "fraud_model.joblib"
METRICS_PATH = BASE_DIR / "reports" / "latest_metrics.json"


def main() -> None:
    dataset_path = DEFAULT_DATASET if DEFAULT_DATASET.exists() else FALLBACK_DATASET
    df = pd.read_csv(dataset_path)
    x, y = prepare_features(df)

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(n_estimators=120, max_depth=8, random_state=42)
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    metrics = {
        "dataset_used": str(dataset_path.name),
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "precision": round(float(precision_score(y_test, predictions, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, predictions, zero_division=0)), 4),
        "classification_report": classification_report(y_test, predictions, zero_division=0),
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    print(f"Model saved to {MODEL_PATH}")
    print(f"Metrics saved to {METRICS_PATH}")


if __name__ == "__main__":
    main()
