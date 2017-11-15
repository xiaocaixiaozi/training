#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import os
import sys
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basedir)
from shop import shopping_cart

if __name__ == '__main__':
    shelf_file = 'shelf'  # 存储商品的文件
    last_file = 'Last_con'  # 存储上次消费的商品记录
    last_list = []
    shopping_cart.main(shelf_file, last_file, last_list)
