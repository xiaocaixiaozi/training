#!/usr/bin/env python
# coding=utf-8
# Author: bloke
# test class


class Person(object):

    author = 'bloke'

    def __init__(self, name):
        self.name = name
        self.department = 'IT'

    def action(self, action):
        print('%s do %s, his department is %s ...' % (self.name, action, self.department))


class BlackPerson(Person):
    def __init__(self, name):
        Person.__init__(self, name)
        self.department = 'Person'
        self.color = 'black'

    def talk(self):
        print('%s\'s color is %s, and his department is %s.    --%s' % (self.name,\
                                                                        self.color, self.department, self.author))


class WhitePerson(Person):

    def __init__(self, name):
        Person.__init__(self, name)
        self.color = 'white'

    def talk(self):
        Person.action(self, 'talk')
        print('%s\'s color is %s, and his department is %s.    --%s' % (self.name,\
                                                                        self.color, self.department, self.author))


bp = BlackPerson('black_one')
bp.talk()

wp = WhitePerson('white_one')
wp.talk()





