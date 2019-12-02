# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# # Author: xfc
# # @Time : 2019/11/12 14:49
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
# class DelisingListSpider(scrapy.Spider):
#     name = 'Delising_list'
#     allowed_domains = ['sse.com.cn']
#
#     list_url = 'http://query.sse.com.cn/security/stock/getStockListData2.do?'
#
#     conn = pymysql.connect(host='10.100.4.99', user='root', passwd='OPDATA', db='opd_common', charset='utf8')
#     cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
#
#     def start_requests(self):
#         data_form = {
#             'isPagination': 'true',
#             # 'stockCode': '',
#             # 'csrcCode': '',
#             # 'areaName': '',
#             'stockType': '5',
#             # 'pageHelp.cacheSize': '1',
#             # 'pageHelp.beginPage': '1',
#             # 'pageHelp.pageSize': '25',
#             # 'pageHelp.pageNo': '1',
#             '_': '1573541790835'
#         }
#         yield scrapy.FormRequest(
#             method="GET",
#             url=self.list_url,
#             formdata=data_form,
#             callback=self.parse,
#             meta={
#
#             }
#         )
#
#     def parse(self, response):
#         vals_item = {
#             'COMPANY_CODE': '原公司代码',
#             'COMPANY_ABBR': '原公司简称',
#             'LISTING_DATE': '上市日期',
#             'CHANGE_DATE': '终止上市时间',
#             'END_SHARE_CODE': '终止上市后股份转让代码',
#             'END_SHARE_MAIN_DEPART': '终止上市后股份转让主办券商',
#             'END_SHARE_VICE_DEPART': '终止上市后股份转让副主办券商',
#             'LISTING_BOARD': 'QYvalue',
#             'NUM': 'QYvalue',
#             'SECURITY_ABBR_A': 'QYvalue',
#             'SECURITY_ABBR_B': 'QYvalue',
#             'SECURITY_CODE_A': 'QYvalue',
#             'SECURITY_CODE_B': 'QYvalue'
#         }
#         print([[vals_item[vals], result[vals]] for result in json.loads(response.text)['result'] for vals in result])
#
#         for result in json.loads(response.text)['result']:
#             item = {}
#             item['country_code'] = 'chn'
#             item['exchange_market_code'] = 'SSE'
#             item['security_code'] = result['COMPANY_CODE']
#             item['company_origin_name'] = result['COMPANY_ABBR']
#             item['listing_date'] = result['LISTING_DATE']
#             item['delisting_date'] = result['CHANGE_DATE']
#             item['transfer_code'] = result['END_SHARE_CODE']
#             item['firm_delisting'] = result['END_SHARE_MAIN_DEPART']
#             item['charge_deputy'] = result['END_SHARE_VICE_DEPART']
#             item['gmt_create'] = str(datetime.now())
#             item['user_create'] = 'xfc'
#             cols, values = zip(*item.items())
#             print(cols, '&' * 20)
#             print(values, '%' * 20)
#             sql = "INSERT INTO `{}` ({}) VALUES {}".format \
#                     (
#                     'Delising_company',
#                     ','.join(cols),
#                     (str(values) + ',')[0:-1]
#                 )
#             print('*' * 20, sql)
#             try:
#                 self.cur.execute(sql)
#                 self.conn.commit()
#             except Exception as e:
#                 print('SQL ERROR !!!', e)
