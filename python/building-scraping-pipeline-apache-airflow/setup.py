from bootstrap import queue

success = queue.setup()
if not success:
    exit(1)