# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# # Author: xfc
# # @Time : 2019/9/29 15:53
#
# """
#
# COMMON_SSE_ZQPZ_GP_GPLB_AGSSR_C     上市日——1
# COMMON_SSE_ZQPZ_GP_GPLB_BGSSR_C     上市日——2
# COMMON_SSE_ZQPZ_GP_GPLB_MSXX_C      董事会秘书电话
# COMMON_SSE_ZQPZ_GP_GPLB_C           公司概况
#
# """
#
# import scrapy
# import json
# import pymysql
# from scrapy import signals
# from datetime import datetime
# # from ..items import CompanyInFoItem
# from ..items import SecretaryName
# from ..items import ListingDateIndex
# from ..items import ListingDateLast
#
#
# class SseDetalInfoSpider(scrapy.Spider):
#     name = 'SSE_details_info'
#     allowed_domains = ['sse.com.cn']
#     info_urls = 'http://query.sse.com.cn/commonQuery.do?'
#
#     params_list = [
#         'COMMON_SSE_ZQPZ_GP_GPLB_C',
#         'COMMON_SSE_ZQPZ_GP_GPLB_MSXX_C',
#         'COMMON_SSE_ZQPZ_GP_GPLB_AGSSR_C',
#         'COMMON_SSE_ZQPZ_GP_GPLB_BGSSR_C'
#     ]
#
#     accpet_params = {
#         'isPagination': 'false',
#     }
#
#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         spider = super(SseDetalInfoSpider, cls).from_crawler(
#             crawler, *args, **kwargs
#         )
#         crawler.signals.connect(spider.spider_opened, signals.spider_opened)
#         # crawler.signals.connect(spider.spider_closed, signals.spider_closed)
#         return spider
#
#     def spider_opened(self, spider):
#         """ 查询当前所有存量公司 """
#         conn = pymysql.connect(**self.settings['DBARGS'])
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT security_code, mark FROM `company_data_source_backup20190929` "
#                            "WHERE mark=0 ORDER BY security_code ASC ;")
#             feild_list = cursor.fetchall()
#             self.stock_code_list = []
#             for self.feild_dict in feild_list:
#                 stock_code = self.feild_dict['security_code']
#                 self.stock_code_list.append(stock_code)
#
#             conn.close()
#
#     def start_requests(self):
#             # 请求公司概况页面
#             print("@"*20, self.stock_code_list)
#             for stock_code in self.stock_code_list:
#                 for parameter in self.params_list:
#                     self.accpet_params['sqlId'] = parameter
#                     self.accpet_params['productid'] = stock_code
#
#                     yield scrapy.FormRequest(
#                         method="GET",
#                         url=self.info_urls,
#                         callback=self.parse,
#                         formdata=self.accpet_params,
#                         meta={
#                             "proxy": "http://58.218.200.253:6618",
#                             "parameter": parameter,
#                             "stock_code": stock_code
#                         }
#                     )
#
#
#     def parse(self, response):
#         jres = json.loads(response.text)
#         if response.meta['parameter'] == 'COMMON_SSE_ZQPZ_GP_GPLB_C':
#             """ 公司概况 """
#             info_datas = jres['result'][0]
#                 # customized_code = ('定制代码', response.meta['customized_code'])
#                 # # 公司简称
#                 # company_name = ('公司简称', response.meta['company_name'])
#                 # # 简称
#                 # short_name = ('简称', response.meta['short_name'])
#                 # # 公司代码
#                 # current_code = ('公司代码', response.meta['current_code'])
#                 # # 代码
#                 # before_code = ('代码', response.meta['before_code'])
#                 # # 上市日期
#                 # listing_date = ('上市日期', response.meta['listing_date'])
#                 # # 市场类型
#                 # market_type = ('市场类型', response.meta['market_type'])
#                 # # 公司代码
#                 # company_code = ('公司代码', result_datas['COMPANY_CODE'])
#                 # # 股票代码
#                 # stock_code = ('股票代码', result_datas['SECURITY_CODE_A'] + '/' + result_datas['SECURITY_CODE_B'])
#                 # # # 上市日
#                 # # item['date_listing'] = (
#                 # # '上市日', response.meta['date_listing_first'] + '/' + response.meta['date_listing_last'])
#                 # # 可转债简称
#                 # bond_short_name = ('可转债简称', result_datas['CHANGEABLE_BOND_ABBR'])
#                 # # 可转债代码
#                 # bond_code = ('可转债代码', result_datas['CHANGEABLE_BOND_CODE'])
#                 # # 公司简称中文
#                 # company_short_name_zh = ('公司简称中文', result_datas['COMPANY_ABBR'])
#                 # # 公司简称英文
#                 # company_short_name_en = ('公司简称英文', result_datas['ENGLISH_ABBR'])
#                 # # 公司全称中文
#                 # company_full_name_zh = ('公司全称中文', result_datas['FULLNAME'])
#                 # # 公司全称英文
#                 # company_full_name_en = ('公司全称英文', result_datas['FULL_NAME_IN_ENGLISH'])
#                 # # 注册地址
#                 # registered_address = ('注册地址', result_datas['COMPANY_ADDRESS'])
#                 # # 通讯地址
#                 # mailing_address = ('通讯地址', result_datas['OFFICE_ADDRESS'])
#                 # # 邮编
#                 # zip_code = ('邮编', result_datas['OFFICE_ZIP'])
#                 # # 法定代表人
#                 # legal_representative = ('法定代表人', result_datas['LEGAL_REPRESENTATIVE'])
#                 # # # 董事会秘书姓名
#                 # # secretary_name = ('董事会秘书姓名', response.meta['secretary_name'])
#                 # # E-mail
#                 # email = ('E-mail', result_datas['E_MAIL_ADDRESS'])
#                 # # 联系电话
#                 # phone = ('联系电话', result_datas['REPR_PHONE'])
#                 # # 网址
#                 # web = ('网址', result_datas['WWW_ADDRESS'])
#                 # # CSRC行业(门类/大类/中类)
#                 # CSRC_industry = ('CSRC行业(门类/大类/中类)', result_datas['CSRC_CODE_DESC'] + '/' + \
#                 #                          result_datas['CSRC_GREAT_CODE_DESC'] + '/' + \
#                 #                          result_datas['CSRC_MIDDLE_CODE_DESC'])
#                 # # SSE行业
#                 # sse_industry = ('SSE行业', result_datas['SSE_CODE_DESC'])
#                 # # 所属省/直辖市
#                 # affiliation = ('所属省/直辖市', result_datas['AREA_NAME_DESC'])
#                 # # 状态
#                 # status = ('状态', result_datas['STATE_CODE_A_DESC'] + '/' + result_datas['STATE_CODE_B_DESC'])
#                 # # 是否上证180样本股
#                 # sample_stocks = ('是否上证180样本股', result_datas['SECURITY_30_DESC'])
#                 # # 是否境外上市
#                 # listed_abroad = ('是否境外上市', result_datas['FOREIGN_LISTING_DESC'])
#                 # # 境外上市地
#                 # listing_place = ('境外上市地', result_datas['FOREIGN_LISTING_ADDRESS'])
#                 # type_market = ('市场类型', response.meta['type_name'])
#                 # exchange_market_code = ('上市交易所', 'SSE')