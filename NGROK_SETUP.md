# 🔗 ngrok Setup Guide

## Manual Installation (Recommended)

Since Chocolatey installation failed due to permissions, here's how to install ngrok manually:

### Step 1: Download ngrok
1. Go to https://ngrok.com/download
2. Download the Windows version
3. Extract the `ngrok.exe` file to a folder (e.g., `C:\ngrok\`)

### Step 2: Add to PATH (Optional)
1. Copy `ngrok.exe` to a folder in your PATH, or
2. Add the folder containing `ngrok.exe` to your system PATH

### Step 3: Sign up for free account
1. Go to https://ngrok.com/signup
2. Create a free account
3. Get your authtoken from the dashboard

### Step 4: Configure ngrok
```bash
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
```

### Step 5: Test installation
```bash
ngrok version
```

## Alternative: Use without ngrok

If you don't want to install ngrok, you can still use the app locally:

```bash
python run_simple.py
```

This will run the app on `http://localhost:8501` (local access only).

## Using with ngrok

Once ngrok is installed, run:

```bash
python run_with_ngrok.py
```

This will:
1. Start the Streamlit app
2. Create a public tunnel with ngrok
3. Show you the public URL that anyone can access

## Troubleshooting

### If ngrok command not found:
- Make sure `ngrok.exe` is in your PATH
- Or run it with full path: `C:\path\to\ngrok.exe http 8501`

### If you get authentication errors:
- Make sure you've added your authtoken: `ngrok config add-authtoken YOUR_TOKEN`

### If the tunnel doesn't work:
- Check if port 8501 is already in use
- Try a different port: `ngrok http 8502` 