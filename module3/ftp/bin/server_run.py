#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import os
import sys
import argparse

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)

from core import create_account
from core import server

def get_args():
    arg = argparse.ArgumentParser(prog='FTP', description='FTP Server')
    arg.add_argument('-c', '--account', required=False, type=str, \
                     help='创建账户并设置密码，如果账户存在，则修改密码')
    arg.add_argument('-l', '--listen', required=False, action='store_true', \
                     help='运行服务')
    arg.add_argument('-s', '--address', required=False, type=str, default='localhost', \
                     help='服务监听地址，默认 localhost')
    arg.add_argument('-p', '--port', required=False, type=int, default=9999, \
                     help='服务监听端口，默认9999')
    return vars(arg.parse_args())


if __name__ == '__main__':
    args = get_args()
    try:
        if args['account']:     # 创建账户
            result = create_account.create(args['account'])
            sys.exit()
        elif args['listen']:    # 运行服务器端
            addr, port = args['address'], args['port']
            print('Running server...[%s:%s]' % (addr, port))
            server.run(addr, port)
    except KeyboardInterrupt as e:
        sys.exit(1)



