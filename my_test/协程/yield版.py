#!/usr/bin/env python
# coding=utf-8
# Author: bloke


def generator():
    for i in range(5):
        name = yield
        print('%s: %s' % (name, i))


def consumer(gen1, gen2):
    gen1.__next__()
    gen2.__next__()
    for i in range(5):
        gen1.send('gen1')
        gen2.send('gen2')
        print('................................')


if __name__ == "__main__":
    g1 = generator()
    g2 = generator()
    consumer(g1, g2)

