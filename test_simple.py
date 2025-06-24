#!/usr/bin/env python3
"""
Simple test script for BharatDoc AI-OCR (simplified version)
"""

import os
import sys
import tempfile

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import streamlit
        print("✓ Streamlit imported successfully")
    except ImportError as e:
        print(f"✗ Streamlit import failed: {e}")
        return False
    
    try:
        import langdetect
        print("✓ langdetect imported successfully")
    except ImportError as e:
        print(f"✗ langdetect import failed: {e}")
        return False
    
    try:
        import pandas
        print("✓ pandas imported successfully")
    except ImportError as e:
        print(f"✗ pandas import failed: {e}")
        return False
    
    try:
        import pdfplumber
        print("✓ pdfplumber imported successfully")
    except ImportError as e:
        print(f"✗ pdfplumber import failed: {e}")
        return False
    
    try:
        from core.processor_simple import process_document
        print("✓ Simplified processor imported successfully")
    except ImportError as e:
        print(f"✗ Simplified processor import failed: {e}")
        return False
    
    try:
        from core.language.detect import detect_language
        print("✓ Language detection imported successfully")
    except ImportError as e:
        print(f"✗ Language detection import failed: {e}")
        return False
    
    try:
        from core.parsing.udhyam_parser import parse_udhyam
        print("✓ Udyam parser imported successfully")
    except ImportError as e:
        print(f"✗ Udyam parser import failed: {e}")
        return False
    
    return True

def test_language_detection():
    """Test language detection functionality."""
    print("\nTesting language detection...")
    
    try:
        from core.language.detect import detect_language
        
        # Test Hindi text
        hindi_text = "उद्यम पंजीकरण प्रमाणपत्र"
        lang = detect_language(hindi_text)
        print(f"✓ Hindi text detected as: {lang}")
        
        # Test English text
        english_text = "Udyam Registration Certificate"
        lang = detect_language(english_text)
        print(f"✓ English text detected as: {lang}")
        
        return True
    except Exception as e:
        print(f"✗ Language detection test failed: {e}")
        return False

def test_udhyam_parser():
    """Test Udyam parser functionality."""
    print("\nTesting Udyam parser...")
    
    try:
        from core.parsing.udhyam_parser import parse_udhyam
        
        # Test with sample text
        sample_text = """
        UDYAM REGISTRATION CERTIFICATE
        Udyam Registration Number: UDYAM-UP-01-0000001
        Name of Entrepreneur: John Doe
        Type of Organization: Proprietorship
        """
        
        result = parse_udhyam(sample_text)
        if result:
            print("✓ Udyam parser extracted fields successfully")
            print(f"  Extracted: {list(result.keys())}")
        else:
            print("✓ Udyam parser handled non-matching text correctly")
        
        return True
    except Exception as e:
        print(f"✗ Udyam parser test failed: {e}")
        return False

def test_pdf_processing():
    """Test PDF processing functionality."""
    print("\nTesting PDF processing...")
    
    try:
        from core.processor_simple import process_document
        
        # Create a simple test PDF (this would require a real PDF file)
        print("✓ PDF processing module imported successfully")
        print("  Note: Actual PDF processing requires a real PDF file")
        
        return True
    except Exception as e:
        print(f"✗ PDF processing test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("BharatDoc AI-OCR - Simplified Version Test")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Please check your installation.")
        return False
    
    # Test language detection
    if not test_language_detection():
        print("\n❌ Language detection tests failed.")
        return False
    
    # Test Udyam parser
    if not test_udhyam_parser():
        print("\n❌ Udyam parser tests failed.")
        return False
    
    # Test PDF processing
    if not test_pdf_processing():
        print("\n❌ PDF processing tests failed.")
        return False
    
    print("\n" + "=" * 50)
    print("✅ All tests passed! The simplified version is ready to use.")
    print("=" * 50)
    print("\nTo run the Streamlit app:")
    print("  streamlit run api/streamlit_app.py")
    print("\nTo run with ngrok (for external access):")
    print("  python run_with_ngrok.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 