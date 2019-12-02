# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# # Author: xfc
# # @Time : 2019/11/1 11:54
#
# """
#
# 股本结构
#
# """
# import scrapy
# import json
# import pymysql
#
# from datetime import datetime
# from scrapy import signals
#
# class StructureExampleSpider(scrapy.Spider):
#     name = 'SSE_structure_example'
#     allowed_domains = ['sse.com.cn']
#
#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         spider = super(StructureExampleSpider, cls).from_crawler(
#             crawler, *args, **kwargs
#         )
#         crawler.signals.connect(spider.spider_opened, signals.spider_opened)
#         return spider
#
#     def spider_opened(self):
#         """ 查询当前所有存量公司 """
#         conn = pymysql.connect(**self.settings['DBARGS'])
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT tone.`company_code`, tone.`exchange_market_code`, tone.`company_name`, "
#                            "tone.`security_code` FROM `company_data_source_complete20191010_copy` as tone "
#                            "WHERE tone.`exchange_market_code`='SSE' AND tone.`company_code` NOT IN ("
#                            "SELECT company_code FROM `company_original_information_detail`)")
#             feild_list = cursor.fetchall()
#             conn.close()
#             return feild_list
#
#     def read_base(self):
#         conn = pymysql.connect(**self.settings['DBARGS'])
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT max(id) FROM ")
#             feild_list = cursor.fetchall()
#             conn.close()
#             return feild_list
#
#     def start_requests(self):
#         for feild_dicts in self.spider_opened():
#             company_code = feild_dicts['company_code']
#             security_code = feild_dicts['security_code']
#             exchange_market_code = feild_dicts['exchange_market_code']
#
#             cap_url = 'http://query.sse.com.cn/security/stock/queryEquityChangeAndReason.do?'
#             form_data = {
#                 'isPagination': 'true',
#                 # 'companyCode': '600062',
#                 # 'pageHelp.pageSize': '25',
#                 # 'pageHelp.pageCount': '50',
#                 # 'pageHelp.pageNo': '1',
#                 # 'pageHelp.beginPage': '1',
#                 # 'pageHelp.cacheSize': '1',
#                 # 'pageHelp.endPage': '5',
#                 # '_': '1568708138396'
#             }
#             form_data['companyCode'] = security_code
#             yield scrapy.FormRequest(
#                 method="GET",
#                 url=cap_url,
#                 formdata=form_data,
#                 callback=self.parse,
#                 meta={
#                     'company_code' : company_code,
#                     'exchange_market_code' : exchange_market_code
#                 }
#             )
#
#             # 数据日期
#             date_url = 'http://query.sse.com.cn/commonQuery.do?'
#             form_data2 = {
#                 # 'jsonCallBack': 'jsonpCallback89125',
#                 'isPagination': 'false',
#                 'sqlId': 'COMMON_SSE_CP_GPLB_GPGK_GBJG_C'
#             }
#             form_data2['companyCode'] = security_code
#             yield scrapy.FormRequest(
#                 url=date_url,
#                 callback=self.parse_date,
#                 method="GET",
#                 formdata=form_data2,
#                 meta={
#                     'company_code': company_code,
#                     'exchange_market_type': exchange_market_code
#                 }
#             )
#
#     def parse(self, response):
#         print(json.loads(response.text)['pageHelp']['total'])
#         # 数据总量
#         data_total = json.loads(response.text)['pageHelp']['total']
#         # 股本变动
#         data_result = json.loads(response.text)['result']
#         for data_feild in data_result:
#             realDate = ('变动日期', data_feild['realDate'])
#             changeReasonDesc = ('变动原因', data_feild['changeReasonDesc'])
#             totalShares = ('变动后股数(万股)', data_feild['totalShares'])
#             # print(realDate, '*&'*20)
#
#     def parse_date(self, response):
#         # print(response.text)
#         print(json.loads(response.text)['result'][0]['REAL_DATE'], '@'*30)
#
#
