# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# # Author: xfc
# # @Time : 2019/11/8 10:13
# import scrapy
# import json
# import pymysql
# import time
# import re
#
# from datetime import datetime
#
# from scrapy import signals
#
#
# class AsampleInfoSpider(scrapy.Spider):
#     name = 'A_sample_info'
#     allowed_domains = ['szse.cn']
#     index_url = 'http://www.szse.cn/api/report/index/companyGeneralization?'
#
#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         spider = super(AsampleInfoSpider, cls).from_crawler(
#             crawler, *args, **kwargs
#         )
#         crawler.signals.connect(spider.spider_opened, signals.spider_opened)
#         return spider
#
#     def spider_opened(self):
#         """ 查询当前所有存量公司 """
#         conn = pymysql.connect(**self.settings['DBARGS'])
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT company_code, security_code FROM `company_data_source_complete`"
#                            " WHERE country_code='chn' AND exchange_market_code='SZSE' AND "
#                            "is_batch=0 ORDER BY security_code ASC ;")
#             feild_list = cursor.fetchall()
#             return feild_list
#
#     def start_requests(self):
#         for uniques in self.spider_opened():
#             data_form = {
#                 'secCode': uniques['security_code'],
#                 'random': '0.2212441162579648'
#             }
#             yield scrapy.FormRequest(
#                 method="GET",
#                 url=self.index_url,
#                 formdata=data_form,
#                 callback=self.parse,
#                 meta={
#                     'company_code': uniques['company_code'],
#                     'security_code': uniques['security_code'],
#                     'proxy': 'http://58.218.92.76:9976'
#                 }
#             )
#
#     def tosavefile(self, unqiue_count):
#         with open('E:\\Restructure\\CHN_SSE\\CHN_SSE\\samples\\custom_code.txt', 'w') as wf:
#             wf.write(unqiue_count)
#
#     def parse(self, response):
#         if (response.status != 200) or (len(response.text) == 0) or (not json.loads(response.text)['data']) or (json.loads(response.text)['data'] is None):
#             with open('sample_error_code2.txt', 'a', encoding='utf-8') as sf:
#                 sf.write((response.meta['company_code'] + ', ' + response.meta['security_code']) + '\n')
#         else:
#             with open('E:\\Restructure\\CHN_SSE\\CHN_SSE\\samples\\custom_code.txt', 'r') as rf:
#                 unqiue_str = rf.read()
#             unique_count = int(unqiue_str)
#             unique_count += 1
#             self.tosavefile(str(unique_count))
#             company_id = "chn" + str(unique_count).zfill(5)
#
#             it1 = [(json.loads(response.text)['cols'][cols], json.loads(response.text)['data'][cols]) for cols in json.loads(response.text)['cols']]
#
#             for feilds in it1:
#                 item = SampleInfo()
#                 item['country_code'] = 'chn'
#                 item['exchange_market_code'] = 'SZSE'
#                 item['security_code'] = response.meta['security_code']
#                 item['company_code'] = response.meta['company_code']
#                 item['display_label'] = feilds[0]
#                 item['information'] = feilds[1]
#                 item['gmt_create'] = str(datetime.now())
#                 item['user_create'] = 'xfc'
#                 yield item
