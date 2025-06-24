import os
import numpy as np
from PIL import Image
import pdfplumber
from .language.detect import detect_language
from .parsing.udhyam_parser import parse_udhyam

# A threshold to decide if a PDF page is scanned.
# If the text extracted from the text layer is less than this, we assume it's scanned.
MIN_TEXT_LENGTH_FOR_DIGITAL = 100
CONFIDENCE_THRESHOLD = 0.7

def _extract_digital_pdf_layout(page):
    """Extract text and layout from a digital PDF page using pdfplumber."""
    layout_blocks = []
    
    # Extract text with positioning
    words = page.extract_words()
    for word in words:
        x0, y0, x1, y1 = word['x0'], word['top'], word['x1'], word['bottom']
        text = word['text']
        lang = detect_language(text)
        layout_blocks.append({
            "bbox": [x0, y0, x1, y1],
            "text": text,
            "language": lang,
            "confidence": 1.0  # Digital PDFs have no confidence, so set to 1.0
        })
    
    return layout_blocks

def _extract_ocr_layout_blocks(layout_blocks):
    """Convert OCR output to a standard format."""
    result = []
    for block in layout_blocks:
        bbox, (text, conf) = block
        lang = detect_language(text)
        result.append({
            "bbox": bbox,
            "text": text,
            "language": lang,
            "confidence": conf
        })
    return result

def _parse_document_type(text):
    """Parse document type and extract fields."""
    # For now, always try Udyam parser
    parsed = parse_udhyam(text)
    if parsed:
        doc_type = "Udyam_Certificate"
    else:
        doc_type = "Unknown"
    return doc_type, parsed

def _extract_tables_from_pdfplumber(pdfplumber_page):
    """Extract tables from a PDF page."""
    tables = []
    for table in pdfplumber_page.extract_tables():
        # Each table is a list of rows; each row is a list of cell values
        tables.append(table)
    return tables

def _postprocess_layout(layout):
    """Post-process layout blocks."""
    # For now, just return the layout as-is
    # In the full version, this would handle watermarks, redaction, etc.
    filtered_blocks = [b for b in layout if b["confidence"] >= CONFIDENCE_THRESHOLD]
    low_confidence_idxs = [i for i, b in enumerate(layout) if b["confidence"] < CONFIDENCE_THRESHOLD]
    
    return {
        "layout": layout,
        "filtered_blocks": filtered_blocks,
        "watermark_idxs": [],  # Simplified version
        "redacted_items": [],  # Simplified version
        "low_confidence_idxs": low_confidence_idxs
    }

def _process_pdf_document(file_path):
    """Processes a PDF file, page by page using pdfplumber only."""
    results = []
    
    with pdfplumber.open(file_path) as doc:
        for page_num, page in enumerate(doc.pages):
            page_data = {"page_number": page_num + 1}

            # 1. Attempt to extract text directly
            text = page.extract_text() or ""

            # 2. Check if the page is likely scanned or text-based
            if len(text.strip()) < MIN_TEXT_LENGTH_FOR_DIGITAL:
                page_data["type"] = "scanned_pdf_page"
                print(f"Page {page_num + 1} seems to be scanned. OCR not available in simplified version.")
                
                # For scanned pages, we'll just extract what we can
                page_data["layout"] = []
                page_data["watermark_blocks"] = []
                page_data["redacted_items"] = []
                page_data["low_confidence_blocks"] = []
                page_data["text"] = text
                page_data["tables"] = []

            else:
                page_data["type"] = "digital_pdf_page"
                print(f"Page {page_num + 1} is a digital PDF. Extracting text layer, layout, and tables.")
                
                layout = _extract_digital_pdf_layout(page)
                post = _postprocess_layout(layout)
                page_data["layout"] = post["layout"]
                page_data["watermark_blocks"] = post["watermark_idxs"]
                page_data["redacted_items"] = post["redacted_items"]
                page_data["low_confidence_blocks"] = post["low_confidence_idxs"]
                page_data["text"] = " ".join([b["text"] for b in post["filtered_blocks"]])
                
                # Table extraction
                tables = _extract_tables_from_pdfplumber(page)
                page_data["tables"] = tables

            # Parse for Udyam fields
            doc_type, parsed = _parse_document_type(page_data["text"])
            page_data["document_type"] = doc_type
            page_data["parsed_fields"] = parsed
            results.append(page_data)
        
    return results

def _process_image_document(file_path):
    """Processes a single image file."""
    print("Image document detected. OCR not available in simplified version.")
    
    # For now, just return basic info
    page_data = {
        "page_number": 1,
        "type": "image",
        "layout": [],
        "watermark_blocks": [],
        "redacted_items": [],
        "low_confidence_blocks": [],
        "text": "",
        "document_type": "Unknown",
        "parsed_fields": {},
        "tables": []
    }
    
    return [page_data]

def process_document(file_path):
    """
    Main function to process a document.
    It identifies the file type and calls the appropriate processor.
    """
    _, file_extension = os.path.splitext(file_path.lower())
    
    if file_extension == ".pdf":
        return _process_pdf_document(file_path)
    elif file_extension in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
        return _process_image_document(file_path)
    else:
        print(f"Error: Unsupported file type '{file_extension}'")
        return None 