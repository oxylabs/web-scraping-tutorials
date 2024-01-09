import requests
from requests.exceptions import ProxyError, ReadTimeout, ConnectTimeout

PROXY = 'http://2.56.215.247:3128'
TIMEOUT_IN_SECONDS = 10

scheme_proxy_map = {
    'https': PROXY,
}
try:
    response = requests.get(
        'https://ip.oxylabs.io', proxies=scheme_proxy_map, timeout=TIMEOUT_IN_SECONDS
    )
except (ProxyError, ReadTimeout, ConnectTimeout) as error:
    print('Unable to connect to the proxy: ', error)
else:
    print(response.text)
