#!/usr/bin/env python
# coding=utf-8
# Author: bloke
# test xml module

from xml.etree import ElementTree as et

tree = et.parse('test2.xml')
root = tree.getroot()
for key in root:
    for subkey in key:
        if subkey.text == ' test':
            subkey.text = 'bloke'

tree.write('test2.xml', encoding='utf-8',)




