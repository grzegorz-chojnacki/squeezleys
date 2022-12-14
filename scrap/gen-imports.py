#!/bin/env python3

import csv
import json


FILE_PATH = 'http://localhost/images/'


def write_all(filepath, rows):
    with open(f'../data/{filepath}', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';', quotechar='"')
        writer.writerow(rows[0].keys())
        writer.writerows(row.values() for row in rows)

with open('products.json') as f:
    products = json.load(f)


categories_rows = []
products_rows = []
combinations_rows = []

categories = sorted(set(product['category'] for product in products))
for idx, category in enumerate(categories):
    idx += 10 # offset indecies as some of the first are reserved
    if category == 'Strona główna':
        continue
    row = {
        'id':               idx,
        'active':           1,
        'name':             category,
        'parent_category':  2,
    }
    categories_rows.append(row)

for idx, product in enumerate(products):
    idx += 10 # offset indecies as some of the first are reserved
    row = {
        'id':                 idx,
        'active':             1,
        'tax_id':             1,
        'name':               product['name'],
        'categories':         product['category'],
        'price_tax_excluded': product['base_price'],
        'on_sale':            1 if bool(product['discount']) else 0,
        'discount_percent':   product['discount'].rstrip('%') if product['discount'] else '',
        'discount_from':      '2022-12-12',
        'discount_to':        '2023-01-12',
        'quantity':           product['available'],
        'visibility':         'both',
        'summary':            product['description_short'],
        'description':        product['description'],
        'image_urls':         ','.join(FILE_PATH + p for p in product['images']),
    }
    products_rows.append(row)

    # Handle combinations
    for variant in product['variants']:
        row = {
            'product_id':             idx,
            'attribute':              'Kolor:color:0',
            'value':                  f'{variant["color"]}:0',
            'combination_quantity':   variant['available'],
            'combination_image_urls': ','.join(FILE_PATH + p for p in variant['images']),
        }
        combinations_rows.append(row)


for filepath, rows in [
        ('categories.csv', categories_rows),
        ('products.csv', products_rows),
        ('combinations.csv', combinations_rows)]:
    write_all(filepath, rows)
