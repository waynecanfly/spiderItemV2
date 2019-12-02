#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/9/20 16:01
import pymysql


def toUpdate(cursor, table, item, unique_code, unique_data):
    """ 更新 """
    cols, values = zip(*item.items())
    sql = "UPDATE `{}` SET {} WHERE {}={};".format(
        table,
        ','.join(["%s='%s'" % (vals, item[vals]) for vals in item]),
        unique_code,
        unique_data
    )
    print('&' * 20, sql)
    cursor.execute(sql, values * 2)


def toInsert(table, item):
    """ 单线程插入 """
    cols, values = zip(*item.items())
    print(cols, '&' * 20)
    print(values, '%' * 20)

    sql = "INSERT INTO `{}` ({}) VALUES {}".format \
            (
            table,
            ','.join(cols),
            (str(values) + ',')[0:-1]
        )
    print('*' * 20, sql)
    return sql



def saveOriginInsert(table, item):
    """ 多值插入 """
    # # for each in item:
    # sql = "INSERT INTO `{}` (company_code, display_label, information) VALUES ('{}', '{}', '{}');"
    # to_sql = (sql.format(table, item['current_code'], item[0], item[1]))
    # print(to_sql, '@'*20)
    # return to_sql
    for clos in item:
        sql = "INSERT INTO `%s` (display_label, information) VALUES ('%s', '%s');"




