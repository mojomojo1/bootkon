## Lab 1: Environment Setup

<walkthrough-tutorial-duration duration="30"></walkthrough-tutorial-duration>
{{ author('Fabian Hirschmann', 'https://linkedin.com/in/fhirschmann') }}
<walkthrough-tutorial-difficulty difficulty="1"></walkthrough-tutorial-difficulty>
<bootkon-cloud-shell-note/>


In this lab, we will set up your environment, synthetically generate a dataset suitable for retail analytics, put it into Cloud Storage, and prepare for use cases like customer propensity modeling and media asset generation.

### Enable services

First, we need to enable some Google Cloud Platform (GCP) services. Enabling GCP services is necessary to access and use the resources and capabilities associated with those services. Each GCP service provides a specific set of features for managing cloud infrastructure, data, AI models, and more. Enabling them takes a few minutes.

<walkthrough-enable-apis apis=
  "storage-component.googleapis.com,
  notebooks.googleapis.com,
  serviceusage.googleapis.com,
  cloudresourcemanager.googleapis.com,
  pubsub.googleapis.com,
  compute.googleapis.com,
  metastore.googleapis.com,
  datacatalog.googleapis.com,
  bigquery.googleapis.com,
  dataplex.googleapis.com,
  datalineage.googleapis.com,
  dataform.googleapis.com,
  dataproc.googleapis.com,
  bigqueryconnection.googleapis.com,
  aiplatform.googleapis.com,
  cloudbuild.googleapis.com,
  cloudaicompanion.googleapis.com,
  artifactregistry.googleapis.com">
</walkthrough-enable-apis>

### Assign permissions

Execute the following script:
```bash
bk-bootstrap
```

But what did it do? Let's ask Gemini while it is running.

1. Open  <walkthrough-editor-open-file filePath=".scripts/bk-bootstrap">`bk-bootstrap`</walkthrough-editor-open-file>.
2. Open Gemini Code Assist
![](../img/code_assist.png)

3. Insert ``What does bk-bootstrap do?`` into the Gemini prompt.

Cloud Shell may ask you to select your project and enable the API. Do not worry about missing licenses.

### Generate and Store Data

Next, we will generate synthetic retail data suitable for our use cases (customer propensity modeling and media asset generation) and store it directly in Cloud Storage.

First, let's create a bucket where we will place the data. Let's name it ``{{ PROJECT_ID }}-retail-data-bucket``:
```bash
gsutil mb -l $REGION gs://{{ PROJECT_ID }}-retail-data-bucket
```
Now, we'll use a Python script to generate the synthetic data. This script will create a few CSV files representing customer transactions, product information, and potentially media usage metadata.

Create a new Python file named generate_retail_data.py:
<walkthrough-editor-open-file filePath="generate_retail_data.py">generate_retail_data.py

Copy and paste the following Python code into generate_retail_data.py:

```Python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from google.cloud import storage
import os

def generate_customer_data(num_customers=1000):
    customer_ids = [f'CUST_{i:05d}' for i in range(num_customers)]
    ages = np.random.randint(18, 75, num_customers)
    genders = np.random.choice(['Male', 'Female', 'Other'], num_customers, p=[0.48, 0.50, 0.02])
    locations = np.random.choice(['North', 'South', 'East', 'West', 'Central'], num_customers)
    loyalty_tiers = np.random.choice(['Bronze', 'Silver', 'Gold', 'Platinum'], num_customers, p=[0.4, 0.3, 0.2, 0.1])
    return pd.DataFrame({
        'customer_id': customer_ids,
        'age': ages,
        'gender': genders,
        'location': locations,
        'loyalty_tier': loyalty_tiers
    })

def generate_product_data(num_products=500):
    product_ids = [f'PROD_{i:04d}' for i in range(num_products)]
    categories = np.random.choice(['Electronics', 'Apparel', 'Home Goods', 'Books', 'Groceries', 'Beauty'], num_products)
    prices = np.round(np.random.uniform(5.0, 500.0, num_products), 2)
    brands = np.random.choice([f'Brand_{chr(65+i)}' for i in range(10)], num_products)
    return pd.DataFrame({
        'product_id': product_ids,
        'category': categories,
        'price': prices,
        'brand': brands
    })

def generate_transaction_data(customers_df, products_df, num_transactions=10000):
    start_date = datetime.now() - timedelta(days=365)
    transactions = []
    for _ in range(num_transactions):
        customer = customers_df.sample(1).iloc[0]
        product = products_df.sample(1).iloc[0]

        transaction_date = start_date + timedelta(days=random.randint(0, 364), 
                                                  hours=random.randint(0, 23), 
                                                  minutes=random.randint(0, 59))
        quantity = random.randint(1, 5)
        total_amount = round(quantity * product['price'], 2)

        transactions.append({
            'transaction_id': f'TRX_{datetime.now().strftime("%Y%m%d%H%M%S%f")}_{_}',
            'customer_id': customer['customer_id'],
            'product_id': product['product_id'],
            'transaction_date': transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
            'quantity': quantity,
            'unit_price': product['price'],
            'total_amount': total_amount
        })
    return pd.DataFrame(transactions)

def generate_media_metadata(num_media_assets=200):
    media_ids = [f'MEDIA_{i:04d}' for i in range(num_media_assets)]
    asset_types = np.random.choice(['Image', 'Video', 'GIF', 'Audio'], num_media_assets, p=[0.6, 0.3, 0.05, 0.05])
    resolutions = np.random.choice(['720p', '1080p', '4K'], num_media_assets, p=[0.4, 0.4, 0.2])
    themes = np.random.choice(['Seasonal', 'Promotional', 'Product Showcase', 'Lifestyle', 'User Generated'], num_media_assets)
    return pd.DataFrame({
        'media_id': media_ids,
        'asset_type': asset_types,
        'resolution': resolutions,
        'theme': themes,
        'creation_date': [(datetime.now() - timedelta(days=random.randint(0, 730))).strftime('%Y-%m-%d') for _ in range(num_media_assets)]
    })

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to gs://{bucket_name}/{destination_blob_name}.")

if __name__ == "__main__":
    print("Generating synthetic retail data...")
    customers_df = generate_customer_data()
    products_df = generate_product_data()
    transactions_df = generate_transaction_data(customers_df, products_df)
    media_df = generate_media_metadata()

    # Save to local CSVs
    os.makedirs('generated_data', exist_ok=True)
    customers_df.to_csv('generated_data/customers.csv', index=False)
    products_df.to_csv('generated_data/products.csv', index=False)
    transactions_df.to_csv('generated_data/transactions.csv', index=False)
    media_df.to_csv('generated_data/media_assets.csv', index=False)
    print("Synthetic data saved locally to 'generated_data/' directory.")

    # Upload to GCS
    project_id = os.environ.get('PROJECT_ID') # Assuming PROJECT_ID is set in the environment
    if not project_id:
        print("Error: PROJECT_ID environment variable not set. Please ensure it's configured.")
        # Fallback for local testing or manual bucket name if PROJECT_ID is not available
        # bucket_name = "your-gcp-project-id-retail-data-bucket" 
        # print(f"Attempting to use hardcoded bucket name: {bucket_name}")
        exit()

    bucket_name = f"{project_id}-retail-data-bucket"

    print(f"Uploading data to gs://{bucket_name}/data/")
    upload_to_gcs(bucket_name, 'generated_data/customers.csv', 'data/customers.csv')
    upload_to_gcs(bucket_name, 'generated_data/products.csv', 'data/products.csv')
    upload_to_gcs(bucket_name, 'generated_data/transactions.csv', 'data/transactions.csv')
    upload_to_gcs(bucket_name, 'generated_data/media_assets.csv', 'data/media_assets.csv')
    print("All synthetic data uploaded to Cloud Storage.")
```
Install the necessary Python libraries: 
```bash
pip install pandas numpy google-cloud-storage
```
Run the Python script to generate and upload the data:
```bash
python generate_retail_data.py
```

This script will generate customers.csv, products.csv, transactions.csv, and media_assets.csv files and upload them into a data/ folder within your new Cloud Storage bucket.

Is the data there? Let's check and open [Cloud Storage](https://console.cloud.google.com/storage/browser/{{ PROJECT_ID }}-bucket). Once you have checked, you may need to resize the window that just opened
to make it smaller in case you run out of screen real estate.

### Create default VPC

The Google Cloud environment we created for you does not come with a Virtual Private Cloud (VPC) network
created by default. Let's create one. If it already exists -- that's ok. 

```bash
gcloud compute networks create default --project=$PROJECT_ID --subnet-mode=auto --bgp-routing-mode="regional"
```

Let's also create/update the subnet to allow internal traffic:

```bash
gcloud compute networks subnets update default --region=$REGION --enable-private-ip-google-access
```

If the command above returned an error about a *visibility check*, please wait two minutes for the permissions to propagate and try again.

Next, create a firewall rule:

```bash
gcloud compute firewall-rules create "default-allow-all-internal" \
    --network="default" \
    --project=$PROJECT_ID \
    --direction=INGRESS \
    --priority=65534 \
    --source-ranges="10.128.0.0/9" \
    --allow=tcp:0-65535,udp:0-65535,icmp
```

### Success

🎉 Congratulations{% if MY_NAME %}, {{ MY_NAME }}{% endif %}! You've officially leveled up from "cloud-curious" to "GCP aware"! 🌩️🚀

