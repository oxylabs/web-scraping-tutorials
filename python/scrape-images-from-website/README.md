# Scrape Images From a Website with Python

## Project requirements

```bash
pip install beautifulsoup4 selenium pandas requests Pillow
```

## Back to square one

```python
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
driver = webdriver.Chrome(executable_path='/nix/path/to/webdriver/executable')
driver.get('https://your.url/here?yes=brilliant')
results = []
content = driver.page_source
soup = BeautifulSoup(content)
```

Our data extraction process begins almost exactly the same (we will import libraries as needed). We assign our preferred webdriver, select the URL from which we will scrape image links and create a list to store them in. As our Chrome driver arrives at the URL, we use the variable ‘content’ to point to the page source and then “soupify” it with BeautifulSoup.

In the previous tutorial, we performed all actions by using built-in and library defined functions. While we could do another tutorial without defining any functions, it is an extremely useful tool for just about any project:

```python
# Example on how to define a function and select custom arguments for the
# code that goes into it.
def function_name(arguments):
    # Function body goes here.
```

We’ll move our URL scraper into a defined function. Additionally, we will reuse the same code we used in the [“Python Web Scraping Tutorial: Step-by-Step” article](https://oxylabs.io/blog/python-web-scraping) and repurpose it to scrape full URLs.

Before

```python
for a in soup.findAll(attrs={'class': 'class'}):
    name = a.find('a')
    if name not in results:
        results.append(name.text)
```

After 

```python
#picking a name that represents the functions will be useful later on.
def parse_image_urls(classes, location, source):
    for a in soup.findAll(attrs={'class': classes}):
        name = a.find(location)
        if name not in results:
            results.append(name.get(source))
```

Note that we now append in a different manner.  Instead of appending the text, we use another function `get()` and add a new parameter ‘source’ to it. We use ‘source’ to indicate the field in the website where image links are stored . They will be nested in a ‘src’, ‘data-src’ or other similar HTML tags.

## Moving forward with defined functions

Let’s assume that our target URL has image links nested in the classes ‘blog-card__link’, ‘img’ and that the URL itself is in the ‘src’ attribute of the element. We would call our newly defined function as such:

```python
parse_image_urls("blog-card__link", "img", "src")
```

Our code should now look something like this:

```python
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome(executable_path='/nix/path/to/webdriver/executable')
driver.get('https://your.url/here?yes=brilliant')
results = []
content = driver.page_source
soup = BeautifulSoup(content)


def parse_image_urls(classes, location, source):
    for a in soup.findAll(attrs={'class': classes}):
        name = a.find(location)
        if name not in results:
            results.append(name.get(source))

parse_image_urls("blog-card__link", "img", "src")
```

Since we sometimes want to export scraped data and we had already used pandas before, we can check by outputting everything into a “.csv” file. If needed, we can always check for any possible semantic errors this way.

```python
df = pd.DataFrame("links": results})
df.to_csv('links.csv', index=False, encoding='utf-8')
```

If we run our code right now, we should get a `links.csv` file outputted right into the running directory.

## Time to extract images from the website

Assuming that we didn’t run into any issues at the end of the previous section, we can continue to download images from websites.

```python
#import library requests to send HTTP requests
import requests
for b in results:
#add the content of the url to a variable
    image_content = requests.get(b).content
```

We will use the requests library to acquire the content stored in the image URL. Our `for` loop above will iterate over our `results` list.

```python
#io manages file-related in/out operations
import io
#creates a byte object out of image_content and point the variable image_file to it
image_file = io.BytesIO(image_content)
```

We are not done yet. So far the “image” we have above is just a Python object.

```python
#we use Pillow to convert our object to an RGB image
from PIL import Image
image = Image.open(image_file).convert('RGB')
```

We are still not done as we need to find a place to save our images. Creating a folder “Test” for the purposes of this tutorial would be the easiest option.

```python
#pathlib let's us point to specific locations. Will be used to save our images.
import pathlib
#hashlib allows us to get hashes. We will be using sha1 to name our images.
import hashlib
#sets a file_path variable which is pointed to 
#our directory and creates a file based on #the sha1 hash of 'image_content' 
#and uses .hexdigest to convert it into a string.
file_path = pathlib.Path('nix/path/to/test', hashlib.sha1(image_content).hexdigest()[:10] + '.png')
image.save(file_path, "PNG", quality=80)
```

## Putting it all together

Let’s combine all of the previous steps without any comments and see how it works out. Note that pandas are greyed out as we are not extracting data into any tables. We kept it in for the sake of convenience. Use it if you need to see or double-check the outputs.

```python
import hashlib
import io
from pathlib import Path
import pandas as pd
import requests
from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver

driver = webdriver.Chrome(executable_path='/nix/path/to/webdriver/executable')
driver.get('https://your.url/here?yes=brilliant')
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
results = []
content = driver.page_source
soup = BeautifulSoup(content)


def gets_url(classes, location, source):
   results = []
   for a in soup.findAll(attrs={'class': classes}):
       name = a.find(location)
       if name not in results:
           results.append(name.get(source))
   return results


driver.quit()

if __name__ == "__main__":
   returned_results = gets_url("blog-card__link", "img", "src")
   for b in returned_results::
    image_content = requests.get(b).content
    image_file = io.BytesIO(image_content)
    image = Image.open(image_file).convert('RGB')
    file_path = pathlib.Path('nix/path/to/test', hashlib.sha1(image_content).hexdigest()[:10] + '.png')
    image.save(file_path, "PNG", quality=80)
```

For efficiency, we quit our webdriver by using “driver.quit()” after retrieving the URL list we need. We no longer need that browser as everything is stored locally.

Running our application will output one of two results:

1.Images are outputted into the folder we selected by defining the ‘file_path’ variable.

2.Python outputs a `403` Forbidden HTTP error.

Obviously, getting the first result means we are finished. We would receive the second outcome if we were to scrape our /blog/ page. Fixing the second outcome will take a little bit of time in most cases, although, at times, there can be more difficult scenarios.

Whenever we use the requests library to send a request to the destination server, a default user-agent “Python-urllib/version.number” is assigned. Some web services might block these user-agents specifically as they are guaranteed to be bots. Fortunately, the requests library allows us to assign any user-agent (or an entire header) we want:

```python
image_content = requests.get(b, headers={'User-agent': 'Mozilla/5.0'}).content
```

## Cleaning up

Our task is finished but the code is still messy.  We can make our application more readable and reusable by putting everything under defined functions:

```python
import io
import pathlib
import hashlib
import pandas as pd
import requests
from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver


def get_content_from_url(url):
   driver = webdriver.Chrome()  # add "executable_path=" if driver not in running directory
   driver.get(url)
   driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
   page_content = driver.page_source
   driver.quit()  # We do not need the browser instance for further steps.
   return page_content


def parse_image_urls(content, classes, location, source):
   soup = BeautifulSoup(content)
   results = []
   for a in soup.findAll(attrs={"class": classes}):
       name = a.find(location)
       if name not in results:
           results.append(name.get(source))
   return results


def save_urls_to_csv(image_urls):
   df = pd.DataFrame({"links": image_urls})
   df.to_csv("links.csv", index=False, encoding="utf-8")


def get_and_save_image_to_file(image_url, output_dir):
   response = requests.get(image_url, headers={"User-agent": "Mozilla/5.0"})
   image_content = response.content
   image_file = io.BytesIO(image_content)
   image = Image.open(image_file).convert("RGB")
   filename = hashlib.sha1(image_content).hexdigest()[:10] + ".png"
   file_path = output_dir / filename
   image.save(file_path, "PNG", quality=80)


def main():
   url = "https://your.url/here?yes=brilliant"
   content = get_content_from_url(url)
   image_urls = parse_image_urls(
       content=content, classes="blog-card__link", location="img", source="src",
   )
   save_urls_to_csv(image_urls)

   for image_url in image_urls:
       get_and_save_image_to_file(
           image_url, output_dir=pathlib.Path("nix/path/to/test"),
       )


if __name__ == "__main__":  #only executes if imported as main file
   main()
```
