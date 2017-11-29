#!/usr/bin/env python
# coding=utf-8
# Author: bloke
# configparse

import configparser

'''
# write
config = configparser.ConfigParser()
config['DEFAULT'] = {
    'ServerAliveInterval': '45',
    'Compression': 'yes',
    'CompressionLevel': '9'
}
config['bitbucket.org'] = {}
config['bitbucket.org']['User'] = 'hg'
the_config = config['bitbucket.org']
the_config['Port'] = '50022'
the_config['ForwardX11'] = 'no'

with open('example.ini', 'w') as configfile:
    config.write(configfile, space_around_delimiters=True)
'''

'''
# read
config = configparser.ConfigParser()
config.read('example.ini', encoding='utf-8')
bloke = config['bitbucket.org']
ForwardX11 = bloke.getboolean('ForwardX11')
site = bloke.get('site', fallback='bloke')

print(ForwardX11)
print(site)
'''



