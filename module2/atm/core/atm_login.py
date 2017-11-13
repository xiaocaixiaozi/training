#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import os
import sys
import random
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)
from conf import db_setting
from core.tools import hash

db = '../db/atm.db'
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

def atm_auth(func):
    '''
    用于信用卡用户登录认证，并且返回该用户的信息给func
    :param func: 待认证的方法
    '''
    def wrapper(*args, **kwargs):
        while 1:
            card_num = input('卡号: ').strip()
            password = input('密码: ').strip()
            if not card_num or not password or not card_num.isdigit():
                print('请输入正确的信息.')
                continue
            else:
                data = db_setting.select_table(db, select_sql, user_table, card_num)
                if data:
                    real_password = data[0][2]
                    if hash(password) == real_password:
                        result = func(user_data=data[0], *args, **kwargs)
                        break
                    else:
                        print('用户名或密码错误.')
                        continue
        return result
    return wrapper


def create_user(db=db, create_user_sql=create_user_sql, user_table=user_table, insert_user_sql=insert_user_sql):
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
            password = hash(password)
            break
    result = db_setting.insert_table(db, create_user_sql, user_table, insert_user_sql, \
                            [card_num, username, password, 15000, age, address])
    return result

@atm_auth
def get_user_info(user_data):
    '''
    :return: 返回用户信息
    '''
    return user_data

@atm_auth
def user_repay(user_data):
    '''
    用户还款
    :param user_data: 由atm_auth函数返回
    :return: 还款成功，返回True,否则返回False
    '''
    card_num, user_name, passwd, balance, age, address = user_data
    balance = int(balance)
    repay_num = 15000 - balance
    print('您需要还款金额为：%s' % repay_num)
    while 1:
        money = input('请输入您要还款的金额：').strip()
        if money.isdigit():
            money = int(money)
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

@atm_auth
def transfer(user_data):
    '''
    用户转账
    :param user_data: 由atm_auth函数返回
    :return: 转账成功返回True，否则返回False
    '''
    card_num, user_name, passwd, balance, age, address = user_data
    while 1:
        trans_card_num = input('要转账的卡号: ').strip()
        if not trans_card_num.isdigit():
            print('未知卡号.')
            continue
        else:
            trans_data = db_setting.select_table(db, select_sql, user_table, trans_card_num)
            if not trans_data:
                print('未知卡号.')
                continue
            else:
                trans_data = trans_data[0]
                trans_card_num, trans_user_name, trans_passwd, \
                trans_balance, trans_age, trans_address = trans_data
                break
    sign = input('请确认姓名 "%s"  <Y/N>' % trans_user_name).upper()
    if sign == 'Y':
        while 1:
            trans_money = input('请输入要转账的金额: ').strip()
            if not trans_money.isdigit() and not isinstance(trans_money, float):
                print('请输入正确的金额.')
                continue
            elif int(trans_money) > int(balance):
                print('余额不足.')
                continue
            else:
                trans_result = db_setting.update_table(\
                    db, user_table, update_sql, ['balance', int(trans_balance) + int(trans_money), trans_card_num])
                if trans_result:
                    result = db_setting.update_table( \
                        db, user_table, update_sql, ['balance', int(balance) - int(trans_money), card_num])
                    if result:
                        print('成功转账 \033[31;1m%s\033[0m 给 \033[32;1m%s\033[0m (%s)' % \
                              (trans_money, trans_user_name, trans_card_num))
                    else:
                        trans_result = db_setting.update_table( \
                            db, user_table, update_sql,
                            ['balance', int(trans_balance) - int(trans_money), trans_card_num])
                    return True
                else:
                    print('转账失败')
                    return False
    else:
        return True

transfer()

# 当前创建的用户：
# ('19696295', 'bloke', '12345', 11610, '23', 'Gehua')
# ('17052578', 'anon', '54321', 15000, '24', 'Beijing')
# ('10122658', '焦恩', '11111', 14910, '30', 'America')