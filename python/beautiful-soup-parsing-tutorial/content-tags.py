from bs4 import BeautifulSoup

with open('index.html', 'r') as f:
    contents = f.read()
    soup = BeautifulSoup(contents, features="html.parser")

    print(soup.h2)
    print(soup.p)
    print(soup.li)