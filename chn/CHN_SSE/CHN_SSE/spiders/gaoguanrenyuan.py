# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# # Author: xfc
# # @Time : 2019/11/12 0:38
# import scrapy
# import json
# import time
# import pymysql
#
# from datetime import datetime
#
# from scrapy import signals
#
# from CHN_SSE.items import SeniorManagementItem
#
#
# class GgrySpider(scrapy.Spider):
#     name = 'gaoguanrenyuan'
#     allowed_domains = ['sse.com.cn']
#     request_url = 'http://query.sse.com.cn/commonQuery.do?'
#
#     data_form = {
#         'isPagination': 'true',
#         'sqlId': 'COMMON_SSE_ZQPZ_GG_GGRYLB_L',
#         'pageHelp.pageSize': '25',
#         'pageHelp.pageCount': '50',
#         'pageHelp.pageNo': '1',
#         'pageHelp.beginPage': '1',
#         'pageHelp.cacheSize': '1',
#         'pageHelp.endPage': '5',
#         '_': '1573490213499'
#     }
#
#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         spider = super(GgrySpider, cls).from_crawler(
#             crawler, *args, **kwargs
#         )
#         crawler.signals.connect(spider.spider_opened, signals.spider_opened)
#         return spider
#
#     def spider_opened(self):
#         """ 查询当前所有存量公司 """
#         conn = pymysql.connect(**self.settings['DBARGS'])
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT company_code, security_code FROM `company_data_source_complete20191010_copy` WHERE "
#                            "country_code='chn' AND exchange_market_code='SSE' AND is_batch=0 ORDER BY security_code ASC ;")
#             feild_list = cursor.fetchall()
#
#             conn.close()
#             return feild_list
#
#     def start_requests(self):
#         for uniques in self.spider_opened():
#             self.data_form['productid'] = uniques['security_code']
#             yield scrapy.FormRequest(
#                 method="GET",
#                 url=self.request_url,
#                 formdata=self.data_form,
#                 callback=self.parse,
#                 meta={
#                     'company_code': uniques['company_code'],
#                     'security_code': uniques['security_code']
#                 }
#             )
#
#     def parse(self, response):
#         name_item = {
#             'NAME': '姓名',
#             'BUSINESSES': '职务',
#             'START_TIMES': '任职时间',
#             'BUSINESSDESCES': 'QYvalue',
#             'NUM': 'QYvalue'
#         }
#
#         feild_list = [[name_item[result], dats[result], str(int(index)+1)] for index, dats in enumerate(json.loads(response.text)['result']) for result in dats]
#         for data_all in zip(feild_list, [lis for lis in range(1, 6)]):
#             item = SeniorManagementItem()
#             item['country_code'] = 'chn'
#             item['exchange_market_code'] = 'SSE'
#             item['security_code'] = response.meta['security_code']
#             item['company_code'] = response.meta['company_code']
#             item['classification_id'] = 35
#             item['correlation_id'] = data_all[0][-1]
#             item['header'] = data_all[0][0]
#             item['header_sort'] = data_all[1]
#             item['content'] = data_all[0][1]
#             item['gmt_create'] = str(datetime.now())
#             item['user_create'] = 'xfc'
#             yield item
#             # cols, values = zip(*item.items())
#             # print(cols, '&' * 20)
#             # print(values, '%' * 20)
#             # sql = "INSERT INTO `{}` ({}) VALUES {}".format \
#             #         (
#             #         'company_original_information_detail_1111',
#             #         ','.join(cols),
#             #         (str(values) + ',')[0:-1]
#             #     )
#             # print('*' * 20, sql)
#             # try:
#             #     self.cur.execute(sql)
#             #     self.conn.commit()
#             # except Exception as e:
#             #     print('SQL ERROR !!!', e)
#
