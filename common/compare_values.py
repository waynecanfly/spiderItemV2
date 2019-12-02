#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/11/14 17:52


#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/11/14 17:34
import pymysql
import os
import time
import logging

from common.utils import get_china_sse_spider_path
from common.utils import get_china_szse_spider_path
from common.utils import get_hongkong_spider_path
from common.utils import get_table_name
from common.utils import get_file_path


class CompanyValues:

    conn = pymysql.connect(host="10.100.4.99", port=3306, db="opd_common", user="root", passwd="OPDATA",
                           charset="utf8")
    cursor = conn.cursor()

    con = pymysql.connect(host='10.100.4.99', user='root', passwd='OPDATA', db='opd_common', charset='utf8')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __init__(self):
        self.logger = logging.getLogger()
        self.root_path = os.path.abspath(os.path.dirname(__file__)).split('spiderItemV2')[0]
        self.logger_fh = logging.FileHandler(r'%s/LoggerUpdate.log'% self.root_path)
        self.logger_ch = logging.StreamHandler()

        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger_fh.setFormatter(self.formatter)
        self.logger_ch.setFormatter(self.formatter)

    def readBase(self):
        sql = "SELECT" \
              " country_code, exchange_market_code, security_code, company_code, " \
              "display_label, information, gmt_create, user_create " \
              "FROM" \
              " `{}` " \
              "ORDER BY" \
              " id " \
              "ASC ;"
        executavle_sql = sql.format(str(get_table_name()))
        try:
            self.cursor.execute(executavle_sql)
            feild_values = self.cursor.fetchall()
            return feild_values
        except Exception as e:
            return "ERROR Reason Is : %s" % e

    def lingResult(self):
        for unique in self.readBase():
            sql = "SELECT" \
                  " * " \
                  "FROM" \
                  " `company_raw_info` " \
                  "WHERE" \
                  " company_code='{}' " \
                  "AND" \
                  " country_code='{}' " \
                  "AND" \
                  " exchange_market_code='{}' " \
                  "AND" \
                  " security_code='{}' " \
                  "AND" \
                  " display_label='{}' " \
                  "AND" \
                  " information='{}' " \
                  "ORDER BY" \
                  " security_code " \
                  "ASC ;".format(
                unique[3],
                unique[0],
                unique[1],
                unique[2],
                unique[4],
                unique[5]
            )
            try:
                self.cur.execute(sql)
                if self.cur.execute(sql) == 0:
                    self.insertdata(unique)
                    self.logger.info("数据更新：%s，%s" % (unique[4], unique[5]))
                else:
                    pass

            except Exception as e:
                print(e)

    def insertdata(self, unique):
        item = {}
        item['company_code'] = unique[3]
        item['country_code'] = unique[0]
        item['exchange_market_code'] = unique[1]
        item['security_code'] = unique[2]
        item['display_label'] = unique[4]
        item['information'] = unique[5]
        item['gmt_create'] = str(unique[6])
        item['user_create'] = unique[7]
        cols, values = zip(*item.items())
        sql = "INSERT INTO `{}` ({}) VALUES {}".format \
                (
                'company_raw_info',
                ','.join(cols),
                (str(values) + ',')[0:-1]
            )
        self.logger.info(sql)
        try:
            self.cursor.execute(sql)
            self.conn.commit()

        except Exception as e:
            self.logger.info("ERROR IS %s" % e)


if __name__ == '__main__':
    keys = CompanyValues()
    keys.lingResult()
