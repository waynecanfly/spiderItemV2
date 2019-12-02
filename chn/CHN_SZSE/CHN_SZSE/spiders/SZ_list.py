#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/10/16 14:17
import scrapy
import json
import pymysql
import re

from datetime import datetime
from ..items import ChnSzseItem

class SzSeInFoSpider(scrapy.Spider):
    name = 'SZ_list'
    allowed_domains = ['szse.cn']

    list_url = 'http://www.szse.cn/api/report/ShowReport/data?'

    data_form_A = {
        'SHOWTYPE': 'JSON',
        'CATALOGID': '1110',
        'TABKEY': 'tab1',
    }

    data_form_B = {
        'SHOWTYPE': 'JSON',
        'CATALOGID': '1110',
        'TABKEY': 'tab2',
    }

    data_form_C = {
        'SHOWTYPE': 'JSON',
        'CATALOGID': '1110',
        'TABKEY': 'tab3',
    }

    def start_requests(self):
        """ 分类请求 """
        page_A = 1
        self.data_form_A['PAGENO'] = str(page_A)
        yield scrapy.FormRequest(
            method="GET",
            callback=self.parse_A,
            url=self.list_url,
            formdata=self.data_form_A,
            meta={
                'page_A': page_A,
                'proxy': 'http://58.218.200.229:6251'
            }
        )

        page_B = 1
        self.data_form_B['PAGENO'] = str(page_B)
        yield scrapy.FormRequest(
            method="GET",
            callback=self.parse_B,
            url=self.list_url,
            formdata=self.data_form_B,
            meta={
                'page_B': page_B,
                'proxy': 'http://58.218.200.228:6929'
            }
        )

    def tosavefile(self, unqiue_count):
        with open('E:\\Restructure\\CHN_SSE\\CHN_SSE\\samples\\custom_code.txt', 'w') as wf:
            wf.write(unqiue_count)

    def parse_A(self, response):
        pg_A = 1
        jres_A = json.loads(response.text)[0]['data']

        for blank_dict in jres_A:

            with open('E:\\Restructure\\CHN_SSE\\CHN_SSE\\samples\\custom_code.txt', 'r') as rf:
                unqiue_str = rf.read()
            unique_count = int(unqiue_str)
            unique_count += 1
            self.tosavefile(str(unique_count))
            company_id = "chn" + str(unique_count).zfill(5)

            item = ChnSzseItem()
            item['company_id'] = company_id
            item['security_code'] = blank_dict['zqdm']
            item['company_abbreviation'] = ''.join(re.findall(r'<u>(.*?)</u>', blank_dict['gsjc']))
            item['country_code'] = 'chn'
            item['latest_url'] = response.url
            item['latest_date'] = blank_dict['agssrq']
            item['spider_name'] = 'SZ_list'
            item['gmt_create'] = str(datetime.now())
            item['user_create'] = 'xfc'
            yield item

        while pg_A < 110:
            pg_A += 1
            data_pg_A = {
                'SHOWTYPE': 'JSON',
                'CATALOGID': '1110',
                'TABKEY': 'tab1',
                'PAGENO': str(pg_A)
            }
            yield scrapy.FormRequest(
                method="GET",
                callback=self.parse_A,
                url=self.list_url,
                formdata=data_pg_A
            )

    def parse_B(self, response):
        pg_B = 1
        jres_B = json.loads(response.text)
        for blanck_B in jres_B[1]['data']:

            with open('E:\\Restructure\\CHN_SSE\\CHN_SSE\\samples\\custom_code.txt', 'r') as rf:
                unqiue_str = rf.read()
            unique_count = int(unqiue_str)
            unique_count += 1
            self.tosavefile(str(unique_count))
            company_id = "chn" + str(unique_count).zfill(5)

            item = ChnSzseItem()
            item['company_id'] = company_id
            item['security_code'] = blanck_B['zqdm']
            item['company_abbreviation'] = ''.join(re.findall(r'<u>(.*?)</u>', blanck_B['gsjc']))
            item['country_code'] = 'chn'
            item['latest_url'] = response.url
            item['latest_date'] = blanck_B['bgssrq']
            item['spider_name'] = 'SZ_list'
            item['gmt_create'] = str(datetime.now())
            item['user_create'] = 'xfc'
            yield item

        while pg_B < 4:
            pg_B += 1
            # print(pg_A, '*'*30)
            data_pg_B = {
                'SHOWTYPE': 'JSON',
                'CATALOGID': '1110',
                'TABKEY': 'tab1',
                'PAGENO': str(pg_B)
            }
            yield scrapy.FormRequest(
                method="GET",
                callback=self.parse_B,
                url=self.list_url,
                formdata=data_pg_B
            )


    def parse_C(self, response):
        pass
        pg_C = 1
        print(json.loads(response.text)[2]['data'])
        jres_C = json.loads(response.text)
        for blanck_C in jres_C[2]['data']:

            with open('E:\\Restructure\\CHN_SSE\\CHN_SSE\\samples\\custom_code.txt', 'r') as rf:
                unqiue_str = rf.read()
            unique_count = int(unqiue_str)
            unique_count += 1
            self.tosavefile(str(unique_count))
            company_id = "chn" + str(unique_count).zfill(5)

            item = {}
            item['company_id'] = company_id
            item['security_code'] = blanck_C['zqdm']
            item['company_abbreviation'] = ''.join(re.findall(r'<u>(.*?)</u>', blanck_C['gsjc']))
            item['country_code'] = 'chn'
            item['latest_url'] = response.url
            item['latest_date'] = blanck_C['agssrq']
            item['spider_name'] = 'SZ_list'
            item['gmt_create'] = str(datetime.now())
            item['user_create'] = 'xfc'

            # item['company_code'] = company_id
            # item['incorporation_code'] = blanck_C['zqdm']
            # item['incorporation_name'] = ''.join(re.findall(r'<u>(.*?)</u>', blanck_C['gsjc']))
            # item['A_unique_code'] = blanck_C['agdm']
            # item['A_shares'] = blanck_C['agjc']
            # item['A_listing_date'] = blanck_C['agssrq']
            # item['B_unique_code'] = blanck_C['bgdm']
            # item['B_shares'] = blanck_C['bgjc']
            # item['B_listing_date'] = blanck_C['bgssrq']
            # item['whole_details'] = blanck_C['sshymc']
            yield item

        while pg_C < 3:
            pg_C += 1
            data_pg_C = {
                'SHOWTYPE': 'JSON',
                'CATALOGID': '1110',
                'TABKEY': 'tab1',
                'PAGENO': str(pg_C)
            }
            yield scrapy.FormRequest(
                method="GET",
                callback=self.parse_C,
                url=self.list_url,
                formdata=data_pg_C
            )