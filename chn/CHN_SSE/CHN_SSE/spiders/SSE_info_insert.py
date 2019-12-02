# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# # Author: xfc
# # @Time : 2019/10/10 15:52
# """
#
# 上海交易所：
#     公司详情信息
#
# """
#
# import scrapy
# import json
# import pymysql
# import requests
# import random
# from datetime import datetime
#
# from scrapy import signals
# from ..items import SecretaryName
#
#
# class SseInfoSpider(scrapy.Spider):
#     name = 'SSE_info_insert'
#     allowed_domains = ['sse.com.cn']
#     info_url = 'http://query.sse.com.cn/commonQuery.do?'
#     common_sse_list = [
#         'COMMON_SSE_ZQPZ_GP_GPLB_C',
#         'COMMON_SSE_ZQPZ_GP_GPLB_MSXX_C',
#         'COMMON_SSE_ZQPZ_GP_GPLB_AGSSR_C',
#         'COMMON_SSE_ZQPZ_GP_GPLB_BGSSR_C'
#     ]
#
#     ip_pool = [
#         "58.218.201.114:6645",
#         "58.218.200.214:2575",
#         "58.218.200.253:4606",
#         "58.218.200.214:7702",
#         "58.218.200.253:3251",
#         "58.218.201.74:3354",
#         "58.218.200.253:3103",
#         "58.218.201.74:5791",
#         "58.218.200.253:6534",
#         "58.218.201.114:7859",
#         "58.218.200.253:2823",
#         "58.218.201.74:4034",
#         "58.218.200.253:2972",
#         "58.218.201.74:6591",
#         "58.218.201.114:7727",
#         "58.218.201.114:8372",
#         "58.218.201.114:8771",
#         "58.218.201.74:3451",
#         "58.218.201.114:5110",
#     ]
#
#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         spider = super(SseInfoSpider, cls).from_crawler(
#             crawler, *args, **kwargs
#         )
#         crawler.signals.connect(spider.spider_opened, signals.spider_opened)
#         return spider
#
#     def spider_opened(self):
#         """ 查询当前所有存量公司 """
#         conn = pymysql.connect(**self.settings['DBARGS'])
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT company_id, security_code FROM `company_data_source_complete20191010` "
#                            "WHERE country_code='chn' AND is_batch=0 ORDER BY security_code ASC ;")
#             feild_list = cursor.fetchall()
#             conn.close()
#             queue_list = []
#             for feild_dict in feild_list:
#                 queue_list.append([feild_dict['company_id'], feild_dict['security_code']])
#
#             return queue_list
#
#     def get_proxy(self):
#         with open('E:\\Restructure\\CHN_SSE\\CHN_SSE\\samples\\ip_proxy.txt', 'r') as rf:
#             ip_address = rf.read()
#         print(ip_address, '*'*50)
#
#     def start_requests(self):
#         """
#
#         COMMON_SSE_ZQPZ_GP_GPLB_AGSSR_C     上市日——1
#         COMMON_SSE_ZQPZ_GP_GPLB_BGSSR_C     上市日——2
#         COMMON_SSE_ZQPZ_GP_GPLB_MSXX_C      董事会秘书电话
#         COMMON_SSE_ZQPZ_GP_GPLB_C           公司概况
#
#         """
#
#         for fir_code in self.spider_opened():
#
#             accpet_params = {
#                 'isPagination': 'false',
#             }
#
#             # for source_id in self.common_sse_list:
#             accpet_params['sqlId'] = 'COMMON_SSE_ZQPZ_GP_GPLB_BGSSR_C'
#             accpet_params['productid'] = fir_code[1]
#
#             yield scrapy.FormRequest(
#                 method="GET",
#                 callback=self.parse,
#                 url=self.info_url,
#                 formdata=accpet_params,
#                 meta={
#                     'company_id' : fir_code[0],
#                     'security_code' : fir_code[1],
#                     # 'proxy' : 'http://' + random.choice(self.ip_pool)
#                 }
#             )
#
#     def parse(self, response):
#         try:
#             if len(json.loads(response.text)['result']) != 0:
#                 jres = json.loads(response.text)['result'][0]
#                 secretary_name = ('上市日2', jres['SECURITY_OF_THE_BOARD_OF_DIRE'])
#                 item = SecretaryName()
#                 item['country_code'] = 'chn'
#                 item['company_code'] = response.meta['company_id']
#                 item['display_label'] = secretary_name[0]
#                 item['information'] = secretary_name[1]
#                 item['gmt_create'] = str(datetime.now())
#                 item['user_create'] = 'xfc'
#                 yield item
#
#         except:
#             with open('unique_code.txt', 'a') as wf:
#                 wf.write((response.meta['company_id'] + ', ' + response.meta['security_code']) + '\n')
#
