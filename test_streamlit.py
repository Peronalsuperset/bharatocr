#!/usr/bin/env python3
import sys
import os

print("Testing Streamlit import...")
try:
    import streamlit
    print("✓ Streamlit imported successfully")
except ImportError as e:
    print(f"✗ Streamlit import failed: {e}")
    sys.exit(1)

print("\nTesting Streamlit app import...")
try:
    from api.streamlit_app import *
    print("✓ Streamlit app imported successfully")
except ImportError as e:
    print(f"✗ Streamlit app import failed: {e}")
    sys.exit(1)

print("\nAll tests passed! Streamlit should work.") 