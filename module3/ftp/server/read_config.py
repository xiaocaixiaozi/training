#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import configparser
import os


class GetConfig(object):
    """
        读取配置[通用],所有配置都在conf目录下，用户只需输入配置文件名即可，
        程序会自动在conf目录下查找
    """
    BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CONFIGDIR = os.path.join(BASEDIR, 'conf')

    def __init__(self, config_path):
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path, encoding='utf-8')

    def get_config(self, item):
        """读取方法"""
        item_info = self.config[item]
        return item_info

    def set_config(self):
        """修改方法，返回ConfigParser对象"""
        return self.config

