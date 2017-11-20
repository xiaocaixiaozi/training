# /usr/bin/env python
# coding=utf8
# Author: itanony

db = 'info.txt'


def user_exit(name):
    '判断用户名是否存在'
    with open(db, 'r') as f:
        for line in f.readlines():
            if name == line.split(" ")[0]:
                return True


def search(username, ):
    if user_exit(username):
        with open(db, 'r') as f:
            for line in f.readlines():
                if username in line:
                    print(line.split(' ')[1])
    else:
        print("用户不存在")


def modify(username, salary=''):
    if user_exit(username):
        new_salary = input("Please input salary:")
        with open(db, "r") as f:
            lines = f.readlines()
        with open(db, "w") as f:
            for line in lines:
                if username in line:
                    line = "%s %s\n" % (username, new_salary)
                f.write(line)
        print("修改成功")
    else:
        print("用户不存在")


def add(username, salary=''):
    if not user_exit(username):
        salary = input("Please input salary:")
        with open(db, 'a', encoding='utf8') as f:
            f.write("%s %s\n" % (username, salary))
        print("添加成功")
    else:
        print("用户已经存在")

func_dict = [
    ["查询用户", search],
    ["修改用户", modify],
    ["添加用户", add],
]

while 1:
    for n in range(len(func_dict)):
        print(n,func_dict[n][0])
    choice = input("Please Input Your Choice,[q] for exit>> ")

    if int(choice) in range(len(func_dict)):
        username = input("请输入用户名>> ")
        func_dict[int(choice)][1](username)
    elif choice == 'q':
        break
    else:
        print("输入有误,重新输入")
