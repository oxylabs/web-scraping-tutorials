import csv
import aiohttp
import asyncio

CSV_FILENAME = 'proxies.csv'
URL_TO_CHECK = 'https://ip.oxylabs.io'
TIMEOUT_IN_SECONDS = 10


async def check_proxy(url, proxy):
    try:
        session_timeout = aiohttp.ClientTimeout(
            total=None, sock_connect=TIMEOUT_IN_SECONDS, sock_read=TIMEOUT_IN_SECONDS
        )
        async with aiohttp.ClientSession(timeout=session_timeout) as session:
            async with session.get(
                url, proxy=proxy, timeout=TIMEOUT_IN_SECONDS
            ) as resp:
                print(await resp.text())
    except Exception as error:
        print('Proxy responded with an error: ', error)
        return


async def main():
    tasks = []
    with open(CSV_FILENAME) as open_file:
        reader = csv.reader(open_file)
        for csv_row in reader:
            task = asyncio.create_task(check_proxy(URL_TO_CHECK, csv_row[0]))
            tasks.append(task)

    await asyncio.gather(*tasks)


asyncio.run(main())
