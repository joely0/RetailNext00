"""
Google Cloud Storage download utility
Downloads embeddings file from GCS bucket for deployment
"""

import os
from google.cloud import storage
import pandas as pd
import ast

def download_embeddings_from_gcs(bucket_name, source_blob_name, destination_file_name):
    """
    Download embeddings file from Google Cloud Storage
    
    Args:
        bucket_name: GCS bucket name
        source_blob_name: Path to file in bucket (e.g., 'data/sample_styles_with_embeddings.csv')
        destination_file_name: Local path to save file
    """
    try:
        # Initialize GCS client
        storage_client = storage.Client()
        
        # Get bucket and blob
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        
        # Download the file
        blob.download_to_filename(destination_file_name)
        
        print(f"✅ Downloaded {source_blob_name} to {destination_file_name}")
        return True
        
    except Exception as e:
        print(f"❌ Error downloading from GCS: {e}")
        return False

def load_embeddings_with_gcs_fallback(bucket_name=None, blob_name=None):
    """
    Load embeddings file with fallback to GCS if local file doesn't exist
    
    Args:
        bucket_name: GCS bucket name (optional)
        blob_name: Path to file in bucket (optional)
    """
    local_path = "data/sample_clothes/sample_styles_with_embeddings.csv"
    
    # Check if local file exists
    if os.path.exists(local_path):
        print("📁 Using local embeddings file")
        try:
            styles_df = pd.read_csv(local_path, on_bad_lines="skip")
            styles_df["embeddings"] = styles_df["embeddings"].apply(ast.literal_eval)
            return styles_df
        except Exception as e:
            print(f"❌ Error loading local file: {e}")
    
    # Try to download from GCS if credentials are available
    if bucket_name and blob_name:
        print("☁️ Attempting to download from Google Cloud Storage...")
        if download_embeddings_from_gcs(bucket_name, blob_name, local_path):
            try:
                styles_df = pd.read_csv(local_path, on_bad_lines="skip")
                styles_df["embeddings"] = styles_df["embeddings"].apply(ast.literal_eval)
                return styles_df
            except Exception as e:
                print(f"❌ Error loading downloaded file: {e}")
    
    # Fallback: create sample data
    print("📝 Creating sample embeddings for demo...")
    return create_sample_embeddings()

def create_sample_embeddings():
    """Create sample embeddings for demo purposes"""
    import numpy as np
    
    # Create sample data
    sample_data = {
        'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'productDisplayName': [
            'Blue Denim Jacket',
            'White Cotton T-shirt', 
            'Black Leather Boots',
            'Red Summer Dress',
            'Gray Hoodie',
            'Black Skinny Jeans',
            'White Sneakers',
            'Floral Blouse',
            'Brown Belt',
            'Silver Necklace'
        ],
        'articleType': ['Jackets', 'T-shirts', 'Shoes', 'Dresses', 'Hoodies', 
                       'Jeans', 'Shoes', 'Tops', 'Belts', 'Accessories'],
        'gender': ['Unisex', 'Unisex', 'Unisex', 'Women', 'Unisex', 
                  'Unisex', 'Unisex', 'Women', 'Unisex', 'Unisex']
    }
    
    sample_df = pd.DataFrame(sample_data)
    
    # Create dummy embeddings (1536-dimensional vectors like OpenAI embeddings)
    print(f"Creating sample embeddings for {len(sample_df)} items...")
    
    embeddings = []
    for i in range(len(sample_df)):
        # Create a random embedding vector (1536 dimensions like text-embedding-3-large)
        embedding = np.random.rand(1536).tolist()
        embeddings.append(embedding)
    
    # Add embeddings to the dataframe
    sample_df['embeddings'] = embeddings
    
    print(f"✅ Sample dataset created with {len(sample_df)} items")
    return sample_df 