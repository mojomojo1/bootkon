#!/bin/bash

INPUT_DATA_FILE="src/ml/instances.json"
ENDPOINT_ID="$(gcloud ai endpoints list --region=$REGION \
    --filter=display_name=bootkon-endpoint \
    | grep ENDPOINT_ID | awk '{ print $2 }' | head -n 1)"
ACCESS_TOKEN="$(gcloud auth print-access-token)"

curl \
-X POST \
-H "Authorization: Bearer $ACCESS_TOKEN" \
-H "Content-Type: application/json" \
"https://us-central1-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/us-central1/endpoints/${ENDPOINT_ID}:predict" -d "@${INPUT_DATA_FILE}"