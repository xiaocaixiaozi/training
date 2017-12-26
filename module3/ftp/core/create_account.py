#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import hashlib
from .read_config import GetConfig
import os


class CreateAccount(GetConfig):
    """创建ftp账号"""
    def __init__(self, username):
        super().__init__(os.path.join(super().CONFIGDIR, 'config.ini'))
        self.username = username
        self.password = ''
        self.config_shadow_file = super().get_config('account').get('shadow_file')
        self.shadow_path = super().CONFIGDIR + os.path.sep + self.config_shadow_file

    @staticmethod
    def generate_pass():
        """获取输入的密码"""
        for i in range(3):
            password = input('New Password: ').strip()
            if not password:
                continue
            else:
                check_password = input('Retype Password: ').strip()
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
        print('[%s] 设置密码成功' % self.username)
        with open(self.shadow_path, 'w') as f:
            shadow_config.write(f)

    def __del__(self):
        del self.username


def create(username):
    account = CreateAccount(username)
    sign = account.hash_password()
    if sign is False:
        print('操作失败')
        return False
    account.close()
    return True




