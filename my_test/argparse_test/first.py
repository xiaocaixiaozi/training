#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import argparse

def hello():
    print('hello...')

parse = argparse.ArgumentParser(description='This is a test.')
parse.add_argument('-f', required=False, type=str, help='指定文件名', metavar='filename')
parse.add_argument('-a', required=False, type=int, help='指定优先级', metavar='INT')
parse.add_argument('-n', required=False, action='store_false', help='不进行DNS解析', default=False)
parse.add_argument('-v', required=False, action='store_true', help='显示详细信息')
parse.add_argument('-p', required=False, help='Print hello', action='store_true')
args = parse.parse_args()
args = vars(args)
print(args)
if args['p']:
    hello()




