#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)
from conf import db_setting
from core.tools import hash
from core.tools import generate_card
from core.tools import record_log

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
select_lock_sql = 'SELECT * FROM lock;'
atm_logger = record_log('../logs/atm.log')   # ATM操作日志

def get_lock_info():
    '''
    查询锁定卡号
    '''
    data = db_setting.select_table(db, select_lock_sql, lock_table)
    atm_logger.info('Query lock the account table. <%s>' % select_lock_sql)
    return data

def check_lock(card_num):
    '''
    检查卡号是否被锁定
    :param card_num: 被检查的卡号
    :return: 如果被锁定，返回True，否则返回False
    '''
    lock_user_data = db_setting.select_table(db, select_sql, lock_table)
    checks = [card_num in user for user in lock_user_data]
    if True in checks:
        atm_logger.info('Test %s card number is locked. <locked>' % card_num)
        return True
    else:
        atm_logger.info('Test %s card number is locked. <not locked>' % card_num)
        return False

def update_user_data(key, value, card_num):
    result = db_setting.update_table(db, user_table, update_sql, [key, value, card_num])
    return result

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
                if check_lock(card_num):
                    print('此卡号已被锁定 [ \033[31;1m%s\033[0m ]\n如需解锁，请到柜台办理.' % card_num)
                    atm_logger.warning('%s auth failed.' % card_num)
                    return False
                data = db_setting.select_table(db, select_sql, user_table, card_num)
                if data:
                    real_password = data[0][2]
                    if hash(password) == real_password:
                        atm_logger.info('%s auth success.' % card_num)
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
    card_num = generate_card()
    print("为您发布信用卡: 卡号为\033[31;0m%s\033[0m, 余额为\033[32;0m15000\033[0m元人民币" % card_num)
    while 1:
        password = input('请输入密码：').strip()
        if password:
            password = hash(password)
            break
    result = db_setting.insert_table(db, create_user_sql, user_table, insert_user_sql, \
                            [card_num, username, password, 15000, age, address])
    if result:
        atm_logger.info('Create %s card number, the message is [%s, %s, %s].' % (card_num, username, age, address))
    else:
        atm_logger.error('Card number %s failed to be created, the message is [%s, %s, %s].' % (card_num, username, age, address))
    return result

@atm_auth
def get_user_info(user_data):
    '''
    :return: 返回用户信息
    '''
    atm_logger.info('Get user info. [%s]' % str(user_data))
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
                    atm_logger.info('%s account successfully repay %s yuan.' % (card_num, money))
                    user_logger = record_log('../logs/%s.log' % card_num)
                    user_logger.info('repay %s yuan success.' % money)
                    return True
                else:
                    print('还款失败')
                    atm_logger.warning('%s account repayment failed.' % card_num)
                    user_logger = record_log('../logs/%s.log' % card_num)
                    user_logger.warning('repay %s yuan failed.' % money)
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
                        atm_logger.info('[%s] account successfully transferred to [%s] account %s yuan.' % \
                                        (card_num, trans_card_num, trans_money))
                        user_logger = record_log('../logs/%s.log' % card_num)
                        user_logger.info('transfer %s yuan to %s success.' % (trans_money, trans_card_num))
                        return True
                    else:
                        trans_result = db_setting.update_table( \
                            db, user_table, update_sql,
                            ['balance', int(trans_balance) - int(trans_money), trans_card_num])
                        atm_logger.error('%s account to %s account transfer failed.' % (card_num, trans_card_num))
                        user_logger = record_log('../logs/%s.log' % card_num)
                        user_logger.error('transfer %s yuan to %s failed.' % (trans_money, trans_card_num))
                        return False
                else:
                    print('转账失败')
                    atm_logger.error('%s account to %s account transfer failed.' % (card_num, trans_card_num))
                    user_logger = record_log('../logs/%s.log' % card_num)
                    user_logger.error('transfer %s yuan to %s failed.' % (trans_money, trans_card_num))
                    return False
    else:
        return True

@atm_auth
def cash(user_data):
    '''
    提现，扣取5%手续费
    :param user_data: 由 atm_auth 返回
    :return: 提取成功，返回True，否则返回False
    '''
    while 1:
        money = input('请输入要提取的金额: [q to quit] ').strip()
        if money == 'q':
            return True
        if not money.isdigit() and not isinstance(money, float):
            print('输入错误.')
            continue
        money = int(money)
        fee = money * 0.05
        card_num, user_name, passwd, balance, age, address = user_data
        balance = int(balance)
        if money > balance or (money + fee) > balance:
            print('余额不足.')
            continue
        else:
            balance = balance - money - fee
            result = db_setting.update_table(db, user_table, update_sql, ['balance', balance, card_num])
            if result:
                print('提现成功.')
                atm_logger.info('%s account withdrawals %s yuan, after deducting the fee of %s yuan.' % (card_num, money, fee))
                user_logger = record_log('../logs/%s.log' % card_num)
                user_logger.info('withdraw %s yuan, after deducting the fee of %s yuan.' % (money, fee))
                return True
            else:
                return False

@atm_auth
def lock_user(user_data):
    '''
    锁定账号
    :param user_data: 由atm_auth返回用户信息
    :return: 锁定成功返回True，否则返回False
    '''
    card_num, user_name, passwd, balance, age, address = user_data
    while 1:
        sign = input('您确定锁定该账号吗？[Y/N]').strip().lower()
        if sign == 'n':
            break
            return True
        if sign == 'y':
            result = db_setting.insert_table(db, create_lock_sql, lock_table, insert_lock_sql, [card_num])
            if result:
                print('已成功锁定，如需解锁请到柜台操作.')
                atm_logger.info('%s account successfully locked.' % card_num)
                user_logger = record_log('../logs/%s.log' % card_num)
                user_logger.info('account successfully locked.')
                return True
            else:
                atm_logger.warning('%s account lock failed.' % card_num)
                user_logger = record_log('../logs/%s.log' % card_num)
                user_logger.warning('account lock failed.' % card_num)
                return False

# 当前创建的用户：
# ('17559028', 'Jack', 'jack', 15000, '50', 'Chicago')
# ('19696295', 'bloke', '12345', 11610, '23', 'Gehua')
# ('17052578', 'anon', '54321', 15000, '24', 'Beijing')
# ('10122658', '焦恩', '11111', 13860, '30', 'America')
# ('17360935', 'test01', '11111', 15000, '10', '朝鲜')
#
# 当前锁定账号:
# ('10122658', '17360935')
