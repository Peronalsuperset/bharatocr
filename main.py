import argparse
import os
from core.processor import process_document
from core.output.json_output import write_json
from core.output.csv_output import write_kv_csv, write_tables_csv

def main():
    parser = argparse.ArgumentParser(description="BharatDoc AI-OCR: Process a single document.")
    parser.add_argument("file_path", type=str, help="The path to the document file (PDF, PNG, JPG).")
    parser.add_argument("--outdir", type=str, default="output", help="Directory to save outputs.")
    parser.add_argument("--formats", type=str, default="json,csv", help="Comma-separated output formats: json,csv")
    args = parser.parse_args()

    if not os.path.exists(args.file_path):
        print(f"Error: File not found at '{args.file_path}'")
        return

    os.makedirs(args.outdir, exist_ok=True)
    formats = [fmt.strip() for fmt in args.formats.split(",")]

    print(f"Processing document: {args.file_path}")
    extracted_data = process_document(args.file_path)

    if extracted_data:
        print("\n--- Extracted Data ---")
        for page_num, page_data in enumerate(extracted_data, 1):
            print(f"\n[Page {page_num}] Type: {page_data['type']} Document Type: {page_data.get('document_type','')}")
            if "parsed_fields" in page_data and page_data["parsed_fields"]:
                print("  Parsed Fields:")
                for k, v in page_data["parsed_fields"].items():
                    print(f"    {k}: {v}")
            else:
                print("  No structured fields parsed.")
            if page_data.get("tables"):
                print(f"  Tables Extracted: {len(page_data['tables'])}")
            if page_data.get("watermark_blocks"):
                print(f"  Watermark Blocks: {len(page_data['watermark_blocks'])}")
            if page_data.get("redacted_items"):
                print(f"  Redacted Items: {page_data['redacted_items']}")
            if page_data.get("low_confidence_blocks"):
                print(f"  Low Confidence Blocks: {len(page_data['low_confidence_blocks'])}")
            # Save outputs
            base = os.path.splitext(os.path.basename(args.file_path))[0]
            for fmt in formats:
                if fmt == "json":
                    outpath = os.path.join(args.outdir, f"{base}_page{page_num}.json")
                    write_json(page_data, outpath)
                elif fmt == "csv":
                    outpath = os.path.join(args.outdir, f"{base}_page{page_num}.csv")
                    write_kv_csv(page_data.get("parsed_fields", {}), outpath)
                    if page_data.get("tables"):
                        prefix = os.path.join(args.outdir, f"{base}_page{page_num}_table")
                        write_tables_csv(page_data["tables"], prefix)
    else:
        print("No data was extracted from the document.")

if __name__ == "__main__":
    main() 