from bs4 import BeautifulSoup

with open('index.html', 'r') as f:
    contents = f.read()
    soup = BeautifulSoup(contents, features="html.parser")

    for child in soup.descendants:
        if child.name:
            print(child.name)