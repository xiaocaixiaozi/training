#!/usr/bin/env python
# coding=utf-8
# Author: bloke

from .read_config import GetConfig
import hashlib
import logging
import os


def check_auth(account, password, auth_file):
    """验证登录的账号密码是否在正确"""
    config = GetConfig(auth_file)
    auth = config.get_config('password')
    if account not in auth:
        return False
    elif password != auth[account]:
        return False
    return True


def hash_password(password):
    """加密密码"""
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    hash_password = md5.hexdigest()
    return hash_password


def record_log(log_level):
    """日志记录"""
    LOGDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep + 'logs'
    logger = logging.Logger('FTP')
    fh = logging.FileHandler(os.path.join(LOGDIR, 'ftp.log'), 'a', 'utf-8')
    try:
        fh.setLevel(log_level)
    except ValueError as e:
        print(e)
        return False
    formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s] %(lineno)s %(message)s', \
                                  datefmt='%y/%m/%d %H:%M:%S')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


def check_root(basedir, current_dir):
    """不可切换目录，判断用户当前目录是否在根目录内，在，则返回True，否则返回False"""
    if basedir not in current_dir:
        return False
    else:
        return True

