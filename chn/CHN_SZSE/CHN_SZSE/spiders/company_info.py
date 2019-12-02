#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/11/6 15:33
import scrapy
import json
import pymysql
import time
import re

from datetime import datetime

from scrapy import signals
from ..items import SecretaryItem
from ..items import StockItem
from ..items import CompanyInfoItem


class CompanyInfoSpider(scrapy.Spider):
    name = 'company_info'
    allowed_domains = ['szse.cn']

    res_url = 'http://www.szse.cn/api/report/index/companyGeneralization?'

    info_item = {
        'zcdz': '注册地址',
        'agdm': 'A股代码',
        'agjc': 'A股简称',
        'agssrq': 'A股上市日期',
        'agzgb': 'A股总股本',
        'agltgb': 'A股流通股本',
        'dldq': '地区',
        'shi': '城市',
        'http': '公司网址',
        'bgdm': 'B股代码',
        'bgjc': 'B股简称',
        'bgssrq': 'B股上市日期',
        'bgzgb': 'B股总股本',
        'bgltgb': 'B股流通股本',
        'sheng': '省份',
        'sshymc': '所属行业',
        'gsqc': '公司全称',
        'ywqc': '英文全称'
    }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(CompanyInfoSpider, cls).from_crawler(
            crawler, *args, **kwargs
        )
        crawler.signals.connect(spider.spider_opened, signals.spider_opened)
        return spider

    def spider_opened(self):
        """ 查询当前所有存量公司 """
        conn = pymysql.connect(**self.settings['DBARGS'])

        with conn.cursor() as cursor:
            cursor.execute("SELECT company_code, security_code FROM `company_base_info` "
                           "WHERE country_code='chn' AND exchange_market_code='SZSE' "
                           "AND is_batch=0 ORDER BY security_code ASC ;")
            feild_list = cursor.fetchall()
            return feild_list

    def start_requests(self):
        for securit in self.spider_opened():
            form_data = {
                "secCode": securit['security_code']
            }
            yield scrapy.FormRequest(
                method="GET",
                url=self.res_url,
                formdata=form_data,
                callback=self.parse,
                meta={
                    "company_code": securit['company_code'],
                    "security_code": securit['security_code'],
                    # "proxy": 'http://58.218.201.74:9175'
                }
            )

    def parse(self, response):
        item = CompanyInfoItem()
        if json.loads(response.text):
            label = json.loads(response.text)['data']
            item['gsqc'] = ('公司全称', label['gsqc'])
            item['ywqc'] = ('英文全称', label['ywqc'])
            item['zcdz'] = ('注册地址', label['zcdz'])
            item['agdm'] = ('A股代码', label['agdm'])
            item['agjc'] = ('A股简称', label['agjc'])
            item['agssrq'] = ('A股上市日期', label['agssrq'])
            item['agzgb'] = ('A股流通股本', label['agzgb'])
            item['agltgb'] = ('A股流通股本', label['agltgb'])
            item['dldq'] = ('地区', label['dldq'])
            item['shi'] = ('城市', label['shi'])
            item['http'] = ('公司网址', label['http'])
            item['bgdm'] = ('B股代码', label['bgdm'])
            item['bgjc'] = ('B股简称', label['bgjc'])
            item['bgssrq'] = ('B股上市日期', label['bgssrq'])
            item['bgzgb'] = ('B股总股本', label['bgzgb'])
            item['bgltgb'] = ('B股流通股本', label['bgltgb'])
            item['sheng'] = ('省份', label['sheng'])
            item['sshymc'] = ('所属行业', label['sshymc'])
            item['company_code'] = ('内部定制编码', response.meta['company_code'])
            item['security_code'] = ('证券代码', response.meta['security_code'])
            yield item
