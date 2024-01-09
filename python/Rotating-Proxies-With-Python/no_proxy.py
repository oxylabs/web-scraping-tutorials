import requests

response = requests.get('https://ip.oxylabs.io/location')
print(response.text)
