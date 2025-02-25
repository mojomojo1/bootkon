# Lab 4: Machine Learning with Vertex AI

Author: 
* Fabian Hirschmann <<fhirschmann@google.com>>

Welcome back 👋😍. During this lab, you will train a machine learning model on the data set you already know. We will deploy it to Vertex AI and finally construct a machine learning pipeline to perform the training process automatically.

We will do it in three different maturity levels:

1. Deploying locally trained models to Vertex AI using prebuilt containers
2. Train and deploy model on Vertex AI using custom containers
3. Use Vertex AI pipeline to train and deploy the model

In this Jupyter Notebook, you can press `Shift + Return` to execute the current code junk and jump to the next one.

## Step 0: Install requirements


```python
!pip install --upgrade --quiet \
    google-cloud-aiplatform==1.72.0 \
    google-cloud-bigquery \
    google-cloud-bigquery \
    google-cloud-logging \
    google-cloud-pipeline-components==2.18.0 \
    fastavro \
    avro \
    pandas
```

Once the command above has finished, <font color=red>please restart your kernel from the menu (Kernel -> Restart Kernel) and continue with step 1.</font>

## Step 1: Import Dependencies and Set Environment Variables

Before we begin, let's import the necessary Python libraries and set a few environment variables for our project.


```python
import random
random.seed(1337)
import os
import string
import random
import logging

import pandas as pd
from google.cloud import aiplatform, bigquery
from sklearn.metrics import roc_curve, auc as auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score

import joblib

import google.cloud.logging
google.cloud.logging.Client().setup_logging(log_level=logging.WARNING)

project = !gcloud config get-value project
PROJECT_ID = project[0]

REGION = "us-central1"
BQ_DATASET = "ml_datasets"
BQ_TABLE = "ulb_fraud_detection_dataproc"
BQ_SOURCE = f"{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"
PIPELINE_ROOT = f"gs://{PROJECT_ID}-bucket/pipelines"
TRAIN_IMAGE_URI=f"{REGION}-docker.pkg.dev/{PROJECT_ID}/bootkon/bootkon-train:latest"
PREDICT_IMAGE_URI=f"{REGION}-docker.pkg.dev/{PROJECT_ID}/bootkon/bootkon-predict:latest"
```

## Step 2: Create dataset for ML

We initialize the AI Platform and BigQuery client to interact with Google Cloud services.


```python
aiplatform.init(project=PROJECT_ID, location=REGION, staging_bucket=f"{PROJECT_ID}-bucket")
bq = bigquery.Client(project=PROJECT_ID, location="us")
```

The BigQuery table we'll be working with is as follows:


```python
BQ_SOURCE
```




    'astute-ace-336608.ml_datasets.ulb_fraud_detection_dataproc'



We execute a query to fetch the dataset from BigQuery and store it in a Pandas DataFrame. We don't need the `Feedback` column for machine learning -- so we will delete it.


```python
data = bq.query(f"SELECT * FROM `{BQ_SOURCE}`").to_dataframe()
data.drop("Feedback", axis=1, inplace=True)
```

Let's have a look at the data set in more detail.


```python
data
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Time</th>
      <th>V1</th>
      <th>V2</th>
      <th>V3</th>
      <th>V4</th>
      <th>V5</th>
      <th>V6</th>
      <th>V7</th>
      <th>V8</th>
      <th>V9</th>
      <th>...</th>
      <th>V21</th>
      <th>V22</th>
      <th>V23</th>
      <th>V24</th>
      <th>V25</th>
      <th>V26</th>
      <th>V27</th>
      <th>V28</th>
      <th>Amount</th>
      <th>Class</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>67573.0</td>
      <td>1.247292</td>
      <td>-1.214023</td>
      <td>1.717765</td>
      <td>-0.129889</td>
      <td>-2.118590</td>
      <td>0.358109</td>
      <td>-1.763690</td>
      <td>0.452637</td>
      <td>0.986597</td>
      <td>...</td>
      <td>0.164138</td>
      <td>0.776612</td>
      <td>0.004733</td>
      <td>0.428537</td>
      <td>0.297247</td>
      <td>-0.029560</td>
      <td>0.090474</td>
      <td>0.022572</td>
      <td>2.0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>127999.0</td>
      <td>-1.534523</td>
      <td>1.122946</td>
      <td>-3.437084</td>
      <td>-0.797825</td>
      <td>1.015405</td>
      <td>-1.250023</td>
      <td>0.585146</td>
      <td>0.872816</td>
      <td>-0.892797</td>
      <td>...</td>
      <td>0.516332</td>
      <td>1.529644</td>
      <td>0.246227</td>
      <td>0.313690</td>
      <td>-0.999467</td>
      <td>0.660153</td>
      <td>0.258338</td>
      <td>-0.068222</td>
      <td>2.0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>145149.0</td>
      <td>2.156547</td>
      <td>0.100973</td>
      <td>-2.700733</td>
      <td>-0.048208</td>
      <td>1.143939</td>
      <td>-0.896822</td>
      <td>0.817691</td>
      <td>-0.407689</td>
      <td>-0.310319</td>
      <td>...</td>
      <td>0.267644</td>
      <td>0.882000</td>
      <td>-0.195982</td>
      <td>0.389867</td>
      <td>0.657228</td>
      <td>0.993540</td>
      <td>-0.157356</td>
      <td>-0.106062</td>
      <td>2.0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>153187.0</td>
      <td>-1.070276</td>
      <td>0.750548</td>
      <td>-0.432043</td>
      <td>0.795662</td>
      <td>1.894683</td>
      <td>-0.913714</td>
      <td>1.370461</td>
      <td>-0.728018</td>
      <td>-0.391775</td>
      <td>...</td>
      <td>0.084740</td>
      <td>0.626613</td>
      <td>-0.215756</td>
      <td>0.581448</td>
      <td>0.018814</td>
      <td>-0.465960</td>
      <td>-0.551073</td>
      <td>0.009276</td>
      <td>2.0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>152869.0</td>
      <td>2.136909</td>
      <td>0.088646</td>
      <td>-2.490914</td>
      <td>0.098321</td>
      <td>0.789008</td>
      <td>-1.399582</td>
      <td>0.854902</td>
      <td>-0.492912</td>
      <td>-0.254999</td>
      <td>...</td>
      <td>0.278034</td>
      <td>0.934892</td>
      <td>-0.211839</td>
      <td>-0.234266</td>
      <td>0.609699</td>
      <td>1.020898</td>
      <td>-0.154427</td>
      <td>-0.112532</td>
      <td>2.0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>284802</th>
      <td>63644.0</td>
      <td>0.971875</td>
      <td>-0.050017</td>
      <td>0.745618</td>
      <td>0.992303</td>
      <td>-0.024952</td>
      <td>1.071646</td>
      <td>-0.465425</td>
      <td>0.532930</td>
      <td>0.318431</td>
      <td>...</td>
      <td>-0.054716</td>
      <td>-0.102631</td>
      <td>0.281037</td>
      <td>-0.703291</td>
      <td>-0.102724</td>
      <td>-0.512912</td>
      <td>0.098703</td>
      <td>0.023487</td>
      <td>20.0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>284803</th>
      <td>82872.0</td>
      <td>1.562782</td>
      <td>-1.229601</td>
      <td>-1.158630</td>
      <td>-2.496174</td>
      <td>0.974909</td>
      <td>3.237633</td>
      <td>-1.478926</td>
      <td>0.745097</td>
      <td>-1.985665</td>
      <td>...</td>
      <td>-0.263261</td>
      <td>-0.527888</td>
      <td>-0.006884</td>
      <td>0.982099</td>
      <td>0.546208</td>
      <td>-0.191959</td>
      <td>0.031388</td>
      <td>0.015444</td>
      <td>20.0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>284804</th>
      <td>143865.0</td>
      <td>2.277261</td>
      <td>-1.618792</td>
      <td>-2.363003</td>
      <td>-2.596243</td>
      <td>1.166023</td>
      <td>3.433015</td>
      <td>-1.622363</td>
      <td>0.798377</td>
      <td>-1.403863</td>
      <td>...</td>
      <td>-0.166966</td>
      <td>-0.075929</td>
      <td>0.263730</td>
      <td>0.687151</td>
      <td>-0.130091</td>
      <td>-0.140835</td>
      <td>0.027717</td>
      <td>-0.056861</td>
      <td>20.0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>284805</th>
      <td>36081.0</td>
      <td>1.306817</td>
      <td>-0.541898</td>
      <td>0.166026</td>
      <td>-0.632248</td>
      <td>-0.698127</td>
      <td>-0.418271</td>
      <td>-0.424042</td>
      <td>-0.036891</td>
      <td>-1.062217</td>
      <td>...</td>
      <td>0.250819</td>
      <td>0.764577</td>
      <td>-0.132648</td>
      <td>0.281172</td>
      <td>0.660827</td>
      <td>-0.066862</td>
      <td>0.003071</td>
      <td>-0.005665</td>
      <td>20.0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>284806</th>
      <td>55262.0</td>
      <td>-1.732064</td>
      <td>0.924056</td>
      <td>1.082680</td>
      <td>0.567256</td>
      <td>-0.007326</td>
      <td>-0.172493</td>
      <td>0.323600</td>
      <td>0.166905</td>
      <td>-0.221053</td>
      <td>...</td>
      <td>0.046174</td>
      <td>0.273960</td>
      <td>0.245251</td>
      <td>0.185157</td>
      <td>-0.043749</td>
      <td>-0.532553</td>
      <td>-0.863063</td>
      <td>-0.369561</td>
      <td>20.0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>284807 rows × 31 columns</p>
</div>



We separate the target variable (`Class`), which we want to predict, from the features (all other columns). The `Class` column indicates whether a transaction is fraudulent (1) or legitimate (0).


```python
target = data["Class"].astype(int)
data.drop("Class", axis=1, inplace=True)
```

Fraud detection datasets are typically highly imbalanced, meaning the majority of transactions are legitimate. We check the distribution of our classes.


```python
target.value_counts()
```




    Class
    0    284315
    1       492
    Name: count, dtype: int64



We split our dataset into two parts:

- Training set (80%): Used to train the machine learning model.
- Testing set (20%): Used to evaluate the performance of the trained model.


```python
X_train, X_test, y_train, y_test = train_test_split(data, target, train_size = 0.80)
```

Let's also save it to Cloud Storage.


```python
X_train.to_csv(f"gs://{PROJECT_ID}-bucket/data/vertex/X_train.csv", index=False)
y_train.to_frame().to_csv(f"gs://{PROJECT_ID}-bucket/data/vertex/y_train.csv", index=False)
```

## Step 3.1: Train a Random Forest classifier

We use a `RandomForestClassifier`, which is an ensemble learning method that creates multiple decision trees and aggregates their predictions. This helps improve accuracy and robustness.


```python
model = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=8, verbose=1)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_pred_prob = model.predict_proba(X_test)[:, 1]
```

    [Parallel(n_jobs=8)]: Using backend ThreadingBackend with 8 concurrent workers.
    [Parallel(n_jobs=8)]: Done  34 tasks      | elapsed:   43.3s
    [Parallel(n_jobs=8)]: Done  50 out of  50 | elapsed:   55.8s finished
    [Parallel(n_jobs=8)]: Using backend ThreadingBackend with 8 concurrent workers.
    [Parallel(n_jobs=8)]: Done  34 tasks      | elapsed:    0.1s
    [Parallel(n_jobs=8)]: Done  50 out of  50 | elapsed:    0.1s finished
    [Parallel(n_jobs=8)]: Using backend ThreadingBackend with 8 concurrent workers.
    [Parallel(n_jobs=8)]: Done  34 tasks      | elapsed:    0.1s
    [Parallel(n_jobs=8)]: Done  50 out of  50 | elapsed:    0.1s finished


We calculate the accuracy of the model, which measures the proportion of correctly classified instances.

For a highly imbalanced data set, the accuracy is often meaningless, because a simple classifier that always says ***not fraud*** will have an accuracy close to 1 already.


```python
accuracy_score(y_test, y_pred)
```




    0.9995611109160493



We compute the ROC AUC (Receiver Operating Characteristic - Area Under the Curve) score. This metric evaluates the model's ability to distinguish between classes. A score closer to 1 indicates better performance.


```python
roc_auc_score(y_test, y_pred_prob)
```




    0.9219180813470536



We save the trained model to a local file so we can deploy it later.


```python
joblib.dump(model, "model.joblib")
```




    ['model.joblib']



We upload the trained model to Vertex AI, where it can be used for predictions.


```python
!gsutil cp model.joblib gs://{PROJECT_ID}-bucket/model/
```

    Copying file://model.joblib [Content-Type=application/octet-stream]...
    / [1 files][  1.2 MiB/  1.2 MiB]                                                
    Operation completed over 1 objects/1.2 MiB.                                      


## Step 3.2: Serve locally trained model on Vertex AI

The Vertex AI Model Registry is a centralized repository in Google Cloud's Vertex AI platform where machine learning (ML) models are stored, managed, and versioned. It allows data scientists and ML engineers to track different model versions, store metadata, and deploy models seamlessly to Vertex AI endpoints for inference.

Key features of the Model Registry include:

* Model Versioning: Track multiple versions of a model.
* Metadata Management: Store details such as model parameters, training data, and performance metrics.
* Deployment & Serving: Deploy registered models to Vertex AI Endpoints, Batch Predictions, or export them for external use.
* Model Governance: Manage access control, approval workflows, and lineage tracking.
* Integration with Pipelines: Automate model registration via Vertex AI Pipelines.

We can register the model we just trained in this notebook as follows:


```python
vertex_model_upload = aiplatform.Model.upload(
    display_name="bootkon-upload-model",
    serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-5:latest",
    artifact_uri=f"gs://{PROJECT_ID}-bucket/model/",
    is_default_version=True,
    version_aliases=["v1"],
)
```

    Creating Model
    Create Model backing LRO: projects/888342260584/locations/us-central1/models/3048036447706677248/operations/5520722546774769664
    Model created. Resource name: projects/888342260584/locations/us-central1/models/3048036447706677248@1
    To use this Model in another session:
    model = aiplatform.Model('projects/888342260584/locations/us-central1/models/3048036447706677248@1')


Once the model has been uploaded, navigate to the [`Model Registry` in Vertex AI](https://console.cloud.google.com/vertex-ai/models). Click on `bootkon-model`. Can you find your newly created model artifact? Open the `VERSION DETAILS` tab and try to find your model artifact on Cloud Storage.

Let's deploy the model to an endpoint for online prediction.


```python
endpoint_upload = aiplatform.Endpoint.create(display_name="bootkon-endpoint-upload")
```

    Creating Endpoint
    Create Endpoint backing LRO: projects/888342260584/locations/us-central1/endpoints/1390056475904180224/operations/6436079171037822976
    Endpoint created. Resource name: projects/888342260584/locations/us-central1/endpoints/1390056475904180224
    To use this Endpoint in another session:
    endpoint = aiplatform.Endpoint('projects/888342260584/locations/us-central1/endpoints/1390056475904180224')


The next code chunk will take around 10min. We don't want to wait for that, so we set `sync=False` and look at the result later.


```python
vertex_model_upload.deploy(
    deployed_model_display_name="bootkon-model-upload",
    endpoint=endpoint_upload,
    machine_type="n2-standard-2",
    sync=False
)
```

    Deploying model to Endpoint : projects/888342260584/locations/us-central1/endpoints/1390056475904180224





    <google.cloud.aiplatform.models.Endpoint object at 0x7f11784d58a0> 
    resource name: projects/888342260584/locations/us-central1/endpoints/1390056475904180224



    Deploy Endpoint model backing LRO: projects/888342260584/locations/us-central1/endpoints/1390056475904180224/operations/7148773812069203968
    Deploying model to Endpoint : projects/888342260584/locations/us-central1/endpoints/3718136008278016000
    Deploy Endpoint model backing LRO: projects/888342260584/locations/us-central1/endpoints/3718136008278016000/operations/1055403516236922880
    Endpoint model deployed. Resource name: projects/888342260584/locations/us-central1/endpoints/1390056475904180224


The next chunk lists the currently deployed models. While the model is deploying, it wont's show up.


```python
endpoint_upload.list_models()
```




    []



## Step 4: Train and serve model using custom containers

In this section, we will train a `RandomForestClassifier` using **custom containers** on Vertex AI and deploy it for real-time predictions. Instead of using pre-built containers, we will package our training and prediction logic into Docker containers, allowing for **full control over dependencies, runtime environments, and scalability**. 

The process consists of two main steps:
1. **Model Training:** We will preprocess the dataset, train a model and save it as a serialized `joblib` file. The trained model will be uploaded to Cloud Storage for deployment.
2. **Model Serving:** Using a separate container, the stored model will be loaded from Cloud Storage, and an API will be exposed via Flask (or **FastAPI** in production) to handle inference requests.

By leveraging Vertex AI’s custom training and prediction services, we can achieve a **scalable, managed ML workflow** while keeping complete flexibility over the training and deployment pipeline.

We will create the following files:

- `train/Dockerfile`: Dockerfile for the training container
- `train/train.py`: Training script
- `predict/Dockerfile`: Dockerfile for the prediction container
- `predict/predict.py`: Prediction script

First, we configure docker.


```python
!gcloud auth configure-docker $REGION-docker.pkg.dev --quiet
```

    WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
    I0000 00:00:1739520189.216623 3264411 fork_posix.cc:75] Other threads are currently calling into gRPC, skipping fork() handlers


    [1;33mWARNING:[0m Your config file at [/home/jupyter/.docker/config.json] contains these credential helper entries:
    
    {
      "credHelpers": {
        "gcr.io": "gcloud",
        "us.gcr.io": "gcloud",
        "eu.gcr.io": "gcloud",
        "asia.gcr.io": "gcloud",
        "staging-k8s.gcr.io": "gcloud",
        "marketplace.gcr.io": "gcloud",
        "us-central1-docker.pkg.dev": "gcloud"
      }
    }
    Adding credentials for: us-central1-docker.pkg.dev
    gcloud credential helpers already registered correctly.



```python

```


```python
mkdir -p train predict
```


```python
%%writefile train/Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY train.py /app/train.py

RUN pip install --no-cache-dir --quiet pandas scikit-learn==1.5.2 google-cloud-storage fsspec gcsfs

ENTRYPOINT ["python", "/app/train.py"]
```

    Overwriting train/Dockerfile



```python
%%writefile predict/Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY predict.py /app/predict.py

RUN pip install --no-cache-dir --quiet pandas scikit-learn==1.5.2 google-cloud-storage google-cloud-aiplatform fsspec gcsfs flask
EXPOSE 8080
ENTRYPOINT ["python", "/app/predict.py"]
```

    Overwriting predict/Dockerfile


The `train.py` script trains a `RandomForestClassifier` using scikit-learn, saves it as a `joblib` file, and uploads it to Cloud Storage. It reads the training data (`X_train` and `y_train`) from CSV files provided as command-line arguments and retrieves the target storage directory from the `AIP_MODEL_DIR` environment variable. The trained model is stored in GCS for later deployment on Vertex AI.



```python
%%writefile train/train.py
import os
import sys

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from google.cloud import storage

AIP_MODEL_DIR = os.environ["AIP_MODEL_DIR"]

X_train = pd.read_csv(sys.argv[1])
y_train = pd.read_csv(sys.argv[2])

model = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=8, verbose=1)
model.fit(X_train, y_train)

joblib.dump(model, "model.joblib")
storage_client = storage.Client()
bucket = storage_client.bucket(AIP_MODEL_DIR.split("/")[2])
blob = bucket.blob("/".join(AIP_MODEL_DIR.split("/")[3:]) + "/model.joblib")
blob.upload_from_filename("model.joblib")
print(f"Wrote model to {AIP_MODEL_DIR}/model.joblib")
```

    Overwriting train/train.py


The `predict.py` script is a flask-based prediction server designed for deployment on Vertex AI using custom containers. It retrieves the model artifacts from Cloud Storage using `prediction_utils.download_model_artifacts()`, loads the model with `joblib`, and exposes two API endpoints:

- **`/predict`** for inference  
- **`/health`** for monitoring the service status  

The script reads environment variables such as `AIP_STORAGE_URI` for downloading the model and `AIP_PREDICT_ROUTE` for defining the prediction route dynamically. 

⚠ **In production,** it is recommended to use **FastAPI** instead of Flask due to its superior performance, asynchronous capabilities, and built-in request validation.



```python
%%writefile predict/predict.py
import os
import joblib

import flask
import numpy as np
from google.cloud.aiplatform.utils import prediction_utils

AIP_STORAGE_URI = os.environ["AIP_STORAGE_URI"]
print(f"Downloading model from {AIP_STORAGE_URI}/model.joblib")
prediction_utils.download_model_artifacts(AIP_STORAGE_URI)
model = joblib.load("model.joblib")

app = flask.Flask(__name__)

@app.route(os.environ.get("AIP_PREDICT_ROUTE", "/predict"), methods=["POST"])
def predict():
    data = flask.request.get_json()
    inputs = np.array(data["instances"])
    predictions = model.predict(inputs).tolist()
    return flask.jsonify({"predictions": predictions})

@app.route(os.environ.get("AIP_HEALTH_ROUTE", "/health"), methods=["GET"])
def health_check():
    print("Received health check")
    return flask.jsonify({"status": "healthy"}), 200

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("AIP_HTTP_PORT", 8080)))
```

    Overwriting predict/predict.py


We will store the container images in a docker repository named `bootkon`. Let's create it first.


```python
!gcloud artifacts repositories create bootkon --repository-format=docker --location={REGION}
```

    Create request issued for: [bootkon]
    Waiting for operation [projects/astute-ace-336608/locations/us-central1/operati
    ons/a240e7fd-936b-403d-9082-8d4f21e4b8cd] to complete...done.                  
    Created repository [bootkon].


We can use Cloud Build to build to image and automatically push it to the container repository we just created.


```python
!cd train && gcloud builds submit --region={REGION} --tag={TRAIN_IMAGE_URI} --timeout=1h --quiet
```

    Creating temporary archive of 2 file(s) totalling 881 bytes before compression.
    Uploading tarball of [.] to [gs://astute-ace-336608_cloudbuild/source/1739520193.925865-5561e710d4574e238008430771be4824.tgz]
    Created [https://cloudbuild.googleapis.com/v1/projects/astute-ace-336608/locations/us-central1/builds/4a4cfab3-abc7-475a-94d1-6ee2b331639d].
    Logs are available at [ https://console.cloud.google.com/cloud-build/builds;region=us-central1/4a4cfab3-abc7-475a-94d1-6ee2b331639d?project=888342260584 ].
    Waiting for build to complete. Polling interval: 1 second(s).
    ----------------------------- REMOTE BUILD OUTPUT ------------------------------
    starting build "4a4cfab3-abc7-475a-94d1-6ee2b331639d"
    
    FETCHSOURCE
    Fetching storage object: gs://astute-ace-336608_cloudbuild/source/1739520193.925865-5561e710d4574e238008430771be4824.tgz#1739520194311893
    Copying gs://astute-ace-336608_cloudbuild/source/1739520193.925865-5561e710d4574e238008430771be4824.tgz#1739520194311893...
    / [1 files][  710.0 B/  710.0 B]                                                
    Operation completed over 1 objects/710.0 B.
    BUILD
    Already have image (with digest): gcr.io/cloud-builders/docker
    Sending build context to Docker daemon  3.584kB
    Step 1/5 : FROM python:3.10-slim
    3.10-slim: Pulling from library/python
    c29f5b76f736: Already exists
    74e68b11a1c1: Pulling fs layer
    a477a912afa7: Pulling fs layer
    8c67a072a8ad: Pulling fs layer
    8c67a072a8ad: Verifying Checksum
    8c67a072a8ad: Download complete
    74e68b11a1c1: Verifying Checksum
    74e68b11a1c1: Download complete
    a477a912afa7: Verifying Checksum
    a477a912afa7: Download complete
    74e68b11a1c1: Pull complete
    a477a912afa7: Pull complete
    8c67a072a8ad: Pull complete
    Digest: sha256:66aad90b231f011cb80e1966e03526a7175f0586724981969b23903abac19081
    Status: Downloaded newer image for python:3.10-slim
     ---> b791f5ccaef8
    Step 2/5 : WORKDIR /app
     ---> Running in a4c9a35c5231
    Removing intermediate container a4c9a35c5231
     ---> 4d95c7cd4069
    Step 3/5 : COPY train.py /app/train.py
     ---> c2646dbfcd40
    Step 4/5 : RUN pip install --no-cache-dir --quiet pandas scikit-learn==1.5.2 google-cloud-storage fsspec gcsfs
     ---> Running in cca02c4961ea
    [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
    [0m[91m
    [notice] A new release of pip is available: 23.0.1 -> 25.0.1
    [notice] To update, run: pip install --upgrade pip
    [0mRemoving intermediate container cca02c4961ea
     ---> e4ffbc86d970
    Step 5/5 : ENTRYPOINT ["python", "/app/train.py"]
     ---> Running in 4516e8570b5c
    Removing intermediate container 4516e8570b5c
     ---> 07a4e7f38388
    Successfully built 07a4e7f38388
    Successfully tagged us-central1-docker.pkg.dev/astute-ace-336608/bootkon/bootkon-train:latest
    PUSH
    Pushing us-central1-docker.pkg.dev/astute-ace-336608/bootkon/bootkon-train:latest
    The push refers to repository [us-central1-docker.pkg.dev/astute-ace-336608/bootkon/bootkon-train]
    3261d1bfd94d: Preparing
    11e08faae4bc: Preparing
    8ee980b23ac5: Preparing
    cd9604f50b89: Preparing
    f52fdf687483: Preparing
    93d4d0473476: Preparing
    7914c8f600f5: Preparing
    93d4d0473476: Waiting
    7914c8f600f5: Waiting
    11e08faae4bc: Pushed
    cd9604f50b89: Pushed
    8ee980b23ac5: Pushed
    f52fdf687483: Pushed
    93d4d0473476: Pushed
    7914c8f600f5: Pushed
    3261d1bfd94d: Pushed
    latest: digest: sha256:3df3f4b2115f482e5e03d32a80728ae40c2ac79db10c857b916244588551a2f8 size: 1786
    DONE
    --------------------------------------------------------------------------------
    ID                                    CREATE_TIME                DURATION  SOURCE                                                                                           IMAGES                                                                        STATUS
    4a4cfab3-abc7-475a-94d1-6ee2b331639d  2025-02-14T08:03:14+00:00  1M18S     gs://astute-ace-336608_cloudbuild/source/1739520193.925865-5561e710d4574e238008430771be4824.tgz  us-central1-docker.pkg.dev/astute-ace-336608/bootkon/bootkon-train (+1 more)  SUCCESS


Let's do the same thing for the prediction image.


```python
!cd predict && gcloud builds submit --region={REGION} --tag={PREDICT_IMAGE_URI} --timeout=1h --quiet
```

    Creating temporary archive of 3 file(s) totalling 1.2 KiB before compression.
    Uploading tarball of [.] to [gs://astute-ace-336608_cloudbuild/source/1739520277.405046-dfbbb67ff0df42cd8d6960c99c151e4b.tgz]
    Created [https://cloudbuild.googleapis.com/v1/projects/astute-ace-336608/locations/us-central1/builds/b250065d-2ef6-405c-9e2d-9fcaf541c0ba].
    Logs are available at [ https://console.cloud.google.com/cloud-build/builds;region=us-central1/b250065d-2ef6-405c-9e2d-9fcaf541c0ba?project=888342260584 ].
    Waiting for build to complete. Polling interval: 1 second(s).
    ----------------------------- REMOTE BUILD OUTPUT ------------------------------
    starting build "b250065d-2ef6-405c-9e2d-9fcaf541c0ba"
    
    FETCHSOURCE
    Fetching storage object: gs://astute-ace-336608_cloudbuild/source/1739520277.405046-dfbbb67ff0df42cd8d6960c99c151e4b.tgz#1739520277719673
    Copying gs://astute-ace-336608_cloudbuild/source/1739520277.405046-dfbbb67ff0df42cd8d6960c99c151e4b.tgz#1739520277719673...
    / [1 files][  961.0 B/  961.0 B]                                                
    Operation completed over 1 objects/961.0 B.
    BUILD
    Already have image (with digest): gcr.io/cloud-builders/docker
    Sending build context to Docker daemon  4.608kB
    Step 1/6 : FROM python:3.10-slim
    3.10-slim: Pulling from library/python
    c29f5b76f736: Already exists
    74e68b11a1c1: Pulling fs layer
    a477a912afa7: Pulling fs layer
    8c67a072a8ad: Pulling fs layer
    8c67a072a8ad: Verifying Checksum
    8c67a072a8ad: Download complete
    74e68b11a1c1: Verifying Checksum
    74e68b11a1c1: Download complete
    a477a912afa7: Verifying Checksum
    a477a912afa7: Download complete
    74e68b11a1c1: Pull complete
    a477a912afa7: Pull complete
    8c67a072a8ad: Pull complete
    Digest: sha256:66aad90b231f011cb80e1966e03526a7175f0586724981969b23903abac19081
    Status: Downloaded newer image for python:3.10-slim
     ---> b791f5ccaef8
    Step 2/6 : WORKDIR /app
     ---> Running in cb91fdd927c1
    Removing intermediate container cb91fdd927c1
     ---> b7f5879a1ebc
    Step 3/6 : COPY predict.py /app/predict.py
     ---> ce7c2e81719d
    Step 4/6 : RUN pip install --no-cache-dir --quiet pandas scikit-learn==1.5.2 google-cloud-storage google-cloud-aiplatform fsspec gcsfs flask
     ---> Running in 8445bb00e041
    [91mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
    [0m[91m
    [notice] A new release of pip is available: 23.0.1 -> 25.0.1
    [notice] To update, run: pip install --upgrade pip
    [0mRemoving intermediate container 8445bb00e041
     ---> 07f2e75e5b95
    Step 5/6 : EXPOSE 8080
     ---> Running in 3cf586da5684
    Removing intermediate container 3cf586da5684
     ---> 116648f185f4
    Step 6/6 : ENTRYPOINT ["python", "/app/predict.py"]
     ---> Running in 7a469addbf34
    Removing intermediate container 7a469addbf34
     ---> b99e0610cc6b
    Successfully built b99e0610cc6b
    Successfully tagged us-central1-docker.pkg.dev/astute-ace-336608/bootkon/bootkon-predict:latest
    PUSH
    Pushing us-central1-docker.pkg.dev/astute-ace-336608/bootkon/bootkon-predict:latest
    The push refers to repository [us-central1-docker.pkg.dev/astute-ace-336608/bootkon/bootkon-predict]
    306df139da4b: Preparing
    2f077ff0d52d: Preparing
    2ce059fc280e: Preparing
    cd9604f50b89: Preparing
    f52fdf687483: Preparing
    93d4d0473476: Preparing
    7914c8f600f5: Preparing
    93d4d0473476: Waiting
    7914c8f600f5: Waiting
    f52fdf687483: Layer already exists
    cd9604f50b89: Layer already exists
    93d4d0473476: Layer already exists
    2f077ff0d52d: Pushed
    2ce059fc280e: Pushed
    7914c8f600f5: Pushed
    306df139da4b: Pushed
    latest: digest: sha256:be0a3754390ac788b7feaf9ff47427636dd65183b5e5ad8690d4ba8a7e731f25 size: 1786
    DONE
    --------------------------------------------------------------------------------
    ID                                    CREATE_TIME                DURATION  SOURCE                                                                                           IMAGES                                                                          STATUS
    b250065d-2ef6-405c-9e2d-9fcaf541c0ba  2025-02-14T08:04:37+00:00  1M37S     gs://astute-ace-336608_cloudbuild/source/1739520277.405046-dfbbb67ff0df42cd8d6960c99c151e4b.tgz  us-central1-docker.pkg.dev/astute-ace-336608/bootkon/bootkon-predict (+1 more)  SUCCESS


Now that the container is ready, we can run it as `CustomContainerTrainingJob` -- giving the training data set as arguments. This will take around 5-10min.


```python
job = aiplatform.CustomContainerTrainingJob(
    display_name = "bootkon-custom",
    container_uri = TRAIN_IMAGE_URI,
    model_serving_container_image_uri = PREDICT_IMAGE_URI
)
```


```python
vertex_model_custom = job.run(
    args=[
        f"gs://{PROJECT_ID}-bucket/data/vertex/X_train.csv",
        f"gs://{PROJECT_ID}-bucket/data/vertex/y_train.csv",
    ]
)
```

    Training Output directory:
    gs://astute-ace-336608-bucket/aiplatform-custom-training-2025-02-14-08:06:16.843 
    View Training:
    https://console.cloud.google.com/ai/platform/locations/us-central1/training/2976178930425266176?project=888342260584
    CustomContainerTrainingJob projects/888342260584/locations/us-central1/trainingPipelines/2976178930425266176 current state:
    PipelineState.PIPELINE_STATE_RUNNING
    View backing custom job:
    https://console.cloud.google.com/ai/platform/locations/us-central1/training/3548195456729219072?project=888342260584
    CustomContainerTrainingJob projects/888342260584/locations/us-central1/trainingPipelines/2976178930425266176 current state:
    PipelineState.PIPELINE_STATE_RUNNING
    CustomContainerTrainingJob projects/888342260584/locations/us-central1/trainingPipelines/2976178930425266176 current state:
    PipelineState.PIPELINE_STATE_RUNNING
    CustomContainerTrainingJob projects/888342260584/locations/us-central1/trainingPipelines/2976178930425266176 current state:
    PipelineState.PIPELINE_STATE_RUNNING
    CustomContainerTrainingJob projects/888342260584/locations/us-central1/trainingPipelines/2976178930425266176 current state:
    PipelineState.PIPELINE_STATE_RUNNING
    CustomContainerTrainingJob projects/888342260584/locations/us-central1/trainingPipelines/2976178930425266176 current state:
    PipelineState.PIPELINE_STATE_RUNNING
    CustomContainerTrainingJob run completed. Resource name: projects/888342260584/locations/us-central1/trainingPipelines/2976178930425266176
    Model available at projects/888342260584/locations/us-central1/models/2302690709376860160



```python
endpoint_custom = aiplatform.Endpoint.create(display_name="bootkon-endpoint-custom")
```

    Creating Endpoint
    Create Endpoint backing LRO: projects/888342260584/locations/us-central1/endpoints/3718136008278016000/operations/5526633521285693440
    Endpoint created. Resource name: projects/888342260584/locations/us-central1/endpoints/3718136008278016000
    To use this Endpoint in another session:
    endpoint = aiplatform.Endpoint('projects/888342260584/locations/us-central1/endpoints/3718136008278016000')


We also deploy this model and don't wait for it to finish (`sync=False`) -- instead we come back later.


```python
vertex_model_custom.deploy(
    deployed_model_display_name="bootkon-model-custom",
    endpoint=endpoint_custom,
    machine_type="n2-standard-2",
    sync=False
)
```




    <google.cloud.aiplatform.models.Endpoint object at 0x7f1178499a50> 
    resource name: projects/888342260584/locations/us-central1/endpoints/3718136008278016000



## Step 5: Train and deploy models using Vertex Pipelines

In this section, we will train a `RandomForestClassifier` using Vertex AI Pipelines and Kubeflow Pipelines (KFP) and deploy it for real-time predictions. Unlike the custom container approach, we will define a pipeline-based workflow for automated training, model storage, and deployment. This approach allows us to achieve repeatability, scalability, and automation for end-to-end ML workflows on Google Cloud.

By leveraging Vertex AI Pipelines, we can create a fully managed, automated ML pipeline that integrates seamlessly with GCP services.



```python
import kfp
from kfp import dsl, compiler

from google_cloud_pipeline_components.types import artifact_types
from google_cloud_pipeline_components.v1.custom_job import CustomTrainingJobOp
from google_cloud_pipeline_components.v1.endpoint import EndpointCreateOp, ModelDeployOp
from google_cloud_pipeline_components.v1.model import ModelUploadOp
from kfp.dsl import importer_node
```

Next, we create a Kubeflow pipeline that automates the training, model upload, and deployment process in Vertex AI.

**Pipeline Steps**

1. Define a Unique Model Directory:
* The pipeline assigns a unique Cloud Storage path for storing the trained model using `PIPELINE_JOB_ID_PLACEHOLDER`, ensuring each run has an isolated model directory.

2. Run a Custom Training Job
* Uses `CustomTrainingJobOp` to launch a training job on Vertex AI.
* The training script is executed inside a custom container (`TRAIN_IMAGE_URI`).
* The trained model is stored in the dynamically created directory (`AIP_MODEL_DIR`).

3. Import the Trained Model as an Artifact
* The `importer_node.importer` step converts the saved model directory into an `UnmanagedContainerModel`, allowing it to be used by Vertex AI.

4. Upload the Model to Vertex AI
* The `ModelUploadOp` registers the trained model in Vertex AI, making it available for deployment.

5. Create an Endpoint for Deployment
* `EndpointCreateOp` initializes a new prediction endpoint in Vertex AI.

6. Deploy the Model to the Endpoint
* `ModelDeployOp` deploys the registered model to the created endpoint with a dedicated `n1-standard-4` machine.

**Key Features**
- **Dynamically generated model path** ensures each pipeline run has an isolated model storage.
- **Custom container training** allows full control over the training process.
- **Automated model registration and deployment** simplifies the end-to-end MLOps workflow.



```python
@kfp.dsl.pipeline(name="bootkon-pipeline")
def pipeline(
    X_train: str,
    y_train: str,
    project: str = PROJECT_ID
):
    model_dir = f"{PIPELINE_ROOT}/model-{kfp.dsl.PIPELINE_JOB_ID_PLACEHOLDER}"
    custom_job_task = CustomTrainingJobOp(
        project=project,
        display_name="bootkon-model-pipeline",
        worker_pool_specs=[
            {
                "containerSpec": {
                    "args": [X_train, y_train],
                    "env": [{"name": "AIP_MODEL_DIR", "value": model_dir}],
                    "imageUri": TRAIN_IMAGE_URI,
                },
                "replicaCount": "1",
                "machineSpec": {
                    "machineType": "n1-standard-4",
                },
            }
        ],
    )

    import_unmanaged_model_task = importer_node.importer(
        artifact_uri=model_dir,
        artifact_class=artifact_types.UnmanagedContainerModel,
        metadata={
            "containerSpec": {
                "imageUri": PREDICT_IMAGE_URI,
            },
        },
    ).after(custom_job_task)

    model_upload_op = ModelUploadOp(
        project=project,
        display_name="bootkon-pipeline-model",
        unmanaged_container_model=import_unmanaged_model_task.outputs["artifact"],
    )
    model_upload_op.after(import_unmanaged_model_task)

    endpoint_create_op = EndpointCreateOp(
        project=project,
        display_name="bootkon-endpoint-pipeline",
    )

    ModelDeployOp(
        endpoint=endpoint_create_op.outputs["endpoint"],
        model=model_upload_op.outputs["model"],
        deployed_model_display_name="bootkon-pipeline-model",
        dedicated_resources_machine_type="n1-standard-4"
    )
```

The following command compiles the `bootkon-pipeline` into a JSON file that can be submitted to Vertex AI.


```python
compiler.Compiler().compile(
    pipeline_func=pipeline,
    package_path="bootkon_pipeline.json",
)
```

And we submit it. Feel free to investigate the pipeline using the link that is printed out.


```python
job = aiplatform.PipelineJob(
    display_name="bootkon-pipeline",
    template_path="bootkon_pipeline.json",
    pipeline_root=PIPELINE_ROOT,
    enable_caching=False,
    project=PROJECT_ID,
    parameter_values={
        "project": PROJECT_ID,
        "X_train": f"gs://{PROJECT_ID}-bucket/data/vertex/X_train.csv",
        "y_train": f"gs://{PROJECT_ID}-bucket/data/vertex/y_train.csv"
    },
)

job.run(sync=False)
```

    Creating PipelineJob
    PipelineJob created. Resource name: projects/888342260584/locations/us-central1/pipelineJobs/bootkon-pipeline-20250214081430
    To use this PipelineJob in another session:
    pipeline_job = aiplatform.PipelineJob.get('projects/888342260584/locations/us-central1/pipelineJobs/bootkon-pipeline-20250214081430')
    View Pipeline Job:
    https://console.cloud.google.com/vertex-ai/locations/us-central1/pipelines/runs/bootkon-pipeline-20250214081430?project=888342260584
    PipelineJob projects/888342260584/locations/us-central1/pipelineJobs/bootkon-pipeline-20250214081430 current state:
    PipelineState.PIPELINE_STATE_RUNNING
    PipelineJob projects/888342260584/locations/us-central1/pipelineJobs/bootkon-pipeline-20250214081430 current state:
    PipelineState.PIPELINE_STATE_RUNNING
    PipelineJob projects/888342260584/locations/us-central1/pipelineJobs/bootkon-pipeline-20250214081430 current state:
    PipelineState.PIPELINE_STATE_RUNNING
    PipelineJob projects/888342260584/locations/us-central1/pipelineJobs/bootkon-pipeline-20250214081430 current state:
    PipelineState.PIPELINE_STATE_RUNNING
    PipelineJob projects/888342260584/locations/us-central1/pipelineJobs/bootkon-pipeline-20250214081430 current state:
    PipelineState.PIPELINE_STATE_RUNNING


## Step 6: Make predictions

We now should have several endpoints deployed. Let's check the endpoint from Step 3.2 (the ***upload*** model):


```python
endpoint_upload.list_models()
```




    []



Let's make a prediction:


```python
response = endpoint_upload.predict(instances=X_test.head(4000).values.tolist())
```

Most of them are ***not fraud*** .


```python
response.predictions[:10]
```




    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]



But there are also a few fraud cases.


```python
sum(response.predictions)
```




    4.0



We can do the same thing with the other endpoint we created through custom containers:


```python
response = endpoint_custom.predict(instances=X_test.head(4000).values.tolist())
```


```python
sum(response.predictions)
```




    4.0



## Investigate results in the Cloud Console

<font color="red"><b>Great job deploying all these models. Now, please go back to the lab in Cloud Shell and continue from there!</b></font>

<img src="../docs/img/lab4/cloud_shell_4.png" width=300/>


```python

```
