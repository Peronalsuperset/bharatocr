# 🚀 Quick ngrok Setup for BharatDoc AI-OCR

## Step 1: Download ngrok
1. Go to: https://ngrok.com/download
2. Click "Download for Windows"
3. Extract the ZIP file
4. Copy `ngrok.exe` to a folder (e.g., `C:\ngrok\`)

## Step 2: Add to PATH (Quick Method)
1. Copy `ngrok.exe` to: `C:\Windows\System32\`
2. Or add the folder to your PATH environment variable

## Step 3: Get Free Account
1. Go to: https://ngrok.com/signup
2. Sign up for free account
3. Get your authtoken from dashboard

## Step 4: Configure ngrok
Open PowerShell and run:
```powershell
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
```

## Step 5: Test Installation
```powershell
ngrok version
```

## Step 6: Deploy with ngrok
```powershell
python deploy.py
```

Choose option 2 when prompted for public access.

## Alternative: Manual ngrok Command
If you prefer to run ngrok manually:

1. Start Streamlit in one terminal:
```powershell
python run_simple.py
```

2. Start ngrok in another terminal:
```powershell
ngrok http 8501
```

3. Use the public URL shown by ngrok

## Troubleshooting
- If ngrok command not found: Make sure it's in your PATH
- If authentication fails: Check your authtoken
- If port 8501 is busy: Stop the existing Streamlit server first 