#!/usr/bin/env python
# coding=utf-8
# Author: bloke


def move(n, a, b, c):
    if n == 1:
        print('move', a, '-->', c)
    else:
        move(n-1, a, c, b)
        move(1, a, b, c)
        move(n-1, b, a, c)


move(4, 'A', 'B', 'C')
