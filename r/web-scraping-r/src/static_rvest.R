library(rvest)
library(dplyr)

httr::set_config(httr::user_agent("Mozilla/5.0 (Macintosh; Chrome/96.0.4664.45"))

link = "https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes"
df = read_html(link) %>% 
        html_element("table.sortable") %>%
        html_table(header = FALSE)

# take column names from second row
names(df) <- df[2,]
# drop first two rows
df = df[-1:-2,]
View(df)


