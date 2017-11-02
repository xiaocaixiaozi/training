#!/usr/bin/env python
# coding=utf-8
# Author: bloke
# Project: 购物车

import os

balance_file = 'balance'
shelf_file = 'shelf'
storage_rack = {}
with open(shelf_file, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        product, price = line.split(':')
        storage_rack[product] = price
user_dict = {'1': '商家', '2':'用户'}
for user_id, user_type in user_dict.items():
    print(user_id + ' : ' + user_type)
while 1:
    user_type = input('User type: ').strip()
    if user_type in user_dict:
        break
shelf_list = []
shelf_dict = {}
with open(shelf_file, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        if line:
            product, price = line.split(':')
            shelf_list.append((product.strip(), price.strip()))
for num, item in enumerate(shelf_list, 1):
    shelf_dict[str(num)] = item
product_list = []
if user_type == '1':        # 商家
    for num, item in enumerate(shelf_list, 1):
        print(item)
    while 1:
        print('Usage: q to quit; u to shelve; l to list'.center(50, '-'))
        choice = input('Choice: ').strip()
        if choice == 'q':
            with open(shelf_file, 'a', encoding='utf-8') as f:
                for product_1 in product_list:
                    f.write(product_1[0] + ':' + product_1[1] + '\n')
            print('Current product list is :')
            with open(shelf_file, 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    print(line, end='')
            break
        if choice == 'l':
            for key in product_list:
                print(key)
        if choice == 'u':
            the_product = input('Product: ').strip()
            the_price = input('Price: ').strip()
            if the_product and the_price and the_price.isdigit():
                product_list.append((the_product, the_price))
            else:
                print('Input error...')
                continue
else:
    shop_list = []
    if os.path.exists(balance_file):
        with open(balance_file, 'r', encoding='utf-8') as f:
            try:
                salary = balance = int(f.read().strip())
            except:
                salary = 0
    if not salary:
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
        if choice == 'q':
            print('You have purchased:')
            for shop_product in shop_list:
                print(shop_product)
            print('Your balance is : %d' % balance)
            with open(balance_file, 'w', encoding='utf-8') as f:
                f.write(str(balance))
            break
        if choice == 'l':
            print('Current product list is:')
            for shop_product in shop_list:
                print(shop_product)
            print('Your balance is %d .' % balance)
        if choice not in shelf_dict:
            continue
        else:
            purchase_product, price = shelf_dict[choice], int(shelf_dict[choice][1])
            if balance >= price:
                shop_list.append(purchase_product)
                balance -= price
                continue
            else:
                print('Your balance is insufficient . [ %d ]' % balance)
                continue

