# Web Scraping With RegEx

# Creating virutal environment

```bash
python3 -m venv scrapingdemo
```

```bash
source ./scrapingdemo/bin/activate
```

# Installing requirements

```bash
pip install requests
```

```bash
pip install beautifulsoup4
```

# Importing the required libraries

```python
import requests
from bs4 import BeautifulSoup 
import re
```

## Sending the GET request

Use the Requests library to send a request to a web page from which you want to scrape the data. In this case, https://books.toscrape.com/. To commence, enter the following:

```python
page = requests.get('https://books.toscrape.com/')
```

## Selecting data

First, create a Beautiful Soup object and pass the page content received from your request during the initialization, including the parser type. As you’re working with an HTML code, select `HTML.parser` as the parser type.

![image](https://user-images.githubusercontent.com/95211181/189277235-ae681699-d475-411a-8bb6-7b3fcb2fc031.png)

By inspecting the elements (right-click and select inspect element) in a browser, you can see that each book title and price are presented inside an `article` element with the class called `product_pod`. Use Beautiful Soup to get all the data inside these elements, and then convert it to a string:

```python
soup = BeautifulSoup(page.content, 'html.parser')
content = soup.find_all(class_='product_pod')
content = str(content)
```

## Processing the data using RegEx

Since the acquired content has a lot of unnecessary data, create two regular expressions to get only the desired data.

![](https://images.prismic.io/oxylabs-sm/YTViYjIyMTItZDczMi00OTVhLTliZDEtY2E2MTZiMDhmMzdh_image3.png?auto=compress,format&rect=0,0,1486,520&w=1486&h=520&fm=webp&q=75)

### Expression # 1
### Finding the pattern

First, inspect the title of the book to find the pattern. You can see above that every title is present after the text `title=` in the format `title=“Titlename”`.

### Generating the expression

Then, create an expression that returns the data inside quotations after the `title=` by specifying `"(.*?)"`.

The first expression is as follows:

```python
re_titles = r'title="(.*?)">'
```

### Expression # 2
### Finding the pattern

First, inspect the price of the book. Every price is present after the text `£` in the format `£=price` before the paragraph tag `</p>`.

### Generating the expression

Then, create an expression that returns the data inside quotations after the `£=` and before the `</p>` by specifying `£(.*?)</p>`.

The second expression is as follows:

```python
re_prices = '£(.*?)</p>'
```

To conclude, use the expressions with `re.findall` to find the substrings matching the patterns. Lastly, save them in the variables `title_list` and `price_list`.

```python
titles_list = re.findall(re_titles, content)
price_list = re.findall(re_prices, content)
```

## Saving the output

To save the output, loop over the pairs for the titles and prices and write them to the `output.txt` file.

```python
with open("output.txt", "w") as f:
   for title, price in zip(titles_list, price_list):
       f.write(title + "\t" + price + "\n")
```

![](https://images.prismic.io/oxylabs-sm/NDQ3OTE2NzItZTQ5MC00YzY5LThiYzAtNDM3MDcwODNkNjBl_image2-1.png?auto=compress,format&rect=0,0,1180,953&w=1180&h=953&fm=webp&q=75)

Putting everything together, this is the complete code that can be run by calling `python demo.py`:

```python
# Importing the required libraries.
import requests
from bs4 import BeautifulSoup
import re

# Requesting the HTML from the web page.
page = requests.get("https://books.toscrape.com/")

# Selecting the data.
soup = BeautifulSoup(page.content, "html.parser")
content = soup.find_all(class_="product_pod")
content = str(content)

# Processing the data using Regular Expressions.
re_titles = r'title="(.*?)">'
titles_list = re.findall(re_titles, content)
re_prices = "£(.*?)</p>"
price_list = re.findall(re_prices, content)

#  Saving the output.
with open("output.txt", "w") as f:
   for title, price in zip(titles_list, price_list):
       f.write(title + "\t" + price + "\n")

```
