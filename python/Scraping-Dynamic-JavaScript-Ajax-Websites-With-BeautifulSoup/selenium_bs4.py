from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
# update executable_path as required
driver = Chrome(executable_path='c:/driver/chromedriver.exe')

driver.get('https://quotes.toscrape.com/js/')

try:
    soup = BeautifulSoup(driver.page_source, "lxml")
    # print first author
    author_element = soup.find("small", class_="author")
    print(author_element.text)

    # print all authors
    all_author_elements = soup.find_all("small", class_="author")
    for element in all_author_elements:
        print(element.text)
finally:
    # always close the browser
    driver.quit()
