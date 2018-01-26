#!/usr/bin/env python
# coding=utf-8
# Author: bloke

from threading import Timer, Thread
import os

def run(name):
    print('Hello, My name is %s, My pid is %s.' % (name, os.getpid()))

t = Timer(3, run, args=('bloke',))  # 3s后执行run函数
t.start()




