from bootstrap import queue, client

jobs = client.create_jobs([
    'https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html',
    'https://books.toscrape.com/catalogue/sharp-objects_997/index.html',
    'https://books.toscrape.com/catalogue/soumission_998/index.html',
    'https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html',
    'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html',
])

for job in jobs['queries']:
    queue.push(job['id'])
    print('job id: %s' % job['id'])