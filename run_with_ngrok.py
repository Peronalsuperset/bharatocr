#!/usr/bin/env python3
"""
Deployment script for BharatDoc AI-OCR with ngrok
Runs the Streamlit app and exposes it via ngrok for external access
"""

import os
import sys
import subprocess
import time
import webbrowser
import requests
import json
from pathlib import Path
import threading

def check_dependencies():
    """Check if required dependencies are installed."""
    print("Checking dependencies...")
    
    required_packages = [
        'streamlit',
        'langdetect', 
        'pandas',
        'numpy',
        'PIL',
        'yaml',
        'pdfplumber'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install them using:")
        print(f"pip install --user {' '.join(missing_packages)}")
        return False
    
    print("✓ All dependencies are installed!")
    return True

def check_ngrok():
    """Check if ngrok is available."""
    print("\nChecking ngrok...")
    
    try:
        # Try to run ngrok version
        result = subprocess.run(['ngrok', 'version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ ngrok is installed and working")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("⚠️  ngrok not found or not working")
    print("\nTo install ngrok:")
    print("1. Download from: https://ngrok.com/download")
    print("2. Extract to a folder in your PATH")
    print("3. Sign up for free account and get authtoken")
    print("4. Run: ngrok config add-authtoken YOUR_TOKEN")
    
    # Try to use ngrok anyway (might be in PATH)
    return True

def get_ngrok_url():
    """Get the public URL from ngrok API."""
    try:
        # Wait a bit for ngrok to start
        time.sleep(3)
        
        # Get ngrok tunnels
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        if response.status_code == 200:
            tunnels = response.json()['tunnels']
            for tunnel in tunnels:
                if tunnel['proto'] == 'https':
                    return tunnel['public_url']
    except Exception as e:
        print(f"⚠️  Could not get ngrok URL: {e}")
    
    return None

def run_streamlit_with_ngrok():
    """Run the Streamlit app with ngrok tunnel."""
    print("\n🚀 Starting BharatDoc AI-OCR with ngrok...")
    print("=" * 60)
    
    # Get the current directory
    current_dir = Path(__file__).parent.absolute()
    streamlit_app_path = current_dir / "api" / "streamlit_app.py"
    
    if not streamlit_app_path.exists():
        print(f"❌ Streamlit app not found at: {streamlit_app_path}")
        return False
    
    print(f"📁 App location: {streamlit_app_path}")
    print("🌐 Starting Streamlit server...")
    
    try:
        # Change to the app directory
        os.chdir(current_dir)
        
        # Start ngrok in background
        print("🔗 Starting ngrok tunnel...")
        ngrok_process = subprocess.Popen([
            'ngrok', 'http', '8501',
            '--log=stdout'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait for ngrok to start
        time.sleep(5)
        
        # Get public URL
        public_url = get_ngrok_url()
        if public_url:
            print(f"✅ Public URL: {public_url}")
        else:
            print("⚠️  Could not get public URL, but ngrok is running")
        
        # Start Streamlit
        print("🌐 Starting Streamlit server...")
        streamlit_cmd = [
            sys.executable, "-m", "streamlit", "run",
            str(streamlit_app_path),
            "--server.port", "8501",
            "--server.address", "0.0.0.0",  # Allow external connections
            "--browser.gatherUsageStats", "false"
        ]
        
        print(f"🚀 Running: {' '.join(streamlit_cmd)}")
        print("\n" + "=" * 60)
        print("📋 Instructions:")
        print("1. The app will be available at the ngrok URL above")
        print("2. Upload PDF or image files to process them")
        print("3. View extracted text, tables, and parsed fields")
        print("4. Download results as JSON or CSV")
        print("5. Press Ctrl+C to stop both servers")
        print("=" * 60)
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(8)
            try:
                if public_url:
                    webbrowser.open(public_url)
                else:
                    webbrowser.open("http://localhost:8501")
            except:
                print("⚠️  Could not open browser automatically.")
                if public_url:
                    print(f"   Please open: {public_url}")
                else:
                    print("   Please open: http://localhost:8501")
        
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Run streamlit
        streamlit_process = subprocess.run(streamlit_cmd)
        
        # Clean up ngrok
        ngrok_process.terminate()
        ngrok_process.wait()
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping servers...")
        try:
            ngrok_process.terminate()
            ngrok_process.wait(timeout=5)
        except:
            pass
        return True
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def main():
    """Main function."""
    print("🇮🇳 BharatDoc AI-OCR - ngrok Deployment")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Check ngrok
    if not check_ngrok():
        print("\n⚠️  ngrok not available, but continuing...")
    
    # Run the app with ngrok
    return run_streamlit_with_ngrok()

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Failed to start the application.")
        sys.exit(1)
    else:
        print("\n✅ Application stopped successfully.") 