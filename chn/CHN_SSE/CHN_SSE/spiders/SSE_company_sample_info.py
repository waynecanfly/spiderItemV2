#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/11/11 11:51
import scrapy
import pymysql
import json
import random

from datetime import datetime

from scrapy import signals
from ..items import SampleInfoItem


class SseCompanySampleSpider(scrapy.Spider):
    name = 'SSE_company_sample_info'
    allowed_domains = ['sse.com.cn']

    info_url = 'http://query.sse.com.cn/commonQuery.do?'

    data_form = {
        'isPagination': 'false',
        'sqlId': 'COMMON_SSE_ZQPZ_GP_GPLB_C',
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
            self.data_form['productid'] = unqie_code['security_code']
            yield scrapy.FormRequest(
                method="GET",
                callback=self.parse_Z,
                url=self.info_url,
                formdata=self.data_form,
                meta={
                    'company_code': unqie_code['company_code'],
                    'security_code': unqie_code['security_code'],
                    # 'proxy': 'http://58.218.92.147:9531'
                }
            )

    def parse_Z(self, response):
        if len(json.loads(response.text)['result']) != 0:

            jres = json.loads(response.text)['result'][0]

            feilds = [
                ('内部编码', response.meta['company_code']),
                ('公司代码', jres['COMPANY_CODE']),
                ('股票代码', (jres['SECURITY_CODE_A'] + '/' + jres['SECURITY_CODE_B'])),
                ('可转债简称', jres['CHANGEABLE_BOND_ABBR']),
                ('可转债代码', jres['CHANGEABLE_BOND_CODE']),
                ('公司简称中文', jres['COMPANY_ABBR']),
                ('公司简称英文', jres['ENGLISH_ABBR']),
                ('公司全称中文', jres['FULLNAME']),
                ('公司全称英文', jres['FULL_NAME_IN_ENGLISH']),
                ('注册地址', jres['COMPANY_ADDRESS']),
                ('通讯地址', jres['OFFICE_ADDRESS']),
                ('邮编', jres['OFFICE_ZIP']),
                ('法定代表人', jres['LEGAL_REPRESENTATIVE']),
                ('E-mail', jres['E_MAIL_ADDRESS']),
                ('联系电话', jres['REPR_PHONE']),
                ('网址', jres['WWW_ADDRESS']),
                ('CSRC行业(门类/大类/中类)', (jres['CSRC_CODE_DESC'] + '/' + jres['CSRC_GREAT_CODE_DESC'] + '/' + jres['CSRC_MIDDLE_CODE_DESC'])),
                ('SSE行业', jres['SSE_CODE_DESC']),
                ('所属省/直辖市', jres['AREA_NAME_DESC']),
                ('状态', (jres['STATE_CODE_A_DESC'] + '/' + jres['STATE_CODE_B_DESC'])),
                ('是否上证180样本股', jres['SECURITY_30_DESC']),
                ('是否境外上市', jres['FOREIGN_LISTING_DESC']),
                ('境外上市地', jres['FOREIGN_LISTING_ADDRESS'])
            ]
            for it2 in feilds:
                item = SampleInfoItem()
                item['country_code'] = 'chn'
                item['exchange_market_code'] = 'SSE'
                item['security_code'] = response.meta['security_code']
                item['company_code'] = response.meta['company_code']
                item['display_label'] = it2[0]
                item['information'] = it2[1]
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
