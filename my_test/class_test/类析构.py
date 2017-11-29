#!/usr/bin/env python
# coding=utf-8
# Author: bloke
# 类 析构方法


class SchoolPerson(object):

    member_num = 0

    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex

    def enroll(self):
        SchoolPerson.member_num += 1
        print('%s enroll successful, %s' % (self.name, self.member_num))

    def __del__(self):
        SchoolPerson.member_num -= 1
        print('Delete ', self.name, self.member_num)


class Teacher(SchoolPerson):

    def __init__(self, name, age, sex, role):
        SchoolPerson.__init__(self, name, age, sex)
        self.role = role

    def tell(self):
        SchoolPerson.enroll(self)
        print(self.__dict__)


class Student(SchoolPerson):

    def __init__(self, name, age, sex, role):
        SchoolPerson.__init__(self, name, age, sex)
        self.role = role

    def tell(self):
        SchoolPerson.enroll(self)
        print(self.__dict__)


t1 = Teacher('teacher1', 30, 'F', 'Teacher')
s1 = Student('student1', 22, 'M', 'Student')

t1.tell()
s1.tell()
t1.tell()
