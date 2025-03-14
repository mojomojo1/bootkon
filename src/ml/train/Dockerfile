FROM python:3.10-slim

WORKDIR /app
COPY train.py /app/train.py

RUN pip install --no-cache-dir --quiet pandas scikit-learn==1.5.2 google-cloud-storage google-cloud-bigquery db-dtypes fsspec gcsfs

ENTRYPOINT ["python", "/app/train.py"]
