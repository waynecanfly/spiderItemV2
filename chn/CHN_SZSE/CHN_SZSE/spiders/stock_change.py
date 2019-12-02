#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/11/6 14:56
import scrapy
import json
import pymysql
import time
import re

from datetime import datetime

from scrapy import signals
from ..items import SecretaryItem
from ..items import StockItem


class StockChangeSpider(scrapy.Spider):
    name = 'stock_change'
    allowed_domains = ['szse.cn']

    res_url = 'http://www.szse.cn/api/report/ShowReport/data?'

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(StockChangeSpider, cls).from_crawler(
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
            'CATALOGID': '1801_cxda',
            'TABKEY': 'tab1'
        }
        for unique_code in self.spider_opened():
            data_form['txtDMorJC'] = unique_code['security_code']
            yield scrapy.FormRequest(
                method="GET",
                url=self.res_url,
                formdata=data_form,
                callback=self.parse,
                meta={
                    "company_code": unique_code['company_code'],
                    "security_code": unique_code['security_code'],
                    "proxy": 'http://58.218.200.226:8761'
                }
            )

    def parse(self, response):
        head_id = 49
        pg_total = json.loads(response.text)[0]['metadata']['pagecount']
        item = StockItem()
        item['country_code'] = 'chn'
        item['company_code'] = response.meta['company_code']
        item['classification_id'] = head_id
        item['correlation_id'] = 1
        item['header'] = '监管措施'
        item['header_sort'] = 1
        item['content'] = str(json.loads(response.text)[0]['data'])
        item['gmt_create'] = str(datetime.now())
        item['user_create'] = 'xfc'
        yield item

        data_form = {
            'SHOWTYPE': 'JSON',
            'CATALOGID': '1801_cxda',
            'TABKEY': 'tab1'
        }
        if pg_total > 1:
            data_form['txtDMorJC'] = response.meta['security_code']
            for pg in range(1, int(pg_total)+1):
                yield scrapy.FormRequest(
                    method="GET",
                    url=self.res_url,
                    formdata=data_form,
                    callback=self.parse,
                    meta={"proxy": 'http://58.218.201.114:8959'}
                )