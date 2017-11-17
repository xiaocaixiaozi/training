#!/usr/bin/env python
# coding=utf-8
# Author: bloke
# ATM入口

import os
import sys
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basedir)
from core import atm_login

atm_api = {
    '查询': atm_login.get_user_info,
    '开户': atm_login.create_user,
    '转账': atm_login.transfer,
    '还款': atm_login.user_repay,
    '提现': atm_login.cash,
    '挂失': atm_login.lock_user
}

key_dict = {}
pre_key_dict = {'1': '开户', '2': '登录'}
while 1:
    try:
        for key, value in pre_key_dict.items():
            print(key + ' > ' + value)
        choice = input('Choice: [q 退出] ').strip()
        if choice == 'q':
            sys.exit(0)
        if choice not in pre_key_dict:
            continue
        if choice == '1':
            atm_login.create_user()
        else:
            user_data = atm_login.check_login()
            del (atm_api['开户'])
            while 1:
                for num, key in enumerate(atm_api, 1):
                    if key != '开户':
                        key_dict[str(num)] = key
                        print(str(num) + ' > ' + key)
                choose = input('请选择操作: [q 退出]').strip()
                if choose == 'q':
                    break
                if choose not in key_dict:
                    print('请重新输入.')
                    continue
                if not user_data:
                    print('登陆失败')
                    break
                state = atm_api[key_dict[choose]](user_data)
                if state:
                    print('操作成功.')
                    print('ATM'.center(50, '='))
                else:
                    print('操作失败.')
                    print('ATM'.center(50, '='))
    except KeyboardInterrupt as e:
        print('Exit.')


