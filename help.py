import pandas as pd
import requests
from bs4 import BeautifulSoup

baseurl = 'https://edibazzar.pl'

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 '
#                   'Safari/537.36',
#     'accept': '*/*'
# }

product_links = []


def get_all_pages():
    for x in range(0, 30):
        res = requests.get(f'https://edibazzar.pl/bizuteria/{x}')
        html = BeautifulSoup(res.text, 'lxml')
        product_list = html.findAll('div', class_='product-inner-wrap')
        return product_list


pages = get_all_pages()


# CHECK
def get_all_links():
    for item in pages:
        for link in item.find_all_next('a', href=True):
            product_links.append(baseurl + link['href'])
        return product_links


_all_links = get_all_links()

_final_result_for_products = []

for links in _all_links:
    r = requests.get(links)
    soup = BeautifulSoup(r.content, 'lxml')
    name = soup.find('h1').get_text(strip=True)
    price1 = soup.find('div', class_='basket').find_next('div', class_='price').find_next(
        'em').get_text().replace(
        '\xa0zł', '')
    div = soup.find('div', class_='resetcss')
    _final_result_for_products.append([
        'name', name,
        'price', price1,
        'div', div
    ])
    pd.DataFrame(_final_result_for_products).to_excel('output.xlsx', header=False, index=False)
