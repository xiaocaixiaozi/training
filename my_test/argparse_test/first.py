#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import argparse

parse = argparse.ArgumentParser(description='This is a test.')
parse.add_argument('-f', required=True, type=str, help='指定文件名', metavar='filename')
parse.add_argument('-a', required=True, type=int, help='指定优先级', metavar='INT')
parse.add_argument('-n', required=False, action='store_false', help='不进行DNS解析', default=False)
parse.add_argument('-v', required=False, action='store_true', help='显示详细信息')
args = parse.parse_args()
args = vars(args)
print(args)



