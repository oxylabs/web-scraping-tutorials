# Handling pages with Next button
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def process_pages():
    url = 'http://books.toscrape.com/catalogue/category/books/fantasy_19/index.html'

    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        footer_element = soup.select_one('li.current')
        print(footer_element.text.strip())

        # Pagination
        next_page_element = soup.select_one('li.next > a')
        if next_page_element:
            next_page_url = next_page_element.get('href')
            url = urljoin(url, next_page_url)
        else:
            break


if __name__ == '__main__':
    process_pages()
