#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import os
import sys
import random
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)
from conf import db_setting

db = '../db/test.db'
user_table = 'users'
lock_table = 'lock'
create_user_sql = '''CREATE TABLE IF NOT EXISTS users(
    card_num char(15) primary key not null,
    user_name char(10) not null,
    password char(50) not null,
    balance int not null,
    age char(3),
    address
);'''
create_lock_sql = 'CREATE TABLE IF NOT EXISTS lock(card_num char(15) primary key not null);'
insert_user_sql = 'INSERT INTO %s values(%s, "%s", "%s", %s, "%s", "%s");'
insert_lock_sql = 'INSERT INTO %s values(%s);'
update_sql = 'UPDATE %s SET %s = "%s" WHERE card_num = "%s";'
select_sql = 'SELECT * FROM %s WHERE card_num = "%s";'

def create_user(db, create_user_sql, user_table, insert_user_sql):
    '''
    创建用户，发布信用卡
    在开户期间，需要用户提供基本信息：用户名，密码，年龄，地址
    卡号使用random随机生成
    '''
    while 1:
        try:
            data = input('输入个人信息，以逗号分隔: [用户名, 年龄, 地址] ').strip()
        except:
            break
            sys.exit(1)
        if len(data.split(',')) != 3:
            print('请输入正确的信息.')
            continue
        else:
            data = [x.strip() for x in data.split(',')]
            username, age, address = data
            if not age.isdigit():
                print('请输入正确的信息.')
                continue
            else:
                break
    card_num = random.randint(10000000, 19999999)
    print("为您发布信用卡: 卡号为\033[31;0m%s\033[0m, 余额为\033[32;0m15000\033[0m元人民币" % card_num)
    while 1:
        password = input('请输入密码：').strip()
        if password:
            break
    result = db_setting.insert_table(db, create_user_sql, user_table, insert_user_sql, \
                            [card_num, username, password, 15000, age, address])
    return result

def get_user_info(db=db, select_sql=select_sql, the_table=user_table):
    '''
    查询用户信息
    期间需要用户输入要查询的卡号，如果为空，则默认查询所有的用户信息
    '''
    card_num = input('请输入卡号，为空则查询所有：').strip()
    data = db_setting.select_table(db, select_sql, the_table, card_num)
    return data

def user_repay(db, select_sql, user_table, update_sql):
    while 1:
        card_num = input('请输入卡号:')
        if card_num:
            user_data = db_setting.select_table(db, select_sql, user_table, card_num)
            if not user_data:
                print('未知卡号')
                continue
            else:
                break
    card_num, user_name, passwd, balance, age, address = user_data
    balance = int(balance)
    repay_num = 15000 - balance
    print('您需要还款金额为：%s' % repay_num)
    while 1:
        money = input('请输入您要还款的金额：').strip()
        if money.isdigit():
            if money > repay_num:
                print('超了，您太有钱了')
                continue
            else:
                balance += money
                result = db_setting.update_table(db, user_table, update_sql, ['balance', balance, card_num])
                if result:
                    print('还款成功')
                    return True
                else:
                    print('还款失败')
                    return False


# 当前创建的用户：
# ('19696295', 'bloke', '12345', 15000, '23', 'Gehua')
# ('17052578', 'anon', '54321', 15000, '24', 'Beijing')

