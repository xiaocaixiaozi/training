#!/usr/bin/env python
# coding=utf-8
# Author: bloke

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sample',
    version='1.0',
    description='Test project.',
    long_description=long_description,
    url='https://github.com/xiaocaixiaozi/training/tree/bloke/module2/atm',
    author='Bloke',
    author_email='bloke_anon@126.com',
    license='MIT',
    keywords='sample atm development',
    packages=find_packages(),
    install_requires=[''],
)
