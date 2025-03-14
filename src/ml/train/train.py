import os
import sys

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from google.cloud import storage, bigquery

AIP_MODEL_DIR = os.environ["AIP_MODEL_DIR"]

bq_source = sys.argv[1]
project = sys.argv[2]

bq = bigquery.Client(project=project, location="us")
data = bq.query(f"SELECT * FROM `{bq_source}`").to_dataframe()
data.drop("Feedback", axis=1, inplace=True)

target = data["Class"].astype(int)
data.drop("Class", axis=1, inplace=True)

X_train, X_test, y_train, y_test = train_test_split(data, target, train_size = 0.80)

model = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=8, verbose=1)
model.fit(X_train, y_train)

joblib.dump(model, "model.joblib")
storage_client = storage.Client()
bucket = storage_client.bucket(AIP_MODEL_DIR.split("/")[2])
blob = bucket.blob("/".join(AIP_MODEL_DIR.split("/")[3:]) + "/model.joblib")
blob.upload_from_filename("model.joblib")
print(f"Wrote model to {AIP_MODEL_DIR}/model.joblib")
