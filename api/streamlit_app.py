import streamlit as st
import tempfile
import os
from core.processor_simple import process_document
from core.output.json_output import write_json
from core.output.csv_output import write_kv_csv, write_tables_csv

st.set_page_config(page_title="BharatDoc AI-OCR", layout="wide")
st.title("🇮🇳 BharatDoc AI-OCR")
st.write("Upload Indian financial/legal documents (PDF, image) for OCR, parsing, and redaction.")

uploaded_files = st.file_uploader("Upload PDF or image files", type=["pdf", "png", "jpg", "jpeg", "tiff", "bmp"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.subheader(f"Results for: {uploaded_file.name}")
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        # Process document
        with st.spinner("Processing..."):
            results = process_document(tmp_path)
        # Display results
        for page in results:
            st.markdown(f"### Page {page['page_number']} ({page['type']})")
            st.write(f"**Document Type:** {page.get('document_type','')}")
            if page.get("parsed_fields"):
                st.write("**Parsed Fields:**")
                st.json(page["parsed_fields"])
            if page.get("tables"):
                for idx, table in enumerate(page["tables"], 1):
                    st.write(f"**Table {idx}:**")
                    st.table(table)
            if page.get("watermark_blocks"):
                st.write(f"**Watermark Blocks:** {len(page['watermark_blocks'])}")
            if page.get("redacted_items"):
                st.write(f"**Redacted Items:** {page['redacted_items']}")
            if page.get("low_confidence_blocks"):
                st.write(f"**Low Confidence Blocks:** {len(page['low_confidence_blocks'])}")
            # Download buttons
            base = os.path.splitext(uploaded_file.name)[0]
            json_name = f"{base}_page{page['page_number']}.json"
            csv_name = f"{base}_page{page['page_number']}.csv"
            # Save to temp for download
            with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as jf:
                write_json(page, jf.name)
                st.download_button("Download JSON", data=open(jf.name, "rb").read(), file_name=json_name)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as cf:
                write_kv_csv(page.get("parsed_fields", {}), cf.name)
                st.download_button("Download CSV (Fields)", data=open(cf.name, "rb").read(), file_name=csv_name)
            # Table CSVs
            if page.get("tables"):
                for idx, table in enumerate(page["tables"], 1):
                    tname = f"{base}_page{page['page_number']}_table{idx}.csv"
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tf:
                        write_tables_csv([table], tf.name[:-4])  # tf.name includes .csv
                        st.download_button(f"Download Table {idx} CSV", data=open(tf.name, "rb").read(), file_name=tname)
        os.remove(tmp_path) 