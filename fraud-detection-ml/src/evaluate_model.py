from pathlib import Path
import json


METRICS_PATH = Path(__file__).resolve().parents[1] / "reports" / "latest_metrics.json"


def main() -> None:
    if not METRICS_PATH.exists():
        raise FileNotFoundError("Metrics file not found. Run train_model.py before evaluation.")

    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    print("Fraud Detection Model Evaluation")
    print(f"Dataset: {metrics['dataset_used']}")
    print(f"Accuracy: {metrics['accuracy']}")
    print(f"Precision: {metrics['precision']}")
    print(f"Recall: {metrics['recall']}")
    print(metrics["classification_report"])


if __name__ == "__main__":
    main()
