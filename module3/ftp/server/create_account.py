#!/usr/bin/env python
# coding=utf-8
# Author: bloke
# 创建账户

import hashlib
from .read_config import GetConfig
import os
import logging
import getpass
from .ftp_tools import record_log


class CreateAccount(GetConfig):
    """创建ftp账号，如果账号存在，则只修改密码"""
    def __init__(self, username):
        super().__init__(os.path.join(super().CONFIGDIR, 'config.ini'))
        self.username = username
        self.password = ''
        self.config_shadow_file = super().get_config('account').get('shadow_file')
        self.shadow_path = super().CONFIGDIR + os.path.sep + self.config_shadow_file
        self.logger = record_log(logging.INFO)
        self.root_dir = super().BASEDIR + os.sep + 'dirs' + os.sep + self.username

    @staticmethod
    def generate_pass():
        """获取输入的密码"""
        for i in range(3):
            password = getpass.getpass('New Password: ').strip()
            if not password:
                continue
            else:
                check_password = getpass.getpass('Retype Password: ').strip()
                if password == check_password:
                    return password
                else:
                    return False
        else:
            return False

    def hash_password(self):
        """
        通过调用generate_pass方法，获取明文密码，之后通过md5加密
        """
        password_data = self.generate_pass()
        if not password_data:
            return False
        else:
            md5 = hashlib.md5()
            md5.update(password_data.encode('utf-8'))
            self.password = md5.hexdigest()

    def close(self):
        """将账号密码写入shadow文件中,shadow文件必须存在，而且password这个section必须存在"""
        shadow_info = GetConfig(self.shadow_path)
        shadow_config = shadow_info.set_config()
        shadow_config.set('password', self.username, self.password)
        print('Create "%s" success.' % self.username)
        self.logger.info('Create "%s" success.' % self.username)
        with open(self.shadow_path, 'w') as f:
            shadow_config.write(f)

    def create_home(self):
        """创建家目录，如果账户已存在(家目录已存在)，则不执行"""
        if not os.path.exists(self.root_dir):
            os.mkdir(self.root_dir)
            with open(os.path.join(self.root_dir, '%s.md' % self.username), 'w') as f:
                f.write('Welcome %s.' % self.username)

    def __del__(self):
        del self.username


def create(username):
    account = CreateAccount(username)
    sign = account.hash_password()
    if sign is False:
        print('操作失败')
        return False
    account.create_home()
    account.close()
    return True

