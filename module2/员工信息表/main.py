# /usr/bin/env python
# coding=utf8
# Author: itanony

import sqlite3
import logging

def log(name='sql'):
    logger = logging.Logger(name)
    file_handler = logging.FileHandler('sql.log', 'a', 'utf-8')
    file_handler.setLevel(logging.INFO)
    data_format = logging.Formatter(fmt='%(asctime)s [%(levelname)s] <%(funcName)s> %(message)s',\
                                    datefmt='%Y/%m/%d %H:%M:%S')
    file_handler.setFormatter(data_format)
    logger.addHandler(file_handler)
    return logger

db = table = 'staff'
create_table_sql = '''CREATE TABLE IF NOT EXISTS %s(
    staff_id INT AUTO_INCREMENT,
    name CHAR(30) NOT NULL,
    age CHAR(3) NOT NULL,
    phone CHAR(20) PRIMARY KEY NOT NULL,
    dept CHAR(15) NOT NULL,
    enroll_date DATETIME DEFAULT (DATETIME('now', 'localtime'))
);''' % table    # 创建数据库表

def def_sql(operate):
    if not operate: return False
    if operate == 'insert':
        while 1:
            name = input('Name: ').strip()
            age = input('Age: ').strip()
            phone = input('Tel: ').strip()
            dept = input('Dept: ').strip()
            if False in [bool(x) for x in [name, age, phone, dept]] \
                    or not age.isdigit() or not phone.isdigit() or name.isdigit():
                print('请输入正确信息.')
                continue
            else:
                break
        insert_sql = 'INSERT INTO %s(name, age, phone, dept) VALUES(%s, %s, %s, %s)' % (table, name, age, phone, dept)
        return insert_sql
    elif operate == 'select':
        pass

def conn_db(func):
    def operate(db_name, command):
        logger = log()
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        result = func(cursor, command, logger)
        if result:
            cursor.close()
            conn.commit()
            conn.close()
            return result
        else:
            conn.rollback()
            cursor.close()
            conn.close()
            return result
    return operate

@conn_db
def operate_sql(cursor, command, logger):
    logger.info(command)
    try:
        cursor.execute(command)
    except sqlite3.OperationalError as e:
        logger.error(e)
        return False
    return True

