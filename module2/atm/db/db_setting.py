#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import sqlite3

db = 'test.db'
user_table = 'users'
lock_table = 'lock'

create_user_sql = '''CREATE TABLE IF NOT EXISTS %s(
    card_num int(15) primary key not null,
    user_name char(10) not null,
    balance int not null,
    age int(3),
    address
);''' % user_table
create_lock_sql = 'CREATE TABLE IF NOT EXISTS %s(card_num int(15) primary key not null);' % lock_table
insert_sql = 'INSERT INTO %s values'
update_sql = 'UPDATE %s SET %s = %s WHERE card_num = %s'
select_sql = 'select * from %s;'

def close_db(cursor, conn):
    cursor.close()
    conn.close()

def create_table(db, create_sql):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    print(create_sql)
    cur = cursor.execute(create_sql)
    conn.commit()
    close_db(cur, conn)

def insert_table(db, create_table_sql, insert_sql):
    create_table(db, create_table_sql)
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    try:
        cursor.execute(insert_sql)
    except sqlite3.ProgrammingError:
        conn.rollback()
        close_db(cursor, conn)
        return False
    conn.commit()
    close_db(cursor, conn)
    return True

def update_user_table(db, table, update_sql, data):
    column, volue, card_num = data
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    try:
        cur = cursor.execute(update_sql % (table, column, volue, card_num))
    except:
        conn.rollback()
        close_db(cursor, conn)
        return False
    conn.commit()
    close_db(cursor, conn)
    return True

def select_table(db, table, select_sql):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cur = cursor.execute(select_sql)
    data = cur.fetchall()
    close_db(cursor, conn)
    return data
