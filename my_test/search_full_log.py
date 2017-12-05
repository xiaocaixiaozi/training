#!/usr/bin/env python
# coding=utf-8
# Author: bloke
# Subject: search tianshan log

"""
    问题： 多线程执行时，每个线程拿的数据串了。。。
"""

import os
import re
import datetime
import time
from multiprocessing.dummy import Pool as ThreadPool


class GETLOGINFO(object):
    """
    获取日志文件的绝对路径
    """
    log_file_dict = {}
    hosts_list = []  # 记录日志的主机地址
    dir_path = r'\c$\TianShan\logs'  # 日志远程访问路径
    siteadminsvc_list, the_mod_info, weiwoo_list, weiwoo_path, pho_vss, pho_erm, nss_log = \
        [], [], [], [], [], [], []
    # 定义正则表达式
    re_time = re.compile(r'(\d{2}:\d{2}):')
    re_session = re.compile(r'processed: session\[([\d\]]+)]')
    re_stream_session = re.compile(r'STREAM\/(\S*)')
    re_stream_num = re.compile(r'-h (\S*)\ -p (\S*)')
    re_weiwoo_session = re.compile(r'weiwoo session\((\w+)\)')
    re_mod_session = re.compile(r'ModPur\/(\S*)')
    re_socket = re.compile(r'(\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d*)')

    def __init__(self, card_num, spec_time, range_time, spec_area):
        self.info_socket, self.info_tianshan = [self.my_call('RtspProxy')], [self.my_call('ssm_tianshan')]
        self.card_num = card_num  # 要搜索的卡号
        self.spec_time = spec_time  # 指定大约时间
        self.range_time = range_time  # 指定的时间范围
        self.spec_area = spec_area  # 指定的区域
        self.re_number = re.compile(r'%s' % self.card_num)  # 匹配卡号
        # 日志模块
        self.log_items = ['RtspProxy', 'ssm_tianshan_s1', 'MODSvc', 'weiwoo', 'Path', 'pho_VSS', 'pho_ERM', \
                          'SiteAdminSvc', 'NSS2', 'NSS', 'NSS3', 'NSS4']
        # 每个日志模块对应的文件数，默认为5个(range(5))
        self.log_item_counts = {
            'ssm_tianshan_s1': range(10),
            'Path': range(10),
            'pho_VSS': range(10),
        }
        # 根据区域，定义主机地址的网络位
        self.area_dict = {
            'A': '172.16.72.',
            'B': '172.16.73.',
            'C': '172.16.74.',
            'D': '172.16.75.',
            'E': '172.16.76.',
            'F': '172.16.77.',
            'G': '172.16.78.',
            'H': '172.16.84.',
        }
        # 根据查询模块，定义主机地址的主机位
        self.mod_dict = {
            'rtspproxy': ['21', '25', '29'],
            'ssm_tianshan': ['21', '25', '29'],
            'mod': ['29'],
            'weiwoo': ['27'],
            'stream1': ['23'],
            'stream2': ['31'],
            'siteadminsvc': ['21'],
        }
        for item in self.log_items:  # 日志文件字典，记录每个日志模块各自对应的日志文件
            self.log_file_dict[item] = ['%s.log' % item] + ['%s.%s.log' % (item, x) \
                                                            for x in self.log_item_counts.get(item, range(5))]
        file_mod_relate_dict = {  # 记录查询模块对应的日志模块
            'rtspproxy': self.log_file_dict['RtspProxy'],
            'ssm_tianshan': self.log_file_dict['ssm_tianshan_s1'],
            'mod': self.log_file_dict['MODSvc'],
            'weiwoo': {
                'weiwoo': self.log_file_dict['weiwoo'],
                'path': self.log_file_dict['Path'],
                'pho_vss': self.log_file_dict['pho_VSS'],
                'pho_erm': self.log_file_dict['pho_ERM']
            },
            'stream1': {
                'NSS': self.log_file_dict['NSS'],
                'NSS2': self.log_file_dict['NSS2']
            },
            'stream2': {
                'NSS3': self.log_file_dict['NSS3'],
                'NSS4': self.log_file_dict['NSS4']
            },
            'siteadminsvc': self.log_file_dict['SiteAdminSvc']
        }
        self.file_mod_relate_dict = file_mod_relate_dict
        # 文件路径
        self.mod_abs_path = self.generate_address('mod')  # 获取日志路径<dict: {host: file_paths}>
        self.siteadmin_abs_path = self.generate_address('siteadminsvc')
        self.weiwoo_abs_path = self.generate_address('weiwoo', 'weiwoo')
        self.path_abs_path = self.generate_address('weiwoo', 'path')
        self.vss_abs_path = self.generate_address('weiwoo', 'pho_vss')
        self.erm_abs_path = self.generate_address('weiwoo', 'pho_erm')

    @staticmethod
    def my_exit(content=''):
        print('Error:', content)
        for i in reversed(range(15)):
            print('[ %s seconds after the exit. ]' % i, end='\r')
            time.sleep(1)
        else:
            os._exit(1)

    @staticmethod
    def my_call(content=''):
        return content.center(50, '*')

    def generate_address(self, spec_mod, sign=''):
        file_abs_path = {}
        for i in map(lambda x: self.area_dict[self.spec_area] + x, [y for y in self.mod_dict[spec_mod]]):
            self.hosts_list.append(i)
        for the_host in self.hosts_list:
            file_abs_path[the_host] = []
            file_l = self.file_mod_relate_dict[spec_mod]
            if isinstance(file_l, dict):
                try:
                    for the_file in file_l[sign]:
                        file_abs_path[the_host].append(r'\\' + the_host + self.dir_path + os.path.sep + the_file)
                    else:
                        continue
                except KeyError as e:
                    self.my_exit(e)
            else:
                for the_file in file_l:
                    file_abs_path[the_host].append(r'\\' + the_host + self.dir_path + os.path.sep + the_file)
        return file_abs_path

    def search_card_number(self):
        """
        搜索rtspproxy相关信息
        :return: 返回卡号、匹配到的IP地址、匹配到的日志文件
        """
        file_abs_path = self.generate_address('rtspproxy')  # 获取日志路径<dict: {host: file_paths}>
        info_card_number = []
        for the_ip, files in file_abs_path.items():
            for the_file in files:
                with open(the_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if self.re_number.findall(line):
                            log_time = self.re_time.findall(line)[0]
                            # 根据给定的时间范围，来匹配此时间段内的事件
                            if abs((datetime.datetime.strptime(self.spec_time, '%H:%M') - \
                                            datetime.datetime.strptime(log_time, '%H:%M')).total_seconds()) < float(
                                self.range_time):
                                info_card_number.append(line)
                    else:
                        # 匹配即退出循环，如果此文件匹配到相关信息，则跳出循环
                        if len(info_card_number) > 0:
                            # 返回对应卡号和时间点的信息，日志文件所在机器的IP地址，匹配到信息的日志文件名
                            return info_card_number, the_ip, the_file
        else:
            self.my_exit('没有匹配到相关信息...')

    def search_socket(self, n=0):
        """
        从得到的卡号的相关信息中匹配出进程相关信息
        :param n: 如果从rtspproxy日志中匹配到多条SETUP记录，会让用户选择需要查询那条SETUP，默认为第一条
        :return: 返回socket相关信息<列表>，session号，IP地址
        """
        info_card_number, the_ip, the_file = self.search_card_number()
        # 如果在指定卡号和时间内，匹配出多行信息，需要用户输入序号
        if len(info_card_number) > 1:
            for l in enumerate(info_card_number):
                print(l)
            try:
                n = int(input('Number: ').strip())
                info_socket_num = self.re_socket.findall(info_card_number[n])[0]
            except KeyboardInterrupt as e:
                self.my_exit('Input error.')
            except IndexError as e:
                self.my_exit("Please enter the correct serial number ! [%s]" % e)
            except TypeError as e:
                self.my_exit("Please enter the correct serial number ! [%s]" % e)
        else:
            print(info_card_number[n])
            try:
                info_socket_num = self.re_socket.findall(info_card_number[n])[0]
            except IndexError as e:
                self.my_exit('No relevant information. [ %s ]' % e)
        with open(the_file, 'r', encoding='utf-8') as f:
            for line in f:
                if info_socket_num in line:
                    self.info_socket.append(line)
        if not self.info_socket:
            self.my_exit('No socket information.')
        else:
            for socket_item in self.info_socket:
                if self.re_session.findall(socket_item):
                    try:
                        session_num = self.re_session.findall(socket_item)[0]
                    except IndexError as e:
                        pass
        return session_num, the_ip

    def search_ssm_tianshan(self):
        """
        通过rtspproxy日志中搜索出的session号，到ssm_tianshan日志中查找相关信息
        :return: 返回从ssm_tianshan中查到的日志<列表>
        """
        session_num, the_ip = self.search_socket()
        tianshan_abs_path = self.generate_address('ssm_tianshan')  # 获取日志路径<dict: {host: file_paths}>
        for ssm_file in tianshan_abs_path[the_ip]:
            with open(ssm_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if session_num in line:
                        self.info_tianshan.append(line)

    def search_id(self):
        """
        在ssm_tianshan日志中搜索到的相关信息中，查找nss、weiwoo、mod等session number
        将nss、weiwoo、mod、nss的主机名、nss的端口作为全局变量
        """
        self.search_ssm_tianshan()
        stream_session, weiwoo_session, mod_session, stream_h, stream_p = '', '', '', '', ''
        for i in self.info_tianshan:
            if self.re_stream_session.findall(i):
                stream_session = self.re_stream_session.findall(i)[0]
                if self.re_stream_num.findall(i):
                    stream_h, stream_p = self.re_stream_num.findall(i)[0]
            if self.re_weiwoo_session.findall(i):
                weiwoo_session = self.re_weiwoo_session.findall(i)[0]
            if self.re_mod_session.findall(i):
                mod_session = self.re_mod_session.findall(i)[0]
        self.stream_session = stream_session
        self.weiwoo_session = weiwoo_session
        self.mod_session = mod_session
        self.stream_h = stream_h
        self.stream_p = stream_p

    def search_mod_info(self):
        self.the_mod_info = [self.my_call('MOD')]
        if self.mod_session:
            for the_ip, file_f in self.mod_abs_path.items():
                for file_n in file_f:
                    with open(file_n, 'r', encoding='utf-8') as f:
                        for line in f:
                            if self.mod_session in line:
                                self.the_mod_info.append(line)
                    if len(self.the_mod_info) > 1:
                        break
                if len(self.the_mod_info) > 1:
                    break

    def search_weiwoo_siteadminsvc_log(self):
        self.siteadminsvc_list = [self.my_call('Siteadminsvc')]
        if self.weiwoo_session:
            for the_ip, items in self.siteadmin_abs_path.items():
                for item in items:
                    with open(item, 'r', encoding='utf-8') as f:
                        for line in f:
                            if self.weiwoo_session in line:
                                self.siteadminsvc_list.append(line)
                    if len(self.siteadminsvc_list) > 1:  # 匹配即停止，跳出循环
                        break
                if len(self.siteadminsvc_list) > 1:
                    break
                    # return self.siteadminsvc_list

    def search_weiwoo_weiwoo_log(self):
        self.weiwoo_list = [self.my_call('Weiwoo')]
        print(self.weiwoo_abs_path)
        if self.weiwoo_session:
            for host_file_list in self.weiwoo_abs_path:
                for item in host_file_list:
                    print(item)
                    with open(item, 'r', encoding='utf-8') as f:
                        for line in f:
                            if self.weiwoo_session in line:
                                self.weiwoo_list.append(line)
                    if len(self.weiwoo_list) > 1:
                        break
                        # return weiwoo_list

    def search_weiwoo_path_log(self):
        self.weiwoo_path = [self.my_call('Weiwoo_path')]
        if self.weiwoo_session:
            for host_file_list in self.path_abs_path:
                for item in host_file_list:
                    print(item)
                    with open(item, 'r', encoding='utf-8') as f:
                        for line in f:
                            if self.weiwoo_session in line:
                                self.weiwoo_path.append(line)
                    if len(self.weiwoo_path) > 1:
                        break
                        # return weiwoo_path

    def search_weiwoo_pho_vss_log(self):
        self.pho_vss = [self.my_call('Pho_vss')]
        if self.weiwoo_session:
            for host_file_list in self.vss_abs_path:
                for item in host_file_list:
                    print(item)
                    with open(item, 'r', encoding='utf-8') as f:
                        for line in f:
                            if self.weiwoo_session in line:
                                self.pho_vss.append(line)
                    if len(self.pho_vss) > 1:
                        break
                        # return pho_vss

    def search_weiwoo_pho_erm_log(self):
        self.pho_erm = [self.my_call('Pho_erm')]
        if self.weiwoo_session:
            for host_file_list in self.erm_abs_path:
                for item in host_file_list:
                    print(item)
                    with open(item, 'r', encoding='utf-8') as f:
                        for line in f:
                            if self.weiwoo_session in line:
                                self.pho_erm.append(line)
                    if len(self.pho_erm) > 1:
                        break
                        # return pho_erm

    def search_stream_info(self):
        self.nss_log = [self.my_call('NSS')]
        if self.stream_session != '':
            if self.stream_h == 'sss6_ss_cl':
                sign1 = 'stream2'
                if self.stream_p == '10800':
                    sign2 = 'NSS3'
                else:
                    sign2 = 'NSS4'
            else:
                sign1 = 'stream1'
                if self.stream_p == '20800':
                    sign2 = 'NSS2'
                else:
                    sign2 = 'NSS'
            if sign1 == 'stream2':
                stream2_file_abs_path = self.generate_address(sign1, sign2)
                for the_ip, file_l in stream2_file_abs_path.items():
                    for file_n in file_l:
                        with open(file_n, 'r', encoding='utf-8') as f:
                            for line in f:
                                if self.stream_session in line:
                                    self.nss_log.append(line)
                        if len(self.nss_log) > 1:
                            break
                    if len(self.nss_log) > 1:
                        break
            else:
                stream1_file_abs_path = self.generate_address(sign1, sign2)
                for the_ip, file_l in stream1_file_abs_path.items():
                    for file_n in file_l:
                        with open(file_n, 'r', encoding='utf-8') as f:
                            for line in f:
                                if self.stream_session in line:
                                    self.nss_log.append(line)
                        if len(self.nss_log) > 1:
                            break
                    if len(self.nss_log) > 1:
                        break
                        # return nss_log


if __name__ == '__main__':
    try:
        while 1:  # 输入卡号
            card_num = input('Card Number: ').strip()
            if card_num:
                break
        while 1:  # 输入时间点
            spec_time = input('Time [HH:MM]: ').strip()
            if not spec_time:
                continue
            if not re.match(r'(\d{2}:\d{2})', spec_time):
                print("Invalid time format !")
                continue
            else:
                break
        while 1:  # 输入时间范围
            range_time = input('Range time [min]: ').strip()
            if not range_time or not range_time.isdigit():
                continue
            else:
                range_time *= 60
                break
        while 1:  # 输入区域
            spec_area = input('Area: ').strip().upper()
            if not spec_area:
                continue
            else:
                break
    except KeyboardInterrupt as e:
        GETLOGINFO.my_exit('Exit')
    # card_num, spec_time, range_time, spec_area = '1370495919', '11:30', '2', 'A'
    search_log = GETLOGINFO(card_num, spec_time, range_time, spec_area)  # 实例化
    print(search_log.generate_address('mod'))
    search_log.search_id()  # 从ssm_tianshan日志中搜索session_id
    pool = ThreadPool()
    for thread in [search_log.search_mod_info, search_log.search_weiwoo_siteadminsvc_log, \
                   search_log.search_weiwoo_weiwoo_log, search_log.search_weiwoo_path_log, \
                   search_log.search_weiwoo_pho_vss_log, search_log.search_weiwoo_pho_erm_log]:
        pool.apply_async(thread)
    pool.close()
    pool.join()
    with open('log_%s.txt' % str(card_num), 'w', encoding='utf-8') as log_file:
        for item in [search_log.info_socket, search_log.info_tianshan, search_log.siteadminsvc_list,
                     search_log.the_mod_info,search_log.weiwoo_list, search_log.weiwoo_path, \
                     search_log.pho_vss, search_log.pho_erm, search_log.nss_log]:
            for line in item:
                log_file.write(line)

    # search_log.search_id()  # 从ssm_tianshan日志中搜索session_id
    # search_log.search_mod_info()                    # mod日志
    # search_log.search_weiwoo_siteadminsvc_log()     # siteadmin日志
    # search_log.search_weiwoo_weiwoo_log()           # weiwoo日志
    # search_log.search_weiwoo_path_log()             # path日志
    # search_log.search_weiwoo_pho_vss_log()          # pho_vss日志
    # search_log.search_weiwoo_pho_erm_log()          # pho_erm日志
    # search_log.search_stream_info()                 # nss日志

