# How to Make Web Scraping Faster – Python Tutorial

## How do you speed up web scraping in Python?

There are a few possible approaches that can help increase the scraping speed:

* Multiprocessing

* Multithreading

* Asyncio

However, let’s first take a look at an unoptimized code to make sure the difference between all is clear.

## Web scraping without optimization

We will be scraping 1000 books from books.toscrape.com. This website is a dummy book store that is perfect for learning. 

## Preparation

The first step is to extract all 1000 links to the books and store them in a CSV file. Run this code file to create the links.csv file. You will need to install requests and Beautiful Soup packages for this code to work.

```python
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_links(url="https://books.toscrape.com/", links=[]):
    r = requests.get(url)
    print(r.url, flush=True)
    soup = BeautifulSoup(r.text, "html.parser")

    for link in soup.select("h3 a"):
        links.append(urljoin(url, link.get("href")))

    next_page = soup.select_one("li.next a")
    if next_page:

        return fetch_links(urljoin(url, next_page.get("href"), links))

    else:
        return links

def refresh_links():
    links = fetch_links()
    
    with open('links.csv', 'w') as f:
        for link in links:
            f.write(link + '\n')

refresh_links()
```

The fetch_links function will retrieve all the links, and refresh_links() will store the output in a file. We skipped sending the user agent as this is a test site. However, you can do so easily using the requests library.

## Writing unoptimized web scraper

We will focus on optimizing 1,000 pages of web scraping in Python.

First, install the requests library using pip:

```bash
pip install requests
```

To keep things simple, we will use regular expressions to extract the title element of the page. Note the `get_links` functions that loads the urls we saved in the previous step.

```python
import csv
import re
import time
import requests

def get_links():
    links = []
    with open("links.csv", "r") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            links.append(row[0])

    return links

def get_response(session, url):
    with session.get(url) as resp:
        print('.', end='', flush=True)
        text = resp.text
        exp = r'(<title>).*(<\/title>)'
        return re.search(exp, text,flags=re.DOTALL).group(0)

def main():
    start_time = time.time()
    with requests.Session() as session:
        results = []
        for url in get_links():
            result = get_response(session, url)
            print(result)

    print(f"{(time.time() - start_time):.2f} seconds")

main()
```

The code without optimization code took 288.62 seconds.

## Web scraping using multiprocessing

Multiprocessing, as the name suggests, is utilizing more than one processor. Most modern computers have more than one CPU core, if not multiple CPUs. Using the multiprocessing module, included with the Python standard library, we can write code that uses all these cores. 

For example, if we have an 8-core CPU, we can essentially write code that can split the task into eight different processes where each process runs in a separate CPU core.

Note that this approach is more suitable when the bottleneck is CPU or when the code is CPU-Bound. We will still see some improvements in our case, though. 

The first step is to import `Pool` and `cpu_count` from the multiprocessing module

```python
from multiprocessing import Pool
```

The other change is required in both `get_response` and  `main` functions. 

```python
def get_response(url):
    resp = requests.get(url)
    print('.', end='', flush=True)
    text = resp.text
    
    exp = r'(<title>).*(<\/title>)'
    return re.search(exp, text, flags=re.DOTALL).group(0)

def main():
    start_time = time.time()
    links = get_links()

    with Pool(100) as p:
        results = p.map(get_response, links)
        
        for result in results:
            print(result)

    print(f"{(time.time() - start_time):.2f} seconds")
```

The most critical line of the code is where we create a Pool. Note that we are using `cpu_count()` function to get the count of CPU cores dynamically. This ensures that this code runs on every machine without any change. 

In our example, the execution time came down to about 142 seconds from 288 seconds on a machine with eight cores. This, as expected, is not a vast improvement. Remember that multiprocessing is suitable when the code is CPU-Bound. Our code is I/O bound; thus we don’t see much improvement.

## Web scraping using multithreading

Multithreading is a great option to optimize web scraping code. A thread is essentially a separate flow of execution. Operating systems typically spawn hundreds of threads and switch the CPU time among these. The switching is so fast that we get the illusion of multitasking. The CPU controls this switching, and it cannot be customized. 

Using the `concurrent.futures` module of Python, we can customize how many threads we create to optimize our code. There is only one huge caveat: managing threads can become messy and error-prone as the code becomes more complex. 

To change our code to utilize multithreading, minimal changes are needed.

First, import `ThreadPoolExecutor`.

```python
from concurrent.futures import ThreadPoolExecutor
```

Next, instead of creating a Pool , create a `ThreadPoolExecutor`:

```python
with ThreadPoolExecutor(max_workers=100) as p:
    results = p.map(get_response, links)
```

Note that you have to specify max workers. This number will depend on the complexity of the code. A too high number may harm your code as the overload of creating the threads may be too much.

For this code, the code execution was complete in 12.10 seconds.

For reference, the unoptimized code took 288 seconds. This is a massive improvement. 

## Asyncio for asynchronous programming

Asynchronous coding using the asyncio module is essentially threading where the code controls the context switching. It also makes coding more effortless and less error-prone. Specifically, for web scraping projects, this is the most suitable approach.

This approach requires quite a lot of changes. First, the requests library will not work. Instead, we will use the aiohttp library for web scraping in Python. This requires a separate installation:

```bash
python3 -m pip install aiohttp
```

Next, import `asyncio` and `aiohttp` modules.

```python
import aiohttp 
import asyncio
```

The `get_response()` function now needs to change to a coroutine. Also, we will be using the same session for every execution. Optionally, you can send the user agent if needed.

Note the use of `async` and `await` keywords.

```python
async def get_response(session, url):
    async with session.get(url) as resp:
        text = await resp.text()
        
        exp = r'(<title>).*(<\/title>)'
        return re.search(exp, text,flags=re.DOTALL).group(0)
```

The most significant changes are in the `main()` function.

First, it needs to change to a coroutine. Next, we will use `aiohttp.ClientSession` to create the session object. Most importantly, we will need to create tasks for all the links. Finally, all the tasks will be sent to an event loop using the `asyncio.gather` method.

```python
async def main():
    start_time = time.time()
    async with aiohttp.ClientSession() as session:

        tasks = []
        for url in get_links():
            tasks.append(asyncio.create_task(get_response(session, url)))

        results = await asyncio.gather(*tasks)
        for result in results:
            print(result)

    print(f"{(time.time() - start_time):.2f} seconds")
```

Lastly, to run the `main()` coroutine, we would need to use `asyncio.run(main())`

This execution took 9.43 seconds. 

As you can see, the asyncio approach was the fastest. This, however, requires an entirely new way of thinking. If you have experience with async-await in any programming language, you will find it familiar.
