# Deployment Guide

## Option 1: Streamlit Cloud (Recommended)

### Steps:
1. **Push to GitHub** (already done ✅)
2. **Go to [share.streamlit.io](https://share.streamlit.io)**
3. **Connect your GitHub account**
4. **Select your repository**: `joely0/RetailNext00`
5. **Set the file path**: `app.py`
6. **Deploy!**

### Advantages:
- ✅ **Free hosting**
- ✅ **Automatic updates** when you push to GitHub
- ✅ **Professional URL** (your-app-name.streamlit.app)
- ✅ **Perfect for interviews** - shows deployment skills
- ✅ **No server management**

---

## Option 2: Railway (Alternative)

### Steps:
1. **Go to [railway.app](https://railway.app)**
2. **Connect GitHub**
3. **Select your repository**
4. **Add environment variables**:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
5. **Deploy**

---

## Option 3: Heroku (Advanced)

### Steps:
1. **Create `Procfile`**:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```
2. **Create `runtime.txt`**:
   ```
   python-3.11.0
   ```
3. **Deploy to Heroku**

---

## Environment Variables

Make sure to set these in your deployment platform:
- `OPENAI_API_KEY`: Your OpenAI API key

## Testing Deployment

After deployment, test:
1. **Image upload** functionality
2. **API calls** to OpenAI
3. **Error handling** with invalid inputs
4. **Performance** with different image sizes

## For Interview Demo

**Streamlit Cloud is perfect** because:
- Shows you can deploy production apps
- Demonstrates full-stack capabilities
- Provides a professional demo URL
- Updates automatically with your code changes 