from bs4 import BeautifulSoup

with open('index.html', 'r') as f:
    contents = f.read()
    soup = BeautifulSoup(contents, features="html.parser")

    for tag in soup.find_all('li'):
        print(tag.text)