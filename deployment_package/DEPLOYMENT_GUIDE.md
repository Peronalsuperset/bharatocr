# 🚀 BharatDoc AI-OCR - Cloud Deployment Guide

This guide provides step-by-step instructions to deploy BharatDoc AI-OCR on various cloud platforms without any local dependencies.

## 📋 Prerequisites

- GitHub account
- Cloud platform account (Streamlit Cloud, Heroku, Railway, etc.)
- No local Python installation required!

## 🌐 Deployment Options

### 1. **Streamlit Cloud (Recommended - Free)**

**Step 1: Prepare Repository**
```bash
# Create a new GitHub repository
# Upload all files from this project
```

**Step 2: Deploy on Streamlit Cloud**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file path: `streamlit_app_cloud.py`
6. Click "Deploy"

**Step 3: Access Your App**
- Your app will be available at: `https://your-app-name.streamlit.app`
- Share this URL with anyone!

---

### 2. **Heroku (Free Tier Available)**

**Step 1: Install Heroku CLI**
```bash
# Download from: https://devcenter.heroku.com/articles/heroku-cli
```

**Step 2: Deploy**
```bash
# Login to Heroku
heroku login

# Create new app
heroku create your-bharatdoc-app

# Deploy
git push heroku main

# Open app
heroku open
```

**Step 3: Scale (Optional)**
```bash
# Scale to free dyno
heroku ps:scale web=1
```

---

### 3. **Railway (Free Tier Available)**

**Step 1: Connect Repository**
1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository

**Step 2: Deploy**
- Railway will automatically detect the configuration
- Deploy will start automatically
- Your app URL will be provided

---

### 4. **Docker Deployment**

**Step 1: Build and Run**
```bash
# Build Docker image
docker build -t bharatdoc-ocr .

# Run container
docker run -p 8501:8501 bharatdoc-ocr
```

**Step 2: Using Docker Compose**
```bash
# Start with Docker Compose
docker-compose up -d

# Access at http://localhost:8501
```

---

### 5. **Google Cloud Run**

**Step 1: Setup Google Cloud**
```bash
# Install Google Cloud CLI
# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

**Step 2: Deploy**
```bash
# Build and deploy
gcloud run deploy bharatdoc-ocr \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

### 6. **AWS App Runner**

**Step 1: Prepare Repository**
- Ensure Dockerfile is in root directory
- Push to GitHub

**Step 2: Deploy on AWS**
1. Go to AWS App Runner console
2. Create new service
3. Connect to GitHub repository
4. Configure build settings
5. Deploy

---

## 🔧 Configuration Files

### Streamlit Cloud
- **Main file**: `streamlit_app_cloud.py`
- **Config**: `.streamlit/config.toml`

### Heroku
- **Procfile**: `Procfile`
- **Runtime**: `runtime.txt`

### Railway
- **Config**: `railway.json`

### Docker
- **Dockerfile**: `Dockerfile`
- **Compose**: `docker-compose.yml`

## 📁 Required Files for Deployment

```
bharatdoc_ai_ocr/
├── streamlit_app_cloud.py      # Main app file
├── requirements_cloud.txt      # Dependencies
├── core/                       # Core modules
│   ├── processor_simple.py
│   ├── language/
│   ├── parsing/
│   └── output/
├── .streamlit/config.toml      # Streamlit config
├── Procfile                    # Heroku
├── railway.json               # Railway
├── Dockerfile                 # Docker
├── docker-compose.yml         # Docker Compose
└── runtime.txt                # Python version
```

## 🌍 Environment Variables

Set these in your cloud platform:

```bash
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

## 🔍 Troubleshooting

### Common Issues

**1. Import Errors**
- Ensure all core modules are included in deployment
- Check file paths in `streamlit_app_cloud.py`

**2. Port Issues**
- Most cloud platforms set PORT environment variable
- App automatically uses `$PORT` or defaults to 8501

**3. Memory Issues**
- Simplified version uses minimal memory
- If issues occur, consider upgrading plan

**4. File Upload Limits**
- Streamlit Cloud: 200MB per file
- Heroku: 100MB per file
- Railway: 100MB per file

### Health Checks

Your app includes health checks:
- **Endpoint**: `/_stcore/health`
- **Expected**: 200 OK response

## 📊 Monitoring

### Logs
- **Streamlit Cloud**: Built-in logging
- **Heroku**: `heroku logs --tail`
- **Railway**: Built-in logging
- **Docker**: `docker logs container_name`

### Metrics
- File uploads processed
- Processing time
- Error rates
- User sessions

## 🔒 Security Considerations

1. **File Uploads**: Temporary files are automatically cleaned up
2. **No Data Storage**: Files are processed in memory only
3. **HTTPS**: All cloud platforms provide SSL certificates
4. **Rate Limiting**: Consider implementing for production use

## 🚀 Production Deployment

For production use:

1. **Upgrade Plans**: Use paid tiers for better performance
2. **Custom Domain**: Configure custom domain names
3. **CDN**: Use CDN for faster global access
4. **Monitoring**: Set up proper monitoring and alerting
5. **Backup**: Regular backups of configuration

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review platform-specific documentation
3. Check application logs
4. Ensure all required files are included

---

## 🎉 Success!

Once deployed, your BharatDoc AI-OCR will be:
- ✅ Accessible from anywhere
- ✅ No local dependencies required
- ✅ Scalable and reliable
- ✅ Free to use (with platform limits)
- ✅ Ready for production use

**Share your deployed URL and start processing documents!** 