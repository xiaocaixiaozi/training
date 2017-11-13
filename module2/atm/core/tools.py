#!/usr/bin/env python
# coding=utf-8
# Author: bloke

from hashlib import sha1
import random

def hash(data):
    '''
    加密给定的密码
    :param data: 需要加密的数据
    :return: 返回十六进制加密后的字符串
    '''
    e = sha1()
    e.update(data.encode('utf-8'))
    return e.hexdigest()

def generate_card():
    card_num = random.randint(10000000, 19999999)
    return card_num

