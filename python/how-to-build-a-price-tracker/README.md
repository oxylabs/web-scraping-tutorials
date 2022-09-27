# How to Build a Price Tracker With Python

## Project requirements

The following price monitoring script works with Python version 3.6 and above. The recommended libraries are as follows:

`Requests` – for sending HTTP requests. In other words, for downloading web pages without a browser. It’s the essential library for the upcoming price monitoring script.

`BeautifulSoup` – for querying the HTML for specific elements. It’s a wrapper over a parser library.

`lxml` – for parsing the HTML. An HTML retrieved by the Requests library is a string that requires parsing into a Python object before querying. Instead of directly using this library, we’ll use BeautifulSoup as a wrapper for a more straightforward API.

`Price-parser` – a library useful for every price monitoring script. It helps to extract the price component from a string that contains it.

`smtplib` – for sending emails.

`Pandas` – for filtering product data and reading and writing CSV files.

Optionally, creating a virtual environment will keep the whole process more organized:

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
```

To install the dependencies, open the terminal and run the following command:

```bash
$ pip install pandas requests beautifulsoup4 price-parser
```

Note that the `smtlib` library is part of Python Standard Library and doesn’t need to be installed separately.

Once the installation is complete, create a new Python file and add the following imports:

```python
import smtplib
import pandas as pd
import requests
from bs4 import BeautifulSoup
from price_parser import Price
```

Additionally, add the following lines for initial configuration:

```python
PRODUCT_URL_CSV = "products.csv"
SAVE_TO_CSV = True
PRICES_CSV = “prices.csv"
SEND_MAIL = True
```

The CSV that contains the target URLs is supplied as `PRODUCT_URL_CSV`.

If the `SAVE_TO_CSV` flag is set to `True`, the fetched prices will be saved to the CSV file specified as `PRICES_CSV`.

`SEND_MAIL` is a flag that can be set to `True` to send email alerts.

## Reading a list of product URLs

The easiest way to store and manage the product URLs is to keep them in a CSV or JSON file. This time we’ll use CSV as it’s easily updatable using a text editor or spreadsheet application.

The CSV should contain at least two fields — `url` and `alert_price`. The product’s title can be extracted from the product URL or stored in the same CSV file. If the price monitor finds product price dropping below a value of the `alert_price` field, it’ll trigger an email alert.

![](https://images.prismic.io/oxylabs-sm/ZWRmNGFkMTQtNTBmNS00ZDkzLWFjOTMtOGZmMjdiZDZkYjQx_product-urls.png?auto=compress,format&rect=0,0,1530,276&w=1530&h=276&fm=webp&dpr=2&q=50)

The CSV file can be read and converted to a dictionary object using Pandas. Let’s wrap this up in a simple function:

```python
def get_urls(csv_file):
    df = pd.read_csv(csv_file)
    return df
```

The function will return a Pandas’ DataFrame object that contains three columns — product, URL, and alert_price (see the image above).

## Scraping the prices

The initial step is to loop over the target URLs.

Note that the `get_urls()` returns a DataFrame object. 

To run a loop, first use the `to_dict()` method of Pandas. When the `to_dict` method is called with the parameter as `records`, it converts the DataFrame into a list of dictionaries. 

Run a loop over each dictionary as follows:

```python
def process_products(df):
    for product in df.to_dict("records"):
        # product["url"] is the URL
```

We’ll revisit this method after writing two additional functions. The first function is to get the HTML and the second function is to extract the price from it.

To get the HTML from response for each URL, run the following function:

```python
def get_response(url):
    response = requests.get(url)
    return response.text
```

Next, create a BeautifulSoup object according to the response and locate the price element using a CSS selector. Use the Price-parser library to extract the price as a float for comparison with the alert price. If you want to better understand how the Price-parser library works, head over to our GitHub repository for examples.

The following function will extract the price from the given HTML, returning it as a float:

```python
def get_price(html):
    soup = BeautifulSoup(html, "lxml")
    el = soup.select_one(".price_color")
    price = Price.fromstring(el.text)
    return price.amount_float
```

Note that the CSS selector used in this example is specific to the scraping target. If you are working with any other site, this is the only place where you would have to change the code.

We’re using BeautifulSoup to locate an element containing the price via CSS selectors. The element is stored in the `el` variable. The text attribute of the `el` tag, `el.text`, contains the price and currency symbol. Price-parser parses this string to extract the price as a float value.

There is more than one product URL in the DataFrame object. Let’s loop over all the rows and update the DataFrame with new information.

The easiest approach is to convert each row into a dictionary. This way, you can read the URL, call the `get_price()` function, and update the required fields.

We’ll add two new keys — the extracted price (price) and a boolean value (alert), which filters rows for sending an email.

The `process_products()` function can now be extended to demonstrate the aforementioned sequence:

```python
def process_products(df):
    updated_products = []
     for product in df.to_dict("records"):
        html = get_response(product["url"])
        product["price"] = get_price(html)
        product["alert"] = product["price"] < product["alert_price"]
        updated_products.append(product)
    return pd.DataFrame(updated_products)
```

This function will return a new DataFrame object containing the product URL and a name read from the CSV. Additionally, it includes the price and alert flag used to send an email on a price drop.

## Saving the output
The final DataFrame containing the updated product data can be saved as CSV using a simple call to the to_csv() function.

Additionally, we’ll check the `SAVE_TO_CSV` flag as follows:

```python
if SAVE_TO_CSV:
        df_updated.to_csv(PRICES_CSV, mode="a")
```

You’ll notice that the mode is set to "a", which stands for “append” to ensure new data is appended if the CSV file is present.

## Sending email alerts

Optionally, you can send an email alert on price drop based on the alert flag. First, create a function that filters the data frame and returns email’s subject and body:

```python
def get_mail(df):
    subject = "Price Drop Alert"
    body = df[df["alert"]].to_string()
    subject_and_message = f"Subject:{subject}\n\n{body}"
    return subject_and_message
```

Now, using `smtplib`, create another function that sends alert emails:

```python
def send_mail(df):
    message_text = get_mail(df)
    with smtplib.SMTP("smtp.server.address", 587) as smtp:
        smtp.starttls()
        smtp.login(mail_user, mail_pass)
        smtp.sendmail(mail_user, mail_to, message_text)
```

This code snippet assumes that you’ll set the variables `mail_user`, `mail_pass`, and `mail_to`.

Putting everything together, this is the main function:

```python
def main():
    df = get_urls(PRODUCT_URL_CSV)
    df_updated = process_products(df)
    if SAVE_TO_CSV:
        df_updated.to_csv(PRICES_CSV, index=False, mode="a")
    if SEND_MAIL:
        send_mail(df_updated)
```

Execute this function to run the entire code. 

If you wish to run this automatically at certain intervals, use cronjob on macOS/Linux or Task Scheduler on Windows. 

Alternatively, you can also deploy this price monitoring script on any cloud service environment.
