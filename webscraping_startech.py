import json
import requests
import unicodedata
from bs4 import BeautifulSoup

def write_to_file(data):
    with open(f'video-cards-details.json', 'w') as file:
        json.dump(data, file)

def normalize_name(name):
    return name.lower().replace(' ', '_')

def normalize_value(value):
    return unicodedata.normalize("NFKD", value)

def gpu_details(url, headers):
    site = requests.get(url, headers=headers)
    soup = BeautifulSoup(site.text, 'lxml')
    table = soup.find_all('table', class_='data-table flex-table')[0]
    table_bodies = table.find_all('tbody')
    gpu_name = soup.find_all('h1', class_='product-name')[0].text
    data = None
    for body in table_bodies:
        all_rows = body.find_all('tr')
        for row in all_rows:
            name = row.find('td', class_='name').text
            value = row.find('td', class_='value').text
            if name in ['Recommended PSU', 'Consumption']:
                name = normalize_name(name)
                value = normalize_value(value)
                data = {gpu_name: {}}
                data[gpu_name][name] = value
    return data


def gpu_list(url, headers):
    site = requests.get(url, headers=headers)
    soup = BeautifulSoup(site.text, 'lxml')
    content = soup.find_all('div', id='content')[0]
    all_rows = content.find_all('div', class_='product-thumb ws-box')
    next_page = None
    all_gpu_details = []
    for row in all_rows:
        link = row.find_all('a')[0]['href']
        details = gpu_details(link, headers)
        if details is not None:
            all_gpu_details.append(details)
    pages_footer = soup.find_all('ul', class_='pagination')[0]
    last_page = pages_footer.find_all('a')[-1]
    if last_page.text == 'NEXT':
        next_page = last_page['href']
    return next_page, all_gpu_details

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ApplewebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}

url = f'https://www.startech.com.bd/tool/pc_builder/choose?component_id=7'
data_to_write = []

while(url is not None):
    url, all_data = gpu_list(url, headers)
    data_to_write += all_data
    print(url)
write_to_file(data_to_write)