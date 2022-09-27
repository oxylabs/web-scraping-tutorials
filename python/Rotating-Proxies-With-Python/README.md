# Rotating Proxies With Python
[<img src="https://img.shields.io/static/v1?label=&message=Python&color=brightgreen" />](https://github.com/topics/python) [<img src="https://img.shields.io/static/v1?label=&message=Web%20Scraping&color=important" />](https://github.com/topics/web-scraping) [<img src="https://img.shields.io/static/v1?label=&message=Rotating%20Proxies&color=blueviolet" />](https://github.com/topics/rotating-proxies)

## Table of Contents

- [Finding Current IP Address](#finding-your-current-ip-address)
- [Using A Single Proxy](#using-a-single-proxy)
- [Rotating Multiple Proxies](#rotating-multiple-proxies)
- [Rotating Multiple Proxies Using Async](#rotating-multiple-proxies-using-async)

## Prerequisites

This article uses the python `requests` module. In order to install it, you can use `virtualenv`. `virtualenv` is a tool to create isolated Python environments.

Start by creating a virtual environment in your project folder by running
```bash
$ virtualenv venv
```
This will install python, pip and common libraries in your project folder.

Next, invoke the source command to activate the environment. 
```bash
$ source venv/bin/activate
```

Lastly, install the `requests` module in the current virtual environment
```bash
$ pip install requests
```

Alternatively, you can install the dependencies from the included [requirements.txt](requirements.txt) file by running

```bash
$ pip install -r requirements.txt
```

Congratulations, you have successfully installed the `request` module. Now, it's time to find out your current Ip address!

## Finding Your Current IP Address

Create a file with the `.py` extension with the following contents (or just copy [no_proxy.py](src/no_proxy.py)):

```python
import requests

response = requests.get('https://ip.oxylabs.io/ip')
print(response.text)
```

Now, run it from a terminal

```bash
$ python no_proxy.py

128.90.50.100
```
The output of this script will show your current IP address, which uniquely identifies you on the network. Instead of exposing it directly when requesting pages, we will use a proxy server.

Let's start by using a single proxy.

## Using A Single Proxy 

Your first step is to [find a free proxy server](https://www.google.com/search?q=free+proxy+server+list).

**Important Note**: free proxies are unreliable, slow and can collect the data about the pages you access. If you're looking for a reliable paid option, we highly recommend using [oxylabs.io](https://oxy.yt/GrVD) 

To use a proxy, you will need its:
* scheme (e.g. `http`)
* ip (e.g. `2.56.215.247`)
* port (e.g. `3128`)
* username and password that is used to connect to the proxy (optional)

Once you have it, you need to set it up in the following format
```
SCHEME://USERNAME:PASSWORD@YOUR_PROXY_IP:YOUR_PROXY_PORT
```

Here are a few examples of the proxy formats you may encounter:
```text
http://2.56.215.247:3128
https://2.56.215.247:8091
https://my-user:aegi1Ohz@2.56.215.247:8044
```

Once you have the proxy information, assign it to a constant.

```python
PROXY = 'http://2.56.215.247:3128'
```

Next, define a timeout in seconds as it is always a good idea to avoid waiting indefinitely for the response that may never be returned (due to network issues, server issues or the problems with the proxy server)
```python
TIMEOUT_IN_SECONDS = 10
```

The requests module [needs to know](https://docs.python-requests.org/en/master/user/advanced/#proxies) when to actually use the proxy.
For that, consider the website you are attempting to access. Does it use http or https?
Since we're trying to access **https**://ip.oxylabs.io/ip, we can define this configuration as follows
```python
scheme_proxy_map = {
    'https': PROXY,
}
```

**Note**: you can specify multiple protocols, and even define specific domains for which a different proxy will be used

```python
scheme_proxy_map = {
    'http': PROXY1,
    'https': PROXY2,
    'https://example.org': PROXY3,
}
```

Finally, we make the request by calling `requests.get` and passing all the variables we defined earlier. We also handle the exceptions and show the error when a network issue occurs.

```python
try:
    response = requests.get('https://ip.oxylabs.io/ip', proxies=scheme_proxy_map, timeout=TIMEOUT_IN_SECONDS)
except (ProxyError, ReadTimeout, ConnectTimeout) as error:
        print('Unable to connect to the proxy: ', error)
else:
    print(response.text)
```

The output of this script should show you the ip of your proxy:

```bash
$ python single_proxy.py

2.56.215.247
```

You are now hidden behind a proxy when making your requests through the python script.
You can find the complete code in the file [single_proxy.py](src/single_proxy.py).

Now we're ready to rotate through a list of proxies, instead of using a single one!

## Rotating Multiple Proxies

If you're using unreliable proxies, it could prove beneficial to save a bunch of them into a csv file and run a loop to determine whether they are still available.

For that purpose, first create a file `proxies.csv` with the following content:
```text
http://2.56.215.247:3128
https://88.198.24.108:8080
http://50.206.25.108:80
http://68.188.59.198:80
... any other proxy servers, each of them on a separate line
```

Then, create a python file and define both the filename, and how long are you willing to wait for a single proxy to respond:

```python
TIMEOUT_IN_SECONDS = 10
CSV_FILENAME = 'proxies.csv'
```

Next, write the code that opens the csv file and reads every proxy server line by line into a `csv_row` variable and builds `scheme_proxy_map` configuration needed by the requests module.

```python
with open(CSV_FILENAME) as open_file:
    reader = csv.reader(open_file)
    for csv_row in reader:
        scheme_proxy_map = {
            'https': csv_row[0],
        }
```

And finally, we use the same scraping code from the previous section to access the website via proxy

```python
with open(CSV_FILENAME) as open_file:
    reader = csv.reader(open_file)
    for csv_row in reader:
        scheme_proxy_map = {
            'https': csv_row[0],
        }
        
        # Access the website via proxy
        try:
            response = requests.get('https://ip.oxylabs.io/ip', proxies=scheme_proxy_map, timeout=TIMEOUT_IN_SECONDS)
        except (ProxyError, ReadTimeout, ConnectTimeout) as error:
            pass
        else:
            print(response.text)
```

**Note**: if you are only interested in scraping the content using *any* working proxy from the list, then add a break after print to stop going through the proxies in the csv file

```python
        try:
            response = requests.get('https://ip.oxylabs.io/ip', proxies=scheme_proxy_map, timeout=TIMEOUT_IN_SECONDS)
        except (ProxyError, ReadTimeout, ConnectTimeout) as error:
            pass
        else:
            print(response.text)
            break # notice the break here
```

This complete code is available in [rotating_multiple_proxies.py](src/rotating_multiple_proxies.py)

The only thing that is preventing us from reaching our full potential is speed.
It's time to tackle that in the next section!

## Rotating Multiple Proxies Using Async

Checking all the proxies in the list one by one may be an option for some, but it has one significant downside - this approach is painfully slow. This is because we are using a synchronous approach. We tackle requests one at a time and only move to the next once the previous one is completed. 

A better option would be to make requests and wait for responses in a non-blocking way - this would speed up the script significantly.

In order to do that we use the `aiohttp` module. You can install it using the following cli command: 

```bash
$ pip install aiohttp
```

Then, create a python file where you define:
* the csv filename that contains the proxy list
* url that you wish to use to check the proxies
* how long are you willing to wait for each proxy - the timeout setting

```python
CSV_FILENAME = 'proxies.csv'
URL_TO_CHECK = 'https://ip.oxylabs.io/ip'
TIMEOUT_IN_SECONDS = 10
```

Next, we define an async function and run it using the asyncio module.
It accepts two parameters: 
* the url it needs to request
* the proxy to use to access it

We then print the response. If the script received an error when attempting to access the url via proxy, it will print it as well.

```python

async def check_proxy(url, proxy):
    try:
        session_timeout = aiohttp.ClientTimeout(total=None,
                                                sock_connect=TIMEOUT_IN_SECONDS,
                                                sock_read=TIMEOUT_IN_SECONDS)
        async with aiohttp.ClientSession(timeout=session_timeout) as session:
            async with session.get(url, proxy=proxy, timeout=TIMEOUT_IN_SECONDS) as resp:
                print(await resp.text())
    except Exception as error:
        # you can comment out this line to only see valid proxies printed out in the command line
        print('Proxy responded with an error: ', error)
        return
```

Then, we define a main function that reads the csv file and creates an asynchronous task to check the proxy for every single record in the csv file. 

```python

async def main():
    tasks = []
    with open(CSV_FILENAME) as open_file:
        reader = csv.reader(open_file)
        for csv_row in reader:
            task = asyncio.create_task(check_proxy(URL_TO_CHECK, csv_row[0]))
            tasks.append(task)

    await asyncio.gather(*tasks)
```

Finally, we run the main function and wait until all the async tasks complete
```python
asyncio.run(main())
```

This complete code is available in [rotating_multiple_proxies.py](src/rotating_multiple_proxies_async.py)

This code now runs exceptionally fast!

# We are open to contribution!

Be sure to play around with it and create a pull request with any improvements you may find.

Happy coding!
