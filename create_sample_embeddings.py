"""
Create a small sample embeddings file for deployment
This creates a minimal dataset that can be deployed to Streamlit Cloud
"""

import pandas as pd
import numpy as np
import ast

def create_sample_embeddings():
    """Create a small sample embeddings file for deployment"""
    
    # Read the original data
    try:
        original_df = pd.read_csv("data/sample_clothes/sample_styles.csv", on_bad_lines="skip")
        print(f"Original dataset has {len(original_df)} items")
    except FileNotFoundError:
        print("Original dataset not found. Creating sample data...")
        # Create sample data if original doesn't exist
        sample_data = {
            'id': [1, 2, 3, 4, 5],
            'productDisplayName': [
                'Blue Denim Jacket',
                'White Cotton T-shirt', 
                'Black Leather Boots',
                'Red Summer Dress',
                'Gray Hoodie'
            ],
            'articleType': ['Jackets', 'T-shirts', 'Shoes', 'Dresses', 'Hoodies'],
            'gender': ['Unisex', 'Unisex', 'Unisex', 'Women', 'Unisex']
        }
        original_df = pd.DataFrame(sample_data)
    
    # Take a small sample (first 50 items or less)
    sample_size = min(50, len(original_df))
    sample_df = original_df.head(sample_size).copy()
    
    # Create dummy embeddings (1536-dimensional vectors like OpenAI embeddings)
    print(f"Creating embeddings for {len(sample_df)} items...")
    
    # Generate random embeddings (in real deployment, these would be actual OpenAI embeddings)
    embeddings = []
    for i in range(len(sample_df)):
        # Create a random embedding vector (1536 dimensions like text-embedding-3-large)
        embedding = np.random.rand(1536).tolist()
        embeddings.append(embedding)
    
    # Add embeddings to the dataframe
    sample_df['embeddings'] = embeddings
    
    # Save the sample file
    output_path = "data/sample_clothes/sample_styles_with_embeddings_sample.csv"
    sample_df.to_csv(output_path, index=False)
    
    print(f"✅ Sample embeddings file created: {output_path}")
    print(f"📊 Sample dataset has {len(sample_df)} items")
    print(f"🎯 Categories: {sample_df['articleType'].unique().tolist()}")
    print(f"👥 Genders: {sample_df['gender'].unique().tolist()}")
    
    return output_path

if __name__ == "__main__":
    create_sample_embeddings() 