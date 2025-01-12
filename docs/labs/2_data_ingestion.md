## Lab 2: Data Ingestion

<walkthrough-tutorial-duration duration="45"></walkthrough-tutorial-duration>
<walkthrough-tutorial-difficulty difficulty="4"></walkthrough-tutorial-difficulty>

Original document: [here](https://docs.google.com/document/d/1NAcQb9qUZsyGSe2yPQWKrBz18ZRVCL7X9e-NDs5lQbk/edit?usp=drive_link)


During this lab, you ingest fraudulent and non fraudulent transactions dataset into BigQuery using three methods:
* Method 1: Using BigLake with data stored in Google Cloud Storage (GCS)
* Method 2: Near real-time ingestion into BigQuery using [Cloud PubSub](https://cloud.google.com/pubsub)
* Method 3: Batch Ingestion into BigQuery using Dataproc Serverless

For all methods, we are ingesting data from the Google Cloud bucket you have created in the previous lab through `bootstrap.sh`. Feel free to have a look at the contents of this bucket:

### Method 1: External table using BigLake

BigLake tables let you query structured data in external data stores with access delegation. Access delegation decouples access to the BigLake table from access to the underlying data store. An external connection associated with a service account is used to connect to the data store.

Because the service account handles retrieving data from the data store, you only have to grant users access to the BigLake table. This lets you enforce fine-grained security at the table level, including row-level and column-level security. For BigLake tables based on Cloud Storage, you can also use dynamic data masking. To learn more about multi-cloud analytic solutions using BigLake tables with Amazon S3 or Blob Storage data, see BigQuery Omni.

Note that this section could also be done in the Google Cloud Console (the GUI). However, in this lab, we will do it on the command line.

First, we create the connection:
```bash
bq mk --connection --location=$REGION --project_id=$PROJECT_ID \
    --connection_type=CLOUD_RESOURCE fraud-transactions-conn
```

When you create a connection resource, BigQuery creates a unique system service account and associates it with the connection.
```bash
bq show --connection ${PROJECT_ID}.${REGION}.fraud-transactions-conn
```
Note the `serviceAccountID`. It should resemble `connection-...@...gserviceaccount.com`.

To connect to Cloud Storage, you must give the new connection read-only access to Cloud Storage so that BigQuery can access files on behalf of users. Let's assign the service account to a variable:
```bash
CONN_SERVICE_ACCOUNT=$(bq --format=prettyjson show --connection ${PROJECT_ID}.${REGION}.fraud-transactions-conn | jq -r ".cloudResource.serviceAccountId")
echo $CONN_SERVICE_ACCOUNT
```

And grant it access to Cloud Storage:
```bash
gcloud storage buckets add-iam-policy-binding gs://${PROJECT_ID}-bucket \
--role=roles/storage.objectViewer \
--member=serviceAccount:$CONN_SERVICE_ACCOUNT
```

Next, we create a dataset that our external table will live in:
```bash
bq --location=${REGION} mk -d ml_datasets
```

Go to the [BigQuery Console](https://console.cloud.google.com/bigquery). check that the dataset has been created successfully (Note: you may need to click "refresh contents" from the 3-dot menu for the project in the Explorer).

Finally, create a table in BigQuery pointing to the data in Cloud Storage:

```bash
bq mk --table \
  --external_table_definition=@PARQUET="gs://${PROJECT_ID}-bucket/bootkon-data/parquet/ulb_fraud_detection/*"@projects/${PROJECT_ID}/locations/${REGION}/connections/fraud-transactions-conn \
  ml_datasets.ulb_fraud_detection_biglake
```

Go to the [BigQuery Console](https://console.cloud.google.com/bigquery) console again and open the dataset and table you just created. Click on `Query` and insert the following SQL query.

```sql
SELECT * FROM `<walkthrough-project-id/>.ml_datasets.ulb_fraud_detection_biglake` LIMIT 1000;
```

Note that you can also execute a query using the `bq` tool:

```bash
bq --location=$REGION query --nouse_legacy_sql "SELECT Time, V1, Amount, Class FROM <walkthrough-project-id/>.ml_datasets.ulb_fraud_detection_biglake LIMIT 10;"
```

Note that the data we are querying still resides on Cloud Storage and there are no copies stored in BigQuery. Using BigLake, BigQuery acts as query engine but not as storage layer.

### Method 2: Real time data ingestion into BigQuery using Pub/Sub

This variant of data ingestion allows real-time streaming into BigQuery using Pub/Sub.

We create an empty table and then stream data into it. For this to work, we need to specify a schema. Have a look at <walkthrough-editor-open-file filePath="src/data_ingestion/my_avro_fraud_detection_schema.json">fraud_detection_bigquery_schema.json</walkthrough-editor-open-file>. This is the schema we are going to use.

Create an empty table using this schema:
```bash
bq --location=$REGION mk --table \
<walkthrough-project-id/>:ml_datasets.ulb_fraud_detection_pubsub src/data_ingestion/fraud_detection_bigquery_schema.json
```

We also need to a Pub/Sub schema:
```bash
gcloud pubsub schemas create fraud-detection-schema \
    --project=$PROJECT_ID  \
    --type=AVRO \
    --definition-file=src/data_ingestion/fraud_detection_pubsub_schema.json
```

And them create a Pub/Sub topic using this schema:
```bash
gcloud pubsub topics create fraud-detection-topic \
    --project=$PROJECT_ID  \
    --schema=fraud-detection-schema \
    --message-encoding=BINARY
```

We also need to give Pub/Sub permissions to write data to BigQuery. The Pub/Sub service account is comprised of the project number (not the id) and an identifier. Let's first figure out the number:
```bash
export PROJECT_NUM=$(gcloud projects describe ${PROJECT_ID} --format="value(projectNumber)")
export PUBSUB_SERVICE_ACCOUNT="service-${PROJECT_NUM}@gcp-sa-pubsub.iam.gserviceaccount.com"
echo $PUBSUB_SERVICE_ACCOUNT
```

And grant the service account access to BigQuery:

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:$PUBSUB_SERVICE_ACCOUNT --role=roles/bigquery.dataEditor

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:$PUBSUB_SERVICE_ACCOUNT --role=roles/bigquery.jobUser  
```

Next, we create the Pub/Sub subscription:
```bash
gcloud pubsub subscriptions create fraud_detection-subscription \
    --project=$PROJECT_ID  \
    --topic=fraud_detection-topic \
    --bigquery-table=$PROJECT_ID.ml_datasets.ulb_fraud_detection_pubsub \
    --use-topic-schema  
```

Feel free to [check it out in the Pub/Sub console](https://console.cloud.google.com/cloudpubsub/subscription).

Since we'll be using Python, let's install the Python <walkthrough-editor-open-file filePath="requirements.txt">packages</walkthrough-editor-open-file> we want to make use of:
```bash
pip install -r requirements.txt
```

Please have a look at <walkthrough-editor-open-file filePath="src/data_ingestion/import_csv_to_bigquery_1.py">import_csv_to_bigquery_1.py</walkthrough-editor-open-file>. This script loads CSV files from Cloud Storage, parses it in Python, and sends it to Pub/Sub - row by row.

Let's execute it.
```bash
./src/data_ingestion/import_csv_to_bigquery_1.py
```

Each line you see on the screen corresponds to one transaction being send to Pub/Sub and written to BigQuery. It would take approximately 40 to 60 minutes for it to finish. So, please cancel the command using 'CTRL + C'.

<!-- 
We can make this faster by using different parameters for Pub/Sub. First, remove all rows you just ingested:
```bash
bq --location=$REGION query --nouse_legacy_sql "DELETE FROM <walkthrough-project-id/>.ml_datasets.ulb_fraud_detection_pubsub WHERE true;"
```

Next, have a look at <walkthrough-editor-open-file filePath="src/data_ingestion/import_csv_to_bigquery_2.py">import_csv_to_bigquery_2.py</walkthrough-editor-open-file>. Can you make out the difference to the first script? Let's execute it:
```bash
./src/data_ingestion/import_csv_to_bigquery_2.py
```
-->

### Method 3: Ingestion using Cloud Dataproc (Apache Spark)

Google Cloud Dataproc is a fully managed and scalable service for running Apache Hadoop, Apache Spark, Apache Flink, Presto, and 30+ open source tools and frameworks. Dataproc allows data to be loaded and also transformed or pre-processed as it is brought in.

Create an empty BigQuery table:
```bash
bq --location=$REGION mk --table \
<walkthrough-project-id/>:ml_datasets.ulb_fraud_detection_dataproc src/data_ingestion/fraud_detection_bigquery_schema.json
```

Open <walkthrough-editor-select-line filePath="src/data_ingestion/import_parquet_to_bigquery.py" startLine="4" endLine="4" startCharacterOffset="14" endCharacterOffset="31">import_parquet_to_bigquery.py</walkthrough-editor-select-line> in the Cloud Shell editor and replace the project id with your project id. Don't forget to save.

Execute it:
```bash
gcloud dataproc batches submit pyspark src/data_ingestion/import_parquet_to_bigquery.py \
    --project=$PROJECT_ID \
    --region=$REGION \
    --deps-bucket=gs://${PROJECT_ID}-bucket
```

While the command is still running, open the [DataProc Console](https://console.cloud.google.com/dataproc/batches) and monitor the job.

After the Dataproc job completes, confirm that data has been loaded into the BigQuery table. You should see over 200,000 records, but the exact count isn't critical:
```bash
bq --location=$REGION query --nouse_legacy_sql "SELECT count(*) as count FROM <walkthrough-project-id/>.ml_datasets.ulb_fraud_detection_dataproc;"
```

You've nailed the data ingestion lab -- great job!

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>