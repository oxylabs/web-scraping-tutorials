# Using Python and Beautiful Soup to Parse Data: Intro Tutorial

## Installing Beautiful Soup

```bash
pip install BeautifulSoup4
```

## Getting started

A sample HTML file will help demonstrate the main methods of how Beautiful Soup parses data. This file is much more simple than your average modern website, however, it will be sufficient for the scope of this tutorial.

```html
<!DOCTYPE html>
<html>
    <head>
        <title>What is a Proxy?</title>
        <meta charset="utf-8">
    </head>

    <body>
        <h2>Proxy types</h2>

        <p>
          There are many different ways to categorize proxies. However, two of   
 the most popular types are residential and data center proxies. Here is a list of the most common types.
        </p>

        <ul id="proxytypes">
            <li>Residential proxies</li>
            <li>Datacenter proxies</li>
            <li>Shared proxies</li>
            <li>Semi-dedicated proxies</li>
            <li>Private proxies</li>
        </ul>

    </body>
</html>
```

## Traversing for HTML tags

First, we can use Beautiful Soup to extract a list of all the tags used in our sample HTML file. For this, we will use the soup.descendants generator.

```python
from bs4 import BeautifulSoup

with open('index.html', 'r') as f:
    contents = f.read()

    soup = BeautifulSoup(contents, features="html.parser")

    for child in soup.descendants:

        if child.name:
            print(child.name)
```

After running this code (right click on code and click “Run”) you should get the below output:

```html
html
head
title
meta
body
h2
p
ul
li
li
li
li
li
```

What just happened? Beautiful Soup traversed our HTML file and printed all the HTML tags that it has found sequentially. Let’s take a quick look at what each line did.

```python
from bs4 import BeautifulSoup
```

This tells Python to use the Beautiful Soup library.

```python
with open('index.html', 'r') as f:
    contents = f.read()
```

And this code, as you could probably guess, gives an instruction to open our sample HTML file and read its contents.

```python
    soup = BeautifulSoup(contents, features="html.parser")
```

This line creates a BeautifulSoup object and passes it to Python’s built-in BeautifulSoup HTML parser. Other parsers, such as lxml, might also be used, but it is a separate external library and for the purpose of this tutorial the built-in parser will do just fine.

```python
    for child in soup.descendants:

        if child.name:
            print(child.name)
```

The final pieces of code, namely the soup.descendants generator, instruct Beautiful Soup to look for HTML tags and print them in the PyCharm console. The results can also easily be exported to a .csv file but we will get to this later.

## Getting the full content of tags

To get the content of tags, this is what we can do:

```python
from bs4 import BeautifulSoup

with open('index.html', 'r') as f:
    contents = f.read()

    soup = BeautifulSoup(contents, features="html.parser")

    print(soup.h2)
    print(soup.p)
    print(soup.li)
```

This is a simple instruction that outputs the HTML tag with its full content in the specified order. Here’s what the output should look like:

```html
<h2>Proxy types</h2>
<p>
          There are many different ways to categorize proxies.  However, two of the most popular types are residential and data center proxies. Here is a list of the most common types.
        </p>
<li>Residential proxies</li>
```

You could also remove the HTML tags and print text only, by using, for example:

```python
    print(soup.li.text)
```

Which in our case will give the following output:

```html
Residential proxies
```

Note that this only prints the first instance of the specified tag. Let’s continue to see how to find elements by ID or using the find_all method to filter elements by specific criteria.

## Using Beautiful Soup to find elements by ID

We can use two similar ways to find elements by ID:

```python
    print(soup.find('ul', attrs={'id': 'proxytypes'}))
```

or

```python
    print(soup.find('ul', id='proxytypes'))
```

Both of these will output the same result in the Python Console:

```html
<ul id="proxytypes">
<li>Residential proxies</li>
<li>Datacenter proxies</li>
<li>Shared proxies</li>
<li>Semi-dedicated proxies</li>
<li>Private proxies</li>
</ul>
```

## Finding all specified tags and extracting text

The find_all method is a great way to extract specific data from an HTML file. It accepts many criteria that make it a flexible tool allowing us to filter data in convenient ways. Yet for this tutorial we do not need anything more complex. Let’s find all items of our list and print them as text only:

```python
   for tag in soup.find_all('li'):
        print(tag.text)
```

This is how the full code should look like:

```python
from bs4 import BeautifulSoup

with open('index.html', 'r') as f:
    contents = f.read()

    soup = BeautifulSoup(contents, features="html.parser")

    for tag in soup.find_all('li'):
        print(tag.text)
```

And here’s the output:

```
Residential proxies
Datacenter proxies
Shared proxies
Semi-dedicated proxies
Private proxies
```

## Exporting data to a .csv file

```bash
pip install pandas
```

Add this line to the beginning of your code to import the library:

```python
import pandas as pd
```

Going further, let’s add some lines that will export the list we extracted earlier to a .csv file. This is how our full code should look like:

```python
from bs4 import BeautifulSoup
import pandas as pd

with open('index.html', 'r') as f:
    contents = f.read()

    soup = BeautifulSoup(contents, features="html.parser")
    results = soup.find_all('li')

    df = pd.DataFrame({'Names': results})
    df.to_csv('names.csv', index=False, encoding='utf-8')
```

What happened here? Let’s take a look:

```python
    results = soup.find_all('li')
```

This line finds all instances of the `<li>` tag and stores it in the results object.

```python
    df = pd.DataFrame({'Names': results})
    df.to_csv('names.csv', index=False, encoding='utf-8')
```
