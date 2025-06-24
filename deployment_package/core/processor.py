import os
import fitz  # PyMuPDF
import numpy as np
from PIL import Image
from .ocr.engine import ocr_engine_manager
from .language.detect import detect_language
from .parsing.udhyam_parser import parse_udhyam
import pdfplumber
from .postprocessing.watermark import flag_watermark_blocks
from .postprocessing.redact import redact_blocks

# A threshold to decide if a PDF page is scanned.
# If the text extracted from the text layer is less than this, we assume it's scanned.
MIN_TEXT_LENGTH_FOR_DIGITAL = 100
CONFIDENCE_THRESHOLD = 0.7

def _convert_page_to_image(page, dpi=300):
    """Converts a PDF page to a numpy array image."""
    pix = page.get_pixmap(dpi=dpi)
    image = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 4: # RGBA
        # Convert to RGB for OCR
        image = image[..., :3]
    return image

def _extract_digital_pdf_layout(page):
    # Extract word-level bounding boxes and text
    words = page.get_text("words")  # list of (x0, y0, x1, y1, word, block_no, line_no, word_no)
    layout_blocks = []
    for w in words:
        x0, y0, x1, y1, word = w[:5]
        lang = detect_language(word)
        layout_blocks.append({
            "bbox": [x0, y0, x1, y1],
            "text": word,
            "language": lang,
            "confidence": 1.0  # Digital PDFs have no confidence, so set to 1.0
        })
    return layout_blocks

def _extract_ocr_layout_blocks(layout_blocks):
    # Convert PaddleOCR output to a standard format
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
    # For now, always try Udyam parser
    parsed = parse_udhyam(text)
    if parsed:
        doc_type = "Udyam_Certificate"
    else:
        doc_type = "Unknown"
    return doc_type, parsed

def _extract_tables_from_pdfplumber(pdfplumber_page):
    tables = []
    for table in pdfplumber_page.extract_tables():
        # Each table is a list of rows; each row is a list of cell values
        tables.append(table)
    return tables

def _postprocess_layout(layout):
    # 1. Watermark filtering
    watermark_idxs = set(flag_watermark_blocks(layout))
    # 2. Redaction
    redacted_layout, redacted_items = redact_blocks(layout)
    # 3. Confidence flagging
    low_confidence_idxs = [i for i, b in enumerate(redacted_layout) if b["confidence"] < CONFIDENCE_THRESHOLD]
    # 4. Filter out watermark blocks from aggregation
    filtered_blocks = [b for i, b in enumerate(redacted_layout) if i not in watermark_idxs]
    return {
        "layout": redacted_layout,
        "filtered_blocks": filtered_blocks,
        "watermark_idxs": list(watermark_idxs),
        "redacted_items": redacted_items,
        "low_confidence_idxs": low_confidence_idxs
    }

def _process_pdf_document(file_path):
    """Processes a PDF file, page by page."""
    doc = fitz.open(file_path)
    results = []
    
    # Open with pdfplumber for table extraction
    with pdfplumber.open(file_path) as plumber_doc:
        for page_num, page in enumerate(doc):
            page_data = {"page_number": page_num + 1}

            # 1. Attempt to extract text directly
            text = page.get_text()

            # 2. Check if the page is likely scanned or text-based
            if len(text.strip()) < MIN_TEXT_LENGTH_FOR_DIGITAL:
                page_data["type"] = "scanned_pdf_page"
                print(f"Page {page_num + 1} seems to be scanned. Performing OCR.")
                
                # Convert page to image
                image_np = _convert_page_to_image(page)
                
                # Perform OCR
                layout_blocks = ocr_engine_manager.extract_text_from_image(image_np)
                layout = _extract_ocr_layout_blocks(layout_blocks)
                post = _postprocess_layout(layout)
                page_data["layout"] = post["layout"]
                page_data["watermark_blocks"] = post["watermark_idxs"]
                page_data["redacted_items"] = post["redacted_items"]
                page_data["low_confidence_blocks"] = post["low_confidence_idxs"]
                page_data["text"] = " ".join([b["text"] for b in post["filtered_blocks"]])
                page_data["tables"] = []  # Table extraction for scanned pages: future work

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
                plumber_page = plumber_doc.pages[page_num]
                tables = _extract_tables_from_pdfplumber(plumber_page)
                page_data["tables"] = tables

            # Parse for Udyam fields
            doc_type, parsed = _parse_document_type(page_data["text"])
            page_data["document_type"] = doc_type
            page_data["parsed_fields"] = parsed
            results.append(page_data)
        
    doc.close()
    return results

def _process_image_document(file_path):
    """Processes a single image file."""
    print("Image document detected. Performing OCR.")
    layout_blocks = ocr_engine_manager.extract_text_from_image(file_path)
    layout = _extract_ocr_layout_blocks(layout_blocks)
    post = _postprocess_layout(layout)
    text = " ".join([b["text"] for b in post["filtered_blocks"]])
    doc_type, parsed = _parse_document_type(text)
    page_data = {
        "page_number": 1,
        "type": "image",
        "layout": post["layout"],
        "watermark_blocks": post["watermark_idxs"],
        "redacted_items": post["redacted_items"],
        "low_confidence_blocks": post["low_confidence_idxs"],
        "text": text,
        "document_type": doc_type,
        "parsed_fields": parsed,
        "tables": []  # Table extraction for images: future work
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