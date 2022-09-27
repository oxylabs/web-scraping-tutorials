from bs4 import BeautifulSoup
import requests


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


if __name__ == '__main__':
    links = parse_sitemap()
