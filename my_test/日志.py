#!/usr/bin/env python
# coding=utf-8
# Author: bloke
# test logging model

import logging

logger = logging.Logger(__name__)
formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s] %(message)s', datefmt='%y/%m/%d %H:%M:%S')

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)

fh = logging.FileHandler('test.log', 'a', 'utf-8')
fh.setLevel(logging.WARNING)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)

logger.info('info.test')
logger.warning('warning.test')
logger.error('error.test')


