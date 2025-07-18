import os


def load_data(df):
    output_dir = "data/processed"
    os.makedirs(output_dir, exist_ok=True)

    print("\n Saving cleaned data to Parquet...")

    # Save as partitioned Parquet (by date)
    df.to_parquet(
        output_dir,
        index=False,
        partition_cols=["date"],
        compression="snappy",
        engine="pyarrow"
    )

    print(f" Data saved to: {output_dir}/ (partitioned by date)")
