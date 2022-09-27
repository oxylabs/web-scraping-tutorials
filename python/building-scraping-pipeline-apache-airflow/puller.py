from pprint import pprint
from bootstrap import queue, client

queue_item = queue.pull()
if not queue_item:
    print('No jobs left in the queue, exiting')
    exit(0)

if not client.is_status_done(queue_item['job_id']):
    queue.touch(queue_item['job_id'])
    print('Job is not yet finished, skipping')
    exit(0)

content_list = client.fetch_content_list(queue_item['job_id'])
if content_list is None:
    print('Job no longer exists in oxy')
    queue.delete(queue_item['job_id'])
    exit(0)

queue.complete(queue_item['job_id'])

for content in content_list:
    pprint(content)