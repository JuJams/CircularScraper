import json
import csv

def parse_json_to_csv(json_path, output_csv):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    output = []
    for item in data:
        name = item.get('name', '').strip()
        description = (item.get('description') or '').strip()
        pre_price = (item.get('pre_price_text') or '').strip()
        price = (item.get('price_text') or '').strip()
        post_price = (item.get('post_price_text') or '').strip()

        # label parsing when it looks like "2 for $5.00" or "$2.99/lb."
        if pre_price:
            final_price = f"{pre_price} ${price}"
        else:
            final_price = f"${price}"
        if post_price:
            final_price += f" {post_price}"

        # price per unit logic
        price_per_unit = ""
        if pre_price.lower().endswith('for') and price.replace('.', '', 1).isdigit():
            try:
                quantity = int(pre_price.lower().replace('for', '').strip())
                unit_price = float(price) / quantity
                price_per_unit = f"${unit_price:.2f}"
            except:
                pass
        else:
            price_per_unit = f"${price}" if price else ""

        category = item.get('categories', [''])[0]

        output.append({
            'name': name,
            'description': description,
            'price': final_price,
            'price_per_unit': price_per_unit,
            'category': category
        })

    # writing to csv
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=output[0].keys())
        writer.writeheader()
        writer.writerows(output)

    print(f"Parsed {len(output)} products into {output_csv}")

if __name__ == "__main__":
    parse_json_to_csv("parseText.json", "output.csv")
