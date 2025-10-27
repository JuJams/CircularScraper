import json
import csv
import argparse

def extract_field(item, field_mapping, field_name):
    keys = field_mapping.get(field_name, [])
    for key in keys:
        parts = key.split(".")
        val = item
        try:
            for part in parts:
                if isinstance(val, list):
                    val = val[0] if val else ""
                val = val.get(part, "")
            if isinstance(val, list):
                return ', '.join(map(str, val))
            return str(val).strip()
        except Exception:
            continue
    return ""

def parse_json_with_mapping(json_file, output_csv, field_mapping, max_rows=1000):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Handle wrapped list in {"data": [...]} etc.
    if isinstance(data, dict):
        for val in data.values():
            if isinstance(val, list):
                data = val
                break

    output_rows = []
    for item in data[:max_rows]:
        row = {}
        for field in ['name', 'description', 'price', 'price_per_unit', 'category']:
            row[field] = extract_field(item, field_mapping, field)
        # if row['price']:
        #     row['price'] = row['price'].replace('$', '').strip()
        if row['price'] != "":
            output_rows.append(row)

    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'description', 'price', 'price_per_unit', 'category'])
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"Successfully wrote {len(output_rows)} rows to {output_csv}")

def main():
    parser = argparse.ArgumentParser(description="Modular JSON to CSV parser with field mapping.")
    parser.add_argument("json_file", help="Path to input JSON file")
    parser.add_argument("output_csv", help="Path to output CSV file")
    parser.add_argument("--mapping_file", help="Path to JSON file with column mappings", required=False)

    args = parser.parse_args()

    # Load column mappings
    if args.mapping_file:
        with open(args.mapping_file, 'r', encoding='utf-8') as mf:
            mapping = json.load(mf)
    else:
        # Default fallback mapping
        mapping = {
            "name": ["name"],
            "description": ["description", "sale_story"],
            "price": ["price_text"],
            "price_per_unit": ["post_price_text"],
            "category": ["categories"]
        }

    parse_json_with_mapping(args.json_file, args.output_csv, mapping)

if __name__ == "__main__":
    main()
