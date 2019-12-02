# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# # Author: xfc
# # @Time : 2019/11/12 23:55
# import scrapy
# import pymysql
# import json
# import random
# import re
#
# from datetime import datetime
#
# from scrapy import signals
#
#
# class DeductProfitSpider(scrapy.Spider):
#     name = 'deduct_profit'
#     allowed_domains = ['sse.com.cn']
#
#     conn = pymysql.connect(host='10.100.4.99', user='root', passwd='OPDATA', db='opd_common', charset='utf8')
#     cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
#
#     def start_requests(self):
#         request_url = 'http://www.sse.com.cn/disclosure/listedinfo/loss/'
#
#         yield scrapy.Request(
#             url=request_url,
#             callback=self.parse
#         )
#
#     def parse(self, response):
#         security_code = response.xpath('/html/body/div[8]/div[2]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div/div/table/tbody/tr/td[1]/text()').extract()
#         security_simple = response.xpath('/html/body/div[8]/div[2]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div/div/table/tbody/tr/td[2]/text()').extract()
#         recurring_profit = response.xpath('/html/body/div[8]/div[2]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div/div/table/tbody/tr/td[3]/text()').extract()
#         profit_date = response.xpath('/html/body/div[8]/div[2]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div/div/table/tbody/tr/td[4]/text()').extract()
#
#         for datas in zip(security_code, security_simple, recurring_profit, profit_date):
#             item = {}
#             item['country_code'] = 'chn'
#             item['exchange_market_code'] = 'SSE'
#             item['security_code'] = datas[0]
#             item['security_simple'] = datas[1]
#             item['recurring_profit'] = datas[2]
#             item['profit_date'] = datas[3]
#             item['gmt_create'] = str(datetime.now())
#             item['user_create'] = 'xfc'
#             cols, values = zip(*item.items())
#             print(cols, '&' * 20)
#             print(values, '%' * 20)
#             sql = "INSERT INTO `{}` ({}) VALUES {}".format \
#                     (
#                     'recurring_gains',
#                     ','.join(cols),
#                     (str(values) + ',')[0:-1]
#                 )
#             print('*' * 20, sql)
#             try:
#                 self.cur.execute(sql)
#                 self.conn.commit()
#             except Exception as e:
#
#                 print('SQL ERROR !!!', e)