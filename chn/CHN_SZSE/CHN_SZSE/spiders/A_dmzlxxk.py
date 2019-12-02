#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/11/8 14:42
import scrapy
import json
import pymysql
import time
import re

from datetime import datetime

from scrapy import signals


class DmzlxxkSpider(scrapy.Spider):
    name = 'A_dmzlxxk'
    allowed_domains = ['szse.cn']
    allow_url = 'http://www.szse.cn/api/report/ShowReport/data?'

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(DmzlxxkSpider, cls).from_crawler(
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
            'CATALOGID': '1901',
            'random': '0.32193977769047843'
        }
        # 'txtDMorJC': '000007',
        # 'TABKEY': 'tab1',

        tab_list = ['tab1', 'tab2']
        for tab_alone in tab_list:
            for uniques in self.spider_opened():
                data_form['TABKEY'] = tab_alone
                data_form['txtDMorJC'] = uniques['security_code']
                yield scrapy.FormRequest(
                    method="GET",
                    url=self.allow_url,
                    formdata=data_form,
                    callback=self.parse,
                    meta={
                        'company_code': uniques['company_code'],
                        'security_code': uniques['security_code'],
                        'tab_value': tab_alone,
                        'proxy': 'http://58.218.92.173:9366'
                    }
                )

    def parse(self, response):
        tab_item = {
            'tab1': '0',
            'tab2': '1'
        }
        tab_num = int(tab_item[str(response.meta['tab_value'])])
        feild_datas = json.loads(response.text)[tab_num]
        if (response.status != 200) or (len(response.text) == 0) or (not feild_datas) or (feild_datas is None):
            with open('dmzlxxk_error.txt', 'a') as rf:
                rf.write((response.meta['company_code'] + ', ' + response.meta['security_code']) + '\n')
        else:
            with open('dmzlxxk_info.txt', 'a', encoding='utf-8') as df:
                df.write((response.meta['company_code'] + ', ' + str(feild_datas)) + '\n')
