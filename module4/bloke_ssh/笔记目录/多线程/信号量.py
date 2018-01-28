#!/usr/bin/env python
# coding=utf-8
# Author: bloke

from threading import Thread, BoundedSemaphore, currentThread
import time

sema = BoundedSemaphore(value=2)
def run():
    """
    第三个线程会报错，这里超时时间为0.5s，因为前两个线程需要在1s之后才可以调用release()方法，
    所以在等待其他线程调用release()方法时超时，导致第三个线程调用acquire()方法失败，
    信号量内部计数器没有减少，但是之后又去调用release()方法，计数器数值超出设定界限，所以抛出ValueError
    """
    sema.acquire(timeout=0.5)
    print('Run....[ %s ]' % currentThread().getName())
    time.sleep(1)
    try:
        sema.release()
    except ValueError as e:
        print('Error:', e)

threads = []
for i in range(3):
    t = Thread(target=run)
    t.start()
    threads.append(t)

for item in threads:
    item.join()









