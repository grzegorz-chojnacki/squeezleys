#!/bin/env python3

import json
DATA_PATH = '../data/raw_data.json'

with open(DATA_PATH) as f:
    products = json.load(f)

ids = set()

def unique(product):
    if (product['id'], product['id_product_attribute']) in ids:
        return False
    else:
        ids.add((product['id'], product['id_product_attribute']))
        return True

products = [product for product in products if unique(product)]
with open(DATA_PATH, 'w') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)
