#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import configparser
import time
import sys
import subprocess
import shutil
import os


class VPN(object):

    def __init__(self, sign):
        self.sign = sign
        self.ip_addr = ''
        self.port = ''
        self.auto_login = 0

    @staticmethod
    def generate_config(filename=r'..\vpn.ini'):
        """
        生成配置文件
        :param filename: 配置文件名
        """
        switch_vpn = configparser.ConfigParser()
        switch_vpn['offical_vpn'] = {
            'IP_ADDR': 'ip',
            'PORT': 'port',
            'AUTO_LOGIN': '0',
            'USER_NAME': 'bloke',
            'PASSWORD': 'bloke_pass'
        }
        switch_vpn['lab_vpn'] = {
            'IP_ADDR': 'ip',
            'PORT': 'port',
            'AUTO_LOGIN': '0',
            'USER_NAME': 'bloke',
            'PASSWORD': 'bloke_pass'
        }
        with open(filename, 'w') as configfile:
            switch_vpn.write(configfile, space_around_delimiters=True)

    def read_config(self, sign, filename=r'..\vpn.ini'):
        config = configparser.ConfigParser()
        config.read(filename, encoding='utf-8')
        try:
            vpn_info = config[sign]
        except KeyError as e:
            self.my_exit(e)
        self.ip_addr = vpn_info['ip_addr']
        self.port = vpn_info['port']
        self.auto_login = vpn_info['auto_login']
        self.user_name = vpn_info['user_name']
        self.password = vpn_info['password']

    def write_config(self, filename=r'..\sslvpn.ini'):
        shutil.copy(filename, '%s.bak' % filename)
        vpn = configparser.ConfigParser()
        vpn.read(filename, encoding='utf-8')
        vpn['VpnConnect']['Hostname'] = self.ip_addr
        vpn['VpnConnect']['Port'] = self.port
        vpn['AccountAuth']['Account'] = self.user_name
        vpn['AccountAuth']['Password'] = self.password
        vpn['PreferencesSetting']['AutoLogin'] = self.auto_login
        with open(filename, 'w') as configfile:
            vpn.write(configfile, space_around_delimiters=False)

    @staticmethod
    def my_exit(content=''):
        """
        静态方法，所有退出时调用
        :param content: 退出时需要打印的内容
        """
        print('Error:', content)
        for i in reversed(range(8)):
            print('[ %s seconds after the exit. ]' % i, end='\r')
            time.sleep(1)
        else:
            sys.exit(1)

    @staticmethod
    def stop_process():
        status, output = subprocess.getstatusoutput('taskkill /F /IM sslvpn-client.exe"')
        return status

    @staticmethod
    def start_process():
        status, output = subprocess.getstatusoutput('..\sslvpn-client.exe')
        return status


if __name__ == '__main__':
    new_config_file = r'..\vpn.ini'
    if not os.path.exists(new_config_file):
        VPN.generate_config()
        VPN.my_exit('请修改配置文件: [ %s ]' % new_config_file)
    choice_dict = {'1': 'offical_vpn', '2': 'lab_vpn'}
    for key in choice_dict:
        print(key, ': ', choice_dict[key])
    while 1:
        choice = input('Choice: ').strip()
        if choice not in choice_dict:
            continue
        else:
            sign = choice_dict[choice]
            break
    bloke = VPN(sign)
    bloke.read_config(sign)
    if not bloke.ip_addr or not bloke.port or not bloke.auto_login or not \
            bloke.user_name or not bloke.password:
        bloke.my_exit('读取配置失败')
    bloke.write_config()
    stop_status = bloke.stop_process()
    if stop_status != 0:
        stop_status = bloke.stop_process()
        if stop_status != 0:
            bloke.my_exit('进程终止失败')
    start_status = bloke.start_process()
    if start_status != 0:
        bloke.my_exit('进程启动失败')
    time.sleep(2)
    bloke.my_exit('切换成功')
