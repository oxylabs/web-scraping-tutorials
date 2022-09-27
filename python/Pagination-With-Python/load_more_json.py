# Handling pages with load more button with JSON
import requests
from bs4 import BeautifulSoup
import math


def process_pages():
    url = 'https://smarthistory.org/wp-json/smthstapi/v1/objects?tag=938&page={}'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    }
    page_numer = 1
    while True:
        response = requests.get(url.format(page_numer), headers=headers)
        data = response.json()
        # Process data
        # ...
        print(response.url)  # only for debug
        if data.get('remaining') and int(data.get('remaining')) > 0:
            page_numer += 1
        else:
            break


if __name__ == '__main__':
    process_pages()
