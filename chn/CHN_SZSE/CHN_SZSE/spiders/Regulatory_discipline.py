#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/11/6 14:16
import scrapy
import json
import re
import pymysql

from datetime import datetime

from scrapy import signals
from ..items import RegItem
from ..items import DisItem


class RegulatorySpider(scrapy.Spider):
    name = 'Regulatory_discipline'
    allowed_domains = ['szse.cn']

    reg_url = 'http://www.szse.cn/api/report/ShowReport/data?'

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(RegulatorySpider, cls).from_crawler(
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
        reg_form = {
            'SHOWTYPE': 'JSON',
            'CATALOGID': '1800_jgxxgk',
            'TABKEY': 'tab1',
            'selectBkmc': '0'
        }
        for unique_code1 in self.spider_opened():
            reg_form['txtZqdm'] = unique_code1['security_code']
            yield scrapy.FormRequest(
                method="GET",
                url=self.reg_url,
                formdata=reg_form,
                callback=self.parse_reg,
                meta={
                    "company_code": unique_code1['company_code'],
                    "proxy": 'http://58.218.201.74:9159'
                }
            )

        dis_form = {
            'SHOWTYPE': 'JSON',
            'CATALOGID': '1800_jgxxgk',
            'TABKEY': 'tab2',
            'selectGsbk': '0'
        }
        for unique_code2 in self.spider_opened():
            dis_form['txtDMorJC'] = unique_code2['security_code']
            yield scrapy.FormRequest(
                method="GET",
                url=self.reg_url,
                formdata=dis_form,
                callback=self.parse_dis,
                meta={
                    "company_code": unique_code2['company_code'],
                    "proxy": 'http://58.218.200.214:8795'
                }
            )

    def parse_reg(self, response):
        head_id = 47
        item = RegItem()
        item['country_code'] = 'chn'
        item['company_code'] = response.meta['company_code']
        item['classification_id'] = head_id
        item['correlation_id'] = 1
        item['header'] = '监管措施'
        item['header_sort'] = 1
        item['content'] = str(json.loads(response.text))
        item['gmt_create'] = str(datetime.now())
        item['user_create'] = 'xfc'
        yield item

    def parse_dis(self, response):
        head_id = 48
        item = DisItem()
        item['country_code'] = 'chn'
        item['company_code'] = response.meta['company_code']
        item['classification_id'] = head_id
        item['correlation_id'] = 1
        item['header'] = '纪律处分'
        item['header_sort'] = 1
        item['content'] = str(json.loads(response.text))
        item['gmt_create'] = str(datetime.now())
        item['user_create'] = 'xfc'
        yield item