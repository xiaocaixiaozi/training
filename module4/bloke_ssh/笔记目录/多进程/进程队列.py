#!/usr/bin/env python
# coding=utf-8
# Author: bloke

from multiprocessing import Process, Queue
import os
import time

def the_get(q):
    print('Size:', q.qsize())
    print(q.get())

def run(q):
    q.put('Current pid: %s' % os.getpid())

if __name__ == '__main__':
    q = Queue()
    plist = []
    pplist = []
    for i in range(10):
        p = Process(target=run, args=(q,))
        p.start()
        plist.append(p)
    for l in range(10):
        time.sleep(1)
        pp = Process(target=the_get, args=(q,))
        pp.start()
        pplist.append(pp)
    for item in plist:
        item.join()
    for itemm in pplist:
        itemm.join()
    print(q.empty())

