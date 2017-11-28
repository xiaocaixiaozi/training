#!/usr/bin/env python
# coding=utf-8
# Author: bloke
# test class

# r1._Role__attr

class member(object):
    def __init__(self, name):
        self.name = name
        self.__heart = 'Normal'

    def info(self, age, sex):
        print('%s\'s age is %s, and sex is %s.' % (self.name, age, sex))
        self.__heart = 'Quick'
        print('Heart -->', self.__heart)

a = member('bloke')
a.info('22', 'man')
print(a.name)
print(a._member__heart)




