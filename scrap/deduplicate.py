#!/bin/env python3

import json
PRODUCTS_PATH = '../data/products.json'

with open(PRODUCTS_PATH) as f:
    products = json.load(f)

names = dict()

def unique(product):
    if product["name"] in names and product == names[product["name"]]:
        return False
    else:
        names[product["name"]] = product
        return True

products = [product for product in products if unique(product)]
with open(PRODUCTS_PATH, 'w') as f:
    json.dump(products, f, ensure_ascii=False, indent=4)
