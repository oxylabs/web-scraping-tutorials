import csv
import re
import time
import requests

def get_links():
    links = []
    with open("links.csv", "r") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            links.append(row[0])

    return links

def get_response(session, url):
    with session.get(url) as resp:
        print('.', end='', flush=True)
        text = resp.text
        exp = r'(<title>).*(<\/title>)'
        return re.search(exp, text,flags=re.DOTALL).group(0)

def main():
    start_time = time.time()
    with requests.Session() as session:
        results = []
        for url in get_links():
            result = get_response(session, url)
            print(result)

    print(f"{(time.time() - start_time):.2f} seconds")

main()