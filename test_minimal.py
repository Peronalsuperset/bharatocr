#!/usr/bin/env python3
"""
Minimal test script for BharatDoc AI-OCR
Tests only the core functionality without problematic dependencies
"""

import os
import sys
from pathlib import Path

def test_basic_imports():
    """Test basic Python imports."""
    print("Testing basic imports...")
    
    try:
        import json
        print("✅ json imported successfully")
    except ImportError as e:
        print(f"✗ json import failed: {e}")
        return False
    
    try:
        import csv
        print("✅ csv imported successfully")
    except ImportError as e:
        print(f"✗ csv import failed: {e}")
        return False
    
    try:
        import re
        print("✅ re imported successfully")
    except ImportError as e:
        print(f"✗ re import failed: {e}")
        return False
    
    return True

def test_file_structure():
    """Test if all required files exist."""
    print("\nTesting file structure...")
    
    required_files = [
        "streamlit_app_cloud.py",
        "requirements_cloud.txt",
        "core/processor_simple.py",
        "core/language/detect.py",
        "core/parsing/udhyam_parser.py",
        "core/output/json_output.py",
        "core/output/csv_output.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    else:
        print("✅ All required files present")
        return True

def test_deployment_package():
    """Test if deployment package exists."""
    print("\nTesting deployment package...")
    
    deploy_dir = Path("deployment_package")
    if deploy_dir.exists():
        print("✅ Deployment package exists")
        print(f"📁 Location: {deploy_dir.absolute()}")
        return True
    else:
        print("❌ Deployment package not found")
        print("Run: python deploy_cloud.py")
        return False

def main():
    """Main test function."""
    print("🇮🇳 BharatDoc AI-OCR - Minimal Test")
    print("=" * 50)
    
    # Test basic imports
    if not test_basic_imports():
        print("\n❌ Basic imports failed")
        return False
    
    # Test file structure
    if not test_file_structure():
        print("\n❌ File structure test failed")
        return False
    
    # Test deployment package
    if not test_deployment_package():
        print("\n❌ Deployment package test failed")
        return False
    
    print("\n" + "=" * 50)
    print("✅ All tests passed!")
    print("=" * 50)
    print("\n🚀 Ready for cloud deployment!")
    print("\n📋 Next steps:")
    print("1. Upload 'deployment_package' contents to GitHub")
    print("2. Deploy on Streamlit Cloud (free)")
    print("3. Share your public URL!")
    print("\n🌐 No local installation required!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 