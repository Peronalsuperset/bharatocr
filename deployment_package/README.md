# BharatDoc AI-OCR - Cloud Deployment

This is a cloud-ready deployment package for BharatDoc AI-OCR.

## Quick Deploy

### Streamlit Cloud (Recommended)
1. Upload all files to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Set main file: `streamlit_app_cloud.py`
5. Deploy!

### Heroku
```bash
heroku create your-app-name
git push heroku main
heroku open
```

### Railway
1. Connect to GitHub repository
2. Railway will auto-detect configuration
3. Deploy automatically

### Docker
```bash
docker build -t bharatdoc-ocr .
docker run -p 8501:8501 bharatdoc-ocr
```

## Features
- ✅ No local dependencies required
- ✅ Works on all major cloud platforms
- ✅ Automatic PDF processing
- ✅ Multi-language support
- ✅ JSON/CSV export

## Support
See DEPLOYMENT_GUIDE.md for detailed instructions.
