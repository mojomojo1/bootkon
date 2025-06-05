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
