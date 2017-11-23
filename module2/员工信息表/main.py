# /usr/bin/env python
# coding=utf8
# Author: bloke
# Subject: 员工信息表

import sqlite3
import logging
import sys

db, table = 'staff.db', 'staff'
create_table_sql = '''CREATE TABLE IF NOT EXISTS %s(
    staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(30) NOT NULL,
    age CHAR(3) NOT NULL,
    phone CHAR(20) NOT NULL UNIQUE,
    dept CHAR(15) NOT NULL,
    enroll_date DATETIME DEFAULT (DATETIME('now', 'localtime'))
);''' % table    # 创建数据库表

def log(name='sql'):
    '''
    生成日志对象
    :param name: 日志名称
    :return: 返回日志对象
    '''
    logger = logging.Logger(name)
    file_handler = logging.FileHandler('sql.log', 'a', 'utf-8')
    file_handler.setLevel(logging.INFO)
    data_format = logging.Formatter(fmt='%(asctime)s [%(levelname)s] <%(funcName)s> %(message)s',\
                                    datefmt='%Y/%m/%d %H:%M:%S')
    file_handler.setFormatter(data_format)
    logger.addHandler(file_handler)
    return logger

def define_insert_sql():
    '''
    生成insert sql语句
    :return: 返回语句
    '''
    n = 1
    while n <= 3:
        name = input('Name: ').strip()
        age = input('Age: ').strip()
        phone = input('Tel: ').strip()
        dept = input('Dept: ').strip()
        if False in [bool(x) for x in [name, age, phone, dept]] \
                or not age.isdigit() or not phone.isdigit() or name.isdigit():
            print('请输入正确信息.')
            n += 1
            continue
        else:
            break
    insert_sql = 'INSERT INTO %s(name, age, phone, dept) VALUES("%s", "%s", "%s", "%s");' % (table, name, age, phone, dept)
    return insert_sql

def check_staff_id():
    '''
    检测输入的员工ID是否非法
    :return: 如果合法，返回员工ID，否则返回False
    '''
    n = 1
    while n <= 3:
        staff_id = input('员工ID: ').strip()
        if not staff_id or not staff_id.isdigit():
            print('# \033[31;1m未知ID.\033[0m\n')
            n += 1
            continue
        else:
            result = operate_sql('select * from %s where staff_id == "%s";' % (table, staff_id))
            if not result:
                print('# \033[31;1m未知ID.\033[0m\n')
                n += 1
                continue
            else:
                return staff_id
    else:
        return False

def define_delete_sql():
    '''
    生成delete sql语句
    :param staff_id: 员工ID
    :return: 返回语句
    '''
    staff_id = check_staff_id()
    if not staff_id:
        return False
    else:
        delete_sql = 'DELETE FROM %s WHERE staff_id = "%s";' % (table, staff_id)
        return delete_sql

def define_select_sql():
    '''
    生成select sql语句
    :return:
    '''
    n = 1
    select_dict = {
        '1': '员工年龄',
        '2': '部门名称',
        '3': '注册时间'
    }
    for key in select_dict:
        print(key, ' --> ', select_dict[key])

    while n <= 3:
        choice = input('您要根据哪个条件查询: ').strip()
        if choice not in select_dict:
            n += 1
            continue
        else:
            break
    if choice == '1':
        age = input('年龄: ').strip()
        select_sql = 'SELECT * FROM %s WHERE age > "%s";' % (table, age)
        return select_sql
    if choice == '2':
        dept = input('部门: ').strip()
        select_sql = 'SELECT * from %s WHERE dept = "%s";' % (table, dept)
        return select_sql
    if choice == '3':
        enroll_date = input('注册年份: ').strip()
        select_sql = "SELECT * FROM {0} WHERE enroll_date like '%{1}%';".format(table, enroll_date)
        return select_sql

def define_update_sql():
    '''
    生成update语句
    :return: 返回语句
    '''
    sign = 1
    staff_id = check_staff_id()
    if not staff_id:
        return False
    else:
        item_dict = {'1': 'name', '2': 'age', '3': 'phone', '4': 'dept'}
        while sign <= 3:
            for n in range(1, len(item_dict)+1):
                print(n, ':', item_dict[str(n)], end='; ')
            key = input('\n要修改编号: ').strip()
            if key not in item_dict:
                print('非法字段,请重新选择')
                sign += 1
                continue
            else:
                key = item_dict[str(key)]
                break
        value = input('修改的值：').strip()
        update_sql = 'UPDATE %s SET %s = "%s" where staff_id = "%s";' % (table, key, value, staff_id)
        return update_sql

def conn_db(func):
    '''
    链接数据库，作为装饰器使用，在执行操作数据库的函数之前调用
    :param func: 操作数据库的函数
    :return: 返回操作后的结果
    '''
    def operate(command):
        logger = log()
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        result = func(cursor, command, logger)
        try:
            data = result.fetchall()
        except AttributeError as e:
            data = result
        if result:
            cursor.close()
            conn.commit()
            conn.close()
            return data
        else:
            conn.rollback()
            cursor.close()
            conn.close()
            return data
    return operate

@conn_db
def operate_sql(cursor, command, logger):
    '''
    操作数据库
    :param cursor: 数据库游标，由装饰器conn_db传入
    :param command: sql语句
    :param logger: 日志对象，由装饰器传入
    :return: 如果操作成功，返回True，否则返回False
    '''
    logger.info(command)
    try:
        data = cursor.execute(command)
    except sqlite3.OperationalError as e:
        logger.error(e)
        return False
    except sqlite3.IntegrityError as i:
        logger.error(i)
        return False
    except ValueError as v:
        logger.error(v)
        return False
    return data

if __name__ == '__main__':
    while 1:
        operate_dict = {
            '查询': define_select_sql,
            '添加': define_insert_sql,
            '删除': define_delete_sql,
            '修改': define_update_sql
        }
        choice_dict = {
            '1': '查询',
            '2': '添加',
            '3': '删除',
            '4': '修改'
        }
        for n in range(1, len(choice_dict)+1):
            print(str(n) + ': ' + choice_dict[str(n)], end=';  ')
        else:
            print('q:quit.')
    #    operate_sql(create_table_sql)
        num = 1
        while num < 3:
            choice = input('Choice: ').strip()
            if choice == 'q':
                sys.exit(0)
            if choice not in choice_dict:
                num += 1
                continue
            else:
                break
        else:
            sys.exit(1)
        sql = operate_dict[choice_dict[str(choice)]]()
        print('\033[32;1mSQL语句: %s\033[0m' % sql)
        result = operate_sql(sql)
        if choice == '1':
            for item in result:
                staff_id, user_name, age, tel, dept, enroll_date = item
                print('ID: %s | 用户名: %s | 年龄: %s | 电话: %s | 部门: %s | 注册日: %s'\
                      % (staff_id, user_name, age, tel, dept, enroll_date))
            else:
                print(('总共匹配%s条数据' % len(result)).center(80, '*'))
        if result != False:
            print('# \033[32;1m操作成功\033[0m\n')
        else:
            print('# \033[31;1m操作失败\033[0m\n')
        continue
