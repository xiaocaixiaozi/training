#!/usr/bin/env python
# coding=utf-8
# Author: bloke


class Person(object):
    """
    自定义Person类
    """
    age = '22'
    sex = 'male'

    def __init__(self, name):
        self.name = name

    def __call__(self):
        print('My name is %s.' % self.name)

    def __getitem__(self, item):
        print('get item', item)

    def __setitem__(self, key, value):
        print('Set %s : [ %s ].' % (key, value))
        self.name = value

    def __delitem__(self, key):
        print('Delete %s.' % key)
        del key


person = Person('bloke')
# person()
# person['name'] = 'user01'
# person()
# person['name']
# del(person['name'])
# person()

