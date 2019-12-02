# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# # Author: xfc
# # @Time : 2019/11/11 13:03
# """
#
# 利润分配
#     分红
#     送股
#
# """
#
# import scrapy
# import json
# import pymysql
#
# from datetime import datetime
# from scrapy import signals
# from ..items import AGFHItem, BGFHItem, AGSGItem, BGSGItem
#
#
# class LiRunFenPeiSpdier(scrapy.Spider):
#     name = 'LiRunFenPei'
#     allowed_domains = ['sse.com.cn']
#
#     request_url = 'http://query.sse.com.cn/commonQuery.do?'
#
#     data_form = {
#         'isPagination': 'false',
#     }
#
#     A_equry = {
#         'RECORD_DATE_A': '股权登记日',
#         'ISS_VOL': '股权登记日总股本(万股)',
#         'EX_DIVIDEND_DATE_A': '除息交易日',
#         'LAST_CLOSE_PRICE_A': '除息前日收盘价',
#         'OPEN_PRICE_A': '除息报价',
#         'DIVIDEND_PER_SHARE1_A': '每股红利',
#         'DIVIDEND_PER_SHARE2_A': 'QYvalue',
#         'TOTAL_DIVIDEND_A': 'QYvalue',
#         'A_SHARES': 'QYvalue',
#         'FULL_NAME': 'QYvalue',
#         'SECURITY_CODE_A': 'QYvalue',
#         'SECURITY_NAME_A': 'QYvalue',
#         'COMPANY_CODE': 'QYvalue'
#     }
#
#     B_equry = {
#         'LAST_TRADE_DATE_B': '最后交易日',
#         'RECORD_DATE_B': '股权登记日',
#         'ISS_VOL': '股权登记日总股本(万股)',
#         'EX_DIVIDEND_DATE_B': '除息交易日',
#         'LAST_CLOSE_PRICE_B': '除息前日收盘价',
#         'OPEN_PRICE_B': '除息报价',
#         'DIVIDEND_PER_SHARE1_B': '每股红利',
#         'EXCHANGE_RATE': '美元汇率',
#         'DIVIDEND_PER_SHARE2_B': 'QYvalue',
#         'TOTAL_DIVIDEND_B': 'QYvalue',
#         'SECURITY_CODE_B': 'B股代码',
#         'SECURITY_NAME_B': '股票名称',
#         'COMPANY_CODE': 'QYvalue',
#         'FULL_NAME': 'QYvalue'
#     }
#
#     A_song = {
#         'RECORD_DATE_A': '股权登记日',
#         'ISS_VOL': '股权登记日总股本(万股)',
#         'EX_RIGHT_DATE_A': '除权基准日',
#         'TRADE_DATE_A': '红股上市日',
#         'ANNOUNCE_DATE': '公告刊登日',
#         'BONUS_RATE': '送股比例(10:?)',
#         'CHANGE_RATE': 'QYvalue',
#         'ANNOUNCE_DESTINATION': 'QYvalue',
#         'COMPANY_CODE': 'QYvalue',
#         'COMPANY_NAME': 'QYvalue',
#         'SECURITY_NAME_A': 'QYvalue',
#         'SECURITY_CODE_A': 'QYvalue',
#     }
#
#     B_song = {
#         'LAST_TRADE_DATE_B': '最后交易日',
#         'RECORD_DATE_B': '股权登记日',
#         'ISS_VOL': '股权登记日总股本(万股)',
#         'EX_RIGHT_DATE_B': '除权基准日',
#         'TRADE_DATE_B': '红股上市日',
#         'ANNOUNCE_DATE': '公告刊登日',
#         'BONUS_RATE': '送股比例(10:?)',
#         'ANNOUNCE_DESTINATION': 'QYvalue',
#         'CHANGE_RATE': 'QYvalue',
#         'COMPANY_CODE': 'QYvalue',
#         'COMPANY_NAME': 'QYvalue',
#         'SECURITY_CODE_B': 'QYvalue',
#         'SECURITY_NAME_B': 'QYvalue'
#     }
#
#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         spider = super(LiRunFenPeiSpdier, cls).from_crawler(
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
#             data_hong = {
#                 'isPagination': 'false',
#                 '_': '1573448284386'
#             }
#             tabId_list = [
#                 'COMMON_SSE_ZQPZ_GG_LYFP_AGFH_L',
#                 'COMMON_SSE_ZQPZ_GG_LYFP_BGFH_L',
#                 'COMMON_SSE_ZQPZ_GG_LYFP_AGSG_L',
#                 'COMMON_SSE_ZQPZ_GG_LYFP_BGSG_L'
#             ]
#             for tabId in tabId_list:
#                 data_hong['productid'] = uniques['security_code']
#                 data_hong['sqlId'] = tabId
#                 yield scrapy.FormRequest(
#                     method="GET",
#                     url=self.request_url,
#                     formdata=data_hong,
#                     callback=self.parse,
#                     meta={
#                         'security_code': uniques['security_code'],
#                         'company_code': uniques['company_code'],
#                         'tab_value': tabId,
#                         # 'proxy': 'http://58.218.92.130:9808'
#                     }
#                 )
#
#     def parse(self, response):
#         if response.meta['tab_value'] == 'COMMON_SSE_ZQPZ_GG_LYFP_AGFH_L':
#             # print(json.loads(response.text), '^'*60)
#             "分红 A股"
#             info_lists = [[self.A_equry[datas], feilds[datas], str(int(index)+1)]
#                           for index, feilds in enumerate(json.loads(response.text)['result']) for datas in feilds]
#
#             for data_all in zip(info_lists, [i for i in range(1, 14)]):
#                 item = AGFHItem()
#                 item['country_code'] = 'chn'
#                 item['exchange_market_code'] = 'SSE'
#                 item['security_code'] = response.meta['security_code']
#                 item['company_code'] = response.meta['company_code']
#                 item['classification_id'] = 50
#                 item['correlation_id'] = data_all[0][-1]
#                 item['header'] = data_all[0][0]
#                 item['header_sort'] = data_all[-1]
#                 item['content'] = data_all[0][1]
#                 item['gmt_create'] = str(datetime.now())
#                 item['user_create'] = 'xfc'
#                 yield item
#                 # cols, values = zip(*item.items())
#                 # print(cols, '&' * 20)
#                 # print(values, '%' * 20)
#                 # sql = "INSERT INTO `{}` ({}) VALUES {}".format \
#                 #         (
#                 #         'company_original_information_detail_1111',
#                 #         ','.join(cols),
#                 #         (str(values) + ',')[0:-1]
#                 #     )
#                 # print('*' * 20, sql)
#                 # try:
#                 #     self.cur.execute(sql)
#                 #     self.conn.commit()
#                 # except Exception as e:
#                 #     print('SQL ERROR !!!', e)
#
#         elif response.meta['tab_value'] == 'COMMON_SSE_ZQPZ_GG_LYFP_BGFH_L':
#             # print(json.loads(response.text), '@' * 60)
#             "分红 B股"
#             info_lists = [[self.B_equry[datas], feilds[datas], str(int(index) + 1)]
#                           for index, feilds in enumerate(json.loads(response.text)['result']) for datas in feilds]
#
#             for data_all in zip(info_lists, [i for i in range(1, 15)]):
#                 item = BGFHItem()
#                 item['country_code'] = 'chn'
#                 item['exchange_market_code'] = 'SSE'
#                 item['security_code'] = response.meta['security_code']
#                 item['company_code'] = response.meta['company_code']
#                 item['classification_id'] = 51
#                 item['correlation_id'] = data_all[0][-1]
#                 item['header'] = data_all[0][0]
#                 item['header_sort'] = data_all[-1]
#                 item['content'] = data_all[0][1]
#                 item['gmt_create'] = str(datetime.now())
#                 item['user_create'] = 'xfc'
#                 yield item
#                 # cols, values = zip(*item.items())
#                 # print(cols, '&' * 20)
#                 # print(values, '%' * 20)
#                 # sql = "INSERT INTO `{}` ({}) VALUES {}".format \
#                 #         (
#                 #         'company_original_information_detail_1111',
#                 #         ','.join(cols),
#                 #         (str(values) + ',')[0:-1]
#                 #     )
#                 # print('*' * 20, sql)
#                 # try:
#                 #     self.cur.execute(sql)
#                 #     self.conn.commit()
#                 # except Exception as e:
#                 #     print('SQL ERROR !!!', e)
#
#         elif response.meta['tab_value'] == 'COMMON_SSE_ZQPZ_GG_LYFP_AGSG_L':
#             # print(json.loads(response.text), '#' * 60)
#             "送股 A股"
#             info_lists = [[self.A_song[datas], feilds[datas], str(int(index) + 1)]
#                           for index, feilds in enumerate(json.loads(response.text)['result']) for datas in feilds]
#
#             for data_all in zip(info_lists, [i for i in range(1, 14)]):
#                 item = AGSGItem()
#                 item['country_code'] = 'chn'
#                 item['exchange_market_code'] = 'SSE'
#                 item['security_code'] = response.meta['security_code']
#                 item['company_code'] = response.meta['company_code']
#                 item['classification_id'] = 52
#                 item['correlation_id'] = data_all[0][-1]
#                 item['header'] = data_all[0][0]
#                 item['header_sort'] = data_all[-1]
#                 item['content'] = data_all[0][1]
#                 item['gmt_create'] = str(datetime.now())
#                 item['user_create'] = 'xfc'
#                 yield item
#                 # cols, values = zip(*item.items())
#                 # print(cols, '&' * 20)
#                 # print(values, '%' * 20)
#                 # sql = "INSERT INTO `{}` ({}) VALUES {}".format \
#                 #         (
#                 #         'company_original_information_detail_1111',
#                 #         ','.join(cols),
#                 #         (str(values) + ',')[0:-1]
#                 #     )
#                 # print('*' * 20, sql)
#                 # try:
#                 #     self.cur.execute(sql)
#                 #     self.conn.commit()
#                 # except Exception as e:
#                 #     print('SQL ERROR !!!', e)
#
#         elif response.meta['tab_value'] == 'COMMON_SSE_ZQPZ_GG_LYFP_BGSG_L':
#             # print(json.loads(response.text), '*' * 60)
#             "送股 B股"
#             info_lists = [[self.B_song[datas], feilds[datas], str(int(index) + 1)]
#                           for index, feilds in enumerate(json.loads(response.text)['result']) for datas in feilds]
#
#             for data_all in zip(info_lists, [i for i in range(1, 14)]):
#                 item = BGSGItem()
#                 item['country_code'] = 'chn'
#                 item['exchange_market_code'] = 'SSE'
#                 item['security_code'] = response.meta['security_code']
#                 item['company_code'] = response.meta['company_code']
#                 item['classification_id'] = 53
#                 item['correlation_id'] = data_all[0][-1]
#                 item['header'] = data_all[0][0]
#                 item['header_sort'] = data_all[-1]
#                 item['content'] = data_all[0][1]
#                 item['gmt_create'] = str(datetime.now())
#                 item['user_create'] = 'xfc'
#                 yield item
#                 # cols, values = zip(*item.items())
#                 # print(cols, '&' * 20)
#                 # print(values, '%' * 20)
#                 # sql = "INSERT INTO `{}` ({}) VALUES {}".format \
#                 #         (
#                 #         'company_original_information_detail_1111',
#                 #         ','.join(cols),
#                 #         (str(values) + ',')[0:-1]
#                 #     )
#                 # print('*' * 20, sql)
#                 # try:
#                 #     self.cur.execute(sql)
#                 #     self.conn.commit()
#                 # except Exception as e:
#                 #     print('SQL ERROR !!!', e)