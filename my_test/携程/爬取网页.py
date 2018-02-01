#!/usr/bin/env python
# coding=utf-8
# Author: bloke

from urllib import request
import time
import gevent
from gevent import monkey

monkey.patch_all()

def get_html(addr, num):
    data = request.urlopen(addr)
    with open('%s.html' % num, 'wb') as f:
        f.write(data.read())
    time.sleep(1)

one = 'http://www.cnblogs.com/alex3714/articles/8359303.html'
two = 'http://www.cnblogs.com/alex3714/articles/8359348.html'
three = 'http://www.cnblogs.com/alex3714/articles/8359358.html'

gevent.joinall([
    gevent.spawn(get_html, one, 1),
    gevent.spawn(get_html, two, 2),
    gevent.spawn(get_html, three, 3),
])












