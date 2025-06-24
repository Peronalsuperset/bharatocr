#!/usr/bin/env python3
"""
Flexible deployment script for BharatDoc AI-OCR
Works with or without ngrok
"""

import os
import sys
import subprocess
import time
import webbrowser
import requests
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
    try:
        result = subprocess.run(['ngrok', 'version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return True
    except:
        pass
    return False

def get_ngrok_url():
    """Get the public URL from ngrok API."""
    try:
        time.sleep(3)
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        if response.status_code == 200:
            tunnels = response.json()['tunnels']
            for tunnel in tunnels:
                if tunnel['proto'] == 'https':
                    return tunnel['public_url']
    except:
        pass
    return None

def run_local():
    """Run the app locally only."""
    print("\n🌐 Starting BharatDoc AI-OCR (Local Access Only)")
    print("=" * 50)
    
    current_dir = Path(__file__).parent.absolute()
    streamlit_app_path = current_dir / "api" / "streamlit_app.py"
    
    if not streamlit_app_path.exists():
        print(f"❌ Streamlit app not found at: {streamlit_app_path}")
        return False
    
    print(f"📁 App location: {streamlit_app_path}")
    print("🌐 Starting Streamlit server...")
    
    try:
        os.chdir(current_dir)
        
        streamlit_cmd = [
            sys.executable, "-m", "streamlit", "run",
            str(streamlit_app_path),
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ]
        
        print(f"🚀 Running: {' '.join(streamlit_cmd)}")
        print("\n" + "=" * 50)
        print("📋 Instructions:")
        print("1. The app will open in your browser automatically")
        print("2. Upload PDF or image files to process them")
        print("3. View extracted text, tables, and parsed fields")
        print("4. Download results as JSON or CSV")
        print("5. Press Ctrl+C to stop the server")
        print("6. Access URL: http://localhost:8501")
        print("=" * 50)
        
        def open_browser():
            time.sleep(3)
            try:
                webbrowser.open("http://localhost:8501")
            except:
                print("⚠️  Could not open browser automatically.")
                print("   Please open: http://localhost:8501")
        
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        subprocess.run(streamlit_cmd)
        return True
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user.")
        return True
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def run_with_ngrok():
    """Run the app with ngrok tunnel."""
    print("\n🌐 Starting BharatDoc AI-OCR with ngrok (Public Access)")
    print("=" * 50)
    
    current_dir = Path(__file__).parent.absolute()
    streamlit_app_path = current_dir / "api" / "streamlit_app.py"
    
    if not streamlit_app_path.exists():
        print(f"❌ Streamlit app not found at: {streamlit_app_path}")
        return False
    
    print(f"📁 App location: {streamlit_app_path}")
    
    try:
        os.chdir(current_dir)
        
        # Start ngrok
        print("🔗 Starting ngrok tunnel...")
        ngrok_process = subprocess.Popen([
            'ngrok', 'http', '8501',
            '--log=stdout'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
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
            "--server.address", "0.0.0.0",
            "--browser.gatherUsageStats", "false"
        ]
        
        print(f"🚀 Running: {' '.join(streamlit_cmd)}")
        print("\n" + "=" * 50)
        print("📋 Instructions:")
        print("1. The app will be available at the ngrok URL above")
        print("2. Upload PDF or image files to process them")
        print("3. View extracted text, tables, and parsed fields")
        print("4. Download results as JSON or CSV")
        print("5. Press Ctrl+C to stop both servers")
        if public_url:
            print(f"6. Public URL: {public_url}")
        print("=" * 50)
        
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
        
        subprocess.run(streamlit_cmd)
        
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
    print("🇮🇳 BharatDoc AI-OCR - Deployment")
    print("=" * 50)
    
    if not check_dependencies():
        return False
    
    # Check if ngrok is available
    has_ngrok = check_ngrok()
    
    if has_ngrok:
        print("\n🔗 ngrok detected!")
        print("Choose deployment option:")
        print("1. Local access only (http://localhost:8501)")
        print("2. Public access with ngrok (shareable URL)")
        
        while True:
            choice = input("\nEnter choice (1 or 2): ").strip()
            if choice == "1":
                return run_local()
            elif choice == "2":
                return run_with_ngrok()
            else:
                print("Please enter 1 or 2")
    else:
        print("\n⚠️  ngrok not found. Running in local mode only.")
        print("To enable public access, install ngrok:")
        print("1. Download from: https://ngrok.com/download")
        print("2. Add to PATH and configure authtoken")
        print("3. Run this script again")
        
        return run_local()

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Failed to start the application.")
        sys.exit(1)
    else:
        print("\n✅ Application stopped successfully.") 