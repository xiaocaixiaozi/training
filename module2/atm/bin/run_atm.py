#!/usr/bin/env python
# coding=utf-8
# Author: bloke

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
while 1:
    for num, key in enumerate(atm_api, 1):
        key_dict[str(num)] = key
        print(str(num) + ' > ' + key)
    choose = input('请选择操作: [q 退出]').strip()
    if choose == 'q':
        break
    if choose not in key_dict:
        print('请重新输入.')
        continue
    state = atm_api[key_dict[choose]]()
    if state:
        print('操作成功.')
        print('ATM'.center(50, '='))
    else:
        print('操作失败.')
        print('ATM'.center(50, '='))
