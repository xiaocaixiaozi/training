#!/usr/bin/env python
# coding=utf-8
# Author: bloke
# Project: 购物车

import os

balance_file = 'balance'    #存储余额的文件
shelf_file = 'shelf'    #存储商品的文件
'''
storage_rack = {}   #货架字典
with open(shelf_file, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        product, price = line.split(':')
        storage_rack[product] = price
'''
user_dict = {'1': '商家', '2':'用户'}
for user_id, user_type in user_dict.items():
    print(user_id + ' : ' + user_type)
while 1:        # 输入客户类型
    user_type = input('User type: ').strip()
    if user_type in user_dict:
        break
shelf_list = []     #上架货物列表
shelf_dict = {}     #上架货物字典
if os.path.exists(shelf_file):
    with open(shelf_file, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if line:
                product, price = line.split(':')
                shelf_list.append((product.strip(), price.strip()))
for num, item in enumerate(shelf_list, 1):
    shelf_dict[str(num)] = item

if user_type == '1':        # 商家
    for num, item in enumerate(shelf_list, 1):
        print(str(num) + '. ', item)
    while 1:
        print('Usage: q to quit; u to shelve; l to list; d to delete'.center(50, '-'))
        choice = input('Choice: ').strip()
        if choice == 'q':       # 退出
            with open(shelf_file, 'w', encoding='utf-8') as f:
                for product_1 in shelf_list:
                    f.write(product_1[0] + ':' + product_1[1] + '\n')
            print('Current product list is :')
            for p in shelf_list:
                print(p)
            break
        if choice == 'l':   # 列出当前货架
            for key in shelf_list:
                print(key)
        if choice == 'u':   # 上架
            the_product = input('Product: ').strip()
            the_price = input('Price: ').strip()
            if the_product and the_price and the_price.isdigit():
                shelf_list.append((the_product, the_price))
            else:
                print('Input error...')
                continue
        if choice == 'd':   # 下架
            for n, k in enumerate(shelf_list):
                print(str(n), k)
            while 1:
                delete_num = input('Choice Num to delete: ').strip()
                if delete_num.isdigit():
                    delete_num = int(delete_num)
                    if delete_num in range(len(shelf_list)):
                        del(shelf_list[delete_num])
                        break
else:       # 用户
    shop_list = []
    if os.path.exists(balance_file):        # 判断是否存在余额文件
        with open(balance_file, 'r', encoding='utf-8') as f:
            try:
                salary = balance = int(f.read().strip())
            except:
                salary = 0
    else:
        salary = 0
    if not salary:      # 如果没有余额文件，需要用户输入自己的工资
        while 1:
            salary = input('Your salary: ').strip()
            if salary.isdigit():
                salary = balance = int(salary)
                break
    for num in shelf_dict.keys():
        print(num + '. ' + '[' + shelf_dict[num][0] + ' : ' + shelf_dict[num][1] + ']')
    while 1:
        print('Usage: q to quit; num to buy; l to list'.center(50, '-'))
        choice = input('Choice: ').strip()
        if choice == 'q':       # 退出
            print('You have purchased:')
            for shop_product in shop_list:
                print(shop_product)
            print('Your balance is : \033[1;32m %d \033[0m' % balance)
            with open(balance_file, 'w', encoding='utf-8') as f:
                f.write(str(balance))
            break
        if choice == 'l':       # 显示当前已购买的货物
            print('Current product list is:')
            for shop_product in shop_list:
                print(shop_product)
            print('Your balance is \033[1;32m %d \033[0m .' % balance)
        if choice not in shelf_dict:
            continue
        else:       # 购买货物
            purchase_product, price = shelf_dict[choice], int(shelf_dict[choice][1])
            if balance >= price:
                shop_list.append(purchase_product)
                balance -= price
                continue
            else:
                print('Your balance is insufficient . [ \033[1;32m %d \033[0m ]' % balance)
                continue

