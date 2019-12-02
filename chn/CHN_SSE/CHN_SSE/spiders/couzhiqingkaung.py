# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# # Author: xfc
# # @Time : 2019/11/12 11:23
# import scrapy
# import json
# import pymysql
# import re
#
# from datetime import datetime
#
# from scrapy import signals
#
# from CHN_SSE.items import FinancingSituationSpecial, FinancingSituationAad, FinancingSituationAFirst
#
#
# class CouZhiQingKuangSpider(scrapy.Spider):
#     name = 'couzhiqingkaung'
#     allowed_domains = ['sse.com.cn']
#     request_url = 'http://query.sse.com.cn/commonQuery.do?'
#
#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         spider = super(CouZhiQingKuangSpider, cls).from_crawler(
#             crawler, *args, **kwargs
#         )
#         crawler.signals.connect(spider.spider_opened, signals.spider_opened)
#         return spider
#
#     def spider_opened(self):
#         """ 查询当前所有存量公司 """
#         conn = pymysql.connect(**self.settings['DBARGS'])
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT"
#                            " company_code, security_code "
#                            "FROM"
#                            " `company_data_source_complete20191010_copy` "
#                            "WHERE"
#                            " country_code='chn' "
#                            "AND"
#                            " exchange_market_code='SSE' "
#                            "AND"
#                            " is_batch=0 "
#                            "ORDER BY"
#                            " security_code "
#                            "ASC ;")
#             feild_list = cursor.fetchall()
#             conn.close()
#             return feild_list
#
#     def start_requests(self):
#         A_first_form = {
#             'isPagination': 'false',
#             'sqlId': 'COMMON_SSE_ZQPZ_GPLB_CZQK_AGSCFX_S',
#             '_': '1573528664083'
#         }
#         for uniques in self.spider_opened():
#             A_first_form['productid'] = uniques['security_code']
#             yield scrapy.FormRequest(
#                 method="GET",
#                 url=self.request_url,
#                 formdata=A_first_form,
#                 callback=self.parse,
#                 meta={
#                     'company_code': uniques['company_code'],
#                     'security_code': uniques['security_code']
#                 }
#             )
#
#             A_add_form = {
#                 'isPagination': 'false',
#                 'productid': uniques['security_code'],
#                 'sqlId': 'COMMON_SSE_ZQPZ_GPLB_CZQK_AGZF_S',
#                 '_': '1573528664084'
#             }
#             yield scrapy.FormRequest(
#                 method="GET",
#                 url=self.request_url,
#                 formdata=A_add_form,
#                 callback=self.parse_Add,
#                 meta={
#                     'company_code': uniques['company_code'],
#                     'security_code': uniques['security_code']
#                 }
#             )
#
#             thing_url = 'http://query.sse.com.cn/marketdata/tradedata/queryStockSpecialQuat.do?'
#             ts_things_form = {
#                 'isPagination': 'true',
#                 'startDate': '',
#                 'endDate': '',
#                 'product': uniques['security_code'],
#                 '_': '1573528664082'
#             }
#             yield scrapy.FormRequest(
#                 method="GET",
#                 url=thing_url,
#                 formdata=ts_things_form,
#                 callback=self.parse_TS,
#                 meta={
#                     'company_code': uniques['company_code'],
#                     'security_code': uniques['security_code']
#                 }
#             )
#
#
#     def parse(self, response):
#         A_data_list = {
#             'ISSUED_VOLUME_A': '发行数(万股)',
#             'ISSUED_PRICE_A': '发行价格',
#             'ISSUED_BEGIN_DATE_A': '发行日期',
#             'RAISED_MONEY_A': '募集资金总额(万元)',
#             'ISSUED_PROFIT_RATE_A1': '发行市盈率(%)-加权法',
#             'ISSUED_PROFIT_RATE_A2': '发行市盈率(%)-摊薄法',
#             'ISSUED_MODE_CODE_A': '发行方式',
#             'MAIN_UNDERWRITER_NAME_A': '主承销商',
#             'GOT_RATE_A': '中签率',
#             'COMPANY_CODE': 'QYvalue',
#             'RANK': 'QYvalue',
#             'SECURITY_ABBR_A': 'QYvalue',
#             'SECURITY_CODE_A': 'QYvalue'
#         }
#         pt_one = [[A_data_list[datas], feilds[datas], str(int(index)+1)] for index, feilds in
#                   enumerate(json.loads(response.text)['result']) for datas in feilds]
#         for data_all in zip(pt_one, [i for i in range(1, 14)]):
#             item = FinancingSituationAFirst()
#             item['country_code'] = 'chn'
#             item['exchange_market_code'] = 'SSE'
#             item['security_code'] = response.meta['security_code']
#             item['company_code'] = response.meta['company_code']
#             item['classification_id'] = 3
#             item['correlation_id'] = data_all[0][-1]
#             item['header'] = data_all[0][0]
#             item['header_sort'] = data_all[-1]
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
#
#     def parse_Add(self, response):
#         A_add_list = {
#             'ISSUED_VOLUME_A': '发行数量(万股)',
#             'ISSUED_PRICE_A': '发行价格, 配售价格',
#             'ISSUED_BEGIN_DATE_A': '发行日期',
#             'ISSUED_MODE_CODE_A': '发行方式',
#             'ISSUED_PROFIT_RATE_A1': '发行市盈率(%)-加权法',
#             'ISSUED_PROFIT_RATE_A2': '发行市盈率(%)-摊薄法',
#             'RECOMMEND_NAME_A': '上市推荐人',
#             'MAIN_UNDERWRITER_NAME_A': '主承销商',
#             'RIGHT_ISSUE_PRICE_A': '中签率%',
#             'SHARE_HOLDER_RATE_A': '老股东配搜比例(10:?)',
#             'COMPANY_CODE': 'QYvalue',
#             'GOT_RATE_A': 'QYvalue',
#             'RAISED_MONEY_A': 'QYvalue',
#             'RANK': 'QYvalue',
#             'SECURITY_ABBR_A': 'QYvalue',
#             'SECURITY_CODE_A': 'QYvalue'
#         }
#         pt_two = [[A_add_list[datas], feilds[datas], str(int(index)+1)] for index, feilds in
#                   enumerate(json.loads(response.text)['result']) for datas in feilds]
#         for data_all in zip(pt_two, [i for i in range(1, 17)]):
#             item = FinancingSituationAad()
#             item['country_code'] = 'chn'
#             item['exchange_market_code'] = 'SSE'
#             item['security_code'] = response.meta['security_code']
#             item['company_code'] = response.meta['company_code']
#             item['classification_id'] = 4
#             item['correlation_id'] = data_all[0][-1]
#             item['header'] = data_all[0][0]
#             item['header_sort'] = data_all[-1]
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
#     def parse_TS(self, response):
#         TS_data_list = {
#             'listingDate': '日期',
#             'listingMark': '事件',
#             'curBonus': '当日流通股本(万股)',
#             'openprice': '开盘价(元)',
#             'highprice': '最高价(元)',
#             'lowprice': '最低价(元)',
#             'closeprice': '收盘价(元)',
#             'tradingvol': '成交量(万股)',
#             'tradingamt': '成交额(万元)',
#             'exchangerate': '换手率(%)',
#             'ROWNUM_': 'QYvalue',
#             'companyCode': 'QYvalue',
#             'productName': 'QYvalue'
#         }
#         pt_three = [[TS_data_list[datas], feilds[datas], str(int(index) + 1)] for index, feilds in
#                     enumerate(json.loads(response.text)['result']) for datas in feilds]
#         for data_all in zip(pt_three, [i for i in range(1, 14)]):
#             item = FinancingSituationSpecial()
#             item['country_code'] = 'chn'
#             item['exchange_market_code'] = 'SSE'
#             item['security_code'] = response.meta['security_code']
#             item['company_code'] = response.meta['company_code']
#             item['classification_id'] = 5
#             item['correlation_id'] = data_all[0][-1]
#             item['header'] = data_all[0][0]
#             item['header_sort'] = data_all[-1]
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