import duckdb
import os

def validate_data(df):
    print("\n Running data validation via DuckDB...")

    os.makedirs("data", exist_ok=True)
    con = duckdb.connect()

    # Register dataframe as DuckDB view
    con.register("sensor_data", df)

    # 1. Data type check & anomaly profile
    profile_query = """
    SELECT 
        reading_type,
        COUNT(*) AS total_records,
        SUM(CASE WHEN anomalous_reading THEN 1 ELSE 0 END) AS anomalous_count,
        ROUND(SUM(CASE WHEN anomalous_reading THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS pct_anomalous,
        SUM(CASE WHEN value IS NULL THEN 1 ELSE 0 END) AS missing_values
    FROM sensor_data
    GROUP BY reading_type
    """

    profile_df = con.execute(profile_query).df()

    # 2. Detect missing hourly timestamps per sensor
    gap_query = """
    SELECT 
        sensor_id,
        reading_type,
        MIN(DATE_TRUNC('hour', timestamp)) AS min_time,
        MAX(DATE_TRUNC('hour', timestamp)) AS max_time,
        COUNT(DISTINCT DATE_TRUNC('hour', timestamp)) AS actual_hours,
        ((DATEDIFF('hour', MIN(DATE_TRUNC('hour', timestamp)), MAX(DATE_TRUNC('hour', timestamp))) + 1) - COUNT(DISTINCT DATE_TRUNC('hour', timestamp))) AS missing_hours
    FROM sensor_data
    GROUP BY sensor_id, reading_type
    """

    gap_df = con.execute(gap_query).df()

    # 3. Merge reports
    final_report = profile_df.merge(
        gap_df, how="outer", on=["reading_type"]
    )

    report_path = "data/data_quality_report.csv"
    final_report.to_csv(report_path, index=False)
    print(f" Validation report saved: {report_path}")
