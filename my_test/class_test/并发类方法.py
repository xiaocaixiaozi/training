#!/usr/bin/env python
# coding=utf-8

import time
import random
from multiprocessing.dummy import Pool as ThreadPool


class MYTEST(object):

    one_list, two_list, three_list = [], [], []

    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex
        print('Start'.center(30, '*'))

    @staticmethod
    def my_sleep():
        print(random.randint(1, 5))
        time.sleep(random.randint(1, 5))

    def talk_one(self):
        # self.my_sleep()
        self.one_list.append('My name is %s.' % self.name)

    def talk_two(self):
        # self.my_sleep()
        self.two_list.append('My age is %s.' % self.age)

    def talk_three(self):
        # self.my_sleep()
        self.three_list.append('My sex is %s.' % self.sex)


if __name__ == '__main__':
    my_test = MYTEST('user01', 22, 'male')
    pool = ThreadPool(3)
    for func in [my_test.talk_one, my_test.talk_two, my_test.talk_three]:
        pool.apply_async(func)
    pool.close()
    pool.join()
    print('one: ', my_test.one_list)
    print('two: ', my_test.two_list)
    print('three: ', my_test.three_list)

