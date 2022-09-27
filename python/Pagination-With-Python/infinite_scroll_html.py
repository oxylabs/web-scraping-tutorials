# Handling pages with load more with HTML response
import requests
from bs4 import BeautifulSoup
import math


def process_pages():
    index_page = 'https://techinstr.myshopify.com/collections/all'
    url = 'https://techinstr.myshopify.com/collections/all?page={}'

    session = requests.session()
    response = session.get(index_page)
    soup = BeautifulSoup(response.text, "lxml")
    count_element = soup.select_one('.filters-toolbar__product-count')
    count_str = count_element.text.replace('products', '')
    count = int(count_str)
    # Process page 1 data here
    page_count = math.ceil(count/8)
    for page_numer in range(2, page_count+1):
        response = session.get(url.format(page_numer))
        soup = BeautifulSoup(response.text, "lxml")
        first_product = soup.select_one('.product-card:nth-child(1) > a > span')
        print(first_product.text.strip())


if __name__ == '__main__':
    process_pages()
