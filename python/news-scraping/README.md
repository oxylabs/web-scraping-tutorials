# News Scraping

[<img src="https://img.shields.io/static/v1?label=&message=Playwright&color=brightgreen" />](https://github.com/topics/playwright) [<img src="https://img.shields.io/static/v1?label=&message=Proxy&color=important" />](https://github.com/topics/Proxy)

- [Fetch HTML Page](#fetch-html-page)
- [Parsing HTML](#parsing-html)
- [Extracting Text](#extracting-text)

This article discusses everything you need to know about news scraping, including the benefits and use cases of news scraping as well as how you can use Python to create an article scraper.

For a detailed explanation, see our [blog post](https://oxy.yt/YrD0).



## Fetch HTML Page

```shell
pip3 install requests
```

Create a new Python file and enter the following code:

```python
import requests
response = requests.get(https://quotes.toscrape.com')

print(response.text) # Prints the entire HTML of the webpage.
```

## Parsing HTML

```shell
pip3 install lxml beautifulsoup4
```

```python
from bs4 import BeautifulSoup
response = requests.get('https://quotes.toscrape.com')
soup = BeautifulSoup(response.text, 'lxml')

title = soup.find('title')
```

## Extracting Text

```python
print(title.get_text()) # Prints page title.
```

### Fine Tuning

```python
soup.find('small',itemprop="author")
```

```python
soup.find('small',class_="author")
```

### Extracting Headlines

```python
headlines = soup.find_all(itemprop="text")

for headline in headlines:
    print(headline.get_text())
```



If you wish to find out more about News Scraping, see our [blog post](https://oxy.yt/YrD0).
