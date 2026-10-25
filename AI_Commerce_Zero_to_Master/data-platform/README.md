# Historical Data Lake -> Warehouse -> Future Processing

This folder gives a runnable local mental model for the production path:

```text
Operational DB / APIs
        |
        +--> Outbox/CDC -> Kafka
                        |
                        v
                  Bronze raw lake
                        |
                  validation/dedupe
                        v
                  Silver canonical data
                        |
                  business transforms
                        v
                  Gold / warehouse marts
                        |
              +---------+---------+
              |                   |
              v                   v
          BI / SQL             feature snapshots
                                  |
                                  v
                              ML / DL / AI
```

Run the whole local pipeline with:

```powershell
cd data-platform\pipelines
python .\run_pipeline.py
```

Only the Python standard library is used so the learner can inspect every line. The local filesystem represents object storage, and SQLite represents the analytical warehouse. The architecture guide explains how the same stages map to Kafka, S3/ADLS/GCS, Parquet/Iceberg/Delta, Spark/Flink/dbt, Snowflake/BigQuery/Redshift/Databricks, feature stores and model training in production.
