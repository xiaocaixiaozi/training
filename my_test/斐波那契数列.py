#!/usr/bin/env python
# coding=utf-8
# Author: bloke
# 斐波那契数列

def fib(num):
    n, a, b = 1, 0, 1
    while n <= num:
        print(b, end=' ')
        a, b = b, a + b
        n += 1
    return 'done'

fib(9)

# 1 1 2 3 5 8 13 21 34

