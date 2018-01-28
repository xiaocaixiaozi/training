#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import threading
import time
import random

event = threading.Event()

def light():
    for i in range(3):
        print('Red lighting.')
        event.set()
        time.sleep(3)
        print('Green lighting.')
        event.clear()
        time.sleep(5)

def car(name):
    while True:
        if event.is_set():
            print('Waiting...%s' % name)
            time.sleep(random.randint(1,3))
        else:
            print('Running...%s' % name)
            time.sleep(random.randint(1,3))

threads = []
for car_name in ['first', 'second', 'three']:
    t = threading.Thread(target=car, args=(car_name,))
    threads.append(t)

l = threading.Thread(target=light)
threads.append(l)

for item in threads:
    item.start()
for n in threads:
    n.join()


