#!/usr/bin/env python
# coding=utf-8
# Author: bloke


class Person(object):
    """练习property"""
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @property
    def info(self):
        print('Name: %s, Age: %s' % (self.name, self.age))

    @info.setter
    def info(self, the_info):
        self.name, self.age = the_info
        self.info

    @info.deleter
    def info(self):
        del self.name


# person = Person('user01', '22')
# person.info
# person.info = ('user02', '23')











