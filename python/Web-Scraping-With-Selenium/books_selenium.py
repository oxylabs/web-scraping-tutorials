import pandas as pd
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

CHROME_DRIVER_PATH = 'c:/WebDrivers/chromedriver.exe'
HOMEPAGE = "http://books.toscrape.com"


def get_data(url, categories):
    browser_options = ChromeOptions()
    browser_options.headless = True

    driver = Chrome(executable_path=CHROME_DRIVER_PATH, options=browser_options)
    driver.get(url)
    driver.implicitly_wait(10)
    data = []
    for category in categories:
        humor = driver.find_element_by_xpath(f'//a[contains(text(),{category})]')
        humor.click()

        try:
            books = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.product_pod'))
            )
        except Exception as e:
            raise e

        for book in books:
            title = book.find_element_by_css_selector("h3 > a")
            price = book.find_element_by_css_selector(".price_color")
            stock = book.find_element_by_css_selector(".instock.availability")
            data.append({
                'title': title.get_attribute("title"),
                'price': price.text,
                'stock': stock.text,
                'Category': category
            })

        driver.get(url)

    driver.quit()
    return data


def export_csv(data):
    df = pd.DataFrame(data)
    # Apply transformations if needed
    df.to_csv("books_exported.csv", index=False)
    print(df)  # DEBUG


def main():
    data = get_data(url=HOMEPAGE, categories=["Humor", "Art"])
    export_csv(data)
    print('DONE')


if __name__ == '__main__':
    main()
