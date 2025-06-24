#!/usr/bin/env python3
"""
Script to stop any existing Streamlit servers
"""

import subprocess
import os

def stop_streamlit():
    """Stop any running Streamlit processes."""
    print("🛑 Stopping any running Streamlit servers...")
    
    try:
        # Find and kill Streamlit processes
        result = subprocess.run([
            'tasklist', '/FI', 'IMAGENAME eq python.exe', '/FO', 'CSV'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            killed = 0
            
            for line in lines:
                if 'streamlit' in line.lower():
                    parts = line.split(',')
                    if len(parts) >= 2:
                        pid = parts[1].strip('"')
                        try:
                            subprocess.run(['taskkill', '/PID', pid, '/F'], 
                                         capture_output=True)
                            killed += 1
                            print(f"✓ Killed Streamlit process (PID: {pid})")
                        except:
                            pass
            
            if killed == 0:
                print("✓ No Streamlit processes found")
            else:
                print(f"✓ Stopped {killed} Streamlit process(es)")
        
        # Also try to kill processes on port 8501
        print("🔍 Checking port 8501...")
        result = subprocess.run([
            'netstat', '-ano', '|', 'findstr', ':8501'
        ], shell=True, capture_output=True, text=True)
        
        if result.stdout.strip():
            print("⚠️  Port 8501 is still in use. You may need to:")
            print("   1. Close any browser tabs with the app")
            print("   2. Restart your terminal")
            print("   3. Or wait a few minutes for the port to be released")
        else:
            print("✓ Port 8501 is free")
            
    except Exception as e:
        print(f"⚠️  Error stopping servers: {e}")

if __name__ == "__main__":
    stop_streamlit() 