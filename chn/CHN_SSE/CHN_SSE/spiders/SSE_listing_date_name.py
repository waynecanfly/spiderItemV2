#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/11/11 12:19
import scrapy
import pymysql
import json
import re
import random

from datetime import datetime

from scrapy import signals

# from chn.CHN_SSE.CHN_SSE.items import MSXXNameItem, AGSSRDateFirstItem, BGSSRDateLastItem

from ..items import MSXXNameItem
from ..items import AGSSRDateFirstItem
from ..items import BGSSRDateLastItem

class SseCompanySampleSpider(scrapy.Spider):
    name = 'SSE_listing_date_name'
    allowed_domains = ['sse.com.cn']

    info_url = 'http://query.sse.com.cn/commonQuery.do?'

    data_form = {
        'isPagination': 'false',
        '_': '1573444591662',
    }

    tab_list = {
        'COMMON_SSE_ZQPZ_GP_GPLB_MSXX_C': '董事会秘书姓名',
        'COMMON_SSE_ZQPZ_GP_GPLB_AGSSR_C': '上市日*1',
        'COMMON_SSE_ZQPZ_GP_GPLB_BGSSR_C': '上市日*2'
    }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(SseCompanySampleSpider, cls).from_crawler(
            crawler, *args, **kwargs
        )
        crawler.signals.connect(spider.spider_opened, signals.spider_opened)
        return spider

    def spider_opened(self):
        """ 查询当前所有存量公司 """
        conn = pymysql.connect(**self.settings['DBARGS'])
        with conn.cursor() as cursor:
            cursor.execute("SELECT company_code, security_code FROM `company_base_info` WHERE "
                           "country_code='chn' AND exchange_market_code='SSE' AND is_batch=0 ORDER BY security_code ASC ;")
            feild_list = cursor.fetchall()

            conn.close()
            return feild_list

    def start_requests(self):
        for unqie_code in self.spider_opened():
            for tab_alone in self.tab_list:
                self.data_form['productid'] = unqie_code['security_code']
                self.data_form['sqlId'] = tab_alone
                yield scrapy.FormRequest(
                    method="GET",
                    callback=self.parse_Z,
                    url=self.info_url,
                    formdata=self.data_form,
                    meta={
                        'company_code': unqie_code['company_code'],
                        'security_code': unqie_code['security_code'],
                        'tab_value': tab_alone,
                        # 'proxy': 'http://58.218.92.147:9531'
                    }
                )

    def parse_Z(self, response):
        if response.meta['tab_value'] == 'COMMON_SSE_ZQPZ_GP_GPLB_MSXX_C':
            item = MSXXNameItem()
            item['country_code'] = 'chn'
            item['exchange_market_code'] = 'SSE'
            item['security_code'] = response.meta['security_code']
            item['company_code'] = response.meta['company_code']
            item['display_label'] = self.tab_list['COMMON_SSE_ZQPZ_GP_GPLB_MSXX_C']
            item['information'] = json.loads(response.text)['result'][0]['SECURITY_OF_THE_BOARD_OF_DIRE']
            item['gmt_create'] = str(datetime.now())
            item['user_create'] = 'xfc'
            yield item
            # cols, values = zip(*item.items())
            # print(cols, '&' * 20)
            # print(values, '%' * 20)
            # sql = "INSERT INTO `{}` ({}) VALUES {}".format \
            #         (
            #         'company_origin_information_survey_1111',
            #         ','.join(cols),
            #         (str(values) + ',')[0:-1]
            #     )
            # print('*' * 20, sql)
            # try:
            #     self.cur.execute(sql)
            #     self.conn.commit()
            # except Exception as e:
            #     print('SQL ERROR !!!', e)

        elif response.meta['tab_value'] == 'COMMON_SSE_ZQPZ_GP_GPLB_AGSSR_C' and json.loads(response.text)['result']:
            item = AGSSRDateFirstItem()
            item['country_code'] = 'chn'
            item['exchange_market_code'] = 'SSE'
            item['security_code'] = response.meta['security_code']
            item['company_code'] = response.meta['company_code']
            item['display_label'] = self.tab_list['COMMON_SSE_ZQPZ_GP_GPLB_AGSSR_C']
            item['information'] = json.loads(response.text)['result'][0]['LISTINGDATEA']
            item['gmt_create'] = str(datetime.now())
            item['user_create'] = 'xfc'
            yield item
            # cols, values = zip(*item.items())
            # print(cols, '&' * 20)
            # print(values, '%' * 20)
            # sql = "INSERT INTO `{}` ({}) VALUES {}".format \
            #         (
            #         'company_origin_information_survey_1111',
            #         ','.join(cols),
            #         (str(values) + ',')[0:-1]
            #     )
            # print('*' * 20, sql)
            # try:
            #     self.cur.execute(sql)
            #     self.conn.commit()
            # except Exception as e:
            #     print('SQL ERROR !!!', e)

        elif response.meta['tab_value'] == 'COMMON_SSE_ZQPZ_GP_GPLB_BGSSR_C' and  len(json.loads(response.text)['result']) != 0:
            item = BGSSRDateLastItem()
            item['country_code'] = 'chn'
            item['exchange_market_code'] = 'SSE'
            item['security_code'] = response.meta['security_code']
            item['company_code'] = response.meta['company_code']
            item['display_label'] = self.tab_list['COMMON_SSE_ZQPZ_GP_GPLB_BGSSR_C']
            item['information'] = json.loads(response.text)['result'][0]['LISTINGDATEB']
            item['gmt_create'] = str(datetime.now())
            item['user_create'] = 'xfc'
            yield item
            # cols, values = zip(*item.items())
            # print(cols, '&' * 20)
            # print(values, '%' * 20)
            # sql = "INSERT INTO `{}` ({}) VALUES {}".format \
            #         (
            #         'company_origin_information_survey_1111',
            #         ','.join(cols),
            #         (str(values) + ',')[0:-1]
            #     )
            # print('*' * 20, sql)
            # try:
            #     self.cur.execute(sql)
            #     self.conn.commit()
            # except Exception as e:
            #     print('SQL ERROR !!!', e)