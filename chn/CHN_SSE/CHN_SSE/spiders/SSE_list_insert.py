#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/10/10 11:16
"""

上交所：
    插入网站公司列表

"""

import scrapy
import json
import pymysql
from datetime import datetime

from scrapy import signals
from ..items import CompanyListItem
from ..items import AddCompanyMarketItem


class ListInsert(scrapy.Spider):
    name = 'SSE_list_insert'
    allowed_domains = ['sse.com.cn']
    code_urls = 'http://query.sse.com.cn/security/stock/getStockListData2.do?'
    info_urls = 'http://query.sse.com.cn/commonQuery.do?'

    common_sse_list = [
        'COMMON_SSE_ZQPZ_GP_GPLB_C',
        'COMMON_SSE_ZQPZ_GP_GPLB_MSXX_C',
        'COMMON_SSE_ZQPZ_GP_GPLB_AGSSR_C',
        'COMMON_SSE_ZQPZ_GP_GPLB_BGSSR_C'
    ]

    market_type_list = [1, 2, 8]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ListInsert, cls).from_crawler(
            crawler, *args, **kwargs
        )
        crawler.signals.connect(spider.spider_opened, signals.spider_opened)
        return spider

    def spider_opened(self):
        """ 查询当前所有存量公司 """
        conn = pymysql.connect(**self.settings['DBARGS'])
        with conn.cursor() as cursor:
            cursor.execute("SELECT security_code FROM `company_base_info` "
                           "WHERE country_code='chn' AND exchange_market_code='SSE' "
                           "AND is_batch=0 ORDER BY security_code ASC ;")
            feild_list = cursor.fetchall()
            conn.close()

            return [unique_code['security_code'] for unique_code in feild_list]

    def tosavefile(self, unqiue_count):
        with open('E:\\Restructure\\CHN_SSE\\CHN_SSE\\samples\\custom_code.txt', 'w') as wf:
            wf.write(unqiue_count)

    def start_requests(self):
        params_list = {
            'isPagination': 'true',
            'pageHelp.pageSize': '1000',
        }

        # 判断市场类型分类
        for market_type in ['1', '2', '8']:
            params_list['stockType'] = market_type

            yield scrapy.FormRequest(
                method = 'GET',
                callback = self.parse,
                url = self.code_urls,
                formdata = params_list,
                meta = {
                    "market_type": market_type,
                    # "proxy": 'http://58.218.200.253:9254'
                }
            )

    def parse(self, response):
        accpet_params = {
            'isPagination': 'false',
        }

        json_data = json.loads(response.text)

        if response.meta['market_type'] == '1':
            type_name = ('主板A股', 'A股代码')
        elif response.meta['market_type'] == '2':
            type_name = ('主板B股', 'B股代码')
        elif response.meta['market_type'] == '8':
            type_name = ('科创板', '科创板代码')
        else:
            return "ERROR TYPE"


        for datas_jres in json_data['result']:

            with open('E:\\Restructure\\CHN_SSE\\CHN_SSE\\samples\\custom_code.txt', 'r') as rf:
                unqiue_str = rf.read()
            unique_count = int(unqiue_str)
            unique_count += 1
            self.tosavefile(str(unique_count))
            company_id = "chn" + str(unique_count).zfill(5)
            # item = {}
            # item['company_id'] = company_id
            # item['type_market'] = type_name
            # item['security_code'] = datas_jres['COMPANY_CODE']
            # item['company_abbreviation'] = ''.join(datas_jres['SECURITY_ABBR_A']).replace('-', datas_jres['SECURITY_ABBR_B'])
            # item['abbreviation'] = ''.join(datas_jres['SECURITY_ABBR_B']).replace('-', datas_jres['SECURITY_ABBR_A'])
            # item['listing_date'] = datas_jres['LISTING_DATE']
            # item['code'] = ''.join(datas_jres['SECURITY_CODE_B']).replace('-', datas_jres['SECURITY_CODE_A'])
            if datas_jres['COMPANY_CODE'] not in self.spider_opened():
                item = CompanyListItem()
                item['company_code'] = company_id
                item['company_short_name'] = ''.join(datas_jres['SECURITY_ABBR_A']).replace('-', datas_jres['SECURITY_ABBR_B'])
                # item['abbreviation'] = ''.join(datas_jres['SECURITY_ABBR_B']).replace('-', datas_jres['SECURITY_ABBR_A'])
                item['country_code'] = 'chn'
                item['exchange_market_code'] = 'SSE'
                item['market_type'] = type_name[0]
                item['security_code'] = datas_jres['COMPANY_CODE']
                item['company_list_url'] = 'http://www.sse.com.cn/assortment/stock/list/share/' + '{市场类型为：' + type_name[0] + '}'
                item['ipo_date'] = datas_jres['LISTING_DATE']
                item['is_batch'] = 1
                item['spider_name'] = 'SSE_list_insert'
                item['gmt_create'] = str(datetime.now())
                item['user_create'] = 'xfc'
                yield item

                yield AddCompanyMarketItem(
                    country_code='chn',
                    exchange_market_code='SSE',
                    security_code=datas_jres['COMPANY_CODE'],
                    company_code=company_id,
                    display_label=type_name[-1],
                    information=''.join(datas_jres['SECURITY_CODE_B']).replace('-', datas_jres['SECURITY_CODE_A']),
                    gmt_create=str(datetime.now()),
                    user_create='xfc'
                )

            # else:
            #     break

            # cols, values = zip(*item.items())
            # print(cols, '&' * 20)
            # print(values, '%' * 20)
            #
            # sql = "INSERT INTO `{}` ({}) VALUES {}".format \
            #         (
            #         'company_data_source_complete20191010',
            #         ','.join(cols),
            #         (str(values) + ',')[0:-1]
            #     )
            # print('*' * 20, sql)
            # try:
            #     self.cur.execute(sql)
            #     self.conn.commit()
            # except Exception as e:
            #     print(e)
            #     return 'SQL ERROR IS : %s ' % e


