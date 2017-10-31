#!/usr/bin/env python
# coding=utf-8
# Author: bloke
# Project: 购物车

while 1:
    salary = input('Salary: ').strip()
    if salary.isdigit():
        salary = int(salary)
        break
shopping_dict = {
    'Iphone6': '5000',
    'Iphone6plus': '5500',
    'Honor6': '1100',
    'Mi5': '2000',
}
storage_rack = {}
for num, item in enumerate(shopping_dict.keys()):
    storage_rack[str(num)] = item
shopping_list = []

while 1:
    for key in storage_rack.keys():
        print(key + '  ' + storage_rack[key] + ' [' + shopping_dict[storage_rack[key]] + ' ]')
    else:
        print('Usage: Num to join; q to quit'.center(60, '-'))
    choice = input('Shopping: ').strip()
    if choice == 'q':
        break
    if choice == 'p':
        for i in shopping_list:
            print(i)
        else:
            choice = input('Shopping: ').strip()
            if choice == 'q':
                break
    if not choice or not choice.isdigit():
        continue
    if choice.isdigit() and choice in storage_rack:
        if int(choice) <= salary:
            print('You purchased %s success.' % storage_rack[choice])
            shopping_list.append([storage_rack[choice], shopping_dict[storage_rack[choice]]])
            salary -= int(shopping_dict[storage_rack[choice]])
        else:
            print('余额不足'.encode('utf-8'))
            continue

print('Your balance is %s.\nYour shopping carts has:' % salary)
for product in shopping_list:
    print(product)

