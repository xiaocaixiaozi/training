#/usr/bin/env python
#coding=utf8
#Author: itanony

import sys
import os
#购物车@20171106
'''
salary = input("Please Input Your Salary: ")
if salary.isdigit():
    salary=int(salary)
else:
    print("请重新输入你的工资")
    sys.exit(1)

commodity=[["iphone",5888],["Mac Pro",12888],["Coffee",35],["Python book",100]]
buyed = []
while 1:
    for n in range(len(commodity)):
        print("%d:%s-->%s" %(n,commodity[n][0],commodity[n][1]))

    # for index,item in enumerate(commodity):
    #     print(index,item)

    choice = input("Please Input Number Of What You want:")
    if choice.isdigit():
        choice=int(choice)
        if choice in range(len(commodity)):
            if commodity[choice][1] <= salary:
                salary = salary - commodity[choice][1]
                buyed.append(commodity[choice][0])
                print("----%d" %salary)
            elif commodity[choice][1]> salary:
                print("你买不起%s\n" %commodity[choice][0])
                print(salary)
        else:
            print("输入有误!请重新输入")
    elif choice=="q":
            print("你购买了以下商品：")
            print(",".join(buyed))
            break
    else:
        print("输入有误！请重新输入")
'''
#新版购物车
# 1、商品信息存在文件中
# 2、可以添加商品，修改商品价格





pro_info = "product.list"

identified = input("请输入你的身份，1:商家,0：用户:,q:退出")
s_function = ["添加商品","修改价格"]

def is_float(anum):
    '''判断数是否为小数，不考虑负值'''
    if anum.count(".")==1:
        left = anum.split(".")[0]
        right = anum.split('.')[1]
        if left.isdigit() and right.isdigit():
            return True
    else:
        return False
def modify_price(fname,product_name,new_price):
    with open(fname,"r") as f:
        lines = f.readlines()
    with open(fname,"w") as f:
        for line in lines:
            line=line.strip()
            if product_name in line:
                line = line.replace(line.split(',')[1],new_price)
            f.write("%s\n" %line)
    print("修改价格成功！")

def product_exist(product_name):
    dict1 = {}
    if os.path.exists(pro_info):
        if os.path.getsize(pro_info):
            with open(pro_info, "r") as f:
                for line in f.readlines():
                    dict1[line.split(",")[0]] = line.split(",")[1].strip("\n")
            if product_name in dict1:
                return True
        else:
            return False
    return False

if identified == "1":
    while 1:
        for i in range(len(s_function)):
            print(i,s_function[i])
        s_choice1= input("0添加商品，1修改价格:")
        if s_choice1.isdigit():
            if s_choice1 == "1":
                s_product = input("请输入要修改价格的商品名称:")
                dict_product = {}
                if not product_exist(s_product):
                    print("商品不存在！")
                else:
                    while 1:
                        pro_price = input("请输入商品新价格:")
                        if pro_price.isdigit() or is_float(pro_info):
                            modify_price(pro_info,s_product,pro_price)
                            break
                        else:
                            print("请输入正确的商品价格")

            elif s_choice1 == "0":
                s_nProduct=input("请输入要添加商品的名称")
                s_nprice = input("请输入要添加商品的价格")

                if product_exist(s_nProduct):
                    print("商品%s已经存在，你可以修改价格" % s_nProduct)
                else:
                    with open(pro_info, "a") as f:
                        f.write("%s,%s\n" % (s_nProduct, s_nprice))
                    print("商品添加成功！！")
        elif s_choice1 == "q":
            sys.exit()
        else:
            print("输入有误，请重新输入！！")
elif identified == "0":
    cart=[]
    while True:
        salary = input("请输入你的工资:")
        if salary.isdigit():
            salary = int(salary)
            break
        else:
            print("请重新输入工资")
    while 1:
        with open(pro_info) as f:
            lines = f.readlines()
        for x in range(len(lines)):
            print (x,lines[x].strip())
        c_choice1 = input("输入你要购买商品的编号,[q]退出:")
        if c_choice1.isdigit():
            c_choice1 = int(c_choice1)
            price = int(lines[c_choice1].split(",")[1])
            product = lines[c_choice1].split(",")[0]
            if salary >= price:
                cart.append(product)
                salary -= price
            elif salary < price:
                print("你买不起！！")
        elif c_choice1 == "q":
            print("你买了以下东西")
            print(','.join(cart))
            break
        else:
            print("输入错误，重新输入！")
