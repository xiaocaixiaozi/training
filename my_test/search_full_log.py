#!/usr/bin/env python
# coding=utf-8
# Author: bloke
# Subject: search tianshan log


def generate_file_list():
    log_file_dict = {}
    log_items = ['RtspProxy', 'ssm_tianshan_s1', 'MODSvc', 'weiwoo', 'Path', 'pho_VSS', 'pho_ERM', \
                 'SiteAdminSvc', 'NSS2', 'NSS', 'NSS3', 'NSS4']
    log_item_counts = {
        'ssm_tianshan_s1': range(10),
        'Path': range(10),
        'pho_VSS': range(10),
    }
    for item in log_items:
        log_file_dict[item] = ['%s.log' % item] + ['%s.%s.log' % (item, x) \
                                                   for x in log_item_counts.get(item, range(5))]
    return log_file_dict


def generate_address(spec_area, spec_host):

    # 区域网段
    area_dict = {
        'A': '172.16.72.',
        'B': '172.16.73.',
        'C': '172.16.74.',
        'D': '172.16.75.',
        'E': '172.16.76.',
        'F': '172.16.77.',
        'G': '172.16.78.',
        'H': '172.16.84.',
    }
    # 主机位
    host_dict = {
        'rtspproxy': ['21', '25', '29'],
        'ssm_tianshan': ['21', '25', '29'],
        'mod': ['29'],
        'weiwoo': ['27'],
        'stream1': ['23'],
        'stream2': ['31'],
        'siteadminsvc': ['21'],
    }
    for i in map(lambda x: area_dict[spec_area] + x, [y for y in host_dict[spec_host]]):
        print(i)


generate_address('A', 'rtspproxy')

