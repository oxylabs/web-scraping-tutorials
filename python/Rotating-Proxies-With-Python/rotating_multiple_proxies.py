import csv

import requests
from requests.exceptions import ProxyError, ReadTimeout, ConnectTimeout

TIMEOUT_IN_SECONDS = 10
CSV_FILENAME = 'proxies.csv'

with open(CSV_FILENAME) as open_file:
    reader = csv.reader(open_file)
    for csv_row in reader:
        scheme_proxy_map = {
            'https': csv_row[0],
        }

        try:
            response = requests.get(
                'https://ip.oxylabs.io/ip',
                proxies=scheme_proxy_map,
                timeout=TIMEOUT_IN_SECONDS,
            )
        except (ProxyError, ReadTimeout, ConnectTimeout) as error:
            pass
        else:
            print(response.text)
