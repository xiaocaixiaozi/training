#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import time
import sys
import os

'''
print('Error: my_test_test')
for i in reversed(range(6)):
    print('[ %s seconds after the exit. ]' % i, end='\r')
    time.sleep(1)
'''

def my_exit():
    os._exit(1)

try:
    my_exit()
except SystemExit as e:
    pass


print('bloke')






