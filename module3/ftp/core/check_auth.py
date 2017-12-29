#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import os
import sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASEDIR)
from core import read_config


# if __name__ == '__main__':
config = read_config.GetConfig(BASEDIR + os.sep + 'conf' + os.sep + 'shadow')
auth = config.get_config('password')
print('user02' in auth)