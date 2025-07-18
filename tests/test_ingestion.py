from src.ingestion import validate_schema
import pandas as pd

def test_validate_schema_pass():
    df = pd.DataFrame({
        "sensor_id": ["sensor_1"],
        "timestamp": ["2023-06-01T08:00:00"],
        "reading_type": ["temperature"],
        "value": [25.0],
        "battery_level": [88.5]
    })
    validate_schema(df, "test_file")

def test_validate_schema_fail():
    df = pd.DataFrame({"foo": [1]})
    try:
        validate_schema(df, "test_file")
        assert False, "Schema mismatch should raise ValueError"
    except ValueError:
        pass  # Expected
