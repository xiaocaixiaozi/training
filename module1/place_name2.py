#!/usr/bin/env python
# coding=utf-8
# Author: bloke
# Project: 地名分级显示

import requests
import re
import sys


def get_place(url, place_re):   #获取数据
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Maxthon/5.1.1.1000 Chrome/55.0.2883.75 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    try:
        data = place_re.findall(response.text)[0]
        return(data)
    except IndexError as e:
        return(None)


url = 'https://www.douban.com/note/290487992/'
place_re = re.compile(r'<div class="note" id="link-report">(.*?)</div>', re.S)
data = get_place(url, place_re)
if not data: sys.exit()
the_data = re.findall(r'(直辖市)：(.*?)<br><br>(\S{1,2}地区)<br>(.*?)<br><br>(\S{1,2}地区)<br>(.*?)<br><br>(\S{1,2}地区)<br>(.*?)<br><br>(\S{1,2}地区)<br>(.*?)<br><br>(\S{1,2}地区)<br>(.*?)<br><br>(\S{1,2}地区)<br>(.*?)<br>港澳台', data, re.S)
provinces = the_data[0]
provinces_dict = {}

for num in range(2, len(provinces), 2):     # 返回 地区、省、市 字典
    child_dict = {}
    child_data = provinces[num+1].split('<br>')
    if len(child_data) >= 1:
        for item in child_data:
            city, district = item.split('：')
            child_dict[city] = district
        else:
            provinces_dict[provinces[num]] = child_dict
    else:
        provinces_dict[provinces[num]] = provinces[num+1]
'''
province_list = list(provinces_dict.keys())
while 1:
    for num, province in enumerate(province_list):      # 列出地区
        print(str(num) + ' : ' + province)
    else:
        print('-- Usage: q to exit; num to join. --')
    select_province = input('Input Prevince: ').strip()
    if not select_province:
        continue
    if select_province == 'q':
        sys.exit(0)
    try:
        select_province = int(select_province)
        if select_province in range(len(province_list)):
            city_dict = provinces_dict[province_list[select_province]]
            if isinstance(city_dict, dict):
                city_list = list(city_dict.keys())
                while 1:
                    for city_num, city_name in enumerate(city_list):  # 列出省份
                        print(str(city_num) + ' : ' + city_name)
                    else:
                        print('-- Usage: q to exit; b to go up; num to join. --')
                    select_district = input('Input City: ').strip()
                    if select_district == 'q':
                        sys.exit(0)
                    elif select_district == 'b':
                        break
                    try:
                        select_district = int(select_district)
                        if select_district in range(len(city_list)):
                            for the_district in city_dict[city_list[select_district]].split():      # 列出市区
                                print(the_district)
                            else:
                                print('-- Usage: q to exit; b to go up. --')
                                while 1:
                                    the_select = input('Input: ').strip()
                                    if the_select == 'q':
                                        sys.exit(0)
                                    elif the_select == 'b':
                                        break
                                    else:
                                        continue
                    except SystemExit as e:     # 捕获 sys.exit 抛出的 SystemExit 异常
                        sys.exit(0)
                    except:
                        continue
    except ValueError as e:
        continue
'''

def echo_value(the_dict, item_list=[]):
    for num_f, key_f in enumerate(the_dict.keys(), 1):
        print(num_f, key_f)
    while 1:
        key_dict = {}
        for num, key in enumerate(the_dict.keys(), 1):
            key_dict[num] = key
#            print(num, key)
        choice = input('Choice num: ').strip()
        if choice == 'b':
            if len(item_list) <= 1:
                break
            else:
                item_list.pop()
        elif choice == 'q':
            sys.exit(0)
        else:
            try:
                choice = int(choice)
            except ValueError as e:
                print(e)
                continue
        data = the_dict[key_dict[choice]]
        item_list.append(data)
        if isinstance(data, dict):
            echo_value(data, item_list)
        else:
            for item in item_list[-1].split():
                print(item)


echo_value(provinces_dict)



#print(provinces_dict)



















