# Google Cloud Storage Setup Guide

## Step 1: Upload Your Embeddings File to GCS

### Using Google Cloud Console:
1. **Go to [Google Cloud Console](https://console.cloud.google.com/)**
2. **Create a new bucket** (or use existing):
   - Name: `your-project-embeddings` (or any name)
   - Location: Choose closest to your deployment
   - Storage class: Standard
3. **Upload your file**:
   - Upload `data/sample_clothes/sample_styles_with_embeddings.csv`
   - Keep the same path: `data/sample_styles_with_embeddings.csv`

### Using gsutil (Command Line):
```bash
# Create bucket
gsutil mb gs://your-project-embeddings

# Upload file
gsutil cp data/sample_clothes/sample_styles_with_embeddings.csv gs://your-project-embeddings/data/sample_styles_with_embeddings.csv
```

## Step 2: Set Up Authentication

### Option A: Service Account (Recommended for Production)
1. **Create a service account**:
   - Go to IAM & Admin > Service Accounts
   - Create new service account
   - Grant "Storage Object Viewer" role
2. **Download JSON key**:
   - Create and download JSON key file
3. **Set environment variable**:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your-key.json"
   ```

### Option B: Application Default Credentials (Local Development)
```bash
gcloud auth application-default login
```

## Step 3: Configure Streamlit Cloud

Add these environment variables to your Streamlit Cloud app:

### Required Variables:
- `OPENAI_API_KEY`: Your OpenAI API key
- `GCS_BUCKET_NAME`: Your GCS bucket name (e.g., `your-project-embeddings`)
- `GCS_BLOB_NAME`: Path to file in bucket (e.g., `data/sample_styles_with_embeddings.csv`)

### Optional (if using service account):
- `GOOGLE_APPLICATION_CREDENTIALS`: Base64 encoded service account JSON

## Step 4: Deploy

1. **Commit and push your changes**:
   ```bash
   git add .
   git commit -m "Add GCS integration for embeddings"
   git push origin main
   ```

2. **Redeploy on Streamlit Cloud**

## Step 5: Test

Your app will now:
1. **Try to load local file** (for development)
2. **Download from GCS** (if local file not found)
3. **Create sample data** (as final fallback)

## Benefits of This Approach:

✅ **Scalable**: Can handle large files  
✅ **Cost-effective**: GCS is very cheap  
✅ **Professional**: Shows cloud integration skills  
✅ **Reliable**: Multiple fallback options  
✅ **Production-ready**: Demonstrates enterprise practices  

## Troubleshooting:

- **Permission errors**: Check service account roles
- **File not found**: Verify bucket name and blob path
- **Authentication**: Ensure credentials are properly set
- **Costs**: GCS charges ~$0.02/GB/month for storage

## Alternative: Simple Demo Approach

If you prefer a simpler approach for demonstration purposes, you can:

1. **Use the sample data fallback** (already implemented)
2. **Skip GCS setup** - the app will automatically create sample embeddings
3. **Focus on the core functionality** - image analysis and matching

The app will work perfectly fine with the sample data for demo purposes! 