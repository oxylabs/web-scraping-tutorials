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