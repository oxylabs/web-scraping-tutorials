import requests
import pandas as pd


keyword = "<your_keyword>"

payload = {
    "source": "SEARCH_ENGINE_search",
    "domain": "com",
    "query": keyword,
    "parse": "true",
}

response = requests.request(
    "POST",
    "https://realtime.oxylabs.io/v1/queries",
    auth=("<your_username>", "<your_password>"),
    json=payload,
)

list_comparison = [
    [x["url"], x["title"]]
    for x in response.json()["results"][0]["content"]["results"]["organic"]
]

print(list_comparison)
