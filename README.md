# BharatDoc AI-OCR

A comprehensive multimodal, multilingual OCR system for Indian financial and legal documents.

This project is an implementation of the design provided, aiming to create a robust OCR pipeline with the following capabilities:
-   Handles multiple file types (PDF, JPEG, PNG).
-   Distinguishes between text-based and scanned PDFs.
-   Supports multiple Indian languages.
-   Extracts structured data (key-value pairs, tables).
-   Outputs in various formats (JSON, Excel, CSV).

## Project Structure

The project follows a modular architecture, with each component in its own directory within the `core` folder.

-   `api/`: UI and API layer (FastAPI, Streamlit/Gradio).
-   `core/`: Main processing logic.
    -   `language/`: Language detection and translation.
    -   `layout/`: Layout analysis.
    -   `ocr/`: OCR engine integration.
    -   `output/`: Output generation.
    -   `parsing/`: Document-specific data extraction.
    -   `postprocessing/`: Redaction, confidence scoring.
    -   `preprocessing/`: Image and document preprocessing.
-   `data/`: Sample documents for testing and development.
-   `models/`: Trained AI/ML models.
-   `tests/`: Unit and integration tests.
-   `utils/`: Helper functions.

## Getting Started

1.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    python main.py
    ``` 