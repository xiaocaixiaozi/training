#/usr/bin/env python
#coding=utf8
#Author: itanony

db = 'info.txt'
funcs = ['查询',
         '修改',
         '增加',
         '退出']
def user_exit(name):
    with open(db,'r') as f:
        for line in f.readlines():
            if name == line.split(" ")[0]:
                return True

while 1:
    for x in range(len(funcs)):
        print ("%s.%s" %(x,funcs[x]))
    choice = input(">>>")
    if choice.isdigit():
        choice = int(choice)
        if choice == 0:
            username = input("username:")
            if user_exit(username):
                with open(db,mode='r') as f:
                    for line in f:
                        if username in line:
                            print(line.split(" ")[1])
            else:
                print("no such user")
        elif choice == 1:
            username = input("username:")
            if user_exit(username):
                salary = input("new salary:")
                with open(db,"r") as f:
                    lines = f.readlines()
                with open(db,"w") as f:
                    for line in lines:
                        if username in line:
                            line = "%s %s\n" %(username,salary)
                        f.write(line)
                print("修改成功")
            else:
                print("no such user")

        elif choice == 2:
            username = input("username")
            if not user_exit(username):
                salary = input("salary:")
                with open(db,"a") as f:
                    line = "%s %s\n" %(username,salary)
                    f.write(line)
                print("添加成功")
            else:
                print("用户已经存在")

        elif choice == 3:
            print("再见")
            break
    else:
        print("傻逼！重新输入")





