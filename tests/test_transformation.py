from src.transformation import transform_data
import pandas as pd

def test_transform_data():
    sample = pd.DataFrame({
        "sensor_id": ["sensor_1", "sensor_2"],
        "timestamp": ["2023-06-01T08:00:00", "2023-06-01T08:10:00"],
        "reading_type": ["temperature", "humidity"],
        "value": [25.0, 55.0],
        "battery_level": [78.0, 83.5]
    })

    transformed = transform_data(sample)

    assert "normalized_value" in transformed.columns
    assert "anomalous_reading" in transformed.columns
    assert not transformed.empty
