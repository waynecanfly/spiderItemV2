#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/9/20 16:01
import json
import time

import pymysql

conn = pymysql.connect(host="10.100.4.99", port=3306, db="opd_common", user="root", passwd="OPDATA",
                           charset="utf8")
cursor = conn.cursor()

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


def toInsert(conn, cursor, table, item):
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
    cursor.execute(sql)
    conn.commit()

def saveOriginInsert(cursor, table, item):
    """ 多值插入 """
    for each in item:
        sql = "INSERT INTO `%s` (%s) VALUES %s;"
        cursor.execute(sql, [table, item[each]])


def HKEXqueryCompanyCode(cursor, table, companyName):
    # 对companyName做特殊处理防止sql语法错误
    if "'" in companyName:
        companyName = '"' + str(companyName) + '"'
    else:
        companyName = "'" + str(companyName) + "'"

    sql = "select company_code from {table} where company_name = {company_name}".format(
        table=table,
        company_name=companyName
    )
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        return res[0]
    else:
        print(companyName)


def removeRepeatByComNm(cursor, table):
    del_list = []
    query_sql = "select id,company_name,count(*) as count from {table} where country_code='HKG' group by company_name having count>1".format(
        table=table
    )
    cursor.execute(query_sql)
    res_tup = cursor.fetchall()
    if res_tup:
        for res in res_tup:
            id = res[0]
            delete_sql = "delete from {table} where company_id='{id}'".format(
                table=table, id=id
            )
            cursor.execute(delete_sql)
            conn.commit()
            print('*' * 20, delete_sql)
    else:
        print('*' * 20, '没有重复的数据')

def HKEXGetSymCode(cursor, table):
    stoct_list = []
    sql = "select security_code from {table} where country_code='HKG' and security_type='Equity'".format(
        table=table
    )

    cursor.execute(sql)
    res_tuple = cursor.fetchall()
    for res in res_tuple:
        stoct_list.append(res[0])

    return stoct_list

def HKEXGetCompcodeBySymCode(cursor, table, sym):
    sql = "select company_code from {table} where security_code='{sym}' and country_code='HKG'".format(
        table=table,
        sym=sym
    )

    cursor.execute(sql)
    res = cursor.fetchone()
    return res

def HKEXGetStockCode(cursor, table):
    '''获取香港security type为Equity或者REITs的公司stock code'''

    sql = "select security_code, company_short_name, company_code from {table} where country_code='HKG' and security_type in ('Equity','REITs')".format(
        table=table
    )

    cursor.execute(sql)
    res = cursor.fetchall()
    return res


def HKEXGetStockCode1(cursor):
    sql = "select security_code, company_short_name, company_code from company_data_source_complete20191010_copy1 where " \
          "company_code not in (SELECT company_code from financial_origin_began_complete20191101_copy1 where country_code='HKG' " \
          "GROUP BY company_code) and country_code='HKG' and security_type in ('Equity','REITs')"
    cursor.execute(sql)
    res = cursor.fetchall()
    return res

def HKEXGetStockCodeHeadlineType(cursor):
    sql = "select security_code, company_short_name, company_code from company_data_source_complete20191010_copy1 where " \
          "company_code not in (SELECT company_code from financial_origin_began_complete20191101_copy1 where country_code='HKG' " \
          "and source_category='headline category' GROUP BY company_code) and country_code='HKG' and security_type in ('Equity','REITs')"
    cursor.execute(sql)
    res = cursor.fetchall()
    return res


def HKEXGetStockCodeDocumentType(cursor):
    sql = "select security_code, company_short_name, company_code from company_data_source_complete20191010_copy1 where " \
          "company_code not in (select company_code from financial_origin_began_complete20191101_copy1_copy1 where country_code='HKG' " \
          "and source_category='document type' GROUP BY company_code) and country_code='HKG' and security_type in ('Equity','REITs')"

    cursor.execute(sql)
    res = cursor.fetchall()
    return res


def HKEXIsNewDelistedSec(stock_code):
    sql = "select security_code from company_listing_status_hkg where security_code='{security_code}' and country_code='HKG'".format(security_code=stock_code)
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        return True
    else:
        return False



def HKEXGetCompanyCodeNotInRepeatSectypesBySym(cursor, table, stock_code):
    sql = "select company_code from {table} where security_code={security_code} and security_type not in ('Inline Warrants', 'DWs')"\
        .format(table=table, security_code=stock_code)
    print(sql)
    cursor.execute(sql)
    res = cursor.fetchone()
    return res[0]

def HKEXGetHtmlTypeFileInfo(cursor):
    sql = "select company_code, doc_source_url, source_category from financial_origin_began_complete20191101_copy1_copy1 where" \
          " country_code='HKG' and doc_type='htm' and is_inflows_financial_html=0"
    cursor.execute(sql)
    res = cursor.fetchall()
    return res


def HKEXIsNewCompany(stockCode, tableName, securityType):
    sql = "select * from {tablename} where security_code='{stock_code}' and security_type='{security_type}' and country_code='HKG'".format(
        tablename=tableName,stock_code=stockCode,security_type=securityType
    )
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        return True
    else:
        return False


def HKEXIsNewFile(tableName, cateGory, docSourceUrl, companyCode):
    sql = "select * from {tablename} where company_code='{companyCode} and 'country_code='HKG' and source_category='{cateGory}' and doc_source_url='{docSourceUrl}'".format(
        tablename=tableName, companyCode=companyCode, cateGory=cateGory, docSourceUrl=docSourceUrl
    )
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        return True
    else:
        return False



if __name__ == '__main__':
    conn = pymysql.connect(host="10.100.4.99", port=3306, db="opd_common", user="root", passwd="OPDATA",
                           charset="utf8")
    cursor = conn.cursor()
    result = HKEXIsNewFile('financial_origin_began_complete20191101_copy1_copy1', 'headline category', 'https://www1ADFASDFlistedco/listconews/sehk/2019/0319/ltn20190319630.pdf')
    if not result:
        print('是一份新文件')
    else:
        print('文件已存在')
