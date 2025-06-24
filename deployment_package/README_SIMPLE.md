# BharatDoc AI-OCR - Simplified Version

A simplified version of BharatDoc AI-OCR that works on Windows without problematic dependencies like PyMuPDF and OpenCV.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install --user -r requirements_minimal.txt
```

### 2. Test Installation

```bash
python test_simple.py
```

### 3. Run the Application

```bash
python run_simple.py
```

The app will automatically open in your browser at `http://localhost:8501`

## 📋 What's Included

### ✅ Working Features
- **PDF Processing**: Digital PDF text extraction and table detection
- **Language Detection**: Hindi, English, and other Indian languages
- **Document Parsing**: Udyam certificate field extraction
- **Web Interface**: Streamlit-based UI for file upload and processing
- **Output Formats**: JSON and CSV export

### ⚠️ Limitations (Simplified Version)
- **No OCR**: Scanned PDFs and images cannot be processed (requires PaddleOCR)
- **No Image Processing**: Advanced image preprocessing not available
- **No Watermark Detection**: Basic watermark filtering only
- **No Redaction**: Basic redaction functionality only

## 🛠️ Installation Troubleshooting

### If you get stuck at "Preparing metadata (pyproject.toml)"

This happens when packages try to build from source. The simplified version avoids this by using only pre-built wheels.

### If you get permission errors

Use the `--user` flag:
```bash
pip install --user package_name
```

### If OpenCV fails to install

The simplified version doesn't require OpenCV. If you need it later, try:
```bash
pip install --user opencv-python-headless
```

## 📁 Project Structure

```
bharatdoc_ai_ocr/
├── api/
│   └── streamlit_app.py          # Web interface
├── core/
│   ├── processor_simple.py       # Simplified document processor
│   ├── language/
│   │   └── detect.py            # Language detection
│   ├── parsing/
│   │   └── udhyam_parser.py     # Udyam certificate parser
│   └── output/
│       ├── json_output.py       # JSON export
│       └── csv_output.py        # CSV export
├── requirements_minimal.txt      # Minimal dependencies
├── test_simple.py               # Test script
└── run_simple.py                # Deployment script
```

## 🔧 Usage

1. **Upload Files**: Use the web interface to upload PDF files
2. **Process Documents**: The system will automatically:
   - Extract text and layout
   - Detect language
   - Parse document fields
   - Extract tables
3. **Download Results**: Get results in JSON or CSV format

## 🎯 Supported Document Types

- **Digital PDFs**: Full text extraction and table detection
- **Udyam Certificates**: Automatic field parsing
- **Other Documents**: Basic text extraction

## 🚀 Future Enhancements

To add full OCR capabilities later:

1. Install PaddleOCR:
```bash
pip install --user paddleocr paddlepaddle
```

2. Install PyMuPDF (if needed):
```bash
pip install --user PyMuPDF
```

3. Switch back to the full processor in `api/streamlit_app.py`

## 📞 Support

If you encounter issues:

1. Run the test script: `python test_simple.py`
2. Check that all dependencies are installed
3. Ensure you're using Python 3.8+ on Windows

## 🎉 Success!

Once running, you'll have a working OCR system for Indian financial and legal documents that can:
- Process digital PDFs
- Extract text and tables
- Detect languages
- Parse Udyam certificates
- Export results in multiple formats 