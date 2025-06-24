#!/usr/bin/env python3
"""
BharatDoc AI-OCR - Cloud Deployment Version
Optimized for deployment on Streamlit Cloud, Heroku, Railway, etc.
No local dependencies required!
"""

import streamlit as st
import tempfile
import os
import sys
from pathlib import Path

# Add the core directory to Python path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

try:
    from core.processor_simple import process_document
    from core.output.json_output import write_json
    from core.output.csv_output import write_kv_csv, write_tables_csv
except ImportError as e:
    st.error(f"Import error: {e}")
    st.info("Please ensure all core modules are available in the deployment package.")

# Page configuration
st.set_page_config(
    page_title="BharatDoc AI-OCR",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function."""
    
    # Header
    st.title("🇮🇳 BharatDoc AI-OCR")
    st.markdown("### Advanced OCR System for Indian Financial & Legal Documents")
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Features")
        st.markdown("""
        ✅ **Digital PDF Processing**
        ✅ **Text & Table Extraction**
        ✅ **Multi-language Detection**
        ✅ **Document Parsing**
        ✅ **JSON/CSV Export**
        """)
        
        st.header("📄 Supported Formats")
        st.markdown("""
        - **PDF Files** (Digital)
        - **Images** (Basic support)
        - **Udyam Certificates**
        - **Financial Documents**
        """)
        
        st.header("🌐 Deployment Info")
        st.info("This is a cloud-deployed version with no local dependencies required!")
    
    # Main content
    st.markdown("### 📤 Upload Documents")
    st.write("Upload your Indian financial or legal documents for automated processing and analysis.")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Choose PDF or image files",
        type=["pdf", "png", "jpg", "jpeg", "tiff", "bmp"],
        accept_multiple_files=True,
        help="Select one or more files to process"
    )
    
    if uploaded_files:
        st.markdown("### 🔄 Processing Results")
        
        # Process each uploaded file
        for uploaded_file in uploaded_files:
            with st.expander(f"📄 {uploaded_file.name}", expanded=True):
                st.write(f"**File Type:** {uploaded_file.type}")
                st.write(f"**File Size:** {uploaded_file.size} bytes")
                
                # Create temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name
                
                try:
                    # Process document
                    with st.spinner(f"Processing {uploaded_file.name}..."):
                        results = process_document(tmp_path)
                    
                    if results:
                        st.success(f"✅ Successfully processed {uploaded_file.name}")
                        
                        # Display results for each page
                        for page in results:
                            st.markdown(f"#### 📃 Page {page['page_number']} ({page['type']})")
                            
                            # Document type
                            if page.get('document_type'):
                                st.markdown(f"**Document Type:** {page['document_type']}")
                            
                            # Parsed fields
                            if page.get("parsed_fields"):
                                st.markdown("**📋 Extracted Fields:**")
                                st.json(page["parsed_fields"])
                            
                            # Tables
                            if page.get("tables"):
                                st.markdown("**📊 Extracted Tables:**")
                                for idx, table in enumerate(page["tables"], 1):
                                    st.markdown(f"**Table {idx}:**")
                                    if table and len(table) > 0:
                                        st.table(table)
                                    else:
                                        st.info("Empty table detected")
                            
                            # Statistics
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                if page.get("watermark_blocks"):
                                    st.metric("Watermark Blocks", len(page['watermark_blocks']))
                            with col2:
                                if page.get("redacted_items"):
                                    st.metric("Redacted Items", len(page['redacted_items']))
                            with col3:
                                if page.get("low_confidence_blocks"):
                                    st.metric("Low Confidence", len(page['low_confidence_blocks']))
                            
                            # Download options
                            st.markdown("**💾 Download Results:**")
                            base = os.path.splitext(uploaded_file.name)[0]
                            
                            # JSON download
                            json_name = f"{base}_page{page['page_number']}.json"
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as jf:
                                write_json(page, jf.name)
                                with open(jf.name, "rb") as f:
                                    st.download_button(
                                        label="📄 Download JSON",
                                        data=f.read(),
                                        file_name=json_name,
                                        mime="application/json"
                                    )
                                os.unlink(jf.name)
                            
                            # CSV download
                            csv_name = f"{base}_page{page['page_number']}.csv"
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as cf:
                                write_kv_csv(page.get("parsed_fields", {}), cf.name)
                                with open(cf.name, "rb") as f:
                                    st.download_button(
                                        label="📊 Download CSV (Fields)",
                                        data=f.read(),
                                        file_name=csv_name,
                                        mime="text/csv"
                                    )
                                os.unlink(cf.name)
                            
                            # Table CSVs
                            if page.get("tables"):
                                for idx, table in enumerate(page["tables"], 1):
                                    if table and len(table) > 0:
                                        tname = f"{base}_page{page['page_number']}_table{idx}.csv"
                                        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tf:
                                            write_tables_csv([table], tf.name[:-4])
                                            with open(tf.name, "rb") as f:
                                                st.download_button(
                                                    label=f"📊 Download Table {idx} CSV",
                                                    data=f.read(),
                                                    file_name=tname,
                                                    mime="text/csv"
                                                )
                                            os.unlink(tf.name)
                    
                    else:
                        st.error(f"❌ Failed to process {uploaded_file.name}")
                
                except Exception as e:
                    st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
                    st.info("This might be due to file format issues or processing limitations.")
                
                finally:
                    # Clean up temporary file
                    try:
                        os.unlink(tmp_path)
                    except:
                        pass
    else:
        # Show instructions when no files are uploaded
        st.markdown("### 📋 Instructions")
        st.info("""
        **How to use:**
        1. **Upload Files:** Use the file uploader above to select your documents
        2. **Automatic Processing:** The system will extract text, tables, and parse fields
        3. **View Results:** See extracted data, document type, and confidence scores
        4. **Download:** Get results in JSON or CSV format
        """)
        
        st.markdown("### 🎯 Supported Document Types")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **📄 Financial Documents:**
            - Bank Statements
            - Invoices
            - Receipts
            - Tax Documents
            """)
        
        with col2:
            st.markdown("""
            **📋 Legal Documents:**
            - Udyam Certificates
            - Contracts
            - Agreements
            - Certificates
            """)
        
        st.markdown("### ⚠️ Current Limitations")
        st.warning("""
        **Simplified Version:**
        - OCR for scanned documents not available
        - Advanced image processing limited
        - Best results with digital PDFs
        """)

if __name__ == "__main__":
    main() 