#/usr/bin/env python
#coding=utf8
#Author: itanony

import getpass
username = input("Please input username: ")
        #input 输入的默认类型为 string ，输入数字时需要注意转换

password = getpass.getpass("Please input password: ")

print (username,password)
