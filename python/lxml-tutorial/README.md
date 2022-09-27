# lxml Tutorial: XML Processing and Web Scraping With lxml

[<img src="https://img.shields.io/static/v1?label=&message=lxml&color=brightgreen" />](https://github.com/topics/lxml) [<img src="https://img.shields.io/static/v1?label=&message=Web%20Scraping&color=important" />](https://github.com/topics/web-scraping)

- [Installation](#installation)
- [Creating a simple XML document](#creating-a-simple-xml-document)
- [The Element class](#the-element-class)
- [The SubElement class](#the-subelement-class)
- [Setting text and attributes](#setting-text-and-attributes)
- [Parse an XML file using LXML in Python](#parse-an-xml-file-using-lxml-in-python)
- [Finding elements in XML](#finding-elements-in-xml)
- [Handling HTML with lxml.html](#handling-html-with-lxmlhtml)
- [lxml web scraping tutorial](#lxml-web-scraping-tutorial)
- [Conclusion](#conclusion)

In this lxml Python tutorial, we will explore the lxml library. We will go through the basics of creating XML documents and then jump on processing XML and HTML documents. Finally, we will put together all the pieces and see how to extract data using lxml. 

For a detailed explanation, see our [blog post](https://oxy.yt/BrAk).

## Installation

The best way to download and install the lxml library is to use the pip package manager. This works on Windows, Mac, and Linux:

```shell
pip3 install lxml
```

## Creating a simple XML document

A very simple XML document would look like this:

```xml
<root>
    <branch>
        <branch_one>
        </branch_one>
        <branch_one>
        </branch_one >
    </branch>
</root>
```

## The Element class

To create an XML document using python lxml, the first step is to import the `etree` module of lxml:

```python
>>> from lxml import etree
```

In this example, we will create an HTML, which is XML compliant. It means that the root element will have its name as html:

```python
>>> root = etree.Element("html")
```

Similarly, every html will have a head and a body:

```python
>>> head = etree.Element("head")
>>> body = etree.Element("body")
```

To create parent-child relationships, we can simply use the append() method.

```python
>>> root.append(head)
>>> root.append(body)
```

This document can be serialized and printed to the terminal with the help of `tostring()` function:

```python
>>> print(etree.tostring(root, pretty_print=True).decode())
```

## The SubElement class

Creating an `Element` object and calling the `append()` function can make the code messy and unreadable. The easiest way is to use the `SubElement` type:

```python
body = etree.Element("body")
root.append(body)

# is same as 

body = etree.SubElement(root,"body")
```

## Setting text and attributes

Here are the examples:

```python
para = etree.SubElement(body, "p")
para.text="Hello World!"
```

Similarly, attributes can be set using key-value convention:

```python
para.set("style", "font-size:20pt")
```

One thing to note here is that the attribute can be passed in the constructor of SubElement:

```python
para = etree.SubElement(body, "p", style="font-size:20pt", id="firstPara")
para.text = "Hello World!"
```

Here is the complete code:

```python
from lxml import etree
 
root = etree.Element("html")
head = etree.SubElement(root, "head")
title = etree.SubElement(head, "title")
title.text = "This is Page Title"
body = etree.SubElement(root, "body")
heading = etree.SubElement(body, "h1", style="font-size:20pt", id="head")
heading.text = "Hello World!"
para = etree.SubElement(body, "p",  id="firstPara")
para.text = "This HTML is XML Compliant!"
para = etree.SubElement(body, "p",  id="secondPara")
para.text = "This is the second paragraph."
 
etree.dump(root)  # prints everything to console. Use for debug only
```

Add the following lines at the bottom of the snippet and run it again:

```python
with open(‘input.html’, ‘wb’) as f:
    f.write(etree.tostring(root, pretty_print=True)
```

## Parse an XML file using LXML in Python

Save the following snippet as input.html.

```html
<html>
  <head>
    <title>This is Page Title</title>
  </head>
  <body>
    <h1 style="font-size:20pt" id="head">Hello World!</h1>
    <p id="firstPara">This HTML is XML Compliant!</p>
    <p id="secondPara">This is the second paragraph.</p>
  </body>
</html>
```

To get the root element, simply call the `getroot()` method.

```python
from lxml import etree
 
tree = etree.parse('input.html')
elem = tree.getroot()
etree.dump(elem) #prints file contents to console
```

The lxml.etree module exposes another method that can be used to parse contents from a valid xml string — `fromstring()`

```python
xml = '<html><body>Hello</body></html>'
root = etree.fromstring(xml)
etree.dump(root)
```

If you want to dig deeper into parsing, we have already written a tutorial on [BeautifulSoup](https://oxylabs.io/blog/beautiful-soup-parsing-tutorial), a Python package used for parsing HTML and XML documents. 

## Finding elements in XML

Broadly, there are two ways of finding elements using the Python lxml library. The first is by using the Python lxml querying languages: XPath and ElementPath.

```python
tree = etree.parse('input.html')
elem = tree.getroot()
para = elem.find('body/p')
etree.dump(para)
 
# Output 
# <p id="firstPara">This HTML is XML Compliant!</p>
```

Similarly, `findall()` will return a list of all the elements matching the selector.

```python
elem = tree.getroot()
para = elem.findall('body/p')
for e in para:
    etree.dump(e)
 
# Outputs
# <p id="firstPara">This HTML is XML Compliant!</p>
# <p id="secondPara">This is the second paragraph.</p>
```

Another way of selecting the elements is by using XPath directly

```python
para = elem.xpath('//p/text()')
for e in para:
    print(e)
 
# Output
# This HTML is XML Compliant!
# This is the second paragraph.
```

## Handling HTML with lxml.html

Here is the code to print all paragraphs from the same HTML file.

```python
from lxml import html
with open('input.html') as f:
    html_string = f.read()
tree = html.fromstring(html_string)
para = tree.xpath('//p/text()')
for e in para:
    print(e)
 
# Output
# This HTML is XML Compliant!
# This is the second paragraph
```

## lxml web scraping tutorial 

Now that we know how to parse and find elements in XML and HTML, the only missing piece is getting the HTML of a web page.

For this, the Requests library is a great choice:

```
pip install requests
```

Once the requests library is installed, HTML of any web page can be retrieved using  `get()` method. Here is an example.

```python
import requests
 
response = requests.get('http://books.toscrape.com/')
print(response.text)
# prints source HTML
```

Here is a quick example that prints a list of countries from Wikipedia:

```python
import requests
from lxml import html
 
response = requests.get('https://en.wikipedia.org/wiki/List_of_countries_by_population_in_2010')
 
tree = html.fromstring(response.text)
countries = tree.xpath('//span[@class="flagicon"]')
for country in countries:
    print(country.xpath('./following-sibling::a/text()')[0])
```

The following modified code prints the country name and image URL of the flag.

```python
for country in countries:
    flag = country.xpath('./img/@src')[0]
    country = country.xpath('./following-sibling::a/text()')[0]
    print(country, flag)
```

## Conclusion

If you wish to find out more about XML Processing and Web Scraping With lxml, see our [blog post](https://oxy.yt/BrAk).
