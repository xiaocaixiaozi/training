#!/usr/bin/env python
# coding=utf-8
# Author: bloke
# Project: 登陆接口

import hashlib
import os
import sys
import getpass

pass_file = 'passwd'    # 密码文件
lock_file = 'lock'      # 锁定账号文件
pass_dict = {}      # 密码字典

while 1:    # 判断用户是否输入为空
    username = input('Login_user: ').strip()
    if username:
        break

if os.path.exists(lock_file):       # 如果用户在lock文件中，则退出
    with open(lock_file, 'r') as f:
        for line in f.readlines():
            if username == line.strip():
                print('This account is been locked. [ %s ]' % username)
                sys.exit(1)

with open(pass_file, 'r') as f:
    for line in f.readlines():
        item_user, item_pass = line.split(':')
        pass_dict[item_user] = item_pass


def hash_pass(password):    # 使用 hashlib.sha1 加密密码
    cr = hashlib.sha1()
    cr.update(password.encode())
    return cr.hexdigest().strip()


for count in range(3):      # 最多尝试输入三次密码
    if pass_dict.get(username):     # 判断账号是否存在
        try:
            password = getpass.getpass('Login_pass: ').strip()
            password = hash_pass(password)  # 对比密码加密串
            if pass_dict.get(username).strip() == password:
                print('Welcome to %s !' % username)
                break
        except KeyboardInterrupt as e:
            exit(1)
    else:       # 账号不存在则退出
        print('This account don\'t exist. [ %s ]' % username)
        break
else:       # 密码输错三次后，将用户写入lock文件中
    print('Enter too many times, the account is locked. [ %s ]' % username)
    with open(lock_file, 'w') as f:
        f.write(username + '\n')
