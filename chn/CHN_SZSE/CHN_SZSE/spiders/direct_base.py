#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/11/8 10:56
import scrapy
import json
import pymysql
import time
import re

from datetime import datetime
from scrapy import signals

class DirectBaseSpdier(scrapy.Spider):
    name = 'direct_base'
    allowed_domains = ['szse.cn']
    base_url = 'http://www.szse.cn/api/report/ShowReport/data?'

    conn = pymysql.connect(host='10.100.4.99', user='root', passwd='OPDATA', db='opd_common', charset='utf8')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(DirectBaseSpdier, cls).from_crawler(
            crawler, *args, **kwargs
        )
        crawler.signals.connect(spider.spider_opened, signals.spider_opened)
        return spider

    def spider_opened(self):
        """ 查询当前所有存量公司 """
        # try:
        conn = pymysql.connect(**self.settings['DBARGS'])
        with conn.cursor() as cursor:
            cursor.execute("SELECT company_code, security_code FROM `company_data_source_complete20191010_copy`"
                           " WHERE country_code='chn' AND exchange_market_code='SZSE' AND "
                           "is_batch=0 ORDER BY security_code ASC ;")
            feild_list = cursor.fetchall()
            return feild_list
        # except TypeError as e:
        #     return "ERROR AS values %s" % e

    def start_requests(self):
        pg_A = 1
        data_form = {
            'SHOWTYPE': 'JSON',
            'CATALOGID': '1900',
            'random': '0.03996417227611859'
        }

        tab_list = ['tab1', 'tab2', 'tab3']
        for direct_unqiues in self.spider_opened():
            for tab_alone in tab_list:
                data_form['TABKEY'] = tab_alone
                data_form['PAGENO'] = '1'
                data_form['txtDMorJC'] = str(direct_unqiues['security_code'])

                yield scrapy.FormRequest(
                    method="GET",
                    url=self.base_url,
                    callback=self.parse_A,
                    formdata=data_form,
                    meta={
                        'company_code': direct_unqiues['company_code'],
                        'security_code': direct_unqiues['security_code'],
                        'tab_value': tab_alone
                    }

                )

    def parse_A(self, response):
        tab_fail = {
            'tab1': '0',
            'tab2': '1',
            'tab3': '2'
        }
        data_position = int(tab_fail[response.meta['tab_value']])
        serial_value = json.loads(response.text)[data_position]
        pg_A = 1
        pg_count = int(serial_value['metadata']['pagecount'])
        data_form = {
            'SHOWTYPE': 'JSON',
            'CATALOGID': '1900',
            'random': '0.03996417227611859'
        }
        with open('direct_info.txt', 'a', encoding='utf-8') as df:
            df.write((response.meta['company_code'] + ', ' + str(serial_value) + '\n'))
        if (response.status != 200) or (len(response.text) == 0) or (not serial_value) or (serial_value is None):
            with open('error_codes_szse.txt', 'a') as af:
                af.write((response.meta['company_code'] + ', ' + response.meta['security_code']) + '\n')
            tab_list = ['tab1', 'tab2', 'tab3']
            for unqiues in self.spider_opened():
                for tab_alone in tab_list:
                    data_form['TABKEY'] = tab_alone
                    data_form['PAGENO'] = str(pg_A)
                    data_form['txtDMorJC'] = str(unqiues['security_code'])

                    yield scrapy.FormRequest(
                        method="GET",
                        url=self.base_url,
                        formdata=data_form,
                        callback=self.parse_A
                    )
