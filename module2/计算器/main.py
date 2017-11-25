#!/usr/bin/env python
# coding=utf-8
# Author: bloke
# Subject: Calculator

import re
import sys

def cal(first, operator, second):
    data = '%s%s%s' % (first,operator,second)
    result = eval(data)
    return result

def priority(f_item, s_item):
    f, s = 0, 0
    check_dict = {
        3: '(',
        2: '/*',
        1: '+-',
    }
    for key in check_dict:
        if f_item in check_dict[key]:
            f += key
        if s_item in check_dict[key]:
            s += key
    return f, s

def classify(item_list):
    digital_stack, operator_stack = [], []
    for item in item_list:
        if re.findall(r'\d', item):     # 加入数字栈
            digital_stack.append(item)
        elif not operator_stack:       # 加入操作符栈
            operator_stack.append(item)
        elif operator_stack[-1] == '(':
            operator_stack.append(item)
        elif item == ')':
            while 1:
                ope = operator_stack.pop()
                if not ope: break
                if ope == '(':
                    break
                one, two = digital_stack.pop(-2), digital_stack.pop()
                result = cal(one, ope, two)
                digital_stack.append(result)
        else:
            first, second = priority(operator_stack[-1], item)
            if first > second or first == second:        # 前一个运算符优先于后一个运算符，开始运算
                print(digital_stack, operator_stack)
                result = cal(digital_stack.pop(-2), operator_stack.pop(), digital_stack.pop())
                digital_stack.append(result)
                operator_stack.append(item)
            else:
                operator_stack.append(item)
                continue
    else:
        for n in range(len(operator_stack)):
            result = cal(digital_stack.pop(-2), operator_stack.pop(), digital_stack.pop())
            digital_stack.append(result)        # 将计算后的结果再次加入到数字栈中
    return result

def format(data):
    if re.findall(r'[^\d\-\+\(\)\*\/\s]', data):    # 判断是否有除数字和运算符之外的字符，如果有，则返回False
        return False
    data = re.sub(r'\s+', '', data)     # 去掉空格
    data = re.sub(r'\(\-', '(0-', data)     # 将 '(-' 替换为 '(0-',等于将-10替换为0-10
    data = re.split(r'(\d+|\-|\+|\(|\)|\*|\/)', data)   # 格式化字符，生成列表
    data_list = [x for x in data if x]
    if data_list[0] == '-':     # 判断首字符是否为'-'，如果是，则将前两项字符合并
        data_list[1] = data_list[0] + data_list[1]
        del(data_list[0])
    result = classify(data_list)
    return result

def main(data):
    result = format(data)
    return result

if __name__ == '__main__':
    # data = '-20 * (-2 + 393 / (20 * 3 - 10) - 30) * (20 / 3 - 2)'
    n = 1
    while n <= 3:
        data = input('输入计算公式: ').strip()
        if data:
            break
        else:
            n += 1
            continue
    else:
        sys.exit(1)
    result = main(data)
    print('计算结果为: \033[32;1m%s\033[0m' % result)
