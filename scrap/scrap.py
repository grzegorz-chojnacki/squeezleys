#!/usr/bin/env python3

import re
import requests
import json
from time import sleep
from bs4 import BeautifulSoup
from collections import namedtuple
from dataclasses import dataclass
from typing import List

REQUEST_TIMEOUT = 5
product_count = 0
skip_products = 0

Target = namedtuple('Target', 'href, pages')
targets = [
    Target('24-gniotki-squishy', 3),
    Target('215-fidget-toys', 9),
    Target('25-masy-plastyczne-slime', 1),
    Target('181-artykuly-papiernicze', 1),
    Target('49-sensoryczne', 1),
    Target('72-pluszaki-i-maskotki', 1),
    Target('12-fun-zabawki', 2),
    Target('223-mystery-box', 1),
]

scrapped = []


def fetch(url: str):
    global product_count
    try:
        html = requests.get(url).content
    except Exception as e:
        print(f'Request for product #{product_count} failed')
        print(f'Will retry after a short break...')
        sleep(REQUEST_TIMEOUT * 5)
        html = requests.get(url).content

    soup = BeautifulSoup(html, 'lxml')
    print(f'Fetched "{url}", going to sleep for {REQUEST_TIMEOUT}s...')
    sleep(REQUEST_TIMEOUT)
    return soup


def scrap_product(href: str):
    try:
        soup = fetch(href)
        obj = json.loads(soup.find(id='product-details')['data-product'])
        scrapped.append(obj)

        variants = []
        for variant_type in soup.find_all('div', class_='product-variants'):
            if variant_type.find('div', class_='label') is None:
                break

            name, = variant_type.find('div', class_='label').string,
            if name == 'Kolor':
                scrapped['has_variants'] = True

    except Exception as e:
        print(f'Failed to process product #{product_count}')
        print(f'  product link: "{href}"')
        print(repr(e))


def scrap_target(href: str, pages: int):
    global product_count
    for page in range(pages):
        try:
            soup = fetch(f'https://squishysquishies.pl/{href}?page={page + 1}')
            product_links = soup.find_all('a', class_='product-thumbnail')
            for product_link in product_links:
                product_count += 1
                scrap_product(product_link['href'])
        except Exception as e:
            print(f'Failed to process product page')
            print(f'  product page ({page}): "{href}"')
            print(repr(e))


for target in targets:
    scrap_target(target.href, target.pages)

with open('scrapped.json', 'w') as f:
    json.dump(scrapped, f, ensure_ascii=False, indent=4)
print('Saved scrapped products')
