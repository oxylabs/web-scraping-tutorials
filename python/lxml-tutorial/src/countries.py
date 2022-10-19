import requests
from lxml import html

response = requests.get('https://en.wikipedia.org/wiki/List_of_countries_by_population_in_2010')

tree = html.fromstring(response.text)
countries = tree.xpath('//span[@class="flagicon"]')
print()
for country in countries:
    flag = country.xpath('./img/@src')[0]
    country = country.xpath('./following-sibling::a/text()')[0]
    print(country, flag)

# countries = tree.xpath('//span[@class="flagicon"]')
# for country in countries:
#     print(country.xpath('./following-sibling::a/text()')[0])
