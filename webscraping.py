import json
import requests
import unicodedata
from bs4 import BeautifulSoup


def normalize_name(name):
    return name.lower().replace(' ', '_')

def normalize_value(value):
    return unicodedata.normalize("NFKD", value)

def write_to_file(item, data):
    with open(f'{item}.json', 'w') as file:
        json.dump(data, file)


all_items = [
    'processor',
    'motherboard',
    'graphics-card',
    'ram',
    'power-supply'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ApplewebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}

for item in all_items:
    url = f'https://pcbuilder.net/product/{item}/'
    site = requests.get(url, headers=headers)
    soup = BeautifulSoup(site.text, 'lxml')
    table = soup.find_all('table', id='myTable')[0]
    all_rows = table.find_all('tr')
    all_data = []

    for row in all_rows:
        details = row.find_all('td', class_='comp-details')
        product_data = {}
        for detail in details:
            all_names = detail.find_all('div', class_='detail__name')
            all_values = detail.find_all('div', class_='detail__value')
            if len(all_names) != len(all_values):
                raise Exception(f"There's something wrong with the product details in line {all_rows.index(row)}")
            for i in range(len(all_names)):
                name = normalize_name(all_names[i].text[:-1])
                value = normalize_value(all_values[i].text[1:-1])
                product_data[name] = value
            all_data.append(product_data)

    write_to_file(item, all_data)



