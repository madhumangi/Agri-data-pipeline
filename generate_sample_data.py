import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Create sample directory if it doesn't exist
os.makedirs("data/raw", exist_ok=True)

reading_types = ["temperature", "humidity"]

value_ranges = {
    "temperature": (10, 40),
    "humidity": (15, 90),
}

def create_sample_parquet(date_str):
    rows = []
    date = datetime.strptime(date_str, "%Y-%m-%d")
    for i in range(15):  # 15 readings per day
        for rt in reading_types:
            sensor_id = f"sensor_{np.random.randint(1, 6)}"
            ts = date + timedelta(minutes=5 * i)
            value_low, value_high = value_ranges[rt]
            value = round(np.random.uniform(value_low, value_high), 2)
            battery_level = round(np.random.uniform(20, 100), 2)

            rows.append({
                "sensor_id": sensor_id,
                "timestamp": ts.isoformat(),
                "reading_type": rt,
                "value": value,
                "battery_level": battery_level
            })

    df = pd.DataFrame(rows)
    df.to_parquet(f"data/raw/{date_str}.parquet", index=False)
    print(f" Created: data/raw/{date_str}.parquet")

# Generate 3 days of sample data
create_sample_parquet("2025-06-01")
create_sample_parquet("2025-06-02")
create_sample_parquet("2025-06-03")
