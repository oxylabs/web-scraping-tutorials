import csv
import re
import time
import requests
from concurrent.futures import ThreadPoolExecutor

def get_links():
    links = []
    with open("links.csv", "r") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            links.append(row[0])

    return links

def get_response(url):
    resp = requests.get(url)
    print('.', end='', flush=True)
    text = resp.text
    
    exp = r'(<title>).*(<\/title>)'
    return re.search(exp, text, flags=re.DOTALL).group(0)

def main():
    start_time = time.time()
    links = get_links()

    with Pool(100) as p:
        results = p.map(get_response, links)
        
        for result in results:
            print(result)

    print(f"{(time.time() - start_time):.2f} seconds")