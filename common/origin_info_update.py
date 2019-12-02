#! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os
import threading
import time

import pymysql

from common.utils import read_file, alter_file, get_file_path, \
    get_hongkong_spider_path, get_table_name, get_table_date, get_china_sse_spider_path, get_china_szse_spider_path

# 数据库连接
conn = pymysql.connect(host="10.100.4.99", port=3306, db="opd_common", user="root", passwd="OPDATA",
                       charset="utf8")
cursor = conn.cursor()


def createTemporaryTable():
    '''
    在99服务器下建立临时表:company_origin_info_temporary_localtime
    :return:临时表名与创建临时表名的日期
    '''
    # 按照日期生成表名
    # 获取当前时间拼接表名
    localtime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    datelabel = time.strftime('%Y%m%d', time.localtime(time.time()))
    tableName = 'company_origin_info_temporary_' + str(datelabel)

    # 创建表
    # 创建表时，首先判断是否创建过该表，如果是就删除
    DROPTABLE_SQL = "drop table if EXISTS {tablename}".format(tablename=tableName)
    cursor.execute(DROPTABLE_SQL)

    CREATTABLE_SQL = """CREATE TABLE {tablename} (
        id int(20) NOT NULL AUTO_INCREMENT,
        country_code varchar(8) NOT NULL,
        exchange_market_code varchar(10) NOT NULL,
        security_code varchar(80),
        company_code varchar(20) NOT NULL,
        display_label varchar(255) NOT NULL,
        information text,
        data_type varchar(10) not null,
        desciption varchar(255),
        is_synchronization tinyint(2),
        recent_delivery_time datetime,
        is_latest tinyint(1),
        gmt_create datetime,
        user_create varchar(11),
        is_deleted tinyint(2),
        PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """.format(tablename=tableName)
    cursor.execute(CREATTABLE_SQL)
    conn.close()

    msg = localtime + ':' + tableName
    return msg


def schedulingHongkongSpiders():
    HK_PATH = get_hongkong_spider_path()

    os.chdir(HK_PATH)
    os.system("cd scrapy crawl HKEX_origin_info_update")

def schedulingChinaSpiders():
    SSE_PATH = get_china_sse_spider_path()
    SZSE_PATH = get_china_szse_spider_path()
    os.chdir(SSE_PATH)
    os.system("scrapy crawl SSE_list_insert")
    os.system("scrapy crawl SSE_company_sample_info")
    os.system("scrapy crawl SSE_listing_date_name")

    os.chdir(SZSE_PATH)
    os.system("scrapy crawl SZSE_company_list")
    os.system("scrapy crawl company_info")


def schedulingSpiders():
    spiderList = [schedulingHongkongSpiders, schedulingChinaSpiders]
    for spider in spiderList:
        t = threading.Thread(target=spider)
        t.start()

def dropOverDueTable():
    # 获取当前时间
    today = datetime.datetime.now()
    # 计算偏移量
    offset = datetime.timedelta(days=-3)
    # 获取想要的日期的时间
    re_date = (today + offset).strftime('%Y%m%d')
    tablename = 'company_origin_info_temporary_' + str(re_date)
    DROPTABLE_SQL = "drop table if exists {tablename}".format(tablename=tablename)
    cursor.execute(DROPTABLE_SQL)
    print('删除表：'+ tablename)







if __name__ == '__main__':
    # 1、创建临时表,更新文件中表名
    msg = createTemporaryTable()
    file_path = get_file_path()
    oldMsg = read_file(file_path)
    alter_file('tablename.txt', oldMsg, msg)


    # 2、调度爬虫，获取数据
    schedulingSpiders()





    # 4、删除过期表
    dropOverDueTable()