FROM python:3.10-slim

WORKDIR /app
COPY predict.py /app/predict.py

RUN pip install --no-cache-dir --quiet pandas scikit-learn==1.5.2 google-cloud-storage google-cloud-aiplatform fsspec gcsfs flask
EXPOSE 8080
ENTRYPOINT ["python", "/app/predict.py"]
