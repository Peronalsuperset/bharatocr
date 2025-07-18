import json

def write_json(data, output_path):
    """
    Writes structured data (including tables, layout, parsed fields) to a JSON file.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2) 