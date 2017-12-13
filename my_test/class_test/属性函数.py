#!/usr/bin/env python
# coding=utf-8
# Author: bloke


class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @property
    def info(self):
        return('My name is %s, and my age is %s.' % (self.name, self.age))

    @info.setter
    def info(self, name, age='23'):
        self.name = name
        self.age = age
        return('Name: %s, Age: %s.' % (self.name, self.age))

    @info.deleter
    def info(self):
        del self.age

    @property
    def talk(self):
        print(self.name, self.age)

    @talk.setter
    def talk(self, age):
        self.age = age
        print(self.name, self.age)

    def final(self):
        print('Final:', self.name, self.age)

person = Person('bloke', '22')
print(person.info)
person.info = 'user03'
print(person.info)
person.talk
person.talk = '24'
person.talk
print(person.info)
person.final()
