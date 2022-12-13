#!/bin/env python3
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

with open('../data/products.json') as f:
     products = json.load(f)
print('Loaded products')

variantable = [ product for product in products if len(product["variants"]) > 1]
print(f'Found {len(variantable)} products with variants')

with open('../data/raw_data.json') as f:
    raw_data = json.load(f)
print('Loaded raw_data')

urls = set()
for variant in variantable:
    associated = filter(lambda x: x['name'] == variant['name'], raw_data)
    urls.update(map(lambda x: x["link"], associated))


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

raw_data2 = []
for url in urls:
    print(f'# {url}:')
    driver.get(url)

    labels = driver.find_elements(By.CSS_SELECTOR, 'label.label-color')
    print(f'Found {len(labels)} variants')
    for n in range(len(labels)):
        time.sleep(1)
        print(f'- Clicking #{n} label')
        driver.execute_script(f"document.querySelector('label.label-color:nth-child({n + 1}) > input').click()")
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        obj = json.loads(soup.find(id='product-details')['data-product'])
        raw_data2.append(obj)
        print(f'Found color: {obj["attributes"]["3"]["name"]}')
    time.sleep(2)

with open('raw_data2.json', 'w') as f:
    json.dump(raw_data2, f, ensure_ascii=False, indent=4)
print('Saved raw data')
