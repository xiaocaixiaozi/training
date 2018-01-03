#!/usr/bin/env python
# coding=utf-8
# Author: bloke

class first(object):

    def __init__(self, name):
        self.name = name

    def __call__(self):
        print('Name: %s' % self.name)

