#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import os
import argparse
import queue
import threading
import sys
import re
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASEDIR)
from main import bloke_ssh, yaml_tools


def get_args():
    """
    获取命令行参数
    """
    parse = argparse.ArgumentParser(usage='run.py <host-pattern> options', \
                                    description='类Ansible工具')
    parse.add_argument('hosts', type=str, help='指定要运行的主机或主机组')
    parse.add_argument('-m', '--module', type=str, \
                       choices=['exec', 'put', 'get'], default='exec', \
                       help="""{
                       exec: 远程执行命令;
                       put: 上传文件;
                       get: 下载文件}, 默认为exec""")
    parse.add_argument('-a', '--args', type=str, \
                       help='参数')
    parse.add_argument('-l', '--list', action='store_const', const=True, \
                       help='列出指定主机组的主机')
    args = parse.parse_args()
    return vars(args)


def parse_args(args_data):
    """
    解析输入的参数 [--args]
    如果是put、get模块，需要去掉src、dest关键字，并且按照顺序src -> dest 返回；
    如果模块是exec，直接返回参数；
    如果解析错误，则返回False；
    """
    if args_data['module'] == 'exec':
        return args_data['args']
    src_re = re.compile(r'src=(\S+)')
    dest_re = re.compile(r'dest=(\S+)')
    src = src_re.findall(args_data['args'])
    dest = dest_re.findall(args_data['args'])
    if not src or not dest:
        return False
    return src[0], dest[0]


def read_hosts_info(args_data, config_file):
    """
    读取配置文件，返回指定主机或主机组的信息
    如果找不到主机或主机组，则退出程序，返回值为 1
    """
    config_data = yaml_tools.parse_conf(config_file)
    hosts_info = yaml_tools.get_group_info(config_data, args_data['hosts'])
    if not hosts_info:
        hosts_info = yaml_tools.get_host_info(config_data, args_data['hosts'])
        if not hosts_info:
            print('未知主机或主机组: %s' % args_data['hosts'])
            sys.exit(1)
    return hosts_info


if __name__ == '__main__':
    config_dir = os.path.join(BASEDIR, 'conf')
    config_file = os.path.join(config_dir, 'conf.yml')
    args = get_args()
    if args['list']:
        yaml_tools.get_host_list(config_file, args['hosts'])
        sys.exit(0)
    hosts_info = read_hosts_info(args, config_file)
    thread_list = []
    queue = queue.Queue(10)
    run_module = args['module']
    for hostname, hostvalue in hosts_info.items():
        ssh_client = bloke_ssh.MySSH(hostname, **hostvalue)
        ssh_client.connect()
        if not hasattr(ssh_client, run_module):
            print('Unknown module %s.' % run_module)
            sys.exit(1)
        try:
            t = threading.Thread(target=getattr(ssh_client, run_module), \
                                 args=(parse_args(args), queue))
        except Exception as e:
            print(e)
            sys.exit(1)
        t.daemon = True
        t.start()
        thread_list.append(t)
    for l in thread_list:
        l.join(timeout=10)
    while queue.qsize():
        for item in queue.get():
            for line in item:
                print(line, end='')
