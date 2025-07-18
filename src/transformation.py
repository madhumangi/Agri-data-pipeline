import pandas as pd

# Define expected value ranges for anomaly flagging
EXPECTED_RANGES = {
    "temperature": (0, 60),
    "humidity": (10, 90),
}

# Calibration parameters
CALIBRATION = {
    "temperature": {"multiplier": 1.05, "offset": 0.5},
    "humidity": {"multiplier": 1.02, "offset": 0.2},
}

def transform_data(df):
    # Step 1: Clean
    df = df.drop_duplicates()
    df = df.dropna(subset=["value", "timestamp", "sensor_id", "reading_type"])

    # Convert timestamp to datetime and to UTC+5:30
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["timestamp"] = df["timestamp"].dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata")
    df["date"] = df["timestamp"].dt.date

    # Step 2: Outlier Removal using Z-score
    df["zscore"] = df.groupby("reading_type")["value"].transform(
        lambda x: (x - x.mean()) / x.std(ddof=0)
    )
    df = df[df["zscore"].abs() <= 3].copy()

    # Step 3: Anomaly flagging
    def flag_anomaly(row):
        expected = EXPECTED_RANGES.get(row["reading_type"])
        if expected:
            return not (expected[0] <= row["value"] <= expected[1])
        return False

    df["anomalous_reading"] = df.apply(flag_anomaly, axis=1)

    # Step 4: Normalize using calibration logic
    def apply_calibration(row):
        calib = CALIBRATION.get(row["reading_type"], {"multiplier": 1, "offset": 0})
        return row["value"] * calib["multiplier"] + calib["offset"]

    df["normalized_value"] = df.apply(apply_calibration, axis=1)

    # Step 5: Daily average
    df["daily_avg"] = df.groupby(["sensor_id", "reading_type", "date"])["normalized_value"].transform("mean")

    # Step 6: 7-day rolling average
    df["rolling_avg_7d"] = df["daily_avg"]

    return df
