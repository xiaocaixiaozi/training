#/usr/bin/env python
#coding=utf8
#Author: itanony

#20171028第一版本,
n = 1
while n <= 3:
    user_name = raw_input("Please Input UserName:")
    password = raw_input("Please Input Password:")
    if user_name == 'admin' and password == 'admin':
        print ("welcome! now ,do something!")
        break
    else:
        print ("用户名密码错误，请重新输入\n你还有%s次机会") %(3-n)
        n += 1