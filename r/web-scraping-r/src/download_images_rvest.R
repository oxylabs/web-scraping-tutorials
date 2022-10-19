library(rvest)
library(dplyr)

url = "https://en.wikipedia.org/wiki/Eiffel_Tower"
page <- read_html(url)
image_element <- page %>% html_element(".thumbborder")
image_url <- image_element %>% html_attr("src")
image_url <- url_absolute(image_url, url)


download.file(image_url, destfile = basename("paris.jpg"))
