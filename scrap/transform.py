#!/bin/env python3
import json

with open('../data/raw_data.json') as f:
    raw_data = json.load(f)
print('Loaded raw data')

URL_PREFIX='https://squishysquishies.pl/'

products = []
image_urls_all = set()
for entry in raw_data:
    image_urls = [image['bySize']['large_default']['url']
                      for image in entry['images']]

    image_paths = list(map(lambda x: x.lstrip(URL_PREFIX).replace('/', '-'), image_urls))
    image_urls_all.update(image_urls)
    product = {
        'name': entry['name'],
        'category': entry['category_name'],
        'price': entry['price_amount'],
        'base_price': entry['price_tax_exc'],
        'available': entry['quantity'],
        'description': entry['description'],
        'description_short': entry['description_short'],
        'discount': entry['discount_percentage_absolute'],
        'color': None,
        'images': image_paths,
    }
    if 'attributes' in entry and '3' in entry['attributes']:
        product["color"] = entry['attributes']['3']['name']

    products.append(product)

print('Transformed products')

with open('../data/products.json', 'w') as f:
    json.dump(products, f, ensure_ascii=False, indent=4)
print('Saved products')

with open('image-urls', 'w') as f:
    f.writelines(map(lambda x: x+'\n', sorted(image_urls_all)))
print('Saved image urls')
