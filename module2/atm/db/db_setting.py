#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import sqlite3

db = 'test.db'
user_table = 'users'
lock_table = 'lock'

create_user_sql = '''CREATE TABLE IF NOT EXISTS %s(
    card_num char(15) primary key not null,
    user_name char(10) not null,
    balance int not null,
    age char(3),
    address
);''' % user_table
create_lock_sql = 'CREATE TABLE IF NOT EXISTS %s(card_num char(15) primary key not null);' % lock_table
insert_user_sql = 'INSERT INTO %s values(%s, "%s", %s, %s, "%s");'
insert_lock_sql = 'INSERT INTO %s values(%s);'
update_sql = 'UPDATE %s SET %s = "%s" WHERE card_num = "%s";'
select_sql = 'SELECT * FROM %s WHERE card_num = "%s";'

def close_db(cursor, conn):

    '''
    关闭数据库
    :param cursor: 传入需要关闭的数据库游标
    :param conn: 传入需要关闭的数据库连接
    '''

    cursor.close()
    conn.close()

def create_table(db, create_sql):

    '''
    创建表
    :param db: 要创建的数据库名
    :param create_sql: 要执行的创建数据库的sql语句
    :return: 创建成功返回True，失败则为False
    '''

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    try:
        cur = cursor.execute(create_sql)
    except:
        conn.rollback()
        close_db(cursor, conn)
        return False
    conn.commit()
    close_db(cur, conn)
    return True

def define_sql(the_sql, data, table):

    '''
    格式化sql语句
    :param the_sql: 需要格式化的sql语句
    :param data: 要传入sql语句中的数据，在传入时，格式需为列表
    :param table: 需要操作的表名
    :return: 返回格式化之后的sql语句
    '''

    if table == user_table:
        card_num, user_name, balance, age, address = data
        sql = the_sql % (table, card_num, user_name, balance, age, address)
        return sql
    if table == lock_table:
        return the_sql % (table, data[0])

def insert_table(db, create_table_sql, the_table, insert_sql, data):

    '''
    插入数据
    :param db: 要操作的数据库名
    :param create_table_sql: 创建表的sql语句
    :param the_table: 操作的数据库表名
    :param insert_sql: 插入的sql语句
    :param data: 要插入的数据，users表：[卡号]；lock表：[卡号，用户名，余额，年龄，地址]
    :return: True为插入成功，False则失败
    '''

    create_table(db, create_table_sql)
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    sql = define_sql(insert_sql, data, the_table)
    try:
        cursor.execute(sql)
    except sqlite3.IntegrityError:
        conn.rollback()
        close_db(cursor, conn)
        return False
    conn.commit()
    close_db(cursor, conn)
    return True

def update_table(db, table, update_sql, data):

    '''
    更新数据
    :param db: 要操作的数据库名
    :param table: 要更新的表名
    :param update_sql: 要执行的sql语句
    :param data: 传入需要更新的数据，需要传入列表 [字段名，值，卡号]
    :return: 更新成功返回True，失败则为False
    '''

    column, volue, card_num = data
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    try:
        cursor.execute(update_sql % (table, column, volue, card_num))
    except:
        conn.rollback()
        close_db(cursor, conn)
        return False
    conn.commit()
    close_db(cursor, conn)
    return True

def select_table(db, select_sql, the_table, card_num):

    '''
    查询数据
    :param db: 需要操作的数据库名
    :param select_sql: 执行的查询sql语句
    :param the_table: 需要查询的表名
    :param card_num: 卡号
    :return: 返回查询的结果
    '''

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cur = cursor.execute(select_sql % (the_table, card_num))
    data = cur.fetchall()
    close_db(cursor, conn)
    return data
