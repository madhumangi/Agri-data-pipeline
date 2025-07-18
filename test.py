import duckdb
import pandas as pd

df = pd.read_parquet("data/processed/date=2025-06-02/")
con = duckdb.connect()
con.register("processed_data", df)

result = con.execute("""
    SELECT sensor_id, reading_type, ROUND(AVG(normalized_value), 2) AS avg_val
    FROM processed_data
    GROUP BY sensor_id, reading_type
""").df()

print(result)
