#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import urllib.request

import pymysql
import requests
import xlrd as xlrd


# from hongkong.samples.base_rule import HKEXGetCompcodeBySymCode


def get_website_url_file():

    url = 'https://www2.hkexnews.hk/-/media/HKEXnews/Homepage/Others/Quick-Link/Homepage/Other-Useful-Information/Hyperlinks-to-Listed-Co.xlsx'
    dir = os.getcwd()  # 当前工作目录。
    urllib.request.urlretrieve(url, dir + '/Hyperlinks-to-Listed-Co.xlsx')

def get_company_website_map():
    '''爬取公司官网'''
    conn = pymysql.connect(host="10.100.4.99", port=3306, db="opd_common", user="root", passwd="OPDATA",
                           charset="utf8")
    cursor = conn.cursor()
    dir = os.getcwd()
    # 文件路径
    file_path = dir + '/Hyperlinks-to-Listed-Co.xlsx'
    # 获取数据
    data = xlrd.open_workbook(file_path)
    # 获取sheet
    main_table = data.sheet_by_name('Main Board (主板)')
    # 获取总行数
    nrows = main_table.nrows
    for r in range(13, nrows):
        security_code = main_table.cell(r, 0).value
        security_code = str(int(security_code))
        res = HKEXGetCompcodeBySymCode(cursor, 'company_base_info_hkg', security_code)
        if res:
            company_code = res[0]
            gmt_create = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            website_url = main_table.cell(r, 3).value
            insert_sql = "insert into company_raw_info (" \
                              "unique_code, country_code, exchange_market_code, security_code, display_label, information, gmt_create, user_create) values " \
                              "(%s,%s,%s,%s,%s,%s,%s,%s)"
            print('*' * 20, insert_sql)
            cursor.execute(
                insert_sql,
                [
                    str(company_code),
                    'HKG',
                    'HKEX',
                    str(security_code),
                    'website_url',
                    str(website_url),
                    str(gmt_create),
                    'cf'
                ]
            )
            conn.commit()

    gem_table = data.sheet_by_name('GEM')
    # 获取总行数
    nrows = gem_table.nrows
    for r in range(13, nrows):
        security_code = gem_table.cell(r, 0).value
        security_code = str(int(security_code))
        res = HKEXGetCompcodeBySymCode(cursor, 'company_base_info_hkg', security_code)
        if res:
            company_code = res[0]
            gmt_create = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            website_url = gem_table.cell(r, 3).value
            insert_sql = "insert into company_raw_info (" \
                         "unique_code, country_code, exchange_market_code, security_code, display_label, information, gmt_create, user_create) values " \
                         "(%s,%s,%s,%s,%s,%s,%s,%s)"
            print('*' * 20, insert_sql)
            cursor.execute(
                insert_sql,
                [
                    str(company_code),
                    'HKG',
                    'HKEX',
                    str(security_code),
                    'website_url',
                    str(website_url),
                    str(gmt_create),
                    'cf'
                ]
            )
            conn.commit()

def drop_website_url_file():
    dir = os.getcwd()





if __name__ == '__main__':
    # get_website_url_file()
    get_company_website_map()