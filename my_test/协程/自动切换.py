#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import gevent


def one():
    print('one...')
    gevent.sleep(2)
    print('one... again')

def two(name):
    print('%s...' % name)
    gevent.sleep(1)
    print('%s... again' % name)

def three():
    print('three...')
    gevent.sleep(0.1)
    print('three... again')

gevent.joinall([
    gevent.spawn(one),
    gevent.spawn(two, ('two',)),
    gevent.spawn(three)
])







