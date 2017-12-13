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
        """构造方法"""
        self.name = name

    def __call__(self):
        """调用对象时执行"""
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
person()    # 调用__call__方法
person['name'] = 'user01'    # 调用__setitem__方法
person['name']    # 调用__getitem__方法
del(person['name'])    # 调用__delitem__方法


