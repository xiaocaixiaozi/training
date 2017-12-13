#!/usr/bin/env python
# coding=utf-8
# Author: bloke


class A(object):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def talk():
        print('talk'.center(50, '-'))


A.talk()


'''
    def myself(self):
        self.talk()
        print('My name is %s.' % self.name)


my_test = A('user01')
my_test.myself()
'''







