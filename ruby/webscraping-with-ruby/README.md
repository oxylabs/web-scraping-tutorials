# Web Scraping With Ruby

[<img src="https://img.shields.io/static/v1?label=&message=Ruby&color=brightgreen" />](https://github.com/topics/ruby) [<img src="https://img.shields.io/static/v1?label=&message=Web%20Scraping&color=important" />](https://github.com/topics/web-scraping)

- [Installing Ruby](#installing-ruby)
- [Scraping static pages](#scraping-static-pages)
- [Scraping dynamic pages](#scraping-dynamic-pages)

Ruby is a time-tested, open-source programming language. Its first version was released in 1996, while the latest major iteration 3 was dropped in 2020. This article covers tools and techniques for web scraping with Ruby that work with the latest version 3.

We’ll begin with a step-by-step overview of scraping static public web pages first and shift our focus to the means of scraping dynamic pages. While the first approach works with most websites, it will not function with the dynamic pages that use JavaScript to render the content. To handle these sites, we’ll look at headless browsers.


For a detailed explanation, see our [blog post](https://oxy.yt/Dr5a).


## Installing Ruby

To install Ruby on **Windows**, run the following:

```batch
choco install ruby
```

To install Ruby on **macOS**, use a package manager such as [Homebrew](https://brew.sh/). Enter the following in the terminal:

```shell
brew install ruby
```

For **Linux**, use the package manager for your distro. For example, run the following for Ubuntu:

```shell
sudo apt install ruby-full
```

## Scraping static pages

In this section, we’ll write a web scraper that can scrape data from [https://books.toscrape.com](https://books.toscrape.com/). It is a dummy book store for practicing web scraping with static websites.

### Installing required gems

```shell
gem install httparty
gem install nokogiri
gem install csv
```

### Making an HTTP request

```ruby
require 'httparty'
response = HTTParty.get('https://books.toscrape.com/')
if response.code == 200
    puts response.body
else
    puts "Error: #{response.code}"
    exit
end
```

### Parsing HTML with Nokogiri

```ruby
require 'nokogiri'
document = Nokogiri::HTML4(response.body)
```

![](https://oxylabs.io/blog/images/2021/12/book_container.png)

```ruby
books = []
50.times do |i|
  url = "https://books.toscrape.com/catalogue/page-#{i + 1}.html"
  response = HTTParty.get(url)
  document = Nokogiri::HTML(response.body)
  all_book_containers = document.css('article.product_pod')

  all_book_containers.each do |container|
    title = container.css('.image_container > a > img').first['alt']
    price = container.css('.price_color').text.delete('^0-9.')
    availability = container.css('.availability').text.strip
    book = [title, price, availability]
    books << book
  end

end
```

### Writing scraped data to a CSV file

```ruby
require 'csv'
CSV.open('books.csv', 'w+',
         write_headers: true,
         headers: %w[Title Price Availability]) do |csv|

  50.times do |i|
    url = "https://books.toscrape.com/catalogue/page-#{i + 1}.html"
    response = HTTParty.get(url)
    document = Nokogiri::HTML(response.body)
    all_book_containers = document.css('article.product_pod')

    all_book_containers.each do |container|
      title = container.css('h3 a').first['title']
      price = container.css('.price_color').text.delete('^0-9.')
      availability = container.css('.availability').text.strip
      book = [title, price, availability]

      csv << book
    end
  end
end
```

## Scraping dynamic pages

### Required installation

```shell
gem install selenium-webdriver
gem install csv
```

### Loading a dynamic website

```ruby
require 'selenium-webdriver'

driver = Selenium::WebDriver.for(:chrome)
```

### Locating HTML elements via CSS selectors

```ruby
document = Nokogiri::HTML(driver.page_source)
```

![](https://oxylabs.io/blog/images/2021/12/quotes_to_scrape.png)

```ruby
quotes = []
quote_elements = driver.find_elements(css: '.quote')
quote_elements.each do |quote_el|
  quote_text = quote_el.find_element(css: '.text').attribute('textContent')
  author = quote_el.find_element(css: '.author').attribute('textContent')
  quotes << [quote_text, author]
end
```

### Handling pagination

```ruby
quotes = []
while true do
  quote_elements = driver.find_elements(css: '.quote')
  quote_elements.each do |quote_el|
    quote_text = quote_el.find_element(css: '.text').attribute('textContent')
    author = quote_el.find_element(css: '.author').attribute('textContent')
    quotes << [quote_text, author]
  end
  begin
    driver.find_element(css: '.next >a').click
  rescue
    break # Next button not found
  end
end
```

### Creating a CSV file

```ruby
require 'csv'

CSV.open('quotes.csv', 'w+', write_headers: true,
         headers: %w[Quote Author]) do |csv|
  quotes.each do |quote|
    csv << quote
  end
end
```

If you wish to find out more about web scraping with Ruby, see our [blog post](https://oxy.yt/Dr5a).
