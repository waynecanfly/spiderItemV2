# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# # Author: xfc
# # @Time : 2019/10/8 15:45
#
# """
#
# 股本结构
#
# """
# import scrapy
# import json
# import pymysql
# import time
#
# from datetime import datetime
# from scrapy import signals
# from ..items import StructureCapItem
# from ..items import StructureStrItem
# from ..items import EquityStructure
# from ..items import EquityChange
#
#
# class StructureSpider(scrapy.Spider):
#     name = 'SSE_structure'
#     allowed_domains = ['sse.com.cn']
#
#     conn = pymysql.connect(host='10.100.4.99', user='root', passwd='OPDATA', db='opd_common')
#     cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
#
#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         spider = super(StructureSpider, cls).from_crawler(
#             crawler, *args, **kwargs
#         )
#         crawler.signals.connect(spider.spider_opened, signals.spider_opened)
#         return spider
#
#     def spider_opened(self):
#         """ 查询当前所有存量公司 """
#         conn = pymysql.connect(**self.settings['DBARGS'])
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT company_code, security_code FROM `company_data_source_complete20191010_copy`"
#                            " WHERE country_code='chn' AND exchange_market_code='SSE' AND is_batch=0 "
#                            "ORDER BY security_code ASC ;")
#             # cursor.execute("SELECT tone.`company_code`, tone.`exchange_market_code`, tone.`company_name`, "
#             #                "tone.`security_code` FROM `company_data_source_complete20191010_copy` as tone "
#             #                "WHERE tone.`exchange_market_code`='SSE' AND tone.`company_code` NOT IN ("
#             #                "SELECT company_code FROM `company_original_information_detail_c20191104`)")
#             feild_list = cursor.fetchall()
#             conn.close()
#             return feild_list
#
#     def rember_id(self):
#         conn = pymysql.connect(**self.settings['DBARGS'])
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT max(id) FROM `company_original_information_detail_c20191104`")
#             feild_list = cursor.fetchall()
#             conn.close()
#             return feild_list
#
#     def start_requests(self):
#         """  """
#         for feild_datas in self.spider_opened():
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
#             form_data['companyCode'] = feild_datas['security_code']
#             yield scrapy.FormRequest(
#                 method = "GET",
#                 callback = self.parse_str,
#                 url = cap_url,
#                 formdata = form_data,
#                 meta = {
#                     'proxy' : 'http://58.218.200.247:9180',
#                     'company_code' : feild_datas['company_code']
#                 }
#             )
#
#             structure_url = 'http://query.sse.com.cn/commonQuery.do?'
#             str_data = {
#                 'isPagination': 'false',
#                 'sqlId': 'COMMON_SSE_CP_GPLB_GPGK_GBJG_C',
#                 # 'companyCode': '600062',
#             }
#             # str_data['companyCode'] = feild_datas['security_code']
#             # yield scrapy.FormRequest(
#             #     method = "GET",
#             #     callback = self.parse_cap,
#             #     url = structure_url,
#             #     formdata = str_data,
#             #     meta = {
#             #         'proxy' : 'http://58.218.200.227:8781',
#             #         'company_code' : feild_datas['company_code']
#             #     }
#             # )
#
#     def parse_cap(self, response):
#         dict = {}
#         item = EquityStructure()
#         cap_jres = json.loads(response.text)['result']
#         date = time.time()
#         head_id = 0
#         for index, cap_json in enumerate(cap_jres):
#             # 股份结构
#             # limited_circulating_shares = ('有限售流通股', cap_json['LIMITED_SHARES'])
#             # special_voting_unit = ('其中：特别表决权股', cap_json['LIMITED_SHARES'])
#             # unlimited_circulating_shares = ('无限售流通股', cap_json['UNLIMITED_SHARES'])
#             # unlimited_circulating_shares_A = ('无限售流通A股/CDR', cap_json['UNLIMITED_A_SHARES'])
#             # domestic_listed_stock_B = ('境内上市外资股（B股）', cap_json['B_SHARES'])
#             # domestic_listed_stock_total = ('境内上市股票合计', cap_json['DOMESTIC_SHARES'])
#             # data_time = ('数据日期', cap_json['REAL_DATE'])
#             head_id += 1
#             correlation_id = self.rember_id()[0]['max(id)'] + 1
#             head_id = correlation_id + index
#             limited_circulating_shares = ('有限售流通股', cap_json['LIMITED_SHARES'], 1, head_id)
#             special_voting_unit = ('其中：特别表决权股', cap_json['LIMITED_SHARES'], 2, head_id)
#             unlimited_circulating_shares = ('无限售流通股', cap_json['UNLIMITED_SHARES'], 3, head_id)
#             unlimited_circulating_shares_A = ('无限售流通A股/CDR', cap_json['UNLIMITED_A_SHARES'], 4, head_id)
#             domestic_listed_stock_B = ('境内上市外资股（B股）', cap_json['B_SHARES'], 5, head_id)
#             domestic_listed_stock_total = ('境内上市股票合计', cap_json['DOMESTIC_SHARES'], 6, head_id)
#             data_time = ('数据日期', cap_json['REAL_DATE'], 7, head_id)
#             code = response.meta['company_code']
#             classification_id = 7
#
#             dict['limited_circulating_shares'] = limited_circulating_shares
#             dict['special_voting_unit'] = special_voting_unit
#             dict['unlimited_circulating_shares'] = unlimited_circulating_shares
#             dict['unlimited_circulating_shares_A'] = unlimited_circulating_shares_A
#             dict['domestic_listed_stock_B'] = domestic_listed_stock_B
#             dict['domestic_listed_stock_total'] = domestic_listed_stock_total
#             dict['data_time'] = data_time
#             # dict['correlation_id'] = head_id
#             item['company_code'] = code
#             item['classification_id'] = classification_id
#             item['gmt_create'] = str(datetime.now())
#             item['user_create'] = 'xfc'
#             item['result'] = dict
#             yield item
#             # yield StructureCapItem(
#             #     company_code = code,
#             #     data_time = data_time,
#             #     limited_circulating_shares = limited_circulating_shares,
#             #     special_voting_unit = special_voting_unit,
#             #     unlimited_circulating_shares = unlimited_circulating_shares,
#             #     unlimited_circulating_shares_A = unlimited_circulating_shares_A,
#             #     domestic_listed_stock_B = domestic_listed_stock_B,
#             #     domestic_listed_stock_total = domestic_listed_stock_total
#             # )
#     #         # item = {}
#     #         # item['limited_circulating_shares'] = limited_circulating_shares
#     #         # item['special_voting_unit'] = special_voting_unit
#     #         # item['unlimited_circulating_shares'] = unlimited_circulating_shares
#     #         # item['unlimited_circulating_shares_A'] = unlimited_circulating_shares_A
#     #         # item['domestic_listed_stock_B'] = domestic_listed_stock_B
#     #         # item['domestic_listed_stock_total'] = domestic_listed_stock_total
#     #         # item['data_time'] = data_time
#     #         # item['code'] = code
#     #         # with open('test2.txt', 'a') as wf:
#     #         #     wf.write(json.dumps(item) + '\n')
#     def parse_str(self, response):
#         dict1 = {}
#         item1 = EquityChange()
#         jres = json.loads(response.text)['result']
#         date = time.time()
#         head_id = 0
#         for index, str_json in enumerate(jres):
#             # correlation_id = self.rember_id()[0]['max(id)'] + 1
#             # # head_id = correlation_id + index
#             # correlation_id = int(str(date).split('.')[0][-3:] + str(date).split('.')[-1][:6])
#             head_id += 1
#             # 变动日期
#             change_date = ('变动日期', str_json['realDate'], 1, head_id)
#             # 变动原因
#             change_reason = ('变动原因', str_json['changeReasonDesc'], 2, head_id)
#             # 变动后股数
#             change_shares = ('变动后股数', str_json['totalShares'], 3, head_id)
#             # 唯一标识
#             unique_code = ('列标识', str_json['seq'], 4)
#             classification_id = 7
#
#             dict1['change_date'] = change_date
#             dict1['change_reason'] = change_reason
#             dict1['change_shares'] = change_shares
#             # dict1['correlation_id'] = str(date).split('.')[0][-3:] + str(date).split('.')[-1][:6]
#             # item1['correlation_id'] = head_id
#             item1['company_code'] = response.meta['company_code']
#             item1['classification_id'] = classification_id
#             item1['gmt_create'] = str(datetime.now())
#             item1['user_create'] = 'xfc'
#             item1['result'] = dict1
#             yield item1
#
#             # # yield StructureStrItem(
#             # #     company_code = code,
#             # #     change_date = change_date,
#             # #     change_reason = change_reason,
#             # #     change_shares = change_shares
#             # # )
#             #
#             # # item = {}
#             # # item['change_date'] = change_date
#             # # item['change_reason'] = change_reason
#             # # item['change_shares'] = change_shares
#             # # item['code'] = code
#             # # with open('test3.txt', 'a') as wf:
#             # #     wf.write(json.dumps(item) + '\n')
#
#             # cols, values = zip(*dict1.items())
#             # print(cols, '&' * 20)
#             # print(values, '%' * 20)
#             # sql = "INSERT INTO `company_original_information_detail_c20191104` (" \
#             #       "country_code, company_code, classification_id, correlation_id, " \
#             #       "header, content, header_sort, gmt_create, user_create) " \
#             #       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);" % (
#             #     'chn',
#             #     response.meta['company_code'],
#             #     classification_id,
#             #     str(values[-1]),
#             #     str(values[0]),
#             #     str(values[1]),
#             #     str(values[2]),
#             #     str(datetime.now()),
#             #     str(item1['user_create']))
#             #
#             # try:
#             #     self.cur.execute(sql)
#             #     print(sql)
#             # except Exception as e:
#             #     print(e)
#
#
#             # cols, values = zip(*item.items())
#             # print(cols, '&' * 20)
#             # print(values, '%' * 20)
#             #
#             # sql = "INSERT INTO `{}` ({}) VALUES {}".format \
#             #         (
#             #         'security_test20190910',
#             #         ','.join(cols),
#             #         (str(values) + ',')[0:-1]
#             #     )
#             # print('*' * 20, sql)
#             # try:
#             #     cur.execute(sql)
#             #     conn.commit()
#             # except Exception as e:
#             #     print('SQL ERROR !!!', e)
