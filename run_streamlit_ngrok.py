import subprocess
import time
from pyngrok import ngrok
import sys
import os

# Compute absolute path to the Streamlit app
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STREAMLIT_APP_PATH = os.path.join(SCRIPT_DIR, "api", "streamlit_app.py")

if not os.path.exists(STREAMLIT_APP_PATH):
    print(f"ERROR: Streamlit app not found at {STREAMLIT_APP_PATH}")
    sys.exit(1)

# Start Streamlit app in the background
print(f"Starting Streamlit app at {STREAMLIT_APP_PATH} ...")
streamlit_proc = subprocess.Popen([
    sys.executable, "-m", "streamlit", "run", STREAMLIT_APP_PATH
], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait longer for Streamlit to start
print("Waiting for Streamlit to start (15 seconds)...")
time.sleep(15)

# Open ngrok tunnel
print("Starting ngrok tunnel...")
public_url = ngrok.connect(8501)
print(f"\nYour BharatDoc AI-OCR app is live at: {public_url.public_url}\n")
print("Press Ctrl+C to stop.")

try:
    streamlit_proc.wait()
except KeyboardInterrupt:
    print("\nShutting down...")
    streamlit_proc.terminate()
    ngrok.kill()
finally:
    out, err = streamlit_proc.communicate()
    print("\nStreamlit output:\n", out.decode(errors='ignore'))
    print("\nStreamlit errors:\n", err.decode(errors='ignore')) 