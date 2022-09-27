# Rotating-Proxies-with-JavaScript

[<img src="https://img.shields.io/static/v1?label=&message=JavaScript&color=brightgreen" />](https://github.com/topics/javascript) [<img src="https://img.shields.io/static/v1?label=&message=Web%20Scraping&color=important" />](https://github.com/topics/web-scraping) [<img src="https://img.shields.io/static/v1?label=&message=Rotating%20Proxies&color=blueviolet" />](https://github.com/topics/rotating-proxies)

- [Requirements](#requirements)
- [Finding Current IP Aaddress](#finding-current-ip-aaddress)
- [Using Proxy](#using-proxy)
- [Rotating Multiple Proxies](#rotating-multiple-proxies)

## Requirements

In this tutorial, we will be using [Axios](https://github.com/axios/axios) to make requests. If needed, the code can be easily modified for other libraries as well.

Open the terminal and run the following command to initiate a new Node project:

```shell
npm init -y
```

Next step is to install Axios by running the following command:

```sh
npm install axios
```

## Finding Current IP Address

To check if the proxy works properly, first, we need a basic code that prints the current IP address.

The website http://httpbin.org/ip is appropriate for this purpose as it returns IP addresses in a clean format.

Create a new JavaScript file and make changes as outlined below.

The first step would be to import `axios`.

```JavaScript
const axios = require("axios");
```
Next, call the `get()` method and send the URL of the target website.

```javascript
const url = 'https://httpbin.org/ip';
const response = await axios.get(url);
```

To see the data returned by the server, access `data` attribute of the `response` object:

```JavaScript
console.log(response.data);
// Prints current IP
```

For the complete implementation, see the [no_proxy.js](no_proxy.js) file.

## Using a Proxy 

For this example, we are going to use a proxy with IP 46.138.246.248 and port 8088. 

Axios can handle proxies directly. The proxy information needs to be sent as the second parameter of the `get()` method.

The proxy object should have a `host` and `port`. See an example:

```JavaScript
proxy_no_auth = {
    host: '46.138.246.248',
    port: 8088
}
```

If proxies need authentication, simply add an `auth` object with `username` and `password`.

```javascript
proxy_with_auth = {
    host: '46.138.246.248',
    port: 8088,
    auth: {
        username: 'USERNAME',
        password: 'PASSWORD'
    }
}
```

This `proxy_no_auth` or `proxy_with_auth` object can then be sent with the `get` method.

```javascript
const response = await axios.get(url, {
    proxy: proxy_no_auth
});
```

Run this code from the terminal to see the effective IP address.

You will notice that now, instead of your original IP, the IP address of the proxy is printed.

```sh
node single_proxy_axios.js
// Prints {'origin': '46.138.246.248'}
```

See the complete implementation in the [single_proxy_axios.js](single_proxy_axios.js) file.

## Rotating Multiple Proxies

If multiple proxies are available, it is possible to rotate proxies with JavaScript.

Some websites allow downloading a list of proxies as CSV or similar format. 

In this example, we will be working with a file downloaded from one of the free websites. 

This file contains the proxies in this format. Note that proxy and port are separated by a comma.

```
20.94.229.106,80
209.141.55.228,80
103.149.162.194,80
206.253.164.122,80
200.98.114.237,8888
193.164.131.202,7890
98.12.195.129,44
49.206.233.104,80
```

To get a rotating IP proxy using this file, first, we need to read this CSV file in asynchronous code.

To read CSV file asynchronously, install the package [async-csv](https://www.npmjs.com/package/async-csv).

```sh
npm install async-csv
```

We will also need the `fs` package, which does not need a separate install.

After the imports, use the following lines of code to read the CSV file.

```javascript
// Read file from disk:
const csvFile = await fs.readFile('proxy_list.csv');

// Convert CSV string into rows:
const data = await csv.parse(csvFile);
```

The data object is an `Array` that contains each row as `Array`.

We can loop over all these rows using the `map` function.

Note that in the loop, we will call the get method of Axios to call the same URL, each time with a different proxy.

The `get` method of Axios is `async`. This means that we can not call the `map` function of `data` directly.

Instead, we need to use the `Promise` object as follows:

```JavaScript
await Promise.all(data.map(async (item) => {
       // More async code here
    }));
```

It is time to create the `proxy` object. The structure will be as explained in the earlier section.

```javascript
// Create the Proxy object:
proxy_no_auth = {
  host: item[0],
  port: item[1]
};
```

Above lines convert the data from `[ '20.94.229.106', '80' ]` format to `{ host: '20.94.229.106', port: '80' }`format.

Next, call the `get` method and send the proxy object.

```javascript
const url = 'https://httpbin.org/ip';
const response = await axios.get(url, {
  proxy: proxy_no_auth
});
```

For the complete code, please see the [rotating_proxies.js](rotating_proxies.js) file.
