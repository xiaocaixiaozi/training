#!/usr/bin/env python
# coding=utf-8
# Author: bloke
# test random module

import random

def gen_code(num):
    '''
    对列表的随机index执行pop操作，然后通过pop的值是否是
    2的倍数来判断是使用数字还是字母，确保是字母和数字的组合
    :param num: 传入需要生成验证码的位数
    :return:    返回验证码
    '''
    seq = ''
    choice_range = list(range(num))
    for n in range(len(choice_range)):
        sign = choice_range.pop(random.randint(0, len(choice_range)-1))
        if sign % 2 == 0:
            seq += chr(random.randint(65, 90)).lower()
        else:
            seq += str(random.randint(1,9))
    return seq

gen_code(5)




