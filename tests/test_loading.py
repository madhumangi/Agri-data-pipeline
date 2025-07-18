import os

import pandas as pd

RAW_DIR = "data/raw"

def test_raw_data_files_exist():
    assert os.path.exists(RAW_DIR), "Raw data directory does not exist."
    files = os.listdir(RAW_DIR)
    assert any(file.endswith(".parquet") for file in files), "No Parquet files found in raw data."

def test_raw_file_has_expected_columns():
    files = [f for f in os.listdir(RAW_DIR) if f.endswith(".parquet")]
    df = pd.read_parquet(os.path.join(RAW_DIR, files[0]))
    expected_cols = {"sensor_id", "timestamp", "reading_type", "value", "battery_level"}
    assert expected_cols.issubset(set(df.columns)), f"Missing columns: {expected_cols - set(df.columns)}"
