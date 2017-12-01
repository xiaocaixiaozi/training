#!/usr/bin/env python
# coding=utf-8
# Author: bloke


class A(object):

    def __init__(self):
        print('from A'.center(30, '-'))

    def ping(self):
        print('ping in the classA.')


class B(A):

    def __init__(self):
        super().__init__()
        print('from B'.center(30, '-'))

    def ping(self):
        print('ping in the classB')

    def pong(self):
        print('pong in the classB.')


class C(B):

    def __init__(self):
        super().__init__()
        print('BBBBBB')


print(C.mro())
print(B.mro())
print(C())

# @classmethod


