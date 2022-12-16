#!/bin/env python3

import csv
import json


FILE_PATH = 'file:///images/'


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
categories_rows.append({
    'category id': 9,
    'active (0/1)': 1,
    'name *': 'Strona Główna',
    'parent category': 'Home',
    'root category (0/1)': 1,
    'description': '',
    'meta title': '',
    'meta keywords': '',
    'meta description': '',
    'url rewritten': '',
    'image url': '',
})

for idx, category in enumerate(categories):
    idx += 10 # offset indecies as some of the first are reserved
    if category == 'Strona główna':
        continue
    row = {
        'category id': idx,
        'category id': idx,
        'active (0/1)': 1,
        'name *': category,
        'parent category': 9,
        'root category (0/1)': 0,
        'description': '',
        'meta title': '',
        'meta keywords': '',
        'meta description': '',
        'url rewritten': '',
        'image url': '',
    }
    categories_rows.append(row)

for idx, product in enumerate(products):
    idx += 10 # offset indecies as some of the first are reserved
    row = {
        'product id': idx,
        'active (0/1)': 1,
        'name *': product['name'],
        'categories (x,y,z...)': product['category'],
        'price tax excluded': product['base_price'],
        'tax rules id': 1,
        'wholesale price': '',
        'on sale (0/1)':   1 if bool(product['discount']) else 0,
        'discount amount': '',
        'discount percent': product['discount'].rstrip('%') if product['discount'] else '',
        'discount from (yyyy-mm-dd)': '2022-12-12',
        'discount to (yyyy-mm-dd)': '2023-01-12',
        'reference #': '',
        'supplier reference #': '',
        'supplier': '',
        'manufacturer': '',
        'ean13': '',
        'upc': '',
        'MPN': '',
        'ecotax': '',
        'width': '',
        'height': '',
        'depth': '',
        'weight': '',
        'delivery time of in-stock products': '',
        'delivery time of out-of-stock products with allowed orders': '',
        'quantity': product['available'],
        'minimal quantity': '',
        'low stock level': '',
        'send me an email when the quantity is under this level': '',
        'visibility': 'both',
        'additional shipping cost': 8.99,
        'unity': '',
        'unit price': '',
        'summary': product['description_short'],
        'description': product['description'],
        'tags (x,y,z...)': '',
        'meta title': '',
        'meta keywords': '',
        'meta description': '',
        'url rewritten': '',
        'text when in stock': '',
        'text when backorder allowed': '',
        'available for order (0 = no, 1 = yes)': '',
        'product available date': '',
        'product creation date': '',
        'show price (0 = no, 1 = yes)': '',
        'image urls (x,y,z...)': ','.join(FILE_PATH + p for p in product['images']),
        'image alt texts (x,y,z...)': '',
        'delete existing images (0 = no, 1 = yes)': '',
        'feature(name:value:position)': '',
        'available online only (0 = no, 1 = yes)': '',
        'condition': '',
        'customizable (0 = no, 1 = yes)': '',
        'uploadable files (0 = no, 1 = yes)': '',
        'text fields (0 = no, 1 = yes)': '',
        'out of stock action': '',
        'virtual product': '',
        'file url': '',
        'number of allowed downloads': '',
        'expiration date': '',
        'number of days': '',
        'id / name of shop': '',
        'advanced stock management': '',
        'depends on stock': '',
        'warehouse': '',
        'acessories  (x,y,z...)': '',
    }
    products_rows.append(row)

    # Handle combinations
    for variant in product['variants']:
        row = {
            'product id*': idx,
            'product index': '',
            'attribute (name:type:position)*': 'Kolor:color:0',
            'value (value:position)*': f'{variant["color"]}:0',
            'supplier reference': '',
            'reference': '',
            'ean13': '',
            'upc': '',
            'MPN': '',
            'wholesale price': '',
            'impact on price': '',
            'ecotax': '',
            'quantity': variant['available'],
            'minimal quantity': '',
            'low stock level': '',
            'send me an email when the quantity is under this level': '',
            'impact on weight': '',
            'default (0 = no, 1 = yes)': '',
            'combination available date': '',
            'image position': '',
            'image urls (x,y,z...)': ','.join(FILE_PATH + p for p in variant['images']),
            'image alt texts (x,y,z...)': '',
            'id / name of shop': '',
            'advanced stock managment': '',
            'depends on stock': '',
            'warehouse': '',
        }
        combinations_rows.append(row)

for filepath, rows in [
        ('categories.csv', categories_rows),
        ('products.csv', products_rows),
        ('combinations.csv', combinations_rows)]:
    write_all(filepath, rows)
