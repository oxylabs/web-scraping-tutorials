library(rvest)
library(httr)
library(jsonlite)

url <- "https://quotes.toscrape.com/api/quotes?page=1"
page<-read_html(GET(url, timeout(10)))
jsontext <- page %>% html_element("p")  %>% html_text()
r_object <- jsontext %>% fromJSON()
print(r_object$quotes)
