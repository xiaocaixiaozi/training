#/usr/bin/env python
#coding=utf8
#Author: itanony

import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from lib import shopping
from lib import atm
from lib import manager
funcs = {
    "shopping":shopping.shopping,
    "atm":atm.atm,
    "admin": manager.manager
}
while 1:
    for i in range(len(funcs.keys())):
        print( "%s:%s" %(i,list(funcs.keys())[i]))
    user_choice = input("input your choice: ")
    if user_choice.isdigit():
        user_choice = int(user_choice)
        if user_choice in range(len(funcs.keys())):
            funcs[list(funcs.keys())[user_choice]]()
        else:
            print("input err")
    elif user_choice == "q":
        break
    else:
        print("input err")
