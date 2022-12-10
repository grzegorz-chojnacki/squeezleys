#!/bin/env python3

import json
PRODUCTS_PATH = '../data/products.json'

with open(PRODUCTS_PATH) as f:
    products = json.load(f)

names = set()

def unique(product):
    if product["name"] in names:
        return False
    else:
        names.add(product["name"])
        return True

products = [product for product in products if unique(product)]
with open(PRODUCTS_PATH, 'w') as f:
    json.dump(products, f, ensure_ascii=False, indent=4)
