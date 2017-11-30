#!/usr/bin/env python
# coding=utf-8
# Author: bloke
# Subject: copy-like

import os
import datetime
import re
import shutil
import sys
import logging


def generate_logger(log_file='copy.log'):
    """
    生成日志对象
    :param log_file: 日志文件名<绝对路径>
    :return: 返回日志对象
    """
    logger = logging.Logger('copy')
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_file)
    log_format = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s', \
                                   datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    return logger


def do_record(func):
    logger = generate_logger()

    def do_action(*args):
        result = func(*args, logger)
        return result

    return do_action


def generate_time(date=None):
    """
    获取时间，如果没有传入date参数，则默认为当前时间
    :param date: 传入的时间，格式为: "2017-11-30 11:10:00"， 类型必须为str
    :return: 返回格式化后的时间字符串
    """
    if date:
        the_date = datetime.datetime.strptime(date, '%Y-%d-%m %H:%M:%S').strftime('%Y%m%d')
    else:
        the_date = datetime.datetime.now().strftime('%y%m%d')
    return the_date


@do_record
def get_file_path(source_dir, the_time, the_re, logger):
    """
    获取源目录下的文件列表，获取的文件必须是'.xml'结尾，指定的日期格式开头
    :param source_dir: 源目录
    :return: 返回文件列表，绝对路径
    """
    base_dir = os.path.abspath(source_dir)
    the_files = [os.path.join(base_dir, x) for x in os.listdir(source_dir) \
                 if os.path.isfile(os.path.join(base_dir, x)) and x.endswith('.xml')]
    file_list = []
    for f in the_files:
        if the_re.findall(f):
            if the_re.findall(f)[0] == the_time:
                file_list.append(f)
    else:
        if not file_list:
            logger.warning('did not match the file.')
            return False
        else:
            return file_list


@do_record
def do_copy(dest_dir, file_list, logger):
    """
    远程拷贝，将指定的文件拷贝到远程目录
    :param dest_dir: 远程目录
    :param file_list: 文件列表
    :return: 拷贝成功返回True，否则返回False
    """
    if not os.path.exists(dest_dir):
        logger.error('The target directory do not exist... [ %s ]' % dest_dir)
        logger.info(datetime.datetime.now().strftime('%Y/%m/%d_%H:%M:%S').center(50, '*'))
        sys.exit(1)
    for source_f in file_list:
        try:
            logger.info('start copy %s to %s.' % (source_f, dest_dir))
            shutil.copy(source_f, dest_dir)
            logger.info('copy %s to %s success.' % (source_f, dest_dir))
        except FileNotFoundError as f:
            logger.info('copy %s to %s failed, because: %s' % (source_f, dest_dir, f))
        except:
            return False
    else:
        logger.info('Copy Successful.')
        return True


@do_record
def do_backup(file_list, bak_dir, logger):
    """
    本地备份，将拷贝成功的文件移动到本地目录(目录名为指定的日期)
    :param file_list: 远程拷贝成功的文件列表
    :param bak_dir: 本地备份目录
    :return: 备份成功，返回True，否则返回False
    """
    if not os.path.exists(bak_dir):
        os.mkdir(bak_dir)
        logger.info('create backup directory [ %s ]' % bak_dir)
    for source_f in file_list:
        try:
            logger.info('start backup %s to %s.' % (source_f, bak_dir))
            shutil.move(source_f, bak_dir)
            logger.info('backup %s to %s success.' % (source_f, bak_dir))
        except FileNotFoundError as f:
            logger.error('backup %s to %s failed, because %s' % (source_f, bak_dir, f))
        except:
            logger.error('backup %s to %s failed.')
    else:
        logger.info('Backup Successful.')
        return True


if __name__ == '__main__':
    require_time = generate_time()      # 需要备份的文件日期，从文件名获取
    source_path = r'D:\epg'     # 文件源路径
    local_bak_dir = os.path.join(source_path, datetime.datetime.strptime(\
        require_time, '%y%m%d').strftime('%Y-%m-%d'))  # 本地备份路径
    remote_dest_dir = 'D:\epgbak'       # 远程拷贝路径
    file_re = re.compile(r'Gehua.com_GEHU\d{3}(\d{6})')     # 匹配文件名中包含 require_time 变量的文件
    files = get_file_path(source_path, require_time, file_re)
    if not files:
        sys.exit(0)
    copy_sign = do_copy(remote_dest_dir, files)
    if copy_sign:
        mv_sign = do_backup(files, local_bak_dir)
