#!/bin/env python3

import csv
import json

#  0 Product ID
#  1 Active (0/1)
#  2 Name *
#  3 Categories (x,y,z...)
#  4 Price tax excluded
#  5 Tax rules ID
#  6 Wholesale price
#  7 On sale (0/1)
#  8 Discount amount
#  9 Discount percent
# 10 Discount from (yyyy-mm-dd)
# 11 Discount to (yyyy-mm-dd)
# 12 Reference #
# 13 Supplier reference #
# 14 Supplier
# 15 Manufacturer
# 16 EAN13
# 17 UPC
# 18 Ecotax
# 19 Width
# 20 Height
# 21 Depth
# 22 Weight
# 23 Delivery time of in-stock products
# 24 Delivery time of out-of-stock products with allowed orders
# 25 Quantity
# 26 Minimal quantity
# 27 Low stock level
# 28 Send me an email when the quantity is under this level
# 29 Visibility
# 30 Additional shipping cost
# 31 Unity
# 32 Unit price
# 33 Summary
# 34 Description
# 35 Tags (x,y,z...)
# 36 Meta title
# 37 Meta keywords
# 38 Meta description
# 39 URL rewritten
# 40 Text when in stock
# 41 Text when backorder allowed
# 42 Available for order (0 = No, 1 = Yes)
# 43 Product available date
# 44 Product creation date
# 45 Show price (0 = No, 1 = Yes)
# 46 Image URLs (x,y,z...)
# 47 Image alt texts (x,y,z...)
# 48 Delete existing images (0 = No, 1 = Yes)
# 49 Feature(Name:Value:Position)
# 50 Available online only (0 = No, 1 = Yes)
# 51 Condition
# 52 Customizable (0 = No, 1 = Yes)
# 53 Uploadable files (0 = No, 1 = Yes)
# 54 Text fields (0 = No, 1 = Yes)
# 55 Out of stock action
# 56 Virtual product
# 57 File URL
# 58 Number of allowed downloads
# 59 Expiration date
# 60 Number of days
# 61 ID / Name of shop
# 62 Advanced stock management
# 63 Depends On Stock
# 64 Warehouse
# 65 Acessories  (x,y,z...)

#
FILE_PATH = 'http://image-server/'

PRODUCT_ID =  0
ACTIVE =  1
NAME =  2
CATEGORIES =  3
PRICE_TAX_EXCLUDED =  4
ON_SALE =  7
DISCOUNT_PERCENT =  9
DISCOUNT_FROM = 10
DISCOUNT_TO = 11
QUANTITY = 26
MINIMAL_QUANTITY = 27
VISIBILITY = 30
SUMMARY = 34
DESCRIPTION = 35
URL_REWRITTEN = 40
SHOW_PRICE = 46
IMAGE_URLS = 47

category_map = {
  "strona-glowna": "Strona główna",
  "2x2x2": "2x2x2",
  "3x3x3": "3x3x3",
  "4x4x4": "4x4x4",
  "5x5x5": "5x5x5",
  "dlugopisy": "Długopisy",
  "fidget-toys": "Fidget toys",
  "fun-zabawki": "Fun-zabawki",
  "gniotki-antystresowe": "Gniotki antystresowe",
  "gniotki-squishy": "Gniotki squishy",
  "kostki-logiczne": "kostki logiczne",
  "markery-alkoholowe": "Markery Alkoholowe",
  "masy-plastyczne-slime": "Masy plastyczne",
  "mystery-box": "Mystery BOX",
  "piorniki": "Piórniki",
  "pluszaki-i-maskotki": "Pluszaki i maskotki",
  "popit": "Popit",
  "slime": "Slime",
  "zestawy-antystresowe": "Zestawy antystresowe",
  "zestawy-kreatywne": "Zestawy kreatywne"
}


with open('products.json') as f:
    products = json.load(f)


with open('import/categories.csv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter=';', quotechar='"')

    for idx, category in enumerate(category_map.values()):
        if category == "Strona główna":
            continue
        row = [None]*12
        row[PRODUCT_ID]         = idx + 10
        row[ACTIVE]             = 1
        row[NAME]               = category
        row[3]                  = 2
        writer.writerow(row)

with open('import/products.csv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter=';', quotechar='"')

    for idx, product in enumerate(products):
        row = [None]*65
        row[PRODUCT_ID]         = idx + 10
        row[ACTIVE]             = 1
        row[NAME]               = product['name']
        row[CATEGORIES]         = category_map[product['category']]
        row[PRICE_TAX_EXCLUDED] = product['base_price']
        row[ON_SALE]            = 1 if bool(product['discount']) else 0
        row[DISCOUNT_PERCENT]   = product['discount'].rstrip('%') if product['discount'] else ''
        row[DISCOUNT_FROM]      = '2022-12-12'
        row[DISCOUNT_TO]        = '2023-01-12'
        row[QUANTITY]           = product['available']
        row[MINIMAL_QUANTITY]   = 1
        row[VISIBILITY]         = 'both'
        row[SUMMARY]            = product["description_short"]
        row[DESCRIPTION]        = product["description"]
        row[SHOW_PRICE]         = 1
        row[IMAGE_URLS]         = ','.join(map(lambda s: FILE_PATH + s, product["image_urls"]))
        writer.writerow(row)
