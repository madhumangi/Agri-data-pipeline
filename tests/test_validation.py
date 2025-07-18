import os
import pandas as pd

def test_data_quality_report_exists():
    assert os.path.exists("data/data_quality_report.csv"), "Data quality report not found."

def test_report_has_required_columns():
    df = pd.read_csv("data/data_quality_report.csv")
    expected_cols = {"sensor_id", "reading_type", "total_records", "anomalies", "missing_values", "coverage_gaps"}
    assert expected_cols.issubset(set(df.columns)), f"Missing columns in report: {expected_cols - set(df.columns)}"

def test_anomalies_are_not_negative():
    df = pd.read_csv("data/data_quality_report.csv")
    assert (df["anomalies"] >= 0).all(), "Anomalies column has negative values."
