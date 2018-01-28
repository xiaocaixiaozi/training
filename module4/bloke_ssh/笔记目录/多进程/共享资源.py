#!/usr/bin/env python
# coding=utf-8
# Author: bloke

from multiprocessing import Process, Manager
import os

def run(d, l, n):
    d[n] = os.getpid()
    l.append(os.getpid())

if __name__ == '__main__':
    with Manager() as manager:
        d = manager.dict()
        l = manager.list()
        plist = []
        for i in range(5):
            p = Process(target=run, args=(d, l, i))
            p.start()
            plist.append(p)
        for item in plist:
            item.join()
        print(d)
        print(l)

