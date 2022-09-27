# Handling pages with Next button
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def process_pages():
    url = 'https://www.gosc.pl/doc/791526.Zaloz-zbroje'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    page_link_el = soup.select('.pgr_nrs a')
    # process first page
    for link_el in page_link_el:
        link = urljoin(url, link_el.get('href'))
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'lxml')
        print(response.url)
        # process remaining pages


if __name__ == '__main__':
    process_pages()
