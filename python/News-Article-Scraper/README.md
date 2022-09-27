# News Article Scraper
[<img src="https://img.shields.io/static/v1?label=&message=Python&color=brightgreen" />](https://github.com/topics/python) [<img src="https://img.shields.io/static/v1?label=&message=JavaScript&color=blue" />](https://github.com/topics/javascript) [<img src="https://img.shields.io/static/v1?label=&message=web%20scraping&color=important" />](https://github.com/topics/web-scraping) [<img src="https://img.shields.io/static/v1?label=&message=news%20article%20scraping&color=blueviolet" />](https://github.com/topics/news-article-scraping)

## Table of Contents

- [The Overall Approach](#the-overall-approach)
- [Packages Required](#packages-required)
  - [Python Packages](#python-packages)
  - [JavaScript Packages](#javascript-packages)
- [Gathering URLs of News Articles](#gathering-urls-of-news-articles)
  - [What Is a Site Map](#what-is-a-site-map)
  - [Extracting Articles Links Using Python](#extracting-articles-links-using-python)
  - [Extracting Articles Links Using JavaScript](#extracting-articles-links-using-javascript)
  - [What If There Is No Sitemap?](#what-if-there-is-no-sitemap)
- [Parsing News Articles](#parsing-news-articles)
  - [Extracting Article Text Using Python](#extracting-article-text-using-python)
  - [Extracting Article Text Using JavaScript](#extracting-article-text-using-javascript)

News article scraper is a specific kind of scraper that specializes in news articles. Usually, web scraping involves extracting specific data from web pages. 

For example, for a data gathering task of products, the web scraping script will be looking for specific information. Such script will parse the product pages and extract information such as price, availability, etc. This will involve creating the selectors using XPath or CSS Selectors. These selectors will help locate specific information from the page and extract multiple data points.

The news article scrapers are a bit different. The purpose of this data gathering technique is to collect a single data point, and that is a huge block of text. 

This block of text is the news article body. The headline and date published may also be collected, but usually, it is the text which is used for various purposes. One such use case is Elasticsearch. Elasticsearch is a search and analytics tool and works well with unstructured data, so the article text can be consumed by Elasticsearch. 

This article will discuss various ways of web scraping news articles using Python and JavaScript. Even though no prior understanding of web scraping is expected, [this article can help you learn web scraping using Python](https://github.com/oxylabs/Python-Web-Scraping-Tutorial).

## The Overall Approach

There are several parts to handling the challenge. The first part of the challenge is to write the crawler that can extract links to the individual articles from news sites. The second part of the challenge is to extract the text from each page.

Finally, the data will be exported to a file or a database. For some use cases, the data is exported in JSON format, while for others, CSV is more suited. 

## Packages Required

The first step is to prepare the environment. This article covers both Python and JavaScript. You may jump to the section related to your choice of language.

### Python Packages

The most common packages for creating any web crawler are Requests and Beautiful Soup 4.

These packages can be installed using the `pip install` command. Open the terminal, and create a virtual environment (optional but recommended). You can use [virtualenv package](https://pypi.org/project/virtualenv/) ,  [Anaconda distribution](https://docs.anaconda.com/anaconda/navigator/tutorials/manage-environments/), or Python's [venv module](https://docs.python.org/3/tutorial/venv.html) to create virtual environments.

Activate the virtual environment and run the following command. Note that if you are not working with a virtual environment, add `--user` to the following command.

```python
pip install beautifulsoup4 requests
```

This will install both the Requests and Beautiful Soup packages. In the later section of this article, we will discuss other packages and their usage.

To export the data to JSON, CSV, etc., the `csv` and `json` can be used, which are part of the Python standard library. Optionally, `pandas` can be also be used for this task. 

Important: Note that version 4 of [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) is being installed here. Earlier versions are now obsolete. 

### JavaScript Packages

Web scraping news articles with JavaScript requires [NodeJS](https://nodejs.org/en/). This is a runtime that can run JavaScript code without a browser.  We will be using Node.js Packages [axios](https://www.npmjs.com/package/axios) and [cheerio](https://www.npmjs.com/package/cheerio). 

Before installing these packages, install NodeJS first. NodeJS It can be downloaded from the [official download page](https://nodejs.org/en/download/). The installer for Windows and macOS can be downloaded from this page.

For Linux, `apt install` or a similar packaging tool depending on the flavor can be used.

```sh
sudo apt install nodejs	
```

Node Package Manager is also required to install the packages. This is bundled with Windows and macOS installers. For Linux, it can be installed using the `apt install` as follows:

```sh
sudo apt install npm
```

Once `npm` (Node Package Manager) is installed, navigate to the directory where you want to create the code files and initialize a project as follows:

```sh
npm init -y
```

Finally, run `npm install` to install the required packages.

```sh
npm install axios cheerio 
```

With this installation, the development environment is ready.

## Gathering URLs of News Articles

The first step of web scraping news articles is getting the URLs of these individual articles. There are two approaches to get these links:

- Parsing the sitemap XML to get the links
- Parsing a regular HTML page to get the links

This article will focus on writing the crawler using the sitemap. Parsing the page that contains links to articles as regular HTML can be easily done using the same approach. The minute differences are covered in the relevant sections.

### What Is a Site Map

A majority of the website use a site map (or sitemap) that lists the pages of that website. These sitemaps are usually in a specific XML format. These are meant for search engines to index the pages. As a result, most of the sites will keep the sitemaps updated.

If a sitemap is available, that is usually the best place, to begin with. To check if a site has a sitemap available, simply navigate to `sitemap.xml` at the root path.

The URL of the sitemap will look something like: `https://www.example.com/sitemap.xml`.  The sitemaps looks something likes this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <sitemap>
        <loc>https://www.example.com/newsindex.xml</loc>
    </sitemap>
    <sitemap>
        <loc>https://www.example.com/urlsitemapindex.xml</loc>
    </sitemap>
    <sitemap>
        <loc>https://www.example.com/imagesitemapindex.xml</loc>
    </sitemap>
</sitemapindex>
```



Note that as displayed here, this sitemap may links to other sitemaps. In this example, if we open `newsindex.xml`, the final structure will be something like this: 

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset>
    <url>
        <loc>https://www.example.com/link-to-news-1/</loc>
        <news:news>
            <news:publication_date>2021-06-24T16:28:01-08:00</news:publication_date>
            <news:title>This is the title of the news article 1</news:title>
            <news:keywords>keywords, for, search, appear, here</news:keywords>
        </news:news>
        <lastmod>2021-06-24T16:28:01-08:00</lastmod>
        <image:image>
            <image:loc>https://img.example.com/img/example-1.jpg</image:loc>
        </image:image>
    </url>
</urlset>
```

Every news article is listed in a separate set of `<url></url>`  tags. Note that this file contains the link to the actual news article page, and also the last modified date information.

Let's write code to extract this information.

### Extracting Articles Links Using Python

The first step is to retrieve the text of the sitemap.xml. This can be done using the Requests library's `get` method.

```python
response = requests.get("https://www.patrika.com/googlenewssitemap1.xml")
xml_as_str = response.text
```

Once the xml is available, the parsing can be handled by Beautiful soup. Note that it is the parser is explicitly set to `lxml`. 

```python
soup = BeautifulSoup(xml_as_str, "lxml")
```

Note that if you do not have lxml installed already, you can do that by running `pip install lxml`. 

Finally, Beautiful Soup's `find_all` method can be used to extract all the links, which are in the `loc` tag of the XML.

```python
loc_elements = soup.find_all("loc")
links = []
for loc in loc_elements:
    links.append(loc.text)
```

The complete code is in the [extract_article_links.py](code/Python/extract_article_links.py) file.



### Extracting Articles Links Using JavaScript

Web scraping the index page with JavaScript follows the same pattern as Python. The first step is to retrieve the text of the sitemap.xml. This can be done using the `axios` packages.

```javascript
url = `https://www.example.com/sitemap.xml`;
const response = await axios.get(url);
```

This response can then be parsed for querying using the `cheerio` package. Cheerio package's load method needs one additional parameter where the `xmlMode` is set to `true`. This ensures that the response is correctly read as `XML` and not HTML.

```javascript
const $ = cheerio.load(response.data, { xmlMode: true });
```

Now all the `loc` elements can be easily extracted. The `text()` can be used in `each` to create an array of all the links, as following:

```javascript
all_loc = $('loc')
all_loc.each(function () {
    links.push($(this).text())
})
console.log(links.length + ' links found.')
```

Effectively, we are building a JSON object. This object can be written to a `.json` file directly, or can be converted to a CSV format using the `json2csv` package.

The complete code is in the [extract_article_links.js](code/JavaScript/extract_article_links.js) file.

### What If There Is No Sitemap?

Some sites may choose to go without a sitemap. In such cases, this news article scraper needs to know the page that contains all the links to the stories. This page would be in HTML can sometimes be more than one page. This page can be parsed in the same way. The only thing that will change is the way the link is extracted. 

For example, in Python, the following line of code may change:

```python
loc_elements = soup.find_all("loc") # Update this to select the links
```

In JavaScript, you will have set `xmlMode` to `false` explicitly, or omit this optional parameter:

```javascript
const $ = cheerio.load(response.data); //treat as HTML, not XML
all_loc = $('loc'); // Update this to select the links
```

Also, the selector would need to be updated for the links. That's all!

## Parsing News Articles

In this step, we are going to perform the task of web scraping news articles. Now that we have the links to all the news articles, these links can be parsed to extract the required information.

Typically, if you are working on a task of data gathering of news articles, you would be looking at at least two key pieces of information—headline and body.

Getting the headline is easier. The title of the story is typically in a `<h1>` or a `<h2>` tag. This, of course, is going to vary for each website. For this article, we will work with the assumption that the heading is in the `<h1>` tag.

Similarly, the body of the news article is typically contained in a div, span, or a section tag with a class. In this example, the main story is in a div with following markup:

```html
<div id="storyArticle">
    <p>Paragraph 1 of the news article</p>
    <p>Paragraph 2 of the news article</p>
    ...
</div>
```

Almost all news sites follow a similar structure. The news sites have to rely on some kind of content management system. The result is that the markup is the same for all news articles. Also, the HTML tags used also follow the same pattern.

For our example, we are going to work with the above HTML.

All we have to do now is use `requests` (Python) or `axios` (JavaScript) to get the HTML string and then parse the HTML using BeautifulSoup (Python) or Cheerio (JavaScript).

### Extracting Article Text Using Python

The approach of extracting articles will be very similar. We will run a loop over all the links. You may want to use `requests.session` to speed up fetching the data.

```python
s = requests.Session()
for link in links: # processing links in a loop
    response = s.get(link) #using session object
```

Once the response is available, a BeautifulSoup object can be created to extract the heading and the body of the news article.

```python
soup = BeautifulSoup(response.text, "lxml")
heading = soup.select_one('h1').text # News Heading
body = soup.select_one('.complete-story').text
```

The above code will extract all the text from this div. However, if there is any other text, for example, image labels, those will also be extracted. For finer control, a loop can be run over all `<p>` tags to create a list.

```python
para = [] 
for p in soup.select('.complete-story p'):
	para.append(p.text)
```

At the end of this code block, the entire story will be in the list object `para`. This can be converted to a string object using the `join` method.

```python
body = '\n'.join(para) #Each paragraph separated with a new line
```

Finally, we can finish up news page scraping by exporting the data to CSV, JSON, or even saved to a database. Please see [news_article_scraper.py](code/Python/news_article_scraper.py) for the complete code.

### Extracting Article Text Using JavaScript

To extract the article text, simply run a loop over all the links. In this loop, use the axios to download the HTML.

```javascript
links.forEach(async function (story_link) {
    try {
        let story = await axios.get(story_link);
        // 
    } catch (error) {
        console.error('internal\n' + error)
    }
})
```

Once the story is available, we can again use Cheerio to load the HTML and extract the heading and body using CSS selectors.

```javascript
let story = await axios.get(story_link);
let $ = cheerio.load(story.data);
heading = $('h1').text()
body = $('.complete-story p').text()
```

Again, the last step of news page scraping is exporting the data. This data can be exported to CSV, JSON, or any other format based on the requirement.

See [news_article_scraper.js](code/JavaScript/news_article_scraper.js) for the complete code.
