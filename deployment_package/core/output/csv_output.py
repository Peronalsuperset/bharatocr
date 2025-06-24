import csv

def write_kv_csv(data, output_path):
    """
    Writes a dictionary of key-value pairs to a CSV file.
    """
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['key', 'value'])
        for k, v in data.items():
            writer.writerow([k, v])

def write_tables_csv(tables, output_path_prefix):
    """
    Writes each table (list of rows) to a separate CSV file.
    output_path_prefix: e.g., 'output/mydoc_page1_table'
    Files will be named 'output/mydoc_page1_table1.csv', etc.
    """
    for idx, table in enumerate(tables, 1):
        outpath = f"{output_path_prefix}{idx}.csv"
        with open(outpath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for row in table:
                writer.writerow(row) 