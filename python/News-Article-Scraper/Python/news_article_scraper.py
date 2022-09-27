from bs4 import BeautifulSoup
import requests
import csv


def parse_sitemap() -> list:
    response = requests.get("https://www.example.com/sitemap.xml")
    if response.status_code != 200:
        return None
    xml_as_str = response.text

    soup = BeautifulSoup(xml_as_str, "lxml")
    loc_elements = soup.find_all("loc")
    links = []
    for loc in loc_elements:
        links.append(loc.text)

    print(f'Found {len(links)} links')
    return links


def parse_articles(links: list):
    s = requests.Session()
    with open("news.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=['Heading', 'Body'])
        writer.writeheader()
        for link in links:
            response = s.get(link)
            soup = BeautifulSoup(response.text, "lxml")
            heading = soup.select_one('h1').text
            para = []
            for p in soup.select('.complete-story p'):
                para.append(p.text)
            body = '\n'.join(para)
            writer.writerow({'Heading': heading,
                             'Body': body
                             })


if __name__ == '__main__':
    links = parse_sitemap()
    parse_articles(links)
