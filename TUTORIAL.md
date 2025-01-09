<walkthrough-metadata>
  <meta name="title" content="Data & AI Boot-Kon" />
  <meta name="description" content="These labs include detailed step-by-step instructions to guide you. In addition to the labs, you’ll face several challenges that you’ll need to solve on your own or with your group. Groups will be assigned by the event organizers at the start of the event." />
  <meta name="keywords" content="data, ai, bigquery, vertexai, genai, notebook" />
  <meta name="component_id" content="12345" />
</walkthrough-metadata>


# Data and AI Boot-Kon

## Introduction

Welcome to bootkon. 

An imaginary company named FraudFix Technologies specializes in enhancing financial transaction security for Google Cloud enterprise customers across industries like finance and e-commerce.

**Your role**: As a senior data analytics/AI engineer at FraudFix Technologies, you will tackle the challenges of making financial transactions safer using machine learning. Your work will involve analyzing vast amounts of transaction data to detect and prevent fraud, as well as assessing customer sentiment regarding the quality of transaction services. You will leverage a unique synthetic dataset, which includes auto-generated data by Google Gemini and a public European credit card transaction dataset that has been PCA transformed and anonymized. This dataset will be used to train your models, reflecting real-world applications of GCP Data & AI in enhancing financial safety.

### Working with labs

You can insert commands into the terminal using the following icon on top of each code junk:
<walkthrough-cloud-shell-icon></walkthrough-cloud-shell-icon>

Please press this icon in the following code chunk:

```bash
echo "I'm ready to get started."
```

And execute by pressing the return key in the terminal that has been opened in the lower part of your screen.

Press the `START` button below to get started!

## Environment Setup

<walkthrough-tutorial-duration duration="30"></walkthrough-tutorial-duration>
<walkthrough-tutorial-difficulty difficulty="1"></walkthrough-tutorial-difficulty>

In this lab you will grant permissions and set up a default VPC network as a preparatory step.

### **Choice of GCP Product and Service Location**

You are free to choose any GCP region location for your labs. Ensure all your resources are created in the chosen location to avoid connectivity issues and minimize latency and cost. If you don’t have a preferred GCP location, use ***us-central1*** for simplicity.

### **Setup your environment**

Open `vars.sh` <walkthrough-editor-open-file filePath="vars.sh"> in the Cloud Shell editor </walkthrough-editor-open-file> and adapt it. Don't forget to save it.

Now, export the variables to your environment:
```bash
source vars.sh
```

Verify that they have been set correctly:
```bash
echo "PROJECT_ID=$PROJECT_ID REGION=$REGION GCP_USERNAME=$GCP_USERNAME"
```

Have a <walkthrough-editor-open-file filePath="bootstrap.sh">look</walkthrough-editor-open-file> at the bootstrap script and what it does; exeucte it:
```bash
./bootstrap.sh
```

Well done, your environment is now ready for the first lab!
   

## Lab 2: Data Ingestion

<walkthrough-tutorial-duration duration="45"></walkthrough-tutorial-duration>
<walkthrough-tutorial-difficulty difficulty="3"></walkthrough-tutorial-difficulty>

Original document: [here](https://docs.google.com/document/d/1NAcQb9qUZsyGSe2yPQWKrBz18ZRVCL7X9e-NDs5lQbk/edit?usp=drive_link)


During this lab, you ingest fraudulent and non fraudulent transactions dataset into BigQuery using three methods:
* Using BigLake with data stored in Google Cloud Storage (GCS)
* Near real-time ingestion into BigQuery using [Cloud PubSub](https://cloud.google.com/pubsub)
* Batch Ingestion into BigQuery using Dataproc Serverless

For all methods, we are ingesting data from the Google Cloud bucket you have created in the previous lab through `bootstrap.sh`. Feel free to have a look at the contents of this bucket:

### External table using BigLake

BigLake tables let you query structured data in external data stores with access delegation. Access delegation decouples access to the BigLake table from access to the underlying data store. An external connection associated with a service account is used to connect to the data store.

Because the service account handles retrieving data from the data store, you only have to grant users access to the BigLake table. This lets you enforce fine-grained security at the table level, including row-level and column-level security. For BigLake tables based on Cloud Storage, you can also use dynamic data masking. To learn more about multi-cloud analytic solutions using BigLake tables with Amazon S3 or Blob Storage data, see BigQuery Omni.

Note that this section could also be done in the Google Cloud Console (the GUI). However, in this lab, we will do it on the command line.

First, we create the connection:
```bash
bq mk --connection --location=$REGION --project_id=$PROJECT_ID \
    --connection_type=CLOUD_RESOURCE fraud-transactions-conn
```

1. In the Google Cloud console navigate to **Bigquery Studio** and click  the **\+ ADD** button  
2. Choose “***Connections to external data sources***”  
   ![][image2]  
3. As connection type select ***Vertex AI remote models , remote functions and BigLake (Cloud Resources)*** ![][image3]  
4. Enter the connection ID as “fraud-transactions-conn” and choose the US multi-region location.  
5. Click “CREATE CONNECTION”  
6. Open the connection details for the newly added external connection  “fraud-transactions-conn”  
   ![][image4]

7. Note the service account ID and grant it Storage Object Viewer role by following these instructions:.  
     
* Go to IAM & Admin  
* Filter  the Service account

  ![][image5]


* If you can’t find the service account ID, add it as a principal. Follow the steps below.   
  * First click on “Grant Access” 

    ![][image6]

  * Copy and paste the service account id into the “new principals” input box. (make sure you paste the complete service account email).   
  * Add the **Storage Object Viewer** Role and click on Save

    ![][image7]

    

* If you do find the service account id, then click on Edit Principal 


  ![][image8]  
* Click on Add Role and add the Storage Object Viewer role, then click on Save.


  ![][image9]

    
8. From Cloud Shell, create a dataset named **ml\_datasets** in the US multi-region.  
   
 ```
 DATASET\_NAME="ml\_datasets" bq \--location=US mk \-d \\     \--description "Fraudulent and Non Fraudulent transactions BigQuery dataset" \\     $DATASET\_NAME*
 ```

*![][image10]*  
\>\>\> You can ignore the following warning ; warnings.warn("urllib3 ({}) or chardet ({})/charset\_normalizer ({}) doesn't match a supported " 

9. ### Go to BigQuery, check that the dataset has been created successfully (Note: you may need to click “refresh contents” from the 3-dot menu for the project in the Explorer).

   ### ![][image11] 

10. ### Click on the “+” icon on the right end of the tabs in the workspace to open a new  SQL Query;

    ![][image12]

11. ### Create BigLake tables on non-partitioned parquet data on GCS;

*Copy and paste the following commands into the  blank SQL window.*

- *Replace **your-project-id** with your actual project ID in 3 places*


|  Create BigLake table on non partitioned parquet data on GCS |
| :---- |
 ```
CREATE OR REPLACE EXTERNAL TABLE
`your-project-id.ml_datasets.ulb_fraud_detection_blake`
WITH CONNECTION `us.fraud-transactions-conn` OPTIONS (
   format ="PARQUET",
   uris = ['gs://your-project-id-bucket/data-ingestion/parquet/ulb_fraud_detection/*'],
   max_staleness=INTERVAL 30 MINUTE,
   metadata_cache_mode="AUTOMATIC");
```


check the results from BigQuery

 ```
SELECT * FROM `your-project-id.ml_datasets.ulb_fraud_detection_blake` LIMIT 1000;
 ```

*click on ![][image13]* 

The simple select statement should query and return data from our parquet format data files in our Data Lake.   
We can also  explore results with SAVE RESULTS or EXPLORE DATA.  
![][image14]

### **\[LAB\] Real time data ingestion into BigQuery using PUB/SUB**

### **Prerequisite : Enable API (you can skip this step if you completed LAB 1\)**

* Make sure all the following APIs are enabled: BigQuery API, Vertex AI API, Pubsub API, BigQuery Connection API, Dataform API, Secret Manager API 

### ***Step 1: Create PUBSUB Topic with schema and BQ subscription***

1. Run the following SQL to create an empty BQ table 

   

| *BigQuery SQL : Create BigQuery Table for streaming ingestion Replace your-project-id with your current project ID* |
| :---- |

 ```
CREATE OR REPLACE TABLE  `your-project-id.ml_datasets.ulb_fraud_detection`
(
Time FLOAT64 ,
V1 FLOAT64 ,
V2 FLOAT64 ,
V3 FLOAT64 ,
V4 FLOAT64 ,
V5 FLOAT64 ,
V6 FLOAT64 ,
V7 FLOAT64 ,
V8 FLOAT64 ,
V9 FLOAT64 ,
V10 FLOAT64 ,
V11 FLOAT64 ,
V12 FLOAT64 ,
V13 FLOAT64 ,
V14 FLOAT64 ,
V15 FLOAT64 ,
V16 FLOAT64 ,
V17 FLOAT64 ,
V18 FLOAT64 ,
V19 FLOAT64 ,
V20 FLOAT64 ,
V21 FLOAT64 ,
V22 FLOAT64 ,
V23 FLOAT64 ,
V24 FLOAT64 ,
V25 FLOAT64 ,
V26 FLOAT64 ,
V27 FLOAT64 ,
V28 FLOAT64 ,
Amount FLOAT64 ,
Class INTEGER,
Feedback String
);

 ```

2. You can find the PUBSUB schema definition ***my\_avro\_fraud\_detection\_schema.json*** file in $HOME/bootkon-h2-2024/data-ingestion/src directory


| *JSON : PubSub Schema Definition (This is the content of the schema definition file, for you information ONLY)* |
| :---- |

```
{
  "type": "record",
  "name": "Avro",
  "fields": [
    {"name": "Time","type": "float"}, 
    {"name": "V1","type": "float"},
    {"name": "V2","type": "float"}, 
    {"name": "V3","type": "float"},
    {"name": "V4","type": "float"},
    {"name": "V5","type": "float"},
    {"name": "V6","type": "float"},
    {"name": "V7","type": "float"},
    {"name": "V8","type": "float"},
    {"name": "V9","type": "float"},
    {"name": "V10","type": "float"},
    {"name": "V11","type": "float"},
    {"name": "V12","type": "float"},
    {"name": "V13","type": "float"},
    {"name": "V14","type": "float"},
    {"name": "V15","type": "float"},
    {"name": "V16","type": "float"},
    {"name": "V17","type": "float"},
    {"name": "V18","type": "float"},
    {"name": "V19","type": "float"},
    {"name": "V20","type": "float"},
    {"name": "V21","type": "float"},
    {"name": "V22","type": "float"},
    {"name": "V23","type": "float"},
    {"name": "V24","type": "float"},
    {"name": "V25","type": "float"},
    {"name": "V26","type": "float"},
    {"name": "V27","type": "float"},
    {"name": "V28","type": "float"},
    {"name": "Amount","type": "float"}, 
    {"name": "Class","type": "int"} , 
    {"name": "Feedback","type": "string"} 

  ]
}

```

3. Create the PubSub Schema Using gcloud

| *Linux command line : Create PubSub Schema* |
| :---- |

```
cd $HOME/bootkon-h2-2024/data-ingestion/src

export PROJECT_ID=your_project_id

gcloud pubsub schemas create my_fraud_detection_schema \
    --project=$PROJECT_ID  \
    --type=AVRO \
    --definition-file=my_avro_fraud_detection_schema.json
```

4. Create the Pub/Sub Topic:

| *Linux command line : Create PubSub Topic* |
| :---- |

```
gcloud pubsub topics create  my_fraud_detection-topic \
    --project=$PROJECT_ID  \
    --schema=my_fraud_detection_schema \
    --message-encoding=BINARY
```

5. In order to grant  The Pub/Sub service account in IAM needs the following BigQuery roles:  
   
   roles/bigquery.dataEditor \
   roles/bigquery.jobUser 

   

   First, Find Your Pub/Sub Service Account:


| *Linux command line : Find out the  Pub/Sub service account email address* |
| :---- |

```
#export PROJECT_ID=your_project_id
export PROJECT_NUM=$(gcloud projects describe ${PROJECT_ID} --format="value(projectNumber)")
echo $PROJECT_NUM
export PUBSUBSVCACCT=service-$PROJECT_NUM@gcp-sa-pubsub.iam.gserviceaccount.com
echo $PUBSUBSVCACCT
   
```

* Then, Grant Permissions (if not already granted), see below commands:


| *Linux command line : Grant privileges to the Pub/Sub service account* |
| :---- |

```
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member=serviceAccount:$PUBSUBSVCACCT --role=roles/bigquery.dataEditor

gcloud projects add-iam-policy-binding $PROJECT_ID \  --member=serviceAccount:$PUBSUBSVCACCT --role=roles/bigquery.jobUser  
```


6. Create the Pub/Sub BQ subscription:  


| *Linux command line : Create a PUBSUB to BQ Subscription* |
| :---- |

```
gcloud pubsub subscriptions create my_fraud_detection-subscription \
    --project=$PROJECT_ID  \
    --topic=my_fraud_detection-topic \
    --bigquery-table=$PROJECT_ID.ml_datasets.ulb_fraud_detection \
--use-topic-schema  
```

*Note: Make sure $PROJECT\_ID is set correctly.* |

### ***Step 2: Ingest data into BQ through PUBSUB***

1.  Create Virtual env:

| *Linux command line : Create a local virtual environment*  |
| :---- |

```
cd $HOME
python3 -m venv hack
source hack/bin/activate
```

2. Install library requirements 

Navigate to the root directory of the cloned repository, for example , bootkon-h2-2024. You find requirements.txt file. By using the requirements file you will be able to install the following packages ; 

google-cloud-aiplatform \
google-api-python-client \
google-cloud \
google-cloud-bigquery \
google-cloud-bigquery-storage \
google-cloud-pubsub \
google-cloud-logging

| *Linux command line : Install the required packages, Run the following commands within your virtual environment called “hack”* |
| :---- |

```
cd $HOME
cd bootkon-h2-2024/
pip install -r requirements.txt 
```

3. **METHOD 1:** Find the **import\_csv\_to\_bigquery\_1.p**y script under *$HOME/bootkon-h2-2024/data-ingestion/src* directory

   *In the script:* 

* *Replace  your-project-id with your project\_id (in 1 location) (leave the double quotes “ unchanged)*   
* *Replace your-project-id with your project\_id in “bucket\_name” (leave “-bucket” at the end) (in 1 location) (leave the double quotes “ unchanged)*  
* *Comment out the Line (just add **\#** at the beginning):  'os.environ\['GOOGLE\_APPLICATION\_CREDENTIALS'\] \= \<service key json location\>/service-key.json'* 

 

| *Python Script : Import data into BigQuery in near real time \[Method 1\]* |
| :---- |

```
import io
import csv
import json
import avro.schema
from avro.io import BinaryEncoder, DatumWriter
from google.cloud import pubsub_v1
from google.cloud import storage
import os


# Set Google Cloud credentials and project details
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '<service key json location>/service-key.json'

project_id = "your-project-id"
topic_id = "my_fraud_detection-topic"
bucket_name = "your-project-id-bucket"
csv_folder_path = "data-ingestion/csv/ulb_fraud_detection/"
schema_file_path = "data-ingestion/src/my_avro_fraud_detection_schema.json"


# Initialize Cloud Storage client and get the bucket
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)


# Load the AVRO schema from GCS
blob = bucket.blob(schema_file_path)
schema_json = json.loads(blob.download_as_text())
avro_schema = avro.schema.parse(json.dumps(schema_json))


# Pub/Sub client initialization
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)


def publish_avro_record(record):
    bytes_io = io.BytesIO()
    writer = DatumWriter(avro_schema)
    encoder = BinaryEncoder(bytes_io)
    writer.write(record, encoder)
    future = publisher.publish(topic_path, bytes_io.getvalue())
    return future.result()


def process_csv_blob(blob):
    temp_file_path = "/tmp/tempfile.csv"
    blob.download_to_filename(temp_file_path)


    with open(temp_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            feedback = row[-1]
            record = {
               "Time": float(row[0]),
               "V1": float(row[1]),
               "V2": float(row[2]),
               "V3": float(row[3]),
               "V4": float(row[4]),
               "V5": float(row[5]),
               "V6": float(row[6]),
               "V7": float(row[7]),
               "V8": float(row[8]),
               "V9": float(row[9]),
               "V10": float(row[10]),
               "V11": float(row[11]),
               "V12": float(row[12]),
               "V13": float(row[13]),
               "V14": float(row[14]),
               "V15": float(row[15]),
               "V16": float(row[16]),
               "V17": float(row[17]),
               "V18": float(row[18]),
               "V19": float(row[19]),
               "V20": float(row[20]),
               "V21": float(row[21]),
               "V22": float(row[22]),
               "V23": float(row[23]),
               "V24": float(row[24]),
               "V25": float(row[25]),
               "V26": float(row[26]),
               "V27": float(row[27]),
               "V28": float(row[28]),
               "Amount": float(row[29]),
               "Class": int(row[30]),
               "Feedback": feedback
           }
            message_id = publish_avro_record(record)
            print(f"Published message with ID: {message_id}")


# Process all CSV files in the folder
blobs = storage_client.list_blobs(bucket, prefix=csv_folder_path)
for blob in blobs:
    if blob.name.endswith('.csv'):
        process_csv_blob(blob)
```

4. **(you can skip this step if you completed LAB 1\)**  Ensure that your project compute engine service account has access to Dataproc worker , BigQuery Data editor, BigQuery Job user , PUBSUB and GCS bucket.  
5. Run the Python Job

| *Linux command line : Execute the script*  |
| :---- |

```
time python $HOME/bootkon-h2-2024/data-ingestion/src/import_csv_to_bigquery_1.py   
```
**Note: Make sure you run the command within your virtual environment called “hack”.***  |

6. Notice the output of the command execution.  
7. After 4 or 5 minutes do interrupt the execution of the script, (perform a ***ctrl \+ c*** command). This method would have taken approximately between ***40 \- 60*** minutes.   
8. Check that there are some rows  inserted into the ulb\_fraud\_detection table. 

| *BigQuery SQL : Check there are some rows inserted into ulb\_fraud\_detection table* |
| :---- |

```
select * from  `your_project_id.ml_datasets.ulb_fraud_detection` ;
```

9. **Important:** Recreate the *\`your\_project\_id.ml\_datasets.ulb\_fraud\_detection\`* table. 

   

| *BigQuery SQL :  Drop and Recreate BigQuery table   \`your-project-id.ml\_datasets.ulb\_fraud\_detection\`* |
| :---- |

```
DROP TABLE  `your-project-id.ml_datasets.ulb_fraud_detection` ;


CREATE OR REPLACE TABLE  `your-project-id.ml_datasets.ulb_fraud_detection`
(
Time FLOAT64 ,
V1 FLOAT64 ,
V2 FLOAT64 ,
V3 FLOAT64 ,
V4 FLOAT64 ,
V5 FLOAT64 ,
V6 FLOAT64 ,
V7 FLOAT64 ,
V8 FLOAT64 ,
V9 FLOAT64 ,
V10 FLOAT64 ,
V11 FLOAT64 ,
V12 FLOAT64 ,
V13 FLOAT64 ,
V14 FLOAT64 ,
V15 FLOAT64 ,
V16 FLOAT64 ,
V17 FLOAT64 ,
V18 FLOAT64 ,
V19 FLOAT64 ,
V20 FLOAT64 ,
V21 FLOAT64 ,
V22 FLOAT64 ,
V23 FLOAT64 ,
V24 FLOAT64 ,
V25 FLOAT64 ,
V26 FLOAT64 ,
V27 FLOAT64 ,
V28 FLOAT64 ,
Amount FLOAT64 ,
Class INTEGER,
Feedback String
);
```

10. **METHOD 2 \[OPTIONAL\] :** find the  import\_csv\_to\_bigquery\_2.py under *$HOME/bootkon-h2-2024/data-ingestion/src* directory

    *In the script:* 

* *Replace  your-project-id with your project\_id (in 1 location) (leave the double quotes “ unchanged)*  
* *Replace, in  bucket\_name   your-project-id  with your project\_id (leave the “-bucket” suffix) (in 1 location) (leave the double quotes “ unchanged)*  
* *Comment out the Line (just add \# at the beginning): the os.environ\['GOOGLE\_APPLICATION\_CREDENTIALS'\] \= '\<service key json location\>/service-key.json'* 

| *Python Script : Import data into BigQuery in near real time \[Method 2\]* |
| :---- |

```
import io
import csv
import json
import avro.schema
from avro.io import BinaryEncoder, DatumWriter
from google.cloud import pubsub_v1
from google.cloud import storage
import os


# Set Google Cloud credentials and project details
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '<service key json location>/service-key.json'
project_id = "your-project-id"
topic_id = "my_fraud_detection-topic"
bucket_name = "your-project-id-bucket"
csv_folder_path = "data-ingestion/csv/ulb_fraud_detection/"
schema_file_path = "data-ingestion/src/my_avro_fraud_detection_schema.json"


# Initialize Cloud Storage client
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
# Load the AVRO schema from GCS
blob = bucket.blob(schema_file_path)
schema_json = json.loads(blob.download_as_text())
avro_schema = avro.schema.parse(json.dumps(schema_json))


# Pub/Sub client initialization with batch settings
batch_settings = pubsub_v1.types.BatchSettings(
    max_bytes=1024 * 1024,  # One megabyte
    max_latency=1,  # One second
    max_messages=100  # 100 messages
)
publisher = pubsub_v1.PublisherClient(batch_settings=batch_settings)
topic_path = publisher.topic_path(project_id, topic_id)


def publish_avro_record(records_batch):
    """
    Encodes records to AVRO format and publishes them to the specified Pub/Sub topic.
    """
    futures = []
    for record in records_batch:
        # Serialize data
        bytes_io = io.BytesIO()
        writer = DatumWriter(avro_schema)
        encoder = BinaryEncoder(bytes_io)
        writer.write(record, encoder)
        # Publish data
        future = publisher.publish(topic_path, bytes_io.getvalue())
        futures.append(future)
    return futures


def process_csv_blob(blob):
    """
    Reads a CSV file from GCS, encodes rows to AVRO, and publishes in batches to Pub/Sub.
    """
    temp_file_path = "/tmp/tempfile.csv"
    blob.download_to_filename(temp_file_path)


    records_batch = []
    with open(temp_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            feedback = row[-1]
            record = {
               "Time": float(row[0]),
               "V1": float(row[1]),
               "V2": float(row[2]),
               "V3": float(row[3]),
               "V4": float(row[4]),
               "V5": float(row[5]),
               "V6": float(row[6]),
               "V7": float(row[7]),
               "V8": float(row[8]),
               "V9": float(row[9]),
               "V10": float(row[10]),
               "V11": float(row[11]),
               "V12": float(row[12]),
               "V13": float(row[13]),
               "V14": float(row[14]),
               "V15": float(row[15]),
               "V16": float(row[16]),
               "V17": float(row[17]),
               "V18": float(row[18]),
               "V19": float(row[19]),
               "V20": float(row[20]),
               "V21": float(row[21]),
               "V22": float(row[22]),
               "V23": float(row[23]),
               "V24": float(row[24]),
               "V25": float(row[25]),
               "V26": float(row[26]),
               "V27": float(row[27]),
               "V28": float(row[28]),
               "Amount": float(row[29]),
               "Class": int(row[30]),
               "Feedback": feedback
           }
            records_batch.append(record)
            if len(records_batch) >= 100:
                publish_avro_record(records_batch)
                records_batch = []
        if records_batch:
            publish_avro_record(records_batch)


# List and process all CSV files
blobs = storage_client.list_blobs(bucket, prefix=csv_folder_path)
for blob in blobs:
    if blob.name.endswith('.csv'):
        process_csv_blob(blob)

```


11. **(you can skip this step if you completed LAB 1\)** Ensure that your project  compute engine service account has access to Dataproc worker , BigQuery Data editor, BigQuery Job user , PUBSUB and GCS bucket.  
12. Run the Python Job   
    Notice the time it takes to run. Notice the differences between import\_csv\_to\_bigquery\_1.py and import\_csv\_to\_bigquery\_2.py execution time.   The execution of METHOD 1 would have taken approximately between ***40 \- 60 minutes***. 

| *Linux command line : Execute the script (execution should take between 1-2 minutes)* |
| :---- |

```
time python  $HOME/bootkon-h2-2024/data-ingestion/src/import_csv_to_bigquery_2.py  
```
**Note: Make sure you run the command within your virtual environment called “hack”.***  |

13. Check Bigquery row count. 

| *BigQuery SQL : Table Count* |
| :---- |

```
select count(*) from  `your_project_id.ml_datasets.ulb_fraud_detection` ; 
```

Note: The query should return a few hundred thousand records, but the exact count may fluctuate as Pub/Sub continues loading data. The exact count isn't critical. You don't need to wait for the entire ingestion to finish; feel free to proceed with Lab 3 while the data loads in the background.* |

    [TASK\] Take up to a couple (2) of minutes and discuss within your group the key differences between Method 1 and Method 2\. Focus specifically on how the execution time and overall efficiency compare between the two methods.*

### **\[OPTIONAL LAB\] Batch data ingestion into BigQuery using Dataproc**

### Google Cloud Dataproc is a fully managed and scalable service for running Apache Hadoop, Apache Spark, Apache Flink, Presto, and 30+ open source tools and frameworks. Dataproc allows data to be loaded and also transformed or pre-processed as it is brought in.

### **Serverless Dataproc** 

In this lab the Paquet-format files are imported from Google Cloud Storage into BigQuery using PySpark. The label details the steps, including setup and code implementation. 

#### **Prerequisites: (you can skip this step if you completed LAB 1\)**

* Google Cloud Storage (GCS): Ensure your Parquet files are stored in a GCS bucket.  
* BigQuery Dataset & Table: Create or have a BigQuery dataset and table where you want to load the data.  
* Google Cloud SDK: Install the Google Cloud SDK if you intend to use the command line. For simplicity we will use Cloud shell.   
* Enable APIs: Enable the BigQuery, Cloud Storage, and Dataproc Serverless APIs for your project.  
* Download BigQuery Connector for Spark: To read from BigQuery, you'll need the BigQuery Connector for Spark. This should be included in your Spark job's dependencies.  
  * Download Spark 3.5 Jar version : [https://github.com/GoogleCloudDataproc/spark-bigquery-connector](https://github.com/GoogleCloudDataproc/spark-bigquery-connector)  
  * Upload to GCS: *gs://${BUCKET\_NAME}*/jar/

#### **IAM Roles: (you can skip this step if you completed LAB 1\)**

Ensure your Google Cloud user account or service account has the following roles:

* Dataproc Editor (roles/dataproc.editor): Allows for the creation and running of Dataproc Serverless jobs.  
* BigQuery Data Editor (roles/bigquery.dataEditor): Allows for creating tables and inserting data into BigQuery.  
* Storage Object Viewer (roles/storage.objectViewer): Allows reading data from the specified GCS bucket.

#### **Set Up a Dataproc Serverless Spark Batch:**

1. Create an empty BigQuery table ;   
   *Replace your-project-id with your current project ID, and run this query:*  
   

| *BigQuery SQL :  Create BigQuery table for parquet data* |
| :---- |

```
CREATE OR REPLACE TABLE `your-project-id.ml_datasets.ulb_fraud_detection_parquet` AS SELECT * from  `your-project-id.ml_datasets.ulb_fraud_detection_blake` where 1=2;
```

 
2. Download and upload parquet files to GCS **(you can skip this step if you completed LAB 1).**  
3. In Cloud shell, go to directory ; **cd *$HOME/bootkon-h2-2024/data-ingestion/src***   
4. Prepare the **import\_parquet\_to\_bigquery.py** PySpark Script:  
   Adapt your script to read from GCS and write to BigQuery. Ensure you specify the GCS path to your Parquet files and the target BigQuery table.  
- *Replace your-project-id with your current project ID (in 3 locations) (leave the double quotes “ unchanged)*


| *PySpark  Script : Import parquet data into BigQuery table.* |
| :---- |

```
from pyspark.sql import SparkSession

project_id = "your-project-id"
gcs_parquet_path = "gs://your-project-id-bucket/data-ingestion/parquet/ulb_fraud_detection/"

bq_dataset_name = "ml_datasets"
bq_table_name = "ulb_fraud_detection_parquet"

temporary_gcs_bucket = "your-project-id-bucket"

spark = SparkSession.builder\
   .appName("bigquery_to_gcs_parquet")\
   .getOrCreate()

df = spark.read.parquet(gcs_parquet_path)

df.write.format("bigquery") \
    .option("table", f"{project_id}:{bq_dataset_name}.{bq_table_name}") \
    .option("temporaryGcsBucket", temporary_gcs_bucket) \
    .mode("overwrite") \
    .save()

spark.stop()
```


5. Submit a Dataproc Serverless Batch Job:

   Use the Google Cloud Console or the gcloud command-line tool to submit your PySpark job. Here is an example gcloud command (run it from cloud shell):

- *Replace your-project-id with your current project ID (in 3 locations) and your-region  with your GCP region, for example ; us-central1*


| *Linux command line : Submit spark job to Dataproc* |
| :---- |

```
gcloud dataproc batches submit pyspark import_parquet_to_bigquery.py \
    --project=your-project-id \
     --region=your-region \
    --deps-bucket=gs://your-project-id-bucket \
```

This command specifies:

* The location of your PySpark script in GCS.  
* The project and region to run in.  
* A GCS bucket (--deps-bucket) for Dataproc to use for job dependencies.


  

6. Monitor the job execution progress in Dataproc;

From the search write : dataproc   
![][image15]

7. Click on Batches and monitor the execution log from the console   
   ![][image16]  
8. After the Dataproc job completes, confirm that data has been loaded into the BigQuery table (replace your-project-id with your project ID). You should see over 200,000 records, but the exact count isn't critical.  
   Use the following query to check:  
   *SELECT count(\*) FROM \`your-project-id.ml\_datasets.ulb\_fraud\_detection\_parquet\`*  

**🥳🥳Congratulations on completing Lab 2\!**   
**You can now move on to Lab 3 for further practice. 🥳🥳**  


## **\[Hands-on Lab \- 3\] ELT: Dataform & LLM for sentiment analysis from BigQuery**

<walkthrough-tutorial-duration duration="45"></walkthrough-tutorial-duration>
<walkthrough-tutorial-difficulty difficulty="3"></walkthrough-tutorial-difficulty>

Original document [here](https://docs.google.com/document/d/1NxfggQunrCn6ZfwGXAaA_lABDmXtRsfH88jkMDbqlJo/edit?usp=drive_link)

Goal of the lab: We gather user feedback to assess the impact of model adjustments on real-world use (prediction), ensuring that our fraud detection system effectively balances accuracy with user satisfaction. Use Dataform , BigQuery and Gemini to Perform sentiment analysis of customer feedback.

CAUTION:  
This lab is for educational purposes only and should be used with caution in production environments. Google Cloud Platform (GCP) products are changing frequently, and screenshots and instructions might become inaccurate over time. Always refer to the latest GCP documentation for the most up-to-date information.


### ***READING Section : Read the following Explanation of what dataform is and what is its purpose*** 

### **Dataform** 

Dataform is a fully managed service that helps data teams build, version control, and orchestrate SQL workflows in BigQuery. It provides an end-to-end experience for data transformation, including:

* Table definition: Dataform provides a central repository for managing table definitions, column descriptions, and data quality assertions. This makes it easy to keep track of your data schema and ensure that your data is consistent and reliable.  
* Dependency management: Dataform automatically manages the dependencies between your tables, ensuring that they are always processed in the correct order. This simplifies the development and maintenance of complex data pipelines.  
* Orchestration: Dataform orchestrates the execution of your SQL workflows, taking care of all the operational overhead. This frees you up to focus on developing and refining your data pipelines.

Dataform is built on top of Dataform Core, an open source SQL-based language for managing data transformations. Dataform Core provides a variety of features that make it easy to develop and maintain data pipelines, including:

* Incremental updates: Dataform Core can incrementally update your tables, only processing the data that has changed since the last update. This can significantly improve the performance and scalability of your data pipelines.  
* Slowly changing dimensions: Dataform Core provides built-in support for slowly changing dimensions, which are a common type of data in data warehouses. This simplifies the development and maintenance of data pipelines that involve slowly changing dimensions.  
* Reusable code: Dataform Core allows you to write reusable code in JavaScript, which can be used to implement complex data transformations and workflows.

Dataform is integrated with a variety of other Google Cloud services, including GitHub, GitLab, Cloud Composer, and Workflows. This makes it easy to integrate Dataform with your existing development and orchestration workflows.  
Benefits of using Dataform in Google Cloud  
There are many benefits to using Dataform in Google Cloud, including:

* Increased productivity: Dataform can help you to increase the productivity of your data team by automating the development, testing, and execution of data pipelines.  
* Improved data quality: Dataform can help you to improve the quality of your data by providing a central repository for managing table definitions, column descriptions, and data quality assertions.  
* Reduced costs: Dataform can help you to reduce the costs associated with data processing by optimizing the execution of your SQL workflows.  
* Increased scalability: Dataform can help you to scale your data pipelines to meet the needs of your growing business.

### **Use cases for Dataform**

Dataform can be used for a variety of use cases, including:

* Data warehousing: Dataform can be used to build and maintain data warehouses that are scalable and reliable.  
* Data engineering: Dataform can be used to develop and maintain data pipelines that transform and load data into data warehouses.  
* Data analytics: Dataform can be used to develop and maintain data pipelines that prepare data for analysis.  
* Machine learning: Dataform can be used to develop and maintain data pipelines that prepare data for machine learning models.

### ***LAB Section : Dataform Prerequisites*** 

**SKIP below Steps 1, 2 and 3 if you already completed LAB 1** 

1. ### **Enable Services API (you can skip this step if you completed LAB 1\)**

Ensure all necessary APIs (BigQuery API, Vertex AI API, BigQuery Connection API, Dataform API, Secret Manager API) are [enabled](https://console.cloud.google.com/flows/enableapi?apiid=storage-component.googleapis.com%2Cpubsub.googleapis.com%2Cbigquery.googleapis.com%2Cbigqueryconnection.googleapis.com%2Caiplatform.googleapis.com&_ga=2.132962701.243207769.1688884437-279425947.1688884437)

2. ### **Create a connection to an external data source in BigQuery (you can skip this step if you completed LAB 1\)**

* Create an External Connection (Enable BQ Connection API if not already done) and note down the Service Account id from the connection configuration details:  
* Click the \+ADD button on the BigQuery Explorer pane (in the left of the BigQuery console) and click “Connection to external data sources” in the popular sources listed  
* Select Connection type as “Vertex AI remote models , remote functions and Biglake” and provide “fraud-transactions-conn” as Connection ID, select Multi Region location type.  
  ![][image2]  
* Once the connection is created, take a note of the Service Account generated from the connection configuration details

3. ### **Grant Permissions  (you can skip this step if you completed LAB 1\)**

In this step we will grant permissions to the Service Account to access the Vertex AI service:  
Open IAM and add the Service Account you copied after creating the external connection as the Principal and select “Vertex AI User” Role.

4. ### **Using Large Language Models from Vertex AI  (info only)**

Google Cloud’s language models are available within the Vertex AI Studio inside the Vertex AI service.  
**![][image3]**

5. ### **Prompt design (info only)**

Prompt design is the process of creating prompts that elicit the desired response from language models. Writing well structured prompts is an essential part of ensuring accurate, high quality responses from a language model.  
If you need to understand this concept a bit more this is a page that introduces some basic concepts, strategies, and best practices to get you started in designing prompts ([https://cloud.google.com/vertex-ai/docs/generative-ai/learn/introduction-prompt-design](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/introduction-prompt-design)).  
The reference page above also goes into the more advanced settings you can see on the right hand side of the prompt box such as temperature, top K, top P etc.

### ***LAB Section : Creating a Dataform Pipeline***

First step in implementing a pipeline in Dataform is to set up a repository and a development environment. Detailed quickstart and instructions can be found [here](https://cloud.google.com/dataform/docs/quickstart-create-workflow).

Navigate to the BigQuery section in the Google Cloud Platform console, and then select Dataform.  
![][image4]

1. ### **Create a Repository in Dataform** 

Click the “+ CREATE REPOSITORY” button near the top of the page.  
![][image5]  
Use the following values when creating the repository:

- Repository ID: “hackathon-repository”  
- Region: (us-central1)  
- Service Account: (Default Dataform service account)  
  ![][image6]

And click “CREATE”

2. ### **Dataform Service Account** 

Take note and save somewhere the newly created service account for Dataform.  
Example: service-112412469323@gcp-sa-dataform.iam.gserviceaccount.com

![][image7]  
Click “GO TO REPOSITORIES”, and then click on the “hackathon-repository”, the new repository you just created.  
![][image8]

3. ### **Create and initialize a Dataform development workspace**

You should now be in the “DEVELOPMENT WORKSPACES” tab of the hackathon-repository page.

1. Click add **Create development workspace**.  
2. In the **Create development workspace** window, do the following:  
   1. In the **Workspace ID** field, enter “hackathon-\<YOURLASTNAME\>-workspace” (replace \<YOURLASTNAME\> with your name)  
   2. Click **Create**.  
3. The development workspace page appears.  
4. Click on the newly created development workspace   
5. Click **Initialize workspace**.

6. You will copy the dataform files from the following repository, in the next steps.   
   [https://github.com/dace-de/bootkon-h2-2024/tree/main/dataform](https://github.com/dace-de/bootkon-h2-2024/tree/main/dataform)   
7. *Edit  **workflow\_settings.yaml** file :*   
* *Replace defaultDataset value with **ml\_datasets ,***   
* make sure defaultProject value is ***your project id***   
  ***Note:*** Nevermind if you have a different dataform core version, just continue

  *![][image9]*  
* Click on Install Packages ***Only*** ***Once***. You should see a message at the bottom of the page:

  *Package installation succeeded*

8. *Remove the default auto-generated SQLX files; Delete the following files from the “definitions” folder:*  
* *first\_view.sqlx*  
* *second\_view.sqlx*

  *![][image10]*

9. *Click on definitions and create a new directory called “models”:* 

   *![][image11]*

10. *Click on models directory and create 2 new files ;  (make sure all file names are in lowercase and avoid adding spaces to the file names)*  
* [create\_dataset.sqlx](https://github.com/dace-de/bootkon-h2-2024/blob/main/dataform/definitions/models/create_dataset.sqlx)  
* [llm\_model\_connection.sqlx](https://github.com/dace-de/bootkon-h2-2024/blob/main/dataform/definitions/models/llm_model_connection.sqlx)

	  
Those files should be created under ***definitions/models*** directory

*Example:*

*![][image12]*

11. *Copy the contents from [https://github.com/dace-de/bootkon-h2-2024/tree/main/dataform/definitions/models](https://github.com/dace-de/bootkon-h2-2024/tree/main/dataform/definitions/models)  to each of those files.*  
12. *Click on definitions and create 3 new files: (make sure all file names are in lowercase and avoid adding spaces to the file names)*  
* [mview\_ulb\_fraud\_detection.sqlx](https://github.com/dace-de/bootkon-h2-2024/blob/main/dataform/definitions/mview_ulb_fraud_detection.sqlx)  
* [sentiment\_inference.sqlx](https://github.com/dace-de/bootkon-h2-2024/blob/main/dataform/definitions/sentiment_inference.sqlx)  
* [ulb\_fraud\_detection.sqlx](https://github.com/dace-de/bootkon-h2-2024/blob/main/dataform/definitions/ulb_fraud_detection.sqlx)


Those files should be created under ***definitions*** directory

*Example:* 

*![][image13]*

13. *Copy the contents from [https://github.com/dace-de/bootkon-h2-2024/tree/main/dataform/definitions](https://github.com/dace-de/bootkon-h2-2024/tree/main/dataform/definitions) to each of those files.*  
14. *Set the database value to your project ID value in ulb\_fraud\_detection.sqlx file:*

    *![][image14]*

15. *In llm\_model\_connection.sqlx, replace the \`us.llm-connection\` connection with the connection name you have created in LAB 2 during the BigLake section.  If you have followed the steps in LAB 2, the connected name should be “**us.fraud-transactions-conn***”  
    Notice the usage of $ref in line 11, of ***definitions/mview\_ulb\_fraud\_detection.sqlx***  
     “sqlx” file. The advantages of using $ref in Dataform are

* Automatic Reference Management: Ensures correct fully-qualified names for tables and views, avoiding hardcoding and simplifying environment configuration.  
* Dependency Tracking: Builds a dependency graph, ensuring correct creation order and automatic updates when referenced tables change.  
* Enhanced Maintainability: Supports modular and reusable SQL scripts, making the codebase easier to maintain and less error-prone.

5. *Run the dataset creation by TAG. TAG allows you to just execute parts of the workflows and not the entire workflow. Click on Start Execution \> Tags \> "dataset\_ulb\_fraud\_detection\_llm” \> Start Execution*  
   

   *![][image15]*  
6. *Click on Details;*

   *![][image16]*

7. *Notice the Access Denied error on BigQuery for the dataform service account XXX@gcp-sa-dataform.iam.gserviceaccount.com;*

   *![][image17]*

8.  Go to IAM & Admin  \> Grant access and grant ***BigQuery Data Editor , BigQuery Job User and BigQuery Connection User***  to the data from the service account.  Click on Save.


   ![][image18]

   ***Note:*** If you encounter the following policy update screen, just click on update.

   ![][image19]

9. Go back to dataform from the BigQuery console, and retry step ***5***. Notice the execution status. It should be a success.  
   ![][image20]  
10. Click on Compiled graph and explore it;  
    Go to ***Dataform \> hackathon-\<lastname\>-workspace \> Compiled Graph***  
    ![][image21]

### ***LAB Section : Execute the workspace workflow***

1. For  the sentiment inference step to succeed . You need to grant the external connection service account the Vertex AI user privilege. More details can be found in this [link](https://cloud.google.com/bigquery/docs/generate-text-tutorial#grant-permissions). You can find the service account ID under BigQuery Studio \> Your project ID  (example: bootkon-dryrun24ber-886) \> External connections \> fraud-transactions-conn  
     
   ![][image22]  
    ![][image23]

2. Take note of the service account and grant it the ***Vertex AI User*** role.   
   ![][image24]  
     
3. *Back in your Dataform workspace, click **START EXECUTION** from the top menu, then* **“Execute actions”***.*  
   ![][image25]  
4. Click on ***ALL ACTIONS*** Tab then Click on ***START EXECUTION***  
   ![][image26]

5. Check the execution status. It should be a success.  
6. Verify the new table **sentiment\_inference** in the ml\_datasets dataset in BigQuery.  
7. Query the BigQuery table content (At this point you should be familiar with running BigQuery SQL)  
   

| *BigQuery SQL : Check few rows of* sentiment\_inference table |
| :---- |

```
SELECT distinct ml_generate_text_llm_result,
prompt,
Feedback
FROM `ml_datasets.sentiment_inference` LIMIT 10;
```
   

8. **\[Max 2 minutes\]** Discuss the table results within your team group.

9. Before moving to the challenge section of the Lab, go back to the CODE section of the Dataform workspace. At the top of the “Files” section on the left, click ***“Commit X Changes”*** (X should be about 7), add a commit message like, “Bootkon Lab 3”, then click “***Commit all files***” and then ***“Push to Default Branch”***   
   ***![][image27]***

You should now have the message   
***![][image28]***

# ***CHALLENGE Section : Production, Scheduling and Automation*** 

Automate and schedule the compilation and execution of the pipeline. This is done using release configurations and workflow configurations.

***Release Configurations:***  
Release configurations allow you to compile your pipeline code at specific intervals that suit your use case. You can define:

* Branch, Tag, or Commit SHA: Specify which version of your code to use.  
* Frequency: Set how often the compilation should occur, such as daily or weekly.  
* Compilation Overrides: Use settings for testing and development, such as running the pipeline in an isolated project or dataset/table.  
    
  Common practice includes setting up release configurations for both test and production environments. For more information, refer to the [release configuration documentation](https://cloud.google.com/dataform/docs/release-configurations).  
    
  **Workflow Configurations**  
    
  To execute a pipeline based on your specifications and code structure, you need to set up a workflow configuration. This acts as a scheduler where you define:  
    
* Release Configuration: Choose the release configuration to use.  
* Frequency: Set how often the pipeline should run.  
* Actions to Execute: Specify what actions to perform during each run.

  The pipeline will run at the defined frequency using the compiled code from the specified release configuration. For more information, refer to the [workflow configurations documentation](https://cloud.google.com/dataform/docs/workflow-configurations).

  *\[TASK\] Challenge : Take up to 10 minutes to Setup a Daily Frequency Execution of the Workflow*


  ***Goal:*** Set up a daily schedule to automate and execute the workflow you created.

1. Automate and schedule the pipeline’s compilation and execution.  
2. Define release configurations for one production environment (optionally: you can create another one for dev environment)  
3. Set up workflow configurations to schedule pipeline execution (use dataform service account).  
4. Set up a 3 minute frequency execution of the workflow you have created.  
     
     
   ***Note:*** If you are stuck and cannot figure out how to proceed after a few minutes, ask the event moderator for help.

**🥳🥳Congratulations on completing Lab 3\!**   
**You can now move on to Lab 4 for further practice. 🥳🥳**  




# **\<Lunch Time: 60 Minutes\>**

## **\[Hands-on Lab \- 4\] ML Operations with Vertex AI**

<walkthrough-tutorial-duration duration="60"></walkthrough-tutorial-duration>
<walkthrough-tutorial-difficulty difficulty="3"></walkthrough-tutorial-difficulty>

Original document: [here](https://docs.google.com/document/d/1UdI1ffZdjy--_2xNmemQKzPCRXvCVw8JAroZqewiPMs/edit?usp=drive_link)


***Note: You can start Hands-on Lab 5 while the Hands-on Lab 4 training jobs in Notebooks 2 & 3 are still running.***  

**Finally, we create a Vertex AI Notebook (JupyterLab)**

1. Go to Vertex AI in the GCP console.

      ![alt vertexai](https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/vertexai.png?raw=true)

      <a href="https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/vertexai.png?raw=true" target="_parent">View image</a>

2. Click on the Workbench section.

      ![alt workbench](https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/workbench.png?raw=true)

      <a href="https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/workbench.png?raw=true" target="_parent">View image</a>

3. Select “User managed notebooks” 

      ![alt usermanagednotebooks](https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/usermanagednotebooks.png?raw=true)

      <a href="https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/usermanagednotebooks.png?raw=true" target="_parent">View image</a>

4.  “Create new”

      ![alt createnew](https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/createnew.png?raw=true)

      <a href="https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/createnew.png?raw=true" target="_parent">View image</a>

   

5. Name the notebook “***bootkon***” and leave the default network and environment. Leave the cheapest machine type; e2-standard-4 selected; 4 vCPUs and 16GB of RAM are more than enough to perform the ML labs using jupyter notebooks. Do not attach a GPU. Normally it takes around 10 minutes to get the instance created.

   ![alt notebookbootkon](https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/notebookbootkon.png?raw=true)

   <a href="https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/notebookbootkon.png?raw=true" target="_parent">View image</a>

6. Open the Jupyter Lab;

   ![alt openjupyter](https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/openjupyter.png?raw=true)

   <a href="https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/openjupyter.png?raw=true" target="_parent">View image</a>

7. From the Jupyter Lab top menu, click on Git \-\> Clone a Repository 

   ![alt clonerepo](https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/clonerepo.png?raw=true)

   <a href="https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/clonerepo.png?raw=true" target="_parent">View image</a>

8. Enter [https://github.com/fhirschmann/bootkon-h2-2024.git](https://github.com/fhirschmann/bootkon-h2-2024.git) and click on **clone**

   ![alt clonerepo2](https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/clonerepo2.png?raw=true)

   <a href="https://github.com/fhirschmann/bootkon-ng/blob/main/img/lab1/clonerepo2.png?raw=true" target="_parent">View image</a>


## **\[Hands-on Lab \- 5\] Agent Builder and Gemini**

Original document [here](https://docs.google.com/document/d/1_8-HEEIKCCUkwoorpWq8lOI3M1Rn6HqY4SlCW8AitGg/edit?usp=drive_link)

**\<Coffee Break: 30 Minutes\>**

## **Demo Data Canvas & Looker Studio**

No Instructions

**Architecture Challenge**  
No Instructions

To get started, click **Start**




# Tutorial title

<walkthrough-finish-button title="More solutions" tutorial="panels--sic--data-warehouse_toc"></walkthrough-finish-button>

## Congrats!

You have now completed the tutorial for this solution!
