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


def replace_relative_path(base_dir, current_dir, command):
    """
    格式化提交的命令中的目录
    通过比对 base_dir(用户家目录), current_dir(当前目录), 用户请求目录 来确定当前操作位于哪个目录
    """
    if base_dir not in current_dir:
        current_dir = base_dir
    command.replace('\\', '/')
    commands = command.split()
    if len(commands) > 1:
        if commands[1] == '.':      # 当前目录
            return current_dir
        elif commands[1] == '..':   # 上层目录
            return os.path.dirname(current_dir)
        elif commands[1] == '/':    # 用户家目录
            return base_dir
        elif commands[1].startswith('/'):   # 将"/"转换为家目录
            the_path = os.sep.join(commands[1].lstrip('/').split('/'))
            return os.path.join(base_dir, the_path)
        else:
            return os.path.join(current_dir, commands[1])
    else:   # 如果用户没有输入目录，则默认为家目录
        return current_dir


def check_input(data):
    """判断用户输入的判断值"""
    if data.lower() == 'y':
        return True
    elif data.lower() == 'n':
        return False
    else:
        return False

