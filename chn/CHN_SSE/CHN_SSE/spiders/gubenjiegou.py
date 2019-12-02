# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# # Author: xfc
# # @Time : 2019/11/12 9:45
# import scrapy
# import json
# import pymysql
# import time
#
# from datetime import datetime
#
# from scrapy import signals
#
# from CHN_SSE.items import EquityStructureItem, EquityChangeItem
#
#
# class GuBenJieGouSpider(scrapy.Spider):
#     name = 'gubenjiegou'
#     allowed_domains = ['sse.com.cn']
#     allowed_url = 'http://query.sse.com.cn/security/stock/queryEquityChangeAndReason.do?'
#
#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         spider = super(GuBenJieGouSpider, cls).from_crawler(
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
#         change_form = {
#             'isPagination': 'true',
#             '_': '1573523481505'
#         }
#         # 'companyCode': '600016',
#         for uniques in self.spider_opened():
#             change_form['companyCode'] = uniques['security_code']
#             yield scrapy.FormRequest(
#                 method="GET",
#                 url=self.allowed_url,
#                 formdata=change_form,
#                 callback=self.parse,
#                 meta={
#                     'company_code': uniques['company_code'],
#                     'security_code': uniques['security_code']
#                 }
#             )
#
#             capital_url = 'http://query.sse.com.cn/commonQuery.do?'
#             capital_form = {
#                 'isPagination': 'false',
#                 'sqlId': 'COMMON_SSE_CP_GPLB_GPGK_GBJG_C',
#                 'companyCode': uniques['security_code'],
#                 '_': '1573523481502'
#             }
#             yield scrapy.FormRequest(
#                 method="GET",
#                 url=capital_url,
#                 formdata=capital_form,
#                 callback=self.parse_capital,
#                 meta={
#                     'company_code': uniques['company_code'],
#                     'security_code': uniques['security_code']
#                 }
#             )
#
#     def parse(self, response):
#         change_dy = {
#             'realDate': '变动日期',
#             'changeReasonDesc': '变动原因',
#             'totalShares': '变动后股数(万股)',
#             'AShares': 'QYvalue',
#             'BShares': 'QYvalue',
#             'ROWNUM_': 'QYvalue',
#             'changeReason': 'QYvalue',
#             'seq': 'Qyvalue'
#         }
#         datas_list = [[change_dy[datas], feilds[datas], str(int(index)+1)] for index, feilds in enumerate(json.loads(response.text)['result']) for datas in feilds]
#         for data_all in zip(datas_list, [i for i in range(1, 9)]):
#             item = EquityChangeItem()
#             item['country_code'] = 'chn'
#             item['exchange_market_code'] = 'SSE'
#             item['security_code'] = response.meta['security_code']
#             item['company_code'] = response.meta['company_code']
#             item['classification_id'] = 8
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
#     def parse_capital(self, response):
#         change_dy = {
#             'LIMITED_SHARES': '有限售流通股',
#             'LISTING_VOTE_SHARES': '其中：特别表决权股',
#             'UNLIMITED_SHARES': '无限售流通股',
#             'UNLIMITED_A_SHARES': '无限售流通A股/CDR',
#             'B_SHARES': '境内上市外资股（B股）',
#             'DOMESTIC_SHARES': '境内上市股票合计',
#             'REAL_DATE': '数据日期'
#         }
#         datas_list = [[change_dy[datas], feilds[datas], str(int(index) + 1)] for index, feilds in
#                       enumerate(json.loads(response.text)['result']) for datas in feilds]
#         for data_all in zip(datas_list, [i for i in range(1, 8)]):
#             item = EquityStructureItem()
#             item['country_code'] = 'chn'
#             item['exchange_market_code'] = 'SSE'
#             item['security_code'] = response.meta['security_code']
#             item['company_code'] = response.meta['company_code']
#             item['classification_id'] = 7
#             item['correlation_id'] = data_all[0][-1]
#             item['header'] = data_all[0][0]
#             item['header_sort'] = data_all[-1]
#             item['content'] = data_all[0][1]
#             item['info_date'] = ''.join([feilds['REAL_DATE'] for feilds in json.loads(response.text)['result']])
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