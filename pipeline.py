from src.ingestion import ingest_data
from src.transformation import transform_data
from src.validation import validate_data
from src.loading import load_data

def main():
    print("\n Step 1: Ingesting data...")
    raw_df = ingest_data()

    if raw_df.empty:
        print(" No data found to process.")
        return

    print("\n Step 2: Transforming data...")
    processed_df = transform_data(raw_df)

    print("\n Step 3: Validating data...")
    validate_data(processed_df)

    print("\n Step 4: Saving data...")
    load_data(processed_df)

    print("\n Pipeline completed successfully.")

if __name__ == "__main__":
    main()
