#!/usr/bin/env python
# Author: Wissem Khlifi, Fabian Hirschmann
from pyspark.sql import SparkSession

project_id = "astute-ace-336608"
gcs_parquet_path = f"gs://{project_id}-bucket/data/parquet/ulb_fraud_detection/"
bq_dataset_name = "ml_datasets"
bq_table_name = "ulb_fraud_detection_dataproc"
temporary_gcs_bucket = f"gs://{project_id}-bucket"

# Create a SparkSession
spark = SparkSession.builder.appName("bigquery_to_gcs_parquet").getOrCreate()

# Read Parquet Files from GCS
df = spark.read.parquet(gcs_parquet_path)

# Write DataFrame to BigQuery
(
    df.write.format("bigquery")
    .option("table", f"{project_id}:{bq_dataset_name}.{bq_table_name}")
    .option("temporaryGcsBucket", temporary_gcs_bucket)
    .mode("overwrite")
    .save()
)

spark.stop()
