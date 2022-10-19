import requests
from bs4 import BeautifulSoup

for y in list_comparison:
    try:
        print("Scraping: " + y[0])
        html = requests.request("get", y[0])
        soup = BeautifulSoup(html.text)

        try:
            metatitle = (soup.find("title")).get_text()
        except Exception:
            metatitle = ""

        try:
            metadescription = soup.find("meta", attrs={"name": "description"})["content"]
        except Exception:
             metadescription = ""

        try:
            h1 = soup.find("h1").get_text()
        except Exception:
            h1 = ""

        paragraph = [a.get_text() for a in soup.find_all('p')]
        text_length = sum(len(a) for a in paragraph)
        text_counter = sum(a.lower().count(keyword) for a in paragraph)
        metatitle_occurrence = keyword in metatitle.lower()
        h1_occurrence = keyword in h1.lower()
        metatitle_equal = metatitle == y[1]        
        y.extend([metatitle, metatitle_equal, metadescription, h1, paragraph, text_length, text_counter, metatitle_occurrence, h1_occurrence])

    except Exception as e:
        print(e)
        y.extend(["No data"]*9)