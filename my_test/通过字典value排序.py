#!/usr/bin/env python
# coding=utf-8
# Author: bloke
# Subject: 按照字典的value排序

the_dict = {
    'first': 'one',
    'second': 'two',
    'third': '3',
    'fourth': 'four',
    'fifth': '5'
}

new_dict = sorted(the_dict.items(), key=lambda x:x[1])
# key = lambda x: x[1]，设置排序的key为前面可迭代对象的第二个值，也就是value

print(new_dict)







