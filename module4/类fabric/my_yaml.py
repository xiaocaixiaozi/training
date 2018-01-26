#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import os
import yaml
import argparse

# conf_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conf')
# yaml_file = os.path.join(conf_dir, 'conf.yml')

def get_args():
    parse = argparse.ArgumentParser(prog='bloke-ssh', description='类Ansible工具')
    parse.add_argument('--hosts', required=True, type=str, \
                       help='主机组或主机')
    parse.add_argument('-m', '--module', required=False, type=str, \
                       help='要使用的模块', default='shell')
    args = parse.parse_args()
    return vars(args)

args = get_args()
print(args)

# with open(yaml_file, 'r') as f:
#     data = yaml.load(f.read())
#
# print(data)



