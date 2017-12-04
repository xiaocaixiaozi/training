#!/usr/bin/env python
# coding=utf-8

import time
import random
import multiprocessing


class MYTEST(object):

    info_list = []

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
        self.my_sleep()
        return 'My name is %s.' % self.name

    def talk_two(self):
        self.my_sleep()
        return 'My age is %s.' % self.age

    def talk_three(self):
        self.my_sleep()
        return 'My sex is %s.' % self.sex


if __name__ == '__main__':
    start_time = time.time()
    result = []
    res = []
    my_test = MYTEST('user01', 22, 'male')
    pool = multiprocessing.Pool(3)
    # queue = multiprocessing.Queue()
    for i in [my_test.talk_one, my_test.talk_two, my_test.talk_three]:
        result.append(pool.apply_async(i))
    pool.close()
    pool.join()
    for item in result:
        res.append(item.get())
    # my_test.talk_one()
    # my_test.talk_two()
    # my_test.talk_three()
    print(res)
    print(time.time() - start_time)

