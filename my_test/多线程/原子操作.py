#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import dis


def foo():
    l = []
    for i in range(3):
        l.append(i)
    return l

dis.dis(foo)



