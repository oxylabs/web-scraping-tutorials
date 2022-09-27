# How to Make HTTP Requests in Node.js With Fetch API

## What is Fetch API

Fetch API is an application programming interface for fetching network resources. It facilitates making HTTP requests such as GET, POST, etc. 

Fetch API supports new standards, such as Promise, resulting in cleaner code that doesn’t require callbacks.

The native support for the Fetch API exists in all major browsers. JavaScript developers rely on the node-fetch package for the server-side code. The package is wildly popular, with millions of downloads every week.

Node.js has released experimental support for the Fetch API with version 17.5. Since then, you can write your server-side JavaScript code that uses the Fetch API without installing a third-party library. To do so, run the following command:

```node
node --experimental-fetch your_code.js
```

## How to use Fetch API

For the following examples, a dummy website will be used as a target. As the Fetch API returns a Promise object, you can use the fetch-then syntax. To see Node Fetch in action, create a file using a code editor and enter the following lines of code:

```javascript
fetch('https://quotes.toscrape.com/random')
    .then((response) => response.text())
    .then((body) => {
        console.log(body);
    }); 
```

This code sends an HTTP GET request and prints the HTML.

To explain it further, the `fetch()` method returns a Promise object. The first `then()` extracts the text from the response, and the second `then()` prints the response HTML.

Save it as `quotes.js`, open the terminal, and run the following:

```node
node --experimental-fetch quotes.js
```

It'll print the HTML of the page. Additionally, it may also print a warning that Fetch is an experimental feature.

The same code for Node Fetch can also be written using the `async-await` syntax as follows:

```javascript
(async () => {
    const response = await fetch('https://quotes.toscrape.com/random');
    const body = await response.text();
    console.log(body);
})();
```

If you want to extend the code to create a web scraper, you can install a parser such as `Cheerio` and extract specific elements. The following example extracts a quote:

```javascript
const cheerio = require("cheerio");

fetch('https://quotes.toscrape.com/random')
    .then((response) => response.text())
    .then((body) => {
        const $ = cheerio.load(body);
        console.log($('.text').text());

    })
```

If you want to learn more about web scraping with JavaScript and `Node.js`, see this blog post.

## HTTP headers in Fetch API

Now, let's talk about the response headers. The response object contains all of the response headers in the `response.headers` collection. If you wish to print the response headers, you can do so as follows:

```javascript
const url = 'https://httpbin.org/get'
fetch(url)
    .then(response => {
        for(const pair of response.headers){
            console.log(`${pair[0]}: ${pair[1]}`); 
          }
        return response.text();
    }).then(data => {
        console.log(data);
    });
```

While running this code using Node.js, you’ll see all of the response headers as expected. However, things will be unexpectedly different when running in the browser. If a server you attempt to query has CORS headers enabled, your browser will limit the headers you can access for security reasons.

You’ll only be able access the following headers: `Cache-Control`, `Content-Language`, `Content-Type`, `Expires`, `Last-Modified`, and `Pragma`. Read more about it here.

It’s also possible to send custom request headers using the second parameter of `fetch()`, where various options can be set, including headers. The following example shows how to send a custom user-agent in the HTTP request:

```javascript
const url = 'https://httpbin.org/get';
fetch(url, {
    headers: {
        "User-Agent": "My User Agent",
    },
})
    .then((response) => response.json())
    .then(data => {
        console.log(data);
    })
```

As discussed in the next section, the second parameter can be used for additional functionality.

## Sending POST requests

The default request method used by the Fetch API is GET. However, it’s possible to send a POST request as follows:

```javascript
fetch(url, {method: “POST”})
```

Let’s practice sending some dummy data to a test website. You’ll need to convert the data you want to send in the HTTP POST request into a string:

```javascript
const url = 'https://httpbin.org/post'
const data = {
    x: 1920,
    y: 1080,
};
const customHeaders = {
    "Content-Type": "application/json",
}

fetch(url, {
    method: "POST",
    headers: customHeaders,
    body: JSON.stringify(data),
})
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
    });
```

Notice how to set `method: “Post"` and how to use `JSON.stringify(data)` to convert the data into a string.

Similarly, you can also use the HTTP methods such as `DELETE`, `PUT`, etc.

Exception handling
As the Node Fetch API returns a Promise object, you can use the `fetch - then - catch` convention to handle errors:

```javascript
fetch('https://invalid_url')
    .then((response) => response.text())
    .then((body) => {
        console.log(body);
    }).catch((error) => {
        console.error('error in execution', error);
    }); 
```

If you’re using the `async-await` syntax, you can handle errors with the `try - catch` block as follows:

```javascript
(async () => {
    try {
        const response = await fetch('https://invalid_url');
        const body = await response.text();
        console.log(body);
    } catch (error) {
        console.error(error);
    }
})();
```

## Axios vs Fetch API

Axios is a popular Node package for making HTTP `GET` and `POST` requests with ease. Make sure to check our tutorial on web scraping with JavaScript and Node.js to see a practical example of Axios.

To send a GET request, call the `get()` method as follows:

```javascript
const response = await axios.get(url);
```

Similarly, to send a POST request, call the `post()` method as follows:

```javascript
const response = await axios.post(url);
```

Let's take an example to see how the Node Fetch API differs from Axios. Send a `POST` request to https://httpbin.org/post with JSON data. The important things to note here are the following:

* JSON data.

* Custom request headers.

* The response will be in JSON format

Writing the same code using Axios and Fetch API will distinguish the differences. 

The following code uses Axios:

```javascript
const axios = require('axios');
const url = 'https://httpbin.org/post'
const data = {
    x: 1920,
    y: 1080,
};
const customHeaders = {
    "Content-Type": "application/json",
}
axios.post(url, data, {
    headers: customHeaders,
})
.then(({ data }) => {
    console.log(data);
})
.catch((error) => {
    console.error(error);
});
```

And the code below uses Fetch API:

```javascript
const url = 'https://httpbin.org/post'
const data = {
    x: 1920,
    y: 1080,
};
const customHeaders = {
    "Content-Type": "application/json",
}

fetch(url, {
    method: "POST",
    headers: customHeaders,
    body: JSON.stringify(data),
})
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
    })
    .catch((error) => {
        console.error(error);
    });
```

Both of these code snippets will produce the same output.

As evident from the examples above, here are the differences between Axios and Fetch API:

* Fetch API uses the `body` property of the request, while Axios uses the `data` property.

* Using Axios, JSON data can be sent directly, while Fetch API requires the conversion to a string.

* Axios can handle JSON directly. The Fetch API requires the `response.json()` method to be called first to get the response in JSON format.

* The response data variable name must be data in the case of Axios, while it can be anything in the case of Fetch API.

* Axios allows an easy way to monitor update progress using the progress event. There is no direct method in Fetch API.

* Fetch API does not support interceptors, while Axios does.

* Fetch API allows streaming of a response, while Axios doesn’t.
