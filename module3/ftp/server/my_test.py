#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import os

size = 0
for lsroot, lsdir, lsfile in os.walk('..\\dirs'):
    if lsfile:
        for f in lsfile:
            size += os.path.getsize(os.path.join(lsroot, f))
