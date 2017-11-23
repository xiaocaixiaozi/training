#/usr/bin/env python
#coding=utf8
#Author: itanony

import json
import random
import string
admin_db = "../db/manager"
users_db = "../db/users"


def auth(auth_type):
    '''

    :param auth_type:
    :return:
    '''
    def outwrapper(func):
        def wrapper(*args,**kwargs):
            print("%sAuth Request!%s" % ('#'*5, '#'*5))
            username = input("UserName: ")
            password = input("Password: ")
            if auth_type == "manager":
                f = open(admin_db, "r")
            else:
                f = open(users_db, "r")
            dict_m = {}
            for line in f.readlines():
                dict_m[line.split(',')[0]] = line.split(",")[1]
            if username in dict_m.keys() and password == dict_m[username]:
                func()
            else:
                print("Auth Fail！！")
        return wrapper
    return outwrapper


def random_password():
    '''
    return: 生成随机密码
    '''
    return ''.join(random.sample(string.ascii_letters + string.digits, 8))

def user_info():
    '''
    :return: 返回一个dict，格式化输出用户信息
    '''
    dict = {}
    with open(users_db,'r') as f:
        for line in f:
            dict[line.split(",")[0]] = \
                {
                    "password":line.split(",")[1],
                    "remaining":line.split(",")[2],
                    "enable":line.split(",")[3].strip()
                }
    return dict



def check_position(position):
    '''
    判断额度是否为数字
    :param position: 额度
    :return: 判断输入的额度是否为数字
    '''
    if position.isdigit():
        return True
    else:
        return False

def add_user(username,position):
    '''
    :param username: 用户名
    :param position: 用户额度
    :return: 返回好呢？
    '''
    password = random_password()
    print(password)
    with open(users_db,"a",encoding="utf-8") as f:
        f.write("%s,%s,%s,%s,1" %(username,password,position,position) )

def disable_user(username):
    '''
    禁用用户
    :param username:
    :return:
    '''
    userinfo = user_info()
    if userinfo[username]["enable"] == 0:
        print("already disabled")
    else:
        with open(users_db,"r") as f:
            lines = f.readlines()
        with open(users_db,"w") as f:
            for line in lines:
                if line.split(",")[0] == username:
                    line = "%s,0" %(','.join(line.split(",")[:-1]))
            f.write(line)

def modify_positon(username,new_position):
    '''
    调整用户额度
    :param username:
    :param new_position:
    :return:
    '''

    with open(users_db, "r") as f:
        lines = f.readlines()
    with open(users_db, "w") as f:
        for line in lines:
            if line.split(",")[0] == username:
                line = "%s,%s,%s" % (','.join(line.split(",")[:2]),new_position,','.join(line.split(",")[3:]))
        f.write(line)