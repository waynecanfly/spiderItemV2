# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# # Author: xfc
# # @Time : 2019/9/19 17:49
# import scrapy
# import pymysql
# from scrapy import signals
# from twisted.enterprise import adbapi
#
#
#
# class SseInfo(scrapy.Spider):
#     name = 'SSE_info'
#     allowed_domains = ['sse.com.cn']
#
#     info_urls = 'http://query.sse.com.cn/commonQuery.do?'
#
#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         spider = super(SseInfo, cls).from_crawler(
#             crawler, *args, **kwargs
#         )
#         crawler.signals.connect(spider.spider_opened, signals.spider_opened)
#         crawler.signals.connect(spider.spider_closed, signals.spider_closed)
#         return spider
#
#     def spider_opened(self, spider):
#         conn = pymysql.connect(**self.settings['DBARGS'])
#         with conn.cursor() as cursor:
#             # cursor.execute("SELECT "
#             #                "security_code "
#             #                "FROM `company_data_source` "
#             #                "WHERE country_code = 'chn' "
#             #                "AND exchange_market_code = 'sse' "
#             #                "ORDER BY security_code "
#             #                "ASC ;")
#             cursor.execute("SELECT security_code FROM `company_data_source` ORDER BY security_code ASC ;")
#             feild_list = cursor.fetchall()
#             for feild_dict in feild_list:
#                 self.company_code_update = feild_dict['code']
#                 self.unqiue_code_update = feild_dict['security_code']
#
#             conn.close()
#
#
#     def spider_closed(self, spider):
#         conn = pymysql.connect(**self.settings['DBARGS'])
#         with conn.cursor() as cursor:
#             # cursor.execute("SELECT "
#             #                "security_code "
#             #                "FROM `company_data_source` "
#             #                "WHERE country_code = 'chn' "
#             #                "AND exchange_market_code = 'sse' "
#             #                "ORDER BY security_code "
#             #                "ASC ;")
#             cursor.execute("SELECT `company_data_source_test20190910`.`security_code` "
#                            "FROM `company_data_source_test20190910` "
#                            "WHERE security_code "
#                            "NOT IN (SELECT security_code FROM `company_test20190910`)")
#             feild_list = cursor.fetchall()
#             for feild_dict in feild_list:
#                 self.company_code_add = feild_dict['code']
#                 self.unqiue_code_add = feild_dict['security_code']
#
#             conn.close()
#
#     def start_requests(self):
#         """ 发现页面上新增的公司 """
#         data_form = {
#             'isPagination': 'false',
#             'sqlId': 'COMMON_SSE_ZQPZ_GP_GPLB_C',
#         }
#
#         judge = [0 ,1]
#         for judge_value in judge:
#             # 值为0：新增；值为1：更新原来数据
#             if judge_value == 0:
#                 unqiue_code = self.unqiue_code_add
#             elif judge_value == 1:
#                 unqiue_code = self.unqiue_code_update
#
#             else:
#                 break
#
#
#             data_form['productid'] = unqiue_code
#             yield scrapy.FormRequest(method = "GET",
#                                      callback = self.parse,
#                                      url = self.info_urls,
#                                      formdata = data_form,
#                                      meta={
#                                          'judge' : judge
#                                      }
#                                      )
#
#
#
#     def parse(self, response):
#         if response.meta['judge'] == 0:
#             pass
#         elif response.meta['judge'] == 1:
#             pass
#         else:
#             return -1