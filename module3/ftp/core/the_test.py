#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import configparser
import os

# BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# shadow_file = BASEDIR + os.sep + os.path.join('conf', 'shadow')
# config = configparser.ConfigParser()
# config.read(os.path.join(BASEDIR, shadow_file), encoding='utf-8')
# config.set('password', 'bloke', 'bloke')
# with open(shadow_file, 'w') as f:
#     config.write(f)

class MyTest(object):

    def one(self):
        print('one...')

    def two(self):
        print('two...')

    def three(self):
        print('three...')


A = MyTest()
getattr(A, 'four', A.one)()






