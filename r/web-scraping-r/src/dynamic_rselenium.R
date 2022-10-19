# install.packages("RSelenium")
# install.packages("dplyr")

library(RSelenium)
library(dplyr)

# Method 1
# Install chromedriver 
# Documentation at https://cran.r-project.org/web/packages/RSelenium/RSelenium.pdf page 16

rD <- rsDriver(browser="chrome", port=9511L, verbose=F)
remDr <- rD[["client"]]

# Method 2
# Run the following from terminal. Docker required.
# docker pull selenium/standalone-firefox
# docker run -d -p 4445:4444 selenium/standalone-firefox
# Run 
# remDr <- remoteDriver(
#   remoteServerAddr = "localhost",
#   port = 4445L,
#   browserName = "firefox"
# )
# remDr$open()

remDr$navigate("https://books.toscrape.com/")
remDr$getCurrentUrl()

titleElements <- remDr$findElements(using = "xpath", "//article//img")
titles <- sapply(titleElements, function(x){x$getElementAttribute("alt")[[1]]})
pricesElements <- remDr$findElements(using = "xpath", "//*[@class='price_color']")
prices <-  sapply(pricesElements, function(x){x$getElementText()[[1]]})
stockElements <- remDr$findElements(using = "xpath", "//*[@class='instock availability']")
stocks <-  sapply(stockElements, function(x){x$getElementText()[[1]]})

df <- data.frame(titles, prices, stocks)
remDr$close()


write.csv(df, "./books_selenium.csv")

