#!/usr/bin/env python
# coding=utf-8
# Author: bloke

from .read_config import GetConfig
import hashlib


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
