#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/10/18 9:53
import scrapy
import json
import re
import pymysql
import random

from datetime import datetime
from ..items import ChnSzseItem
from ..items import ChnSzseListItem


class SzSeListSpider(scrapy.Spider):
    """
    上市公司列表：
        主板
        中小企业板
        创业板
    """
    name = 'SZ_list_insert'
    allowed_domains = ['szse.cn']

    index_url = 'http://www.szse.cn/api/report/ShowReport/data?'

    ip_list = [
        '58.218.200.227:8769',
        '58.218.200.237:5151',
        '58.218.200.223:8778',
        '58.218.200.223:8753',
    ]

    conn = pymysql.connect(host='10.100.4.99', user='root', passwd='OPDATA', db='opd_common')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)

    def tosavefile(self, unqiue_count):
        with open('E:\\Restructure\\CHN_SSE\\CHN_SSE\\samples\\custom_code.txt', 'w') as wf:
            wf.write(unqiue_count)

    def start_requests(self):
        # 主板
        data_form_A = {
            'SHOWTYPE': 'JSON',
            'CATALOGID': '1110x',
            'TABKEY': 'tab2',
            'PAGENO': '1'
        }

        yield scrapy.FormRequest(
            method="GET",
            callback=self.parse_A,
            url=self.index_url,
            formdata=data_form_A,
            meta={
                # 'proxy': 'http://' + random.choice(self.ip_list),
                'proxy': 'http://58.218.200.227:3268',
                'market_type': '主板'
            }
        )

        # 中小企业版
        data_form_B = {
            'SHOWTYPE': 'JSON',
            'CATALOGID': '1110x',
            'TABKEY': 'tab3',
            'PAGENO': '1'
        }

        yield scrapy.FormRequest(
            method="GET",
            callback=self.parse_B,
            url=self.index_url,
            formdata=data_form_B,
            meta={
                # 'proxy': 'http://' + random.choice(self.ip_list),
                'market_type': '中小企业版'
            }
        )

        # 创业板
        data_form_C = {
            'SHOWTYPE': 'JSON',
            'CATALOGID': '1110x',
            'TABKEY': 'tab4',
            'PAGENO': '1'
        }

        yield scrapy.FormRequest(
            method="GET",
            callback=self.parse_C,
            url=self.index_url,
            formdata=data_form_C,
            meta={
                # 'proxy': 'http://' + random.choice(self.ip_list),
                'market_type': '创业板'
            }
        )

    def parse_A(self, response):
        pg_A = 1
        jres_A = json.loads(response.text)[1]['data']
        for blank_A in jres_A:

            with open('E:\\Restructure\\CHN_SSE\\CHN_SSE\\samples\\custom_code.txt', 'r') as rf:
                unqiue_str = rf.read()
            unique_count = int(unqiue_str)
            unique_count += 1
            self.tosavefile(str(unique_count))
            company_id = "chn" + str(unique_count).zfill(5)

            item = ChnSzseItem()
            item['company_id'] = company_id
            item['security_code'] = blank_A['zqdm']
            item['company_abbreviation'] = ''.join(re.findall(r'<u>(.*?)</u>', blank_A['gsjc']))
            item['company_name'] = blank_A['gsqc']
            item['country_code'] = 'chn'
            item['latest_url'] = ''.join(re.findall(r'<a href=(.*?) target=', blank_A['gsjc']))
            item['spider_name'] = 'SZ_list_insert'
            item['gmt_create'] = str(datetime.now())
            item['user_create'] = 'xfc'
            yield item

            company_code = ('公司代码', company_id)
            company_unique_code = ('证券代码', blank_A['zqdm'])
            company_abbreviation = ('公司简称', ''.join(re.findall(r'<u>(.*?)</u>', blank_A['gsjc'])))
            company_name = ('公司全称', blank_A['gsqc'])
            country_code = ('国家代码', 'chn')
            industry = ('所属行业', blank_A['sshymc'])
            web_site = ('官方网站', blank_A['http'])
            download_url = ('详情页网址', ''.join(re.findall(r'<a href=(.*?) target=', blank_A['gsjc'])))
            market_type = ('市场类型', response.meta['market_type'])
            yield ChnSzseListItem(
                company_code=company_code,
                company_unique_code=company_unique_code,
                company_abbreviation=company_abbreviation,
                company_name=company_name,
                country_code=country_code,
                industry=industry,
                web_site=web_site,
                download_url=download_url,
                market_type=market_type,
            )

        while pg_A < 25:
            pg_A += 1
            data_form_A = {
                'SHOWTYPE': 'JSON',
                'CATALOGID': '1110x',
                'TABKEY': 'tab2',
                'PAGENO': str(pg_A)
            }
            yield scrapy.FormRequest(
                method="GET",
                callback=self.parse_A,
                url=self.index_url,
                formdata=data_form_A
            )



    def parse_B(self, response):
        pg_B = 1
        jres_B = json.loads(response.text)[1]['data']
        for blank_B in jres_B:

            with open('E:\\Restructure\\CHN_SSE\\CHN_SSE\\samples\\custom_code.txt', 'r') as rf:
                unqiue_str = rf.read()
            unique_count = int(unqiue_str)
            unique_count += 1
            self.tosavefile(str(unique_count))
            company_id = "chn" + str(unique_count).zfill(5)

            item = ChnSzseItem()
            item['company_id'] = company_id
            item['security_code'] = blank_B['zqdm']
            item['company_abbreviation'] = ''.join(re.findall(r'<u>(.*?)</u>', blank_B['gsjc']))
            item['company_name'] = blank_B['gsqc']
            item['country_code'] = 'chn'
            item['latest_url'] = ''.join(re.findall(r'<a href=(.*?) target=', blank_B['gsjc']))
            item['spider_name'] = 'SZ_list_insert'
            item['gmt_create'] = str(datetime.now())
            item['user_create'] = 'xfc'

            yield item

            company_code = ('公司代码', company_id)
            company_unique_code = ('证券代码', blank_B['zqdm'])
            company_abbreviation = ('公司简称', ''.join(re.findall(r'<u>(.*?)</u>', blank_B['gsjc'])))
            company_name = ('公司全称', blank_B['gsqc'])
            country_code = ('国家代码', 'chn')
            industry = ('所属行业', blank_B['sshymc'])
            web_site = ('官方网站', blank_B['http'])
            download_url = ('详情页网址', ''.join(re.findall(r'<a href=(.*?) target=', blank_B['gsjc'])))
            market_type = ('市场类型', response.meta['market_type'])
            yield ChnSzseListItem(
                company_code=company_code,
                company_unique_code=company_unique_code,
                company_abbreviation=company_abbreviation,
                company_name=company_name,
                country_code=country_code,
                industry=industry,
                web_site=web_site,
                download_url=download_url,
                market_type=market_type,
            )

        while pg_B < 48:
            pg_B += 1
            data_form_B = {
                'SHOWTYPE': 'JSON',
                'CATALOGID': '1110x',
                'TABKEY': 'tab2',
                'PAGENO': str(pg_B)
            }
            yield scrapy.FormRequest(
                method="GET",
                callback=self.parse_A,
                url=self.index_url,
                formdata=data_form_B
            )

    def parse_C(self, response):
        pg_C = 1
        jres_C = json.loads(response.text)[1]['data']
        for blank_C in jres_C:

            with open('E:\\Restructure\\CHN_SSE\\CHN_SSE\\samples\\custom_code.txt', 'r') as rf:
                unqiue_str = rf.read()
            unique_count = int(unqiue_str)
            unique_count += 1
            self.tosavefile(str(unique_count))
            company_id = "chn" + str(unique_count).zfill(5)

            item = ChnSzseItem()
            item['company_id'] = company_id
            item['security_code'] = blank_C['zqdm']
            item['company_abbreviation'] = ''.join(re.findall(r'<u>(.*?)</u>', blank_C['gsjc']))
            item['company_name'] = blank_C['gsqc']
            item['country_code'] = 'chn'
            item['latest_url'] = ''.join(re.findall(r'<a href=(.*?) target=', blank_C['gsjc']))
            item['spider_name'] = 'SZ_list_insert'
            item['gmt_create'] = str(datetime.now())
            item['user_create'] = 'xfc'

            yield item

            company_code = ('公司代码', company_id)
            company_unique_code = ('证券代码', blank_C['zqdm'])
            company_abbreviation = ('公司简称', ''.join(re.findall(r'<u>(.*?)</u>', blank_C['gsjc'])))
            company_name = ('公司全称', blank_C['gsqc'])
            country_code = ('国家代码', 'chn')
            industry = ('所属行业', blank_C['sshymc'])
            web_site = ('官方网站', blank_C['http'])
            download_url = ('详情页网址', ''.join(re.findall(r'<a href=(.*?) target=', blank_C['gsjc'])))
            market_type = ('市场类型', response.meta['market_type'])
            yield ChnSzseListItem(
                company_code=company_code,
                company_unique_code=company_unique_code,
                company_abbreviation=company_abbreviation,
                company_name=company_name,
                country_code=country_code,
                industry=industry,
                web_site=web_site,
                download_url=download_url,
                market_type=market_type,
            )

        while pg_C < 40:
            pg_C += 1
            data_form_C = {
                'SHOWTYPE': 'JSON',
                'CATALOGID': '1110x',
                'TABKEY': 'tab2',
                'PAGENO': str(pg_C)
            }
            yield scrapy.FormRequest(
                method="GET",
                callback=self.parse_C,
                url=self.index_url,
                formdata=data_form_C
            )
