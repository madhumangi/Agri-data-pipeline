# 🌾 Agri Data Pipeline

A production-grade data pipeline to process, transform, validate, and store agricultural sensor data using Python, Pandas, and DuckDB.

---

## 📁 Folder Structure

```bash
agri-data-pipeline/
├── data/
│   ├── raw/                # Input Parquet files
│   ├── processed/          # Output partitioned Parquet files
│   └── data_quality_report.csv
├── src/
│   ├── ingestion.py        # Read & validate raw data
│   ├── transformation.py   # Clean, enrich, normalize
│   ├── validation.py       # DuckDB-based validation
│   └── loading.py          # Save output Parquet files
├── tests/
│   ├── test_ingestion.py
│   ├── test_transformation.py
│   ├── test_validation.py
│   └── test_loading.py
├── generate_sample_data.py # Script to create test Parquet files
├── pipeline.py             # Main pipeline script
├── requirements.txt        # Python dependencies
├── Dockerfile              # For containerized execution
└── README.md
```

---

## 🧪 Sample Schema

Each `.parquet` file in `data/raw/` contains:

| Column         | Type     | Description              |
| -------------- | -------- | ------------------------ |
| sensor\_id     | string   | Unique ID for the sensor |
| timestamp      | datetime | ISO timestamp (UTC)      |
| reading\_type  | string   | temperature / humidity   |
| value          | float    | Sensor value             |
| battery\_level | float    | Battery %                |

---

## ⚙️ Pipeline Stages

### 1. **Ingestion**

* Reads `.parquet` files from `data/raw/`
* Validates schema, handles corrupt files

### 2. **Transformation**

* Drops duplicates, missing values, outliers
* Flags anomalies based on expected ranges:

  * `temperature`: 0–60°C
  * `humidity`: 10–90%
* Applies calibration logic:

  ```python
  value = value * multiplier + offset
  ```
* Computes:

  * Daily average
  * 7-day rolling average

### 3. **Validation**

* Uses DuckDB SQL to:

  * Profile anomalies and missing data
  * Detect hourly gaps per sensor
* Saves result to `data/data_quality_report.csv`

### 4. **Loading**

* Writes cleaned data to `data/processed/`
* Partitioned by `date`, compressed using `snappy`

---

## 🚀 How to Run

### 1. Install requirements

```bash
pip install -r requirements.txt
```

### 2. Generate sample input files

```bash
python generate_sample_data.py
```

### 3. Run the pipeline

```bash
python pipeline.py
```

---

## 🐳 Docker Setup

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "pipeline.py"]
```

### Build & Run

```bash
docker build -t agri-pipeline .
docker run -v $(pwd)/data:/app/data agri-pipeline
```

On Windows (PowerShell):

```bash
docker run -v ${PWD}/data:/app/data agri-pipeline
```

---

## 📊 Output Files

* Cleaned `.parquet` files in: `data/processed/` (partitioned by `date`)
* Data quality CSV: `data/data_quality_report.csv`

---

## 📊 Example: Data Quality Report Output

The pipeline generates a data quality report using DuckDB and saves it to:

```
data/data_quality_report.csv
```

### Sample Content:

| reading\_type | total\_records | anomalous\_count | pct\_anomalous | missing\_values | sensor\_id | actual\_hours | missing\_hours |
| ------------- | -------------- | ---------------- | -------------- | --------------- | ---------- | ------------- | -------------- |
| temperature   | 20             | 2                | 10.0%          | 0               | sensor\_1  | 18            | 6              |
| humidity      | 20             | 1                | 5.0%           | 0               | sensor\_3  | 19            | 5              |

This report provides visibility into missing values, anomaly rates, and coverage gaps in hourly readings.

---


