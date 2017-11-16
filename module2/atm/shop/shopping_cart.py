#!/usr/bin/env python
# coding=utf-8
# Author: bloke
# Project: 购物车

import os
import sys
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basedir)
from core import atm_login

def get_atm_api(last_file, shop_list):
    '''
    调用信用卡支付接口
    :return: 如果支付成功，返回True，否则返回False
    '''
    money = 0
    print('调取信用卡接口...')
    user_data = atm_login.get_user_info()
    if user_data:
        card_num, user_name, password, balance, age, address = user_data
        balance = int(balance)
        print('当前账户余额: [ %s ]' % balance)
        for shop_product in shop_list:
            money += int(shop_product[1])
        if money > balance:
            print('余额不足.')
            return False
        else:
            result = atm_login.update_user_data('balance', str(balance - money), card_num)
            if result:
                print('支付后账户余额: [ %s ]' % (balance - money))
                with open(last_file, 'w', encoding='utf-8') as f:
                    for l in shop_list:
                        f.write(l[0] + ':' + l[1] + '\n')
                return True
            else:
                return False

def main(shelf_file, last_file, last_list):
    if os.path.exists(last_file):
        with open(last_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.split(':')
                last_list.append((line[0].strip(), line[1].strip()))
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
        for num in shelf_dict.keys():
            print(num + '. ' + '[' + shelf_dict[num][0] + ' : ' + shelf_dict[num][1] + ']')
        while 1:
            print('Usage: q 退出; num 购买; l 列出; a 上次购买记录; p 结账.'.center(50, '-'))
            choice = input('Choice: ').strip()
            if choice == 'q':       # 退出
                print('You have purchased:')
                for shop_product in shop_list:
                    print(shop_product)
                while 1:
                    settle = input('是否结账 <Y/N>').strip().lower()
                    if not settle:
                        continue
                    if settle != 'y':
                        print('退出...')
                        sys.exit(0)
                    result = get_atm_api(last_file, shop_list)
                    if result:
                        print('支付成功.')
                        sys.exit(0)
                    else:
                        print('支付失败.')
                        sys.exit(1)
            if choice == 'a':        #显示上次的购买记录
                for la in last_list:
                    print(la)
            if choice == 'l':       # 显示当前已购买的货物
                print('Current product list is:')
                for shop_product in shop_list:
                    print(shop_product)
            if choice == 'p':
                result = get_atm_api(last_file, shop_list)
                if result:
                    print('支付成功')
                    sys.exit(0)
                else:
                    print('支付失败')
                    sys.exit(1)
            if choice not in shelf_dict:
                continue
            else:       # 购买货物
                shop_list.append(shelf_dict[choice])

if __name__ == '__main__':
    shelf_file = 'shelf'  # 存储商品的文件
    last_file = 'Last_con'  # 存储上次消费的商品记录
    last_list = []
    main(shelf_file, last_file, last_list)
