#/usr/bin/env python
#coding=utf8
#Author: itanony

#20171028第一版本,
# n = 1
# while n <= 3:
#     user_name = raw_input("Please Input UserName:")
#     password = raw_input("Please Input Password:")
#     if user_name == 'admin' and password == 'admin':
#         print ("welcome! now ,do something!")
#         break
#     else:
#         print ("用户名密码错误，请重新输入\n你还有%s次机会") %(3-n)
#         n += 1
#201710209第二版本
import csv
import os
import getpass
n = 0
dict1={}
while n < 3:
    username = input("Please input username: ")
    password = input("Please input password: ")
    #password = getpass.getpass("Please input password")
    f = open("badlist",'r')
    if username in [x.strip(os.linesep) for x in f.readlines()]:
        print(username+" locked")
        break
    f.close()
    with open('passwd.csv','r') as f:
        for line in f.readlines():
            dict1[line.split(",")[0]]=line.split(",")[1].strip("\n")

        if username in dict1.keys() and password == dict1[username]:
            print("welcome sir,do somethings!")
            break
        else:
            print("invalid username or pass,check it!")
            n += 1
else:
    print(username)
    print("user locked.fuck off!")
    with open("badlist",'w') as f:
        f.write(username)