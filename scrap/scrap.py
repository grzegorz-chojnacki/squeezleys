#!/usr/bin/env python3

import re
import requests
import json
from time import sleep
from bs4 import BeautifulSoup
from collections import namedtuple
from dataclasses import dataclass
from typing import List

REQUEST_TIMEOUT = 1

Target = namedtuple('Target', 'href, pages')
targets = [
    # Target('24-gniotki-squishy', 3),
    # Target('215-fidget-toys', 9),
    # Target('25-masy-plastyczne-slime', 1),
    # Target('181-artykuly-papiernicze', 1),
    Target('49-sensoryczne', 1),
    # Target('72-pluszaki-i-maskotki', 1),
    # Target('12-fun-zabawki', 2),
    # Target('223-mystery-box', 1),
]

products = []

def fetch(url: str):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'lxml')
    print(f'fetched "{url}", going to sleep for {REQUEST_TIMEOUT}s...')
    sleep(REQUEST_TIMEOUT)
    return soup

def scrap_product(href: str):
    soup = fetch(href)
    obj = json.loads(soup.find(id='product-details')['data-product'])
    image_urls = [image['bySize']['large_default']['url'] for image in obj['images']]

    variants = []
    for variant_type in soup.find_all('div', class_='product-variants'):
        if variant_type.find('div', class_='label') is None:
            break

        name, = variant_type.find('div', class_='label').string,
        if name == 'Kolor':
            containers = variant_type.find_all('label', class_='label-color')
            for container in containers:
                variants.append({
                    'label': container.find('span', class_='sr-only').string,
                    'value': container.find('span', class_='color')['style'].lstrip('background-color: '),
                })

    product = {
        'name': obj['name'],
        'category': obj['category'],
        'price': obj['price_amount'],
        'base_price': obj['price_without_reduction'],
        'available': obj['quantity'],
        'description': obj['description'],
        'description_short': obj['description_short'],
        'discount': obj['discount_percentage_absolute'],
        'image_urls': image_urls,
        'variants': variants,
    }
    products.append(product)


def scrap_target(href: str, pages: int):
    for page in range(pages):
        soup = fetch(f'https://squishysquishies.pl/{href}?page={page + 1}')
        product_links = soup.find_all('a', class_='product-thumbnail')

    for product_link in product_links:
        scrap_product(product_link['href'])


for target in targets:
    scrap_target(target.href, target.pages)

with open('products.json', 'w') as f:
    json.dump(products, f, ensure_ascii=False, indent=4)