#!/usr/bin/env python
# coding=utf-8
# Author: bloke

from multiprocessing import managers, Process
import os

'''
def sub_run():
    print('Parent pid:', os.getppid())
    print('Current pid:', os.getpid())

if __name__ == '__main__':
    processes = []
    for i in range(3):
        p = Process(target=sub_run)
        p.start()
        processes.append(p)

    for item in processes:
        item.join()
'''

from multiprocessing import Process, Queue

def f(q):
    q.put('X' * 10)

if __name__ == '__main__':
    queue = Queue()
    p = Process(target=f, args=(queue,))
    p.start()
    obj = queue.get()
    p.join()                    # this deadlocks
    print(obj)
