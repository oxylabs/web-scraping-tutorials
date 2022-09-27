from bs4 import BeautifulSoup
import pandas as pd

with open('index.html', 'r') as f:
    contents = f.read()

    soup = BeautifulSoup(contents, features="html.parser")
    results = soup.find_all('li')

    df = pd.DataFrame({'Names': results})
    df.to_csv('names.csv', index=False, encoding='utf-8')