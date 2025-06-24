#!/usr/bin/env python3
"""
Simple deployment script for BharatDoc AI-OCR
Runs the Streamlit app locally without ngrok
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

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

def run_streamlit():
    """Run the Streamlit app."""
    print("\nStarting BharatDoc AI-OCR...")
    print("=" * 50)
    
    # Get the current directory
    current_dir = Path(__file__).parent.absolute()
    streamlit_app_path = current_dir / "api" / "streamlit_app.py"
    
    if not streamlit_app_path.exists():
        print(f"❌ Streamlit app not found at: {streamlit_app_path}")
        return False
    
    print(f"📁 App location: {streamlit_app_path}")
    print("🌐 Starting Streamlit server...")
    print("⏳ Please wait for the browser to open...")
    
    try:
        # Change to the app directory
        os.chdir(current_dir)
        
        # Run streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run",
            str(streamlit_app_path),
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ]
        
        print(f"🚀 Running: {' '.join(cmd)}")
        print("\n" + "=" * 50)
        print("📋 Instructions:")
        print("1. The app will open in your browser automatically")
        print("2. Upload PDF or image files to process them")
        print("3. View extracted text, tables, and parsed fields")
        print("4. Download results as JSON or CSV")
        print("5. Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(3)
            try:
                webbrowser.open("http://localhost:8501")
            except:
                print("⚠️  Could not open browser automatically.")
                print("   Please open: http://localhost:8501")
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Run the streamlit process
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user.")
        return True
    except Exception as e:
        print(f"\n❌ Error running Streamlit: {e}")
        return False

def main():
    """Main function."""
    print("🇮🇳 BharatDoc AI-OCR - Simplified Version")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Run the app
    return run_streamlit()

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Failed to start the application.")
        sys.exit(1)
    else:
        print("\n✅ Application stopped successfully.") 