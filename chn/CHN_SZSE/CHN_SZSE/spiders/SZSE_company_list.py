#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/10/22 18:08
import scrapy
import pymysql
import json
import re

from datetime import datetime

from scrapy import signals

from ..items import SzseCollectionItem2, SzseCollectionItem3, SzseCollectionItem1


class SzSeComapnySpider(scrapy.Spider):
    name = 'SZSE_company_list'
    allowed_domains = ['szse.cn']

    index_url = 'http://www.szse.cn/api/report/ShowReport/data?'

    data_form = {
        'SHOWTYPE': 'JSON',
        'CATALOGID': '1110x',
        # 'TABKEY': 'tab2'
    }

    market_type = {
        'tab2':'主板',
        'tab3':'中小企业板',
        'tab4':'创业板'
    }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(SzSeComapnySpider, cls).from_crawler(
            crawler, *args, **kwargs
        )
        crawler.signals.connect(spider.spider_opened, signals.spider_opened)
        return spider

    def spider_opened(self):
        """ 查询当前所有存量公司 """
        conn = pymysql.connect(**self.settings['DBARGS'])
        with conn.cursor() as cursor:
            cursor.execute("SELECT security_code FROM `company_base_info` "
                           "WHERE country_code='chn' AND exchange_market_code='SZSE' "
                           "AND is_batch=0 ORDER BY security_code ASC ;")
            feild_list = cursor.fetchall()
            conn.close()

            return [unique_code['security_code'] for unique_code in feild_list]

    def tosavefile(self, unqiue_count):
        with open('E:\\Restructure\\CHN_SSE\\CHN_SSE\\samples\\custom_code.txt', 'w') as wf:
            wf.write(unqiue_count)

    def start_requests(self):
        # for tab_key in self.market_type:
        for pg_A in range(1, 25):
            self.data_form['TABKEY'] = 'tab2'
            self.data_form['PAGENO'] = str(pg_A)
            yield scrapy.FormRequest(
                method="GET",
                url=self.index_url,
                callback=self.parse_zhuban,
                formdata=self.data_form,
                meta={
                    'market_type': 'tab2',
                    # 'proxy': 'http://58.218.200.227:3959'
                }
            )

        for pg_B in range(1, 48):
            self.data_form['TABKEY'] = 'tab3'
            self.data_form['PAGENO'] = str(pg_B)
            yield scrapy.FormRequest(
                method="GET",
                url=self.index_url,
                callback=self.parse_zxb,
                formdata=self.data_form,
                meta={
                    'market_type': 'tab3',
                    # 'proxy': 'http://58.218.201.74:6839'
                }
            )

        for pg_C in range(1, 40):
            self.data_form['TABKEY'] = 'tab4'
            self.data_form['PAGENO'] = str(pg_C)
            yield scrapy.FormRequest(
                method="GET",
                url=self.index_url,
                callback=self.parse_cyb,
                formdata=self.data_form,
                meta={
                    'market_type': 'tab4',
                    # 'proxy': 'http://58.218.201.74:6491'
                }
            )

    def parse_zhuban(self, response):
        data_full = json.loads(response.text)[1]['data']
        print(data_full, '&'*20)

        for code_feild in data_full:
            with open('E:\\Restructure\\CHN_SSE\\CHN_SSE\\samples\\custom_code.txt', 'r') as rf:
                unqiue_str = rf.read()
            unique_count = int(unqiue_str)
            unique_count += 1
            self.tosavefile(str(unique_count))
            company_id = "chn" + str(unique_count).zfill(5)

            # 内部编码
            internal_code = company_id
            # 市场类型
            market_type = '主板'
            # 公司代码
            company_unique = code_feild['zqdm']
            # 公司简称
            company_short_name = ''.join(re.findall(r'<u>(.*?)</u>', code_feild['gsjc']))
            # 公司全称
            company_full_name = code_feild['gsqc']
            # 官网
            web = code_feild['http']
            # 所属行业
            industry = code_feild['sshymc']

            if company_unique not in self.spider_opened():

                item = SzseCollectionItem1()
                item['company_code'] = internal_code
                item['company_name'] = company_full_name
                item['company_short_name'] = company_short_name
                item['country_code'] = 'chn'
                item['exchange_market_code'] = 'SZSE'
                item['market_type'] = market_type
                item['security_code'] = company_unique
                item['company_list_url'] = response.url
                item['spider_name'] = 'SZSE_company_list'
                item['gmt_create'] = str(datetime.now())
                item['user_create'] = 'xfc'
                yield item

            else:
                break

    def parse_zxb(self, response):
        data_full = json.loads(response.text)[2]['data']
        for code_feild in data_full:
            with open('E:\\Restructure\\CHN_SSE\\CHN_SSE\\samples\\custom_code.txt', 'r') as rf:
                unqiue_str = rf.read()
            unique_count = int(unqiue_str)
            unique_count += 1
            self.tosavefile(str(unique_count))
            company_id = "chn" + str(unique_count).zfill(5)

            # 内部编码
            internal_code = company_id
            # 市场类型
            market_type = '中小企业板'
            # 公司代码
            company_unique = code_feild['zqdm']
            # 公司简称
            company_short_name = ''.join(re.findall(r'<u>(.*?)</u>', code_feild['gsjc']))
            # 公司全称
            company_full_name = code_feild['gsqc']
            # 官网
            web = code_feild['http']
            # 所属行业
            industry = code_feild['sshymc']

            if company_unique not in self.spider_opened():

                item = SzseCollectionItem2()
                item['company_code'] = internal_code
                item['company_name'] = company_full_name
                item['company_short_name'] = company_short_name
                item['country_code'] = 'chn'
                item['exchange_market_code'] = 'SZSE'
                item['market_type'] = market_type
                item['security_code'] = company_unique
                item['company_list_url'] = response.url
                item['spider_name'] = 'SZSE_company_list'
                item['gmt_create'] = str(datetime.now())
                item['user_create'] = 'xfc'
                yield item

            else:
                break

    def parse_cyb(self, response):
        data_full = json.loads(response.text)[3]['data']
        for code_feild in data_full:
            with open('E:\\Restructure\\CHN_SSE\\CHN_SSE\\samples\\custom_code.txt', 'r') as rf:
                unqiue_str = rf.read()
            unique_count = int(unqiue_str)
            unique_count += 1
            self.tosavefile(str(unique_count))
            company_id = "chn" + str(unique_count).zfill(5)

            # 内部编码
            internal_code = company_id
            # 市场类型
            market_type = '创业板'
            # 公司代码
            company_unique = code_feild['zqdm']
            # 公司简称
            company_short_name = ''.join(re.findall(r'<u>(.*?)</u>', code_feild['gsjc']))
            # 公司全称
            company_full_name = code_feild['gsqc']
            # 官网
            web = code_feild['http']
            # 所属行业
            industry = code_feild['sshymc']

            if company_unique not in self.spider_opened():

                item = SzseCollectionItem3()
                item['company_code'] = internal_code
                item['company_name'] = company_full_name
                item['company_short_name'] = company_short_name
                item['country_code'] = 'chn'
                item['exchange_market_code'] = 'SZSE'
                item['market_type'] = market_type
                item['security_code'] = company_unique
                item['company_list_url'] = response.url
                item['spider_name'] = 'SZSE_company_list'
                item['gmt_create'] = str(datetime.now())
                item['user_create'] = 'xfc'
                yield item

            else:
                break