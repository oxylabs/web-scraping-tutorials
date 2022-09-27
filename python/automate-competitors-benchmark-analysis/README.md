# How to Automate Competitors’ & Benchmark Analysis With Python

- [Using Oxylabs’ solution to retrieve the SERPs results](#using-oxylabs-solution-to-retrieve-the-serps-results)
- [Scraping URLs of the top results](#scraping-urls-of-the-top-results)
- [Obtaining the off-page metrics](#obtaining-the-off-page-metrics)
- [Obtaining the Page Speed metrics](#obtaining-the-page-speed-metrics)
- [Converting Python list into a dataframe and exporting it as an Excel file](#converting-python-list-into-a-dataframe-and-exporting-it-as-an-excel-file)

Doing competitors’ or benchmark analysis for SEO can be a burdensome task as it requires taking into account many factors which usually are extracted from different data sources. 

The purpose of this article is to help you automate the data extraction processes as much as possible. After learning how to do this, you can dedicate your time to what matters: the analysis itself and coming up with actionable insights to strategize.

For a detailed explanation, see our [blog post](https://oxy.yt/erEh).

## Using Oxylabs’ solution to retrieve the SERPs results

```python
import requests

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
```

Viewing the results:

```python
>>> print(list_comparison)
[
    ["https://example.com/result/example-link", "Example Link - Example"],
    ["https://more-examples.net", "Homepage - More Examples"],
    ["https://you-searched-for.com/query=your_keyword", "You Searched for 'your_keyword'. Analyze your search now!"],
]
```

## Scraping URLs of the top results

```python
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
```

## Obtaining the off-page metrics

```python
import time
from mozscape import Mozscape

client = Mozscape("<MOZ username>", "<MOZ password>")

for y in list_comparison:
    try:
        print("Getting MOZ results for: " + y[0])
        domainAuthority = client.urlMetrics(y[0])
        y.extend([domainAuthority["ueid"], domainAuthority["uid"], domainAuthority["pda"]])
    except Exception as e:
        print(e)
        time.sleep(10)  # Retry once after 10 seconds.
        domainAuthority = client.urlMetrics(y[0])
        y.extend([domainAuthority["ueid"], domainAuthority["uid"], domainAuthority["pda"]])
```

## Obtaining the Page Speed metrics

```python
import json

pagespeed_key = "<your page speed key>"


for y in list_comparison:
    try:

        print("Getting results for: " + y[0])
        url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=" + y[0] + "&strategy=mobile&locale=en&key=" + pagespeed_key
        response = requests.request("GET", url)
        data = response.json() 

        overall_score = data["lighthouseResult"]["categories"]["performance"]["score"] * 100
        fcp = data["loadingExperience"]["metrics"]["FIRST_CONTENTFUL_PAINT_MS"]["percentile"]/1000
        fid = data["loadingExperience"]["metrics"]["FIRST_INPUT_DELAY_MS"]["percentile"]/1000
        lcp = data["loadingExperience"]["metrics"]["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"]
        cls = data["loadingExperience"]["metrics"]["CUMULATIVE_LAYOUT_SHIFT_SCORE"]["percentile"]/100



        y.extend([fcp, fid, lcp, cls, overall_score])

    except Exception as e:
        print(e)
        y.extend(["No data", "No data", "No data", "No data", overall_score])
```

## Converting Python list into a dataframe and exporting it as an Excel file

```python
import pandas as pd

df = pd.DataFrame(list_comparison)
df.columns = ["URL","Metatitle SERPs", "Metatitle Onpage","Metatitle Equal", "Metadescription", "H1", "Paragraphs", "Text Length", "Keyword Occurrences Paragraph", "Metatitle Occurrence", "Metadescription Occurrence", "Equity Backlinks MOZ", "Total Backlinks MOZ", "Domain Authority", "FCP", "FID","LCP","CLS","Overall Score"]
df.to_excel('<filename>.xlsx', header=True, index=False)
```

If you wish to find out more, see our [blog post](https://oxy.yt/erEh).
