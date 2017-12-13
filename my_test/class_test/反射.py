#!/usr/bin/env python
# coding=utf-8
# Author: bloke


class Person(object):
    """测试"""
    def __init__(self, name):
        self.name = name

    def talk(self):
        return('%s is talking.' % self.name)


class BlokeError(Exception):
    def __init__(self, e):
        self.e = e

    def __str__(self):
        return self.e


person = Person('bloke')
# print(hasattr(person, 'talk'))
# print(getattr(person, 'talk')())
# if not hasattr(person, 'eat'):
#     setattr(person, 'eat', 'eating...')
# if hasattr(person, 'eat'):
#     delattr(person, 'eat')
try:
    raise BlokeError('bloke.error')
except BlokeError as e:
    print(e)

print(getattr(person, 'bloke', 'bloke.test'))


