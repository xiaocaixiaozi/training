#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import argparse
import sys
import os

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASEDIR)

from core import client


def get_args():
    arg = argparse.ArgumentParser(prog='FTP', description='FTP Server')
    arg.add_argument('-s', '--server', required=False, type=str, \
                     help='服务器地址，默认为localhost', default='localhost')
    arg.add_argument('-p', '--port', required=False, type=int, \
                     help='服务器端口，默认为9999', default=9999)
    arg.add_argument('-u', '--user', required=False, type=str, \
                     help='用户名，默认为anonymous', default='anonymous')
    return vars(arg.parse_args())


if __name__ == '__main__':
    args = get_args()
    host, port, user = args['server'], args['port'], args['user']
    for i in range(3):
        password = input('Password: ').strip()
        if password:
            break
    else:
        sys.exit(1)
    client.Client(user, password, host, port)





