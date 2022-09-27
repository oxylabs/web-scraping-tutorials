# Building a Web Scraper in Golang

[<img src="https://img.shields.io/static/v1?label=&message=go&color=brightgreen" />](https://github.com/topics/go) [<img src="https://img.shields.io/static/v1?label=&message=Web%20Scraping&color=important" />](https://github.com/topics/web-scraping)
- [Installing Go](#installing-go)
- [Parsing HTML with Colly](#parsing-html-with-colly)
- [Handling pagination](#handling-pagination)
- [Writing data to a CSV file](#writing-data-to-a-csv-file)

Web scraping is an automated process of data extraction from a website. As a tool, a web scraper collects and exports data to a more usable format (JSON, CSV) for further analysis. Building a scraper could be complicated, requiring guidance and practical examples. A vast majority of web scraping tutorials concentrate on the most popular scraping languages, such as JavaScript, PHP, and, more often than not – Python. This time let’s take a look at Golang.

Golang, or Go, is designed to leverage the static typing and run-time efficiency of C and usability of Python and JavaScript, with added features of high-performance networking and multiprocessing. It’s also compiled and excels in concurrency, making it quick.

This article will guide you an overview of the process of writing a fast and efficient Golang web scraper.

For a detailed explanation, [see this blog post](https://oxy.yt/IrPZ). 

## Installing Go

```shell
# macOS
brew install go 

# Windows
choco install golang
```

## Parsing HTML with Colly

```shell
go mod init oxylabs.io/web-scraping-with-go
go get github.com/gocolly/colly

```



```go
//books.go

package main

import (
   "encoding/csv"
   "fmt"
   "log"
   "os"

   "github.com/gocolly/colly"
)
func main() {
   // Scraping code here
   fmt.Println("Done")
}
```

### Sending HTTP requests with Colly



```go
c := colly.NewCollector(
   colly.AllowedDomains("books.toscrape.com"),
)
c.OnRequest(func(r *colly.Request) {
   fmt.Println("Visiting", r.URL)
})
c.OnResponse(func(r *colly.Response) {
   fmt.Println(r.StatusCode)
})
```

### Locating HTML elements via CSS selector

```go
func main() {
   c := colly.NewCollector(
colly.AllowedDomains("books.toscrape.com"),
   )

   c.OnHTML("title", func(e *colly.HTMLElement) {
      fmt.Println(e.Text)
   })

   c.OnResponse(func(r *colly.Response) {
      fmt.Println(r.StatusCode)
   })

   c.OnRequest(func(r *colly.Request) {
      fmt.Println("Visiting", r.URL)
   })

   c.Visit("https://books.toscrape.com/")
}
```

### Extracting the HTML elements

![](https://oxylabs.io/blog/images/2021/12/book_container-1.png)

```go
type Book struct {
    Title string
    Price string
}
c.OnHTML(".product_pod", func(e *colly.HTMLElement) {
    book := Book{}
    book.Title = e.ChildAttr(".image_container img", "alt")
    book.Price = e.ChildText(".price_color")
    fmt.Println(book.Title, book.Price)
})
```

## Handling pagination

```go
c.OnHTML(".next > a", func(e *colly.HTMLElement) {
    nextPage := e.Request.AbsoluteURL(e.Attr("href"))
    c.Visit(nextPage)
})
```

## Writing data to a CSV file

```go
func crawl() {
	file, err := os.Create("export2.csv")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	writer := csv.NewWriter(file)
	defer writer.Flush()
	headers := []string{"Title", "Price"}
	writer.Write(headers)

	c := colly.NewCollector(
		colly.AllowedDomains("books.toscrape.com"),
	)

	c.OnRequest(func(r *colly.Request) {
		fmt.Println("Visiting: ", r.URL.String())
	})

	c.OnHTML(".next > a", func(e *colly.HTMLElement) {
		nextPage := e.Request.AbsoluteURL(e.Attr("href"))
		c.Visit(nextPage)
	})

	c.OnHTML(".product_pod", func(e *colly.HTMLElement) {
		book := Book{}
		book.Title = e.ChildAttr(".image_container img", "alt")
		book.Price = e.ChildText(".price_color")
		row := []string{book.Title, book.Price}
		writer.Write(row)
	})

	startUrl := fmt.Sprintf("https://books.toscrape.com/")
	c.Visit(startUrl)
}

```

#### Run the file

```shell
go run books.go
```



If you wish to find out more about web scraping with Go, see our [blog post](https://oxy.yt/IrPZ).
