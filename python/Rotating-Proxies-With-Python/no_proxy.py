import requests

response = requests.get('https://ip.oxylabs.io/ip')
print(response.text)
