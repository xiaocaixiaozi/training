#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import logging
import multiprocessing
import time

def generate_logger(log_file='copy2.log'):
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


def action_01():
    logger = generate_logger()
    for i in range(20):
        time.sleep(1)
        logger.info('in the action_01...')


def action_02():
    logger = generate_logger()
    for l in range(15):
        time.sleep(2)
        logger.info('in the action_02')


if __name__ == '__main__':
    poll = multiprocessing.Pool(2)
    for i in [action_01, action_02]:
        poll.apply_async(i)
    else:
        poll.close()
        poll.join()
    print('Done.')

