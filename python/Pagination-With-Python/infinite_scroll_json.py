# Handling pages with load more with JSON response
import requests


def process_pages():
    url = 'http://quotes.toscrape.com/api/quotes?page={}'
    page_numer = 1
    while True:
        response = requests.get(url.format(page_numer))
        data = response.json()
        # Process data
        # ...
        print(response.url)  # only for debug
        if data.get('has_next'):
            page_numer += 1
        else:
            break


if __name__ == '__main__':
    process_pages()
