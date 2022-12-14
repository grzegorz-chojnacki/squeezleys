#!/bin/env python3
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

with open('scrapped.json') as f:
    scrapped = json.load(f)

variantable = [ entry for entry in scrapped if 'has_variants' in entry]
print(f'Found {len(variantable)} products with variants')

urls = set()
for variant in variantable:
    associated = filter(lambda x: x['name'] == variant['name'], scrapped)
    urls.update(map(lambda x: x["link"], associated))


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

variants = []
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
        variants.append(obj)
        print(f'Found color: {obj["attributes"]["3"]["name"]}')
    time.sleep(2)

with open('variants.json', 'w') as f:
    json.dump(variants, f, ensure_ascii=False, indent=4)
print('Saved raw data')
