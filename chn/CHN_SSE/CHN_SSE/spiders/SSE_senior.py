# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# # Author: xfc
# # @Time : 2019/10/8 10:04
# import scrapy
# import json
# import pymysql
#
# from scrapy import signals
# from datetime import datetime
# from ..items import SeniorInfo
# from ..items import Executive
#
# class SeniorSpider(scrapy.Spider):
#     name = 'SSE_senior'
#     allowed_domains = ['sse.com.cn']
#
#     start_url = 'http://query.sse.com.cn/commonQuery.do?'
#
#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         spider = super(SeniorSpider, cls).from_crawler(
#             crawler, *args, **kwargs
#         )
#         crawler.signals.connect(spider.spider_opened, signals.spider_opened)
#         return spider
#
#     def spider_opened(self):
#         """ 查询当前所有存量公司 """
#         conn = pymysql.connect(**self.settings['DBARGS'])
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT company_code, security_code FROM `company_data_source_complete20191010_copy` "
#                            "WHERE country_code='chn' AND exchange_market_code='SSE' AND is_batch=0 ORDER BY security_code ASC ;")
#             feild_list = cursor.fetchall()
#
#             conn.close()
#
#             return feild_list
#
#     def start_requests(self):
#         """ 第一次请求获取公司高管人员信息 """
#
#         for feild_datas in self.spider_opened():
#
#             senior_data = {
#                 'isPagination': 'true',
#                 'sqlId': 'COMMON_SSE_ZQPZ_GG_GGRYLB_L',
#                 # 'pageHelp.pageSize': '25',
#                 # 'pageHelp.pageCount': '50',
#                 # 'pageHelp.pageNo': '1',
#                 # 'pageHelp.beginPage': '1',
#                 # 'pageHelp.cacheSize': '1',
#                 # 'pageHelp.endPage': '5',
#                 # '_': '1568707971354',
#             }
#             senior_data['productid'] = feild_datas['security_code']
#
#             yield scrapy.FormRequest(
#                 method = "GET",
#                 callback = self.parse,
#                 url = self.start_url,
#                 formdata = senior_data,
#                 meta = {
#                     'security_code' : senior_data['productid'],
#                     'company_code' : feild_datas['company_code'],
#                     'proxy' : 'http://58.218.200.227:9134'
#                 }
#             )
#
#     def parse(self, response):
#         """ 匹配页面信息 """
#         item = Executive()
#         dict = {}
#         json_info = json.loads(response.text)
#         head_id = 0
#         for result_info in json_info['result']:
#             if result_info is None:
#                 print('#'*20, json_info)
#
#             head_id += 1
#             #   任职时间
#             appointment_time = ('任职时间', result_info['START_TIMES'], 1, head_id)
#             #   职务
#             fuction = ('职务', result_info['BUSINESSES'], 2, head_id)
#             #   姓名
#             name = ('姓名', result_info['NAME'], 3, head_id)
#
#             code = ('公司代码', response.meta['company_code'])
#             classification_id = 35
#
#             dict['appointment_time'] = appointment_time
#             dict['fuction'] = fuction
#             dict['name'] = name
#             item['company_code'] = response.meta['company_code']
#             item['classification_id'] = classification_id
#             item['gmt_create'] = str(datetime.now())
#             item['user_create'] = 'xfc'
#             item['result'] = dict
#
#             yield item
#
