import aiohttp 
import asyncio
import csv
import re
import time

def get_links():
    links = []
    with open("links.csv", "r") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            links.append(row[0])

    return links

async def get_response(session, url):
    async with session.get(url) as resp:
        text = await resp.text()
        
        exp = r'(<title>).*(<\/title>)'
        return re.search(exp, text,flags=re.DOTALL).group(0)

async def main():
    start_time = time.time()
    async with aiohttp.ClientSession() as session:

        tasks = []
        for url in get_links():
            tasks.append(asyncio.create_task(get_response(session, url)))

        results = await asyncio.gather(*tasks)
        for result in results:
            print(result)

    print(f"{(time.time() - start_time):.2f} seconds")


asyncio.run(main())