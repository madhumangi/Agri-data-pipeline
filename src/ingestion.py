import os
import pandas as pd

RAW_DIR = "data/raw"

def ingest_data():
    all_data = []
    stats = {
        "files_read": 0,
        "records_processed": 0,
        "records_skipped": 0,
        "errors": []
    }

    for file in sorted(os.listdir(RAW_DIR)):
        if not file.endswith(".parquet"):
            continue

        path = os.path.join(RAW_DIR, file)
        try:
            df = pd.read_parquet(path)
            validate_schema(df, file)
            stats["files_read"] += 1
            stats["records_processed"] += len(df)
            all_data.append(df)
        except Exception as e:
            stats["errors"].append(f"{file}: {str(e)}")

    if all_data:
        df = pd.concat(all_data, ignore_index=True)
    else:
        df = pd.DataFrame()

    print_ingestion_summary(stats)
    return df


def validate_schema(df, file):
    expected_cols = {"sensor_id", "timestamp", "reading_type", "value", "battery_level"}
    if not expected_cols.issubset(set(df.columns)):
        raise ValueError(f"[SCHEMA MISMATCH] in {file}: Found columns {df.columns.tolist()}")


def print_ingestion_summary(stats):
    print("\n INGESTION SUMMARY:")
    print(f" Files read: {stats['files_read']}")
    print(f" Records processed: {stats['records_processed']}")
    print(f" Errors: {len(stats['errors'])}")
    for err in stats["errors"]:
        print(f"  - {err}")
