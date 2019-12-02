# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# # Author: xfc
# # @Time : 2019/10/21 16:28
# import scrapy
# import pymysql
# import json
# import random
#
# from datetime import datetime
#
# from scrapy import signals
# from ..items import MarketTypeItem
#
#
# class MarketTypeSpider(scrapy.Spider):
#     name = 'supplement_market_type'
#     allowed_domains = ['sse.com.cn']
#
#     index_url = 'http://query.sse.com.cn/security/stock/getStockListData.do?'
#
#     data_form = {
#         'isPagination': 'true',
#     }
#
#     stock_type = {'1':'主板A股', '2':'主板B股', '8':'科创板'}
#
#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         spider = super(MarketTypeSpider, cls).from_crawler(
#             crawler, *args, **kwargs
#         )
#         crawler.signals.connect(spider.spider_opened, signals.spider_opened)
#         return spider
#
#     def spider_opened(self):
#         """ 查询当前所有存量公司 """
#         conn = pymysql.connect(**self.settings['DBARGS'])
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT `company_data_source_complete20191010_copy`.`company_id`, "
#                            "`company_data_source_complete20191010_copy`.`security_code` "
#                            "FROM `company_data_source_complete20191010_copy` "
#                            "WHERE `company_data_source_complete20191010_copy`.`company_id` "
#                            "NOT IN (SELECT `company_origin_info_complete20191011_b2`.`company_code` "
#                            "FROM `company_origin_info_complete20191011_b2`)")
#             feild_list = cursor.fetchall()
#             conn.close()
#             return feild_list
#
#     def start_requests(self):
#         for unqie_code in self.spider_opened():
#             for stock_number in self.stock_type:
#                 self.data_form['stockType'] = stock_number
#                 self.data_form['stockCode'] = unqie_code['security_code']
#                 yield scrapy.FormRequest(
#                     method="GET",
#                     callback=self.parse,
#                     url=self.index_url,
#                     formdata=self.data_form,
#                     meta={
#                         # 'proxy': 'http://58.218.200.220:4081',
#                         'company_code': unqie_code['company_id'],
#                         'security_code': unqie_code['security_code'],
#                         'stockType': self.stock_type[stock_number],
#                     }
#                 )
#
#     def parse(self, response):
#         # try:
#         if len(json.loads(response.text)['result']) != 0:
#             print(response.meta['security_code'], '&&&', response.meta['stockType'], '&&&&&&&&&', response.text)
#
#             jres = json.loads(response.text)['result'][0]
#             company_abbreviation_A = ('公司简称', ''.join(jres['SECURITY_ABBR_A']).replace('-', jres['SECURITY_ABBR_B']))
#             company_abbreviation_B = ('简称', ''.join(jres['SECURITY_ABBR_B']).replace('-', jres['SECURITY_ABBR_A']))
#             security_code = ('公司代码', jres['COMPANY_CODE'])
#             abbreviation_code = ('代码', ''.join(jres['SECURITY_CODE_B']).replace('-', jres['SECURITY_CODE_A']))
#             company_listing_date = ('上市公司', jres['LISTING_DATE'])
#             market_type = ('市场类型', response.meta['stockType'])
#             company_code = ('公司代码', response.meta['company_code'])
#
#             yield MarketTypeItem(
#                 company_code = company_code,
#                 company_abbreviation_A = company_abbreviation_A,
#                 company_abbreviation_B = company_abbreviation_B,
#                 security_code = security_code,
#                 abbreviation_code = abbreviation_code,
#                 company_listing_date = company_listing_date,
#                 market_type = market_type,
#             )
#
#         # except Exception as e:
#         #     print(e)