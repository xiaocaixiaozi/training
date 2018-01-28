#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import os
import sys
import yaml
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASEDIR)


def parse_conf(config_file):
    """
    读取yaml格式的配置文件，返回yaml格式的数据
    """
    with open(config_file, 'r') as f:
        data = yaml.load(f.read())
    return data


def generate_info(info):
    """
    生成主机信息字典，默认用户为"root"，默认端口为 22
    如果配置文件中提供，则覆盖默认信息，如果没有提供，则将默认信息添加到主机信息中
    :return: 主机信息字典
    """
    default_info = {'port': 22, 'username': 'root'}
    for key, value in info.items():
        default_info[key] = value
    return default_info


def parse_host_args(host_info):
    """
    配置文件中支持将主机信息格式写为 字典 和 列表，如果是列表，需要转换为字典形式
    """
    tmp_dict = {}
    for info in host_info.split():
        key, value = info.split('=')
        tmp_dict[key.strip()] = value.strip()
    return tmp_dict


def get_group_info(data, group_name):
    """
    从配置文件中读取到的主机信息，过滤除指定的组名 [group_name]的信息，
    如果 group_name 为 "all"，则代表所有主机组
    如果没有找到相对应的主机组信息，则返回False，如果有，则返回主机组的信息，字典格式
    """
    info_dict = {}
    group_info = []
    if group_name == 'all':
        for group_item in data['groups']:
            for group_key, group_value in group_item.items():
                for group_sub_value in group_value:
                    group_info.append(group_sub_value)
    else:
        for item in data['groups']:
            if group_name in item:
                group_info = item[group_name]
                break
        else:
            return False
    for host_info in group_info:    # group_info 是列表
        for host_key, host_value in host_info.items():
            if isinstance(host_value, dict):
                parse_info = generate_info(host_value)
                info_dict[host_key] = parse_info
            elif isinstance(host_value, str):
                parse_value = parse_host_args(host_value)
                parse_info = generate_info(parse_value)
                info_dict[host_key] = parse_info
            else:
                return False        # 不支持的配置文件格式
    else:
        return info_dict


def get_host_info(data, host_name):
    """
    获取单个主机的信息，首先通过get_group_info获取所有主机组的信息，
    然后过滤出指定主机[host_name]的信息
    如果指定主机[host_name]不存在，则返回False，否则返回主机信息，字典格式
    """
    tmp_dict = {}
    all_hosts_info = get_group_info(data, 'all')
    if host_name in all_hosts_info:
        tmp_dict[host_name] = all_hosts_info[host_name]
        return tmp_dict
    else:
        return False


def get_host_list(config_file, group_name):
    """
    获取指定主机组的成员主机名
    """
    data = parse_conf(config_file)
    groups = data['groups']
    if group_name == 'all':
        for group in groups:
            for key, value in group.items():
                print(key)
                for host in value:
                    for host_key, host_value in host.items():
                        print(' ' * 5, host_key)
    else:
        for group in groups:
            if group_name not in group:
                continue
            else:
                hosts_list = group[group_name]
                print(group_name)
                for host in hosts_list:
                    for h in host:
                        print(' ' * 5, h)
                else:
                    break
        else:
            print('未知主机组...')
            return False


if __name__ == '__main__':
    config_dir = os.path.join(BASEDIR, 'conf')
    config_file = os.path.join(config_dir, 'conf.yml')
    get_host_list(config_file, 'mongo')
    # data = parse_conf(config_file)
#     final_dict = get_host_info(data, 'mongo-1')
#     for key, value in final_dict.items():
#         print(key, value)
