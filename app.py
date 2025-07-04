"""
Streamlit App for Clothing Matchmaker
A user-friendly interface for the GPT-4o mini + RAG fashion recommendation system
"""

import streamlit as st
import pandas as pd
import json
import ast
import base64
import os
from PIL import Image
import io

# Local imports
from analysis import analyze_image
from utils.guardrails import check_match
from match.search_similar_items import find_matching_items_with_rag
from config import OPENAI_API_KEY
from utils.gcs_download import load_embeddings_with_gcs_fallback

# Page configuration
st.set_page_config(
    page_title="Fashion Matchmaker",
    page_icon="👗",
    layout="wide"
)

# Check for API key
if not OPENAI_API_KEY:
    st.error("""
    ⚠️ **OpenAI API Key Not Found**
    
    Please set your OpenAI API key as an environment variable:
    
    **For Local Development:**
    ```bash
    export OPENAI_API_KEY="your-api-key-here"
    ```
    
    **For Streamlit Cloud Deployment:**
    1. Go to your app settings in Streamlit Cloud
    2. Add environment variable: `OPENAI_API_KEY`
    3. Set the value to your API key
    4. Redeploy the app
    
    Get your API key from: https://platform.openai.com/api-keys
    """)
    st.stop()

# Title and description
st.title("👗 Fashion Matchmaker")
st.markdown("""
Upload a photo of your clothing item and get AI-powered outfit recommendations!
This app uses GPT-4o mini to analyze your clothing and find matching items.
""")

# Load the dataset with embeddings
@st.cache_data
def load_data():
    """Load the clothing dataset with embeddings from GCS or local file"""
    
    # Get GCS configuration from environment variables
    bucket_name = os.getenv("GCS_BUCKET_NAME")
    blob_name = os.getenv("GCS_BLOB_NAME", "data/sample_styles_with_embeddings.csv")
    public_url = os.getenv("GCS_PUBLIC_URL", "https://storage.googleapis.com/retailnext00/sample_styles_with_embeddings.csv")
    
    try:
        # Try to load with GCS fallback
        styles_df = load_embeddings_with_gcs_fallback(bucket_name, blob_name, public_url)
        return styles_df
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None

def get_data_source():
    """Determine the actual data source being used"""
    local_path = "data/sample_clothes/sample_styles_with_embeddings.csv"
    public_url = os.getenv("GCS_PUBLIC_URL")
    bucket_name = os.getenv("GCS_BUCKET_NAME")
    
    if os.path.exists(local_path):
        return "local"
    elif public_url:
        return "gcs_public"
    elif bucket_name:
        return "gcs_bucket"
    else:
        return "sample"

def encode_image_to_base64(image):
    """Convert PIL image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def main():
    # Load data
    styles_df = load_data()
    if styles_df is None:
        return
    
    # Sidebar for information
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This app demonstrates:
        - **GPT-4o mini** for image analysis
        - **RAG** for similarity search
        - **Embeddings** for matching
        - **Guardrails** for quality control
        - **GCS Integration** for data storage
        """)
        
        st.header("📊 Dataset Info")
        if styles_df is not None:
            st.write(f"Total items: {len(styles_df)}")
            st.write(f"Categories: {len(styles_df['articleType'].unique())}")
            st.write(f"Genders: {sorted(styles_df['gender'].unique().tolist())}")
            
            # Show data source
            data_source = get_data_source()
            if data_source == "local":
                st.info("📁 Using local embeddings file")
            elif data_source == "gcs_public":
                st.info("☁️ Using Google Cloud Storage (Public URL)")
            elif data_source == "gcs_bucket":
                st.info("☁️ Using Google Cloud Storage (Bucket)")
            else:
                st.info("📝 Using sample demo data")
        else:
            st.error("Dataset not loaded")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📸 Upload Your Clothing")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an image of your clothing item",
            type=['jpg', 'jpeg', 'png'],
            help="Upload a clear photo of the clothing item you want to match"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            
            # Analyze button
            if st.button("🔍 Analyze & Find Matches", type="primary"):
                with st.spinner("Analyzing your clothing item..."):
                    try:
                        # Encode image
                        encoded_image = encode_image_to_base64(image)
                        
                        # Get unique subcategories
                        unique_subcategories = styles_df['articleType'].unique()
                        
                        # Analyze the image
                        analysis = analyze_image(encoded_image, unique_subcategories)
                        if analysis is None:
                            st.error("Failed to analyze image. Please check your API key and try again.")
                            return
                        
                        try:
                            image_analysis = json.loads(analysis)
                        except (json.JSONDecodeError, TypeError) as e:
                            st.error(f"Error parsing analysis result: {e}")
                            return
                        
                        # Store results in session state
                        st.session_state.analysis = image_analysis
                        st.session_state.encoded_image = encoded_image
                        st.session_state.uploaded_image = image
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error during analysis: {str(e)}")
    
    with col2:
        st.header("🎯 Analysis Results")
        
        if 'analysis' in st.session_state:
            analysis = st.session_state.analysis
            
            # Display analysis results
            st.subheader("📋 Item Analysis")
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.metric("Category", analysis.get('category', 'N/A'))
            with col_b:
                st.metric("Gender", analysis.get('gender', 'N/A'))
            with col_c:
                st.metric("Suggested Items", len(analysis.get('items', [])))
            
            # Display suggested items
            st.subheader("💡 Suggested Matching Items")
            for i, item in enumerate(analysis.get('items', []), 1):
                st.write(f"{i}. {item}")
            
            # Find and display matching items
            if st.button("🔍 Find Similar Items", type="secondary"):
                with st.spinner("Searching for similar items..."):
                    try:
                        # Extract features
                        item_descs = analysis['items']
                        item_category = analysis['category']
                        item_gender = analysis['gender']
                        
                        # Filter data
                        filtered_items = styles_df.loc[styles_df['gender'].isin([item_gender, 'Unisex'])]
                        filtered_items = filtered_items[filtered_items['articleType'] != item_category]
                        
                        st.info(f"Searching through {len(filtered_items)} items...")
                        
                        # Find matching items
                        matching_items = find_matching_items_with_rag(filtered_items, item_descs)
                        
                        # Store results
                        st.session_state.matching_items = matching_items
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error finding matches: {str(e)}")
    
    # Display matching items
    if 'matching_items' in st.session_state:
        st.header("🎨 Matching Items Found")
        
        matching_items = st.session_state.matching_items
        
        if not matching_items:
            st.warning("No matching items found. Try uploading a different image.")
        else:
            st.success(f"Found {len(matching_items)} potential matches!")
            
            # Create columns for displaying items
            cols = st.columns(min(3, len(matching_items)))
            
            for i, item in enumerate(matching_items):
                col_idx = i % 3
                with cols[col_idx]:
                    st.subheader(f"Item {i+1}")
                    
                    # Try to display image if available
                    item_id = item.get('id')
                    image_path = f"../openai-cookbook/examples/data/sample_clothes/sample_images/{item_id}.jpg"
                    
                    if os.path.exists(image_path):
                        st.image(image_path, caption=f"ID: {item_id}", use_container_width=True)
                    else:
                        st.write(f"Image not found for ID: {item_id}")
                    
                    # Display item details
                    st.write(f"**Name:** {item.get('productDisplayName', 'N/A')}")
                    st.write(f"**Category:** {item.get('articleType', 'N/A')}")
                    st.write(f"**Gender:** {item.get('gender', 'N/A')}")
                    
                    # Add match validation button
                    if st.button(f"✅ Validate Match {i+1}", key=f"validate_{i}"):
                        with st.spinner("Validating match..."):
                            try:
                                # Encode suggested image
                                suggested_image = encode_image_to_base64(Image.open(image_path))
                                
                                # Check match
                                match_result = check_match(st.session_state.encoded_image, suggested_image)
                                if match_result is None:
                                    st.error("Failed to validate match")
                                    continue
                                
                                try:
                                    match = json.loads(match_result)
                                    if match["answer"] == 'yes':
                                        st.success("✅ Items match well!")
                                        st.write(f"**Reason:** {match['reason']}")
                                    else:
                                        st.warning("❌ Items don't match well")
                                        st.write(f"**Reason:** {match['reason']}")
                                except (json.JSONDecodeError, TypeError) as e:
                                    st.error(f"Error parsing validation result: {e}")
                                    
                            except Exception as e:
                                st.error(f"Error during validation: {str(e)}")

if __name__ == "__main__":
    main() 