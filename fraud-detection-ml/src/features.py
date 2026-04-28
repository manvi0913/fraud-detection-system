import pandas as pd


FEATURE_COLUMNS = [
    "amount",
    "hour",
    "velocity_1h",
    "country_mismatch",
    "device_change",
    "merchant_risk",
    "is_international",
]


def prepare_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    transformed = df.copy()
    transformed["amount"] = transformed["amount"].astype(float)
    transformed["hour"] = transformed["hour"].astype(int)
    transformed["velocity_1h"] = transformed["velocity_1h"].astype(int)
    transformed["country_mismatch"] = transformed["country_mismatch"].astype(int)
    transformed["device_change"] = transformed["device_change"].astype(int)
    transformed["merchant_risk"] = transformed["merchant_risk"].astype(int)
    transformed["is_international"] = transformed["is_international"].astype(int)

    x = transformed[FEATURE_COLUMNS]
    y = transformed["is_fraud"].astype(int)
    return x, y
