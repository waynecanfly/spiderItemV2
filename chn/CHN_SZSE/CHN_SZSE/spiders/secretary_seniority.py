#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/11/6 10:08
import scrapy
import json
import pymysql
import time
import re

from datetime import datetime

from scrapy import signals
from ..items import SecretaryItem
from ..items import SecretaryTwoItem
from ..items import SecretaryThreeItem


class SecretarySpider(scrapy.Spider):
    name = 'secretary_seniority'
    allowed_domains = ['szse.cn']

    res_url = 'http://www.szse.cn/api/report/ShowReport/data?'

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(SecretarySpider, cls).from_crawler(
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
        data_form1 = {
            'SHOWTYPE': 'JSON',
            'CATALOGID': '1902',
            'TABKEY': 'tab1',
        }
        for unique_code1 in self.spider_opened():
            data_form1['txtCode'] = unique_code1['security_code']
            yield scrapy.FormRequest(
                method="GET",
                url=self.res_url,
                formdata=data_form1,
                callback=self.parse_tab1,
                meta={
                    "company_code":unique_code1['company_code'],
                    "proxy":'http://58.218.200.228:8779'
                }
            )

        data_form2 = {
            'SHOWTYPE': 'JSON',
            'CATALOGID': '1902',
            'TABKEY': 'tab2'
        }
        for unique_code2 in self.spider_opened():
            data_form2['txtCode'] = unique_code2['security_code']
            yield scrapy.FormRequest(
                method="GET",
                url=self.res_url,
                formdata=data_form2,
                callback=self.parse_tab2,
                meta={
                    "company_code": unique_code2['company_code'],
                    "proxy":'http://58.218.201.114:8782'
                }
            )

        data_form3 = {
            'SHOWTYPE': 'JSON',
            'CATALOGID': '1902',
            'TABKEY': 'tab3'
        }
        for unique_code3 in self.spider_opened():
            data_form3['txtCode'] = unique_code3['security_code']
            yield scrapy.FormRequest(
                method="GET",
                url=self.res_url,
                formdata=data_form3,
                callback=self.parse_tab3,
                meta={
                    "company_code": unique_code3['company_code'],
                    "proxy":'http://58.218.201.114:8782'
                }
            )

    def parse_tab1(self, response):
        """ 解除限售总体情况 """

        classification_id = 40
        item = SecretaryItem()
        # item['gdmc'] = ('解除限售总体情况', str(json.loads(response.text)), 1, classification_id)

        item['country_code'] = 'chn'
        item['company_code'] = response.meta['company_code']
        item['classification_id'] = classification_id
        item['correlation_id'] = 1
        item['header'] = '解除限售总体情况'
        item['header_sort'] = 1
        item['content'] = str(json.loads(response.text))
        item['gmt_create'] = str(datetime.now())
        item['user_create'] = 'xfc'
        yield item


    def parse_tab2(self, response):
        """ 持有股份占总股本1%以上股东解除限售情况 """
        # print(response.text)
        classification_id = 41
        item = SecretaryTwoItem()
        # item['gdmc'] = ('持有股份占总股本1%以上股东解除限售情况', str(json.loads(response.text)), 1, classification_id)

        item['country_code'] = 'chn'
        item['company_code'] = response.meta['company_code']
        item['classification_id'] = classification_id
        item['correlation_id'] = 1
        item['header'] = '持有股份占总股本1%以上股东解除限售情况'
        item['header_sort'] = 1
        item['content'] = str(json.loads(response.text))
        item['gmt_create'] = str(datetime.now())
        item['user_create'] = 'xfc'
        yield item

    def parse_tab3(self, response):
        """ 持有解除限售存量股份占总股本5%以上股东减持1% """
        # print(response.text)
        classification_id = 42
        item = SecretaryThreeItem()
        # item['gdmc'] = ('持有解除限售存量股份占总股本5%以上股东减持1%', str(json.loads(response.text)), 1, classification_id)

        item['country_code'] = 'chn'
        item['company_code'] = response.meta['company_code']
        item['classification_id'] = classification_id
        item['correlation_id'] = 1
        item['header'] = '持有解除限售存量股份占总股本5%以上股东减持1%'
        item['header_sort'] = 1
        item['content'] = str(json.loads(response.text))
        item['gmt_create'] = str(datetime.now())
        item['user_create'] = 'xfc'
        yield item