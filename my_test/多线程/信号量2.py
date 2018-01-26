#!/usr/bin/env python
# coding=utf-8
# Author: bloke

from threading import BoundedSemaphore, Thread, current_thread

sema = BoundedSemaphore()

def run():
    """
    with sema，相当于：
    sema.acquire()
    try:
        do something...
    finally:
        sema.release()
    """
    with sema:
        print('[ %s ]' % current_thread())

tlist = []
for i in range(3):
    t = Thread(target=run)
    t.start()
    tlist.append(t)
for item in tlist:
    item.join()





