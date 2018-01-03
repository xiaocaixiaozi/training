#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import importlib

func = importlib.import_module('one.foo')

obj = func.first('bloke')
obj()


