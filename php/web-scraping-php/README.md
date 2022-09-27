# Web Scraping With PHP 

[<img src="https://img.shields.io/static/v1?label=&message=PHP&color=brightgreen" />](https://github.com/topics/php) [<img src="https://img.shields.io/static/v1?label=&message=Web%20Scraping&color=important" />](https://github.com/topics/web-scraping) 

- [Installing Prerequisites](#installing-prerequisites)
- [Making an HTTP GET request](#making-an-http-get-request)
- [Web scraping in PHP with Goutte](#web-scraping-in-php-with-goutte)
- [Web scraping with Symfony Panther](#web-scraping-with-symfony-panther)

PHP is a general-purpose scripting language and one of the most popular options for web development. For example, WordPress, the most common content management system to create websites, is built using PHP.

PHP offers various building blocks required to build a web scraper, although it can quickly become an increasingly complicated task. Conveniently, there are many open-source libraries that can make web scraping with PHP more accessible.

This article will guide you through the step-by-step process of writing various PHP web scraping routines that can extract public data from static and dynamic web pages

For a detailed explanation, see our [blog post](https://oxy.yt/Jr3d).

## Installing Prerequisites

```sh
# Windows
choco install php
choco install composer
```

or 

```sh
# macOS
brew install php
brew install composer
```

## Making an HTTP GET request

```php
<?php
$html = file_get_contents('https://books.toscrape.com/');
echo $html;
```

## Web scraping in PHP with Goutte

```sh
composer init --no-interaction --require="php >=7.1"
composer require fabpot/goutte
composer update
```

```php
<?php
require 'vendor/autoload.php';
use Goutte\Client;
$client = new Client();
$crawler = $client->request('GET', 'https://books.toscrape.com');
echo $crawler->html();
```

### Locating HTML elements via CSS Selectors

```php
echo $crawler->filter('title')->text(); //CSS
echo $crawler->filterXPath('//title')->text(); //XPath

```

### Extracting the elements

```php
function scrapePage($url, $client){
    $crawler = $client->request('GET', $url);
    $crawler->filter('.product_pod')->each(function ($node) {
            $title = $node->filter('.image_container img')->attr('alt');
            $price = $node->filter('.price_color')->text();
            echo $title . "-" . $price . PHP_EOL;
        });
    }
```



### Handling pagination

```php
function scrapePage($url, $client, $file)
{
   //...
  // Handling Pagination
    try {
        $next_page = $crawler->filter('.next > a')->attr('href');
    } catch (InvalidArgumentException) { //Next page not found
        return null;
    }
    return "https://books.toscrape.com/catalogue/" . $next_page;
}

```

### Writing Data to CSV

```php
function scrapePage($url, $client, $file)
{
    $crawler = $client->request('GET', $url);
    $crawler->filter('.product_pod')->each(function ($node) use ($file) {
        $title = $node->filter('.image_container img')->attr('alt');
        $price = $node->filter('.price_color')->text();
        fputcsv($file, [$title, $price]);
    });
    try {
        $next_page = $crawler->filter('.next > a')->attr('href');
    } catch (InvalidArgumentException) { //Next page not found
        return null;
    }
    return "https://books.toscrape.com/catalogue/" . $next_page;
}

$client = new Client();
$file = fopen("books.csv", "a");
$nextUrl = "https://books.toscrape.com/catalogue/page-1.html";

while ($nextUrl) {
    echo "<h2>" . $nextUrl . "</h2>" . PHP_EOL;
    $nextUrl = scrapePage($nextUrl, $client, $file);
}
fclose($file);
```



## Web scraping with Symfony Panther

```sh
composer init --no-interaction --require="php >=7.1" 
composer require symfony/panther
composer update

brew install chromedriver
```

### Sending HTTP requests with Panther

```php
<?php
require 'vendor/autoload.php';
use \Symfony\Component\Panther\Client;
$client = Client::createChromeClient();
$client->get('https://quotes.toscrape.com/js/');
```

### Locating HTML elements via CSS Selectors

```php
    $crawler = $client->waitFor('.quote');
    $crawler->filter('.quote')->each(function ($node) {
        $author = $node->filter('.author')->text();
        $quote = $node->filter('.text')->text();
       echo $autor." - ".$quote
    });
```

### Handling pagination

```php
while (true) {
    $crawler = $client->waitFor('.quote');
…
    try {
        $client->clickLink('Next');
    } catch (Exception) {
        break;
    }
}
```

### Writing data to a CSV file

```php
$file = fopen("quotes.csv", "a");
while (true) {
    $crawler = $client->waitFor('.quote');
    $crawler->filter('.quote')->each(function ($node) use ($file) {
        $author = $node->filter('.author')->text();
        $quote = $node->filter('.text')->text();
        fputcsv($file, [$author, $quote]);
    });
    try {
        $client->clickLink('Next');
    } catch (Exception) {
        break;
    }
}
fclose($file);
```



If you wish to find out more about web scraping with PHP, see our [blog post](https://oxy.yt/Jr3d).
