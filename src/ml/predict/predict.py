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
