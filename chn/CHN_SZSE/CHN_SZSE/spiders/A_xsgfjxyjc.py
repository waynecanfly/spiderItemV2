#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/11/8 15:07

"""
限售股份的检限与减持
"""

import scrapy
import json
import pymysql
import time
import re

from datetime import datetime

from scrapy import signals


class XsgfijxyjcSpdier(scrapy.Spider):
    name = 'A_xsgfjxyjc'
    allowed_domains = ['szse.cn']
    index_url = 'http://www.szse.cn/api/report/ShowReport/data?'

    conn = pymysql.connect(host='10.100.4.99', user='root', passwd='OPDATA', db='opd_common', charset='utf8')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(XsgfijxyjcSpdier, cls).from_crawler(
            crawler, *args, **kwargs
        )
        crawler.signals.connect(spider.spider_opened, signals.spider_opened)
        return spider

    def spider_opened(self):
        """ 查询当前所有存量公司 """
        conn = pymysql.connect(**self.settings['DBARGS'])
        with conn.cursor() as cursor:
            cursor.execute("SELECT company_code, security_code FROM `company_data_source_complete20191010_copy`"
                           " WHERE country_code='chn' AND exchange_market_code='SZSE' AND "
                           "is_batch=0 ORDER BY security_code ASC ;")
            feild_list = cursor.fetchall()
            return feild_list

    def start_requests(self):
        data_form = {
            'SHOWTYPE': 'JSON',
            'CATALOGID': '1902',
            'random': '0.5131977809341239'
        }

        tab_list = ['tab1', 'tab2']
        for uniques in self.spider_opened():
            for tab_alone in tab_list:
                data_form['txtCode'] = uniques['security_code']
                data_form['TABKEY'] = tab_alone
                yield scrapy.FormRequest(
                    method="GET",
                    url=self.index_url,
                    formdata=data_form,
                    callback=self.parse,
                    meta={
                        "company_code": uniques['company_code'],
                        "security_code": uniques['security_code'],
                        "tab_value": tab_alone,
                        "proxy": 'http://58.218.92.72:9808'
                    }
                )

    def parse(self, response):
        tab_tuple = {
            'tab1': 0,
            'tab2': 1
        }
        tab_num = tab_tuple[response.meta['tab_value']]
        feild_datas = json.loads(response.text)[tab_num]
        if (response.status != 200) or (len(response.text) == 0) or (not feild_datas) or (feild_datas is None):
            with open('xsgfjxyjc_error_code.txt', 'a') as xf:
                xf.write((response.meta['company_code'] + ', ' + response.meta['security_code']) + '\n')
        else:
            with open('xsgfjxyjc_info.txt', 'a', encoding='utf-8') as wf:
                wf.write((response.meta['company_code'] + ', ' + str(feild_datas)) + '\n')