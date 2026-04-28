from pathlib import Path
import random

import pandas as pd


OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "generated_transactions.csv"


def build_row(index: int) -> dict:
    is_fraud = 1 if random.random() < 0.22 else 0

    if is_fraud:
        amount = random.randint(25000, 150000)
        hour = random.choice([0, 1, 2, 3, 4, 5, 23])
        velocity_1h = random.randint(4, 12)
        country_mismatch = random.choice([1, 1, 1, 0])
        device_change = random.choice([1, 1, 0])
        merchant_risk = random.choice([1, 1, 0])
        is_international = random.choice([1, 1, 0])
    else:
        amount = random.randint(300, 18000)
        hour = random.randint(8, 22)
        velocity_1h = random.randint(1, 3)
        country_mismatch = random.choice([0, 0, 0, 1])
        device_change = random.choice([0, 0, 1])
        merchant_risk = random.choice([0, 0, 1])
        is_international = random.choice([0, 0, 1])

    return {
        "record_id": f"REC-{index:05d}",
        "amount": amount,
        "hour": hour,
        "velocity_1h": velocity_1h,
        "country_mismatch": country_mismatch,
        "device_change": device_change,
        "merchant_risk": merchant_risk,
        "is_international": is_international,
        "is_fraud": is_fraud,
    }


def main() -> None:
    random.seed(42)
    dataset = [build_row(index) for index in range(1, 1501)]
    df = pd.DataFrame(dataset)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Dataset written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
