#!/usr/bin/env python
# coding=utf-8
# Author: bloke

from multiprocessing import Lock, Process
import os

def run(lock, n):
    with lock:
        print('Process... [%s: %s]' % (n, os.getpid()))

if __name__ == '__main__':
    lock = Lock()
    plist = []
    for i in range(10):
        p = Process(target=run, args=(lock, i))
        p.start()
    for item in plist:
        item.join()



