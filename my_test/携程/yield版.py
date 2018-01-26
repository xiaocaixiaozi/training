#!/usr/bin/env python
# coding=utf-8
# Author: bloke

def one():
    while True:
        print('In the first func.')
        name = yield
        print('name:', name)

def two():
    a.__next__()
    for i in range(5):
        print('In the second func.')
        a.send('bloke_%s' % i)

if __name__ == '__main__':
    a = one()
    two()



