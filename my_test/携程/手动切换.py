#!/usr/bin/env python
# coding=utf-8
# Author: bloke

from greenlet import greenlet

def one():
    print(1)
    second.switch()
    print(3)
    second.switch()

def two():
    print(2)
    first.switch()
    print(4)

first = greenlet(one)
second = greenlet(two)

first.switch()










