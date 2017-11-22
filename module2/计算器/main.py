#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import re

# data = input('计算: ').strip()
data = '2 * (2 + 3 / (1+2) * (30-2)) - 2 / 3'   # 59.333333333333336

re_brackets = re.compile(r'(\([^()]+\))')   # 匹配小括号


