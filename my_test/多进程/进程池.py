#!/usr/bin/env python
# coding=utf-8
# Author: bloke

from multiprocessing import Pool
import os
import time

def run(n):
    time.sleep(1)
    print('In the child process: %s [%s]' % (n, os.getpid()))
    return n

def run_exit(m):
    print('End...%s [%s]' % (m, os.getpid()))

if __name__ == '__main__':
    pool = Pool()
    for i in range(8):
        # callback回调函数，接受一个参数，参数为run执行的返回结果
        pool.apply_async(run, args=(i,), callback=run_exit)

    pool.close()    # close 或 terminate 必须在join之前调用
    pool.join()



