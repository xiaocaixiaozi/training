#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import queue
import threading
import time

# q = queue.Queue()     # FIFO
# q = queue.LifoQueue(maxsize=3)    # LIFO
q = queue.PriorityQueue()   # Priority
threads = []
queue_num = 5

def worker():
    while True:
        data = q.get()
        if data[1] is None:
            break
        print('Get:', data)
        q.task_done()
        time.sleep(1)

for thread in range(2):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for n in range(queue_num):
    q.put((n, 'Item_%s' % n))
    print('Put:', 'Item_%s' % n)

q.join()

for i in range(queue_num):
    q.put((0, None))

for t in threads:
    t.join()

