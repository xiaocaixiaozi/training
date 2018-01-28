#!/usr/bin/env python
# coding=utf-8
# Author: bloke

from multiprocessing import Process, Pipe
import os

def sub(left_conn):
    left_conn.send('Child pid: %s, Parent pid: %s.' % (os.getpid(), os.getppid()))

if __name__ == '__main__':
    left_conn, right_conn = Pipe()
    p = Process(target=sub, args=(left_conn,))
    p.start()
    p.join()
    print(right_conn.recv())







