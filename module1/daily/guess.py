#/usr/bin/env python
#coding=utf8
#Author: itanony

age = 132
count = 0
while count < 3:
    guess_age = int(input("please input age: "))
    if age == guess_age:
        print("Yes You get it!")
        break
    elif guess_age > age:
        print("think smaller..")
    else:
        print("think bigger..")
    count += 1
else:
    print("try so many times,fuck off...")