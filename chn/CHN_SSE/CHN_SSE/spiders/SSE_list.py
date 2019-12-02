# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# # Author: xfc
# # @Time : 2019/9/25 14:11
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
#
# from ..items import CompanyDataSourceItem
# from ..items import CompanyInFoItem
# from ..items import SecretaryName
# from ..items import ListingDateIndex
# from ..items import ListingDateLast
#
# from scrapy.spidermiddlewares.httperror import HttpError
# from twisted.internet.error import DNSLookupError
# from twisted.internet.error import TimeoutError, TCPTimedOutError
# from twisted.internet.error import ConnectionRefusedError
# from twisted.web._newclient import ResponseNeverReceived
#
#
# class ChnSseSpdierSpider(scrapy.Spider):
#     name = 'SSE_list'
#     allowed_domains = ['sse.com.cn']
#
#     code_urls = 'http://query.sse.com.cn/security/stock/getStockListData2.do?'
#     info_urls = 'http://query.sse.com.cn/commonQuery.do?'
#
#     market_type_list = ['1', '2', '8']
#     params_list = [
#         'COMMON_SSE_ZQPZ_GP_GPLB_C',
#         'COMMON_SSE_ZQPZ_GP_GPLB_MSXX_C',
#         'COMMON_SSE_ZQPZ_GP_GPLB_AGSSR_C',
#         'COMMON_SSE_ZQPZ_GP_GPLB_BGSSR_C'
#     ]
#     accpet_params = {
#         'isPagination': 'false',
#     }
#
#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         spider = super(ChnSseSpdierSpider, cls).from_crawler(
#             crawler, *args, **kwargs
#         )
#         crawler.signals.connect(spider.spider_opened, signals.spider_opened)
#         return spider
#
#     def spider_opened(self, spider):
#         """ 查询当前所有存量公司 """
#         conn = pymysql.connect(**self.settings['DBARGS'])
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT security_code FROM `company_data_source` ORDER BY security_code ASC ;")
#             feild_list = cursor.fetchall()
#             self.unique_list = []
#             for feild_dict in feild_list:
#                 self.unique_list.append(feild_dict['security_code'])
#
#             conn.close()
#
#     def tosavefile(self, unqiue_count):
#         with open('E:\\Restructure\\CHN_SSE\\CHN_SSE\\samples\\custom_code.txt', 'w') as wf:
#             wf.write(unqiue_count)
#
#     def start_requests(self):
#         """ 第一次请求，请求股票列表页面信息 """
#
#         params_list = {
#             'isPagination': 'true',
#             'stockCode': '',
#             'csrcCode': '',
#             'areaName': '',
#             'pageHelp.pageSize': '1000'
#         }
#         # 判断市场类型分类
#         for market_type in self.market_type_list:
#             if market_type == '1':
#                 type_name = '主板A股'
#             elif market_type == '2':
#                 type_name = '主板B股'
#             elif market_type == '8':
#                 type_name = '科创板'
#             else:
#                 break                    # 错误市场类型
#             params_list['stockType'] = market_type
#
#             yield scrapy.FormRequest(
#                 method = 'GET',
#                 callback = self.parse,
#                 url = self.code_urls,
#                 formdata = params_list,
#                 meta = {
#                     "type_name": type_name,
#                     # "proxy": 'http://58.218.200.253:6324'
#                 }
#             )
#
#     def parse(self, response):
#         """ 获取所有股票列表信息，主要获取证券代码 """
#         pg_info = json.loads(response.text)
#         for results in pg_info['result']:
#             # item = {}
#             # item['company_name'] = results['SECURITY_ABBR_A']           # 公司简称
#             # item['short_name'] = results['SECURITY_ABBR_B']             # 简称
#             # item['current_code'] = results['SECURITY_CODE_A']           # 公司代码
#             # item['before_code'] = results['SECURITY_CODE_B']            # 代码
#             # item['listing_date'] = results['LISTING_DATE']              # 上市日期
#             # item['market_type'] = response.meta['type_name']            # 市场类型
#             with open('E:\\Restructure\\CHN_SSE\\CHN_SSE\\samples\\custom_code.txt', 'r') as rf:
#                 unqiue_str = rf.read()
#             unique_count = int(unqiue_str)
#             unique_count += 1
#             self.tosavefile(str(unique_count))
#             company_id = "chn" + str(unique_count).zfill(5)
#
#             # 判断新增公司
#             # if results['COMPANY_CODE'] not in self.unique_list:
#             #     with open('new_download_code2.txt', 'a') as lf:
#             #         lf.write((results['COMPANY_ABBR'] + ', ' + results['COMPANY_CODE'] + ', ' + response.meta['type_name']) + '\n')
#
#             item = CompanyDataSourceItem()
#             item['company_id'] = company_id
#             item['company_abbreviation'] = results['COMPANY_ABBR']
#             item['country_code'] = 'chn'
#             item['security_code'] = results['COMPANY_CODE']
#             item['latest_url'] = response.url
#             item['latest_date'] = results['LISTING_DATE']
#             item['spider_name'] = 'CHN_SSE_spider'
#             # item['mark'] = 0
#             item['gmt_create'] = str(datetime.now())
#             item['user_create'] = 'xfc'
#             yield item
#
#             company_name = ''.join(results['SECURITY_ABBR_A']).replace('-', results['SECURITY_ABBR_B'])  # 公司简称
#             short_name = results['SECURITY_ABBR_B']  # 简称
#             current_code = ''.join(results['SECURITY_CODE_A']).replace('-', results['SECURITY_CODE_B'])  # 公司代码
#             before_code = results['SECURITY_CODE_B']  # 代码
#             listing_date = results['LISTING_DATE']  # 上市日期
#             market_type = response.meta['type_name']  # 市场类型
#             self.accpet_params['sqlId'] = 'COMMON_SSE_ZQPZ_GP_GPLB_C'
#             self.accpet_params['productid'] = results['COMPANY_CODE']
#
#             yield scrapy.FormRequest(
#                 method="GET",
#                 url = self.info_urls,
#                 formdata = self.accpet_params,
#                 callback = self.parse_get_name,
#                 errback = self.errback_scraping,
#                 meta={
#                     # "proxy": 'http://58.218.200.249:7972',
#                     'company_name' : company_name,
#                     'short_name' : short_name,
#                     'current_code' : current_code,
#                     'before_code' : before_code,
#                     'listing_date' : listing_date,
#                     'market_type' : market_type,                # 首页信息
#                     'request_code' : results['COMPANY_CODE'],
#                     'type_name' : response.meta['type_name'],
#                     'customized_code': company_id,
#                 }
#             )
#
#     def parse_get_name(self, response):
#         try:
#             result_datas = json.loads(response.text)['result'][0]
#             customized_code = ('定制代码', response.meta['customized_code'])
#             # 公司简称
#             company_name = ('公司简称', response.meta['company_name'])
#             # 简称
#             short_name = ('简称', response.meta['short_name'])
#             # 公司代码
#             current_code = ('公司代码', response.meta['current_code'])
#             # 代码
#             before_code = ('代码', response.meta['before_code'])
#             # 上市日期
#             listing_date = ('上市日期', response.meta['listing_date'])
#             # 市场类型
#             market_type = ('市场类型', response.meta['market_type'])
#             # 公司代码
#             company_code = ('公司代码', result_datas['COMPANY_CODE'])
#             # 股票代码
#             stock_code = ('股票代码', result_datas['SECURITY_CODE_A'] + '/' + result_datas['SECURITY_CODE_B'])
#             # 可转债简称
#             bond_short_name = ('可转债简称', result_datas['CHANGEABLE_BOND_ABBR'])
#             # 可转债代码
#             bond_code = ('可转债代码', result_datas['CHANGEABLE_BOND_CODE'])
#             # 公司简称中文
#             company_short_name_zh = ('公司简称中文', result_datas['COMPANY_ABBR'])
#             # 公司简称英文
#             company_short_name_en = ('公司简称英文', result_datas['ENGLISH_ABBR'])
#             # 公司全称中文
#             company_full_name_zh = ('公司全称中文', result_datas['FULLNAME'])
#             # 公司全称英文
#             company_full_name_en = ('公司全称英文', result_datas['FULL_NAME_IN_ENGLISH'])
#             # 注册地址
#             registered_address = ('注册地址', result_datas['COMPANY_ADDRESS'])
#             # 通讯地址
#             mailing_address = ('通讯地址', result_datas['OFFICE_ADDRESS'])
#             # 邮编
#             zip_code = ('邮编', result_datas['OFFICE_ZIP'])
#             # 法定代表人
#             legal_representative = ('法定代表人', result_datas['LEGAL_REPRESENTATIVE'])
#             # E-mail
#             email = ('E-mail', result_datas['E_MAIL_ADDRESS'])
#             # 联系电话
#             phone = ('联系电话', result_datas['REPR_PHONE'])
#             # 网址
#             web = ('网址', result_datas['WWW_ADDRESS'])
#             # CSRC行业(门类/大类/中类)
#             CSRC_industry = ('CSRC行业(门类/大类/中类)', result_datas['CSRC_CODE_DESC'] + '/' + \
#                                      result_datas['CSRC_GREAT_CODE_DESC'] + '/' + \
#                                      result_datas['CSRC_MIDDLE_CODE_DESC'])
#             # SSE行业
#             sse_industry = ('SSE行业', result_datas['SSE_CODE_DESC'])
#             # 所属省/直辖市
#             affiliation = ('所属省/直辖市', result_datas['AREA_NAME_DESC'])
#             # 状态
#             status = ('状态', result_datas['STATE_CODE_A_DESC'] + '/' + result_datas['STATE_CODE_B_DESC'])
#             # 是否上证180样本股
#             sample_stocks = ('是否上证180样本股', result_datas['SECURITY_30_DESC'])
#             # 是否境外上市
#             listed_abroad = ('是否境外上市', result_datas['FOREIGN_LISTING_DESC'])
#             # 境外上市地
#             listing_place = ('境外上市地', result_datas['FOREIGN_LISTING_ADDRESS'])
#             type_market = ('市场类型', response.meta['type_name'])
#             exchange_market_code = ('上市交易所', 'SSE')
#
#             yield CompanyInFoItem(
#                 exchange_market_code=exchange_market_code,
#                 type_market=type_market,
#                 customized_code=customized_code,
#                 company_name=company_name,
#                 short_name=short_name,
#                 current_code=current_code,
#                 before_code=before_code,
#                 listing_date=listing_date,
#                 market_type=market_type,
#                 company_code=company_code,
#                 stock_code=stock_code,
#                 bond_short_name=bond_short_name,
#                 bond_code=bond_code,
#                 company_short_name_zh=company_short_name_zh,
#                 company_short_name_en=company_short_name_en,
#                 company_full_name_zh=company_full_name_zh,
#                 company_full_name_en=company_full_name_en,
#                 registered_address=registered_address,
#                 mailing_address=mailing_address,
#                 zip_code=zip_code,
#                 legal_representative=legal_representative,
#                 email=email,
#                 phone=phone,
#                 web=web,
#                 CSRC_industry=CSRC_industry,
#                 sse_industry=sse_industry,
#                 affiliation=affiliation,
#                 status=status,
#                 sample_stocks=sample_stocks,
#                 listed_abroad=listed_abroad,
#                 listing_place=listing_place
#             )
#         except:
#             with open('unqie_code1.txt', 'a') as af:
#                 af.write((response.meta['customized_code'] + ', ' +response.meta['current_code']) + '\n')
#
#         self.accpet_params['sqlId'] = 'COMMON_SSE_ZQPZ_GP_GPLB_MSXX_C'
#         self.accpet_params['productid'] = response.meta['request_code']
#         # print(self.accpet_params, '@'*20)
#         yield scrapy.FormRequest(
#             url=self.info_urls,
#             method="GET",
#             callback=self.parse_name,
#             errback=self.errback_scraping,
#             formdata=self.accpet_params,
#             meta={
#                 'request_code': response.meta['request_code'],
#                 'customized_code': response.meta['customized_code'],
#                 # 'proxy': 'http://58.218.200.220:4602'
#             }
#         )
#
#     def parse_name(self, response):
#         try:
#             secretary_names = json.loads(response.text)['result'][0]['SECURITY_OF_THE_BOARD_OF_DIRE']
#             secretary_name = ('董事会秘书姓名', secretary_names)
#             item = SecretaryName()
#             item['country_code'] = 'chn'
#             item['company_code'] = response.meta['customized_code']
#             item['display_label'] = secretary_name[0]
#             item['information'] = secretary_name[1]
#             item['gmt_create'] = str(datetime.now())
#             item['user_create'] = 'xfc'
#             yield item
#         except:
#             with open('unqie_code2.txt', 'a') as af:
#                 af.write((response.meta['customized_code'] + ', ' +response.meta['current_code']) + '\n')
#         # print(item['company_code'], '董事会秘书姓名: %s' % "*******************")
#
#         self.accpet_params['sqlId'] = 'COMMON_SSE_ZQPZ_GP_GPLB_AGSSR_C'
#         self.accpet_params['productid'] = response.meta['request_code']
#         yield scrapy.FormRequest(
#             method="GET",
#             callback=self.parse_listing_front,
#             errback=self.errback_scraping,
#             url=self.info_urls,
#             formdata=self.accpet_params,
#             meta={
#                 'request_code': response.meta['request_code'],
#                 'customized_code': response.meta['customized_code'],
#                 # 'proxy': 'http://58.218.201.122:8841'
#             }
#         )
#
#     def parse_listing_front(self, response):
#         try:
#             if json.loads(response.text)['result']:
#                 listing_first = json.loads(response.text)['result'][0]['LISTINGDATEA']
#                 listing_one = ('上市日_1', listing_first)
#                 item = ListingDateIndex()
#                 item['country_code'] = 'chn'
#                 item['company_code'] = response.meta['customized_code']
#                 item['display_label'] = listing_one[0]
#                 item['information'] = listing_one[1]
#                 item['gmt_create'] = str(datetime.now())
#                 item['user_create'] = 'xfc'
#                 yield item
#         except:
#             with open('unqie_code3.txt', 'a') as af:
#                 af.write((response.meta['customized_code'] + ', ' +response.meta['current_code']) + '\n')
#
#             self.accpet_params['sqlId'] = 'COMMON_SSE_ZQPZ_GP_GPLB_BGSSR_C'
#             self.accpet_params['productid'] = response.meta['request_code']
#             yield scrapy.FormRequest(
#                 method="GET",
#                 callback=self.parse_listing_last,
#                 errback=self.errback_scraping,
#                 url=self.info_urls,
#                 formdata=self.accpet_params,
#                 meta={
#                     'request_code': response.meta['request_code'],
#                     'customized_code': response.meta['customized_code'],
#                     # 'proxy': 'http://58.218.200.229:2469'
#                 }
#             )
#
#     def parse_listing_last(self, response):
#         try:
#             if json.loads(response.text)['result']:
#                 listing_late = json.loads(response.text)['result'][0]['LISTINGDATEB']
#                 listing_lates = ('上市日_2', listing_late)
#                 item = ListingDateLast()
#                 item['country_code'] = 'chn'
#                 item['company_code'] = response.meta['customized_code']
#                 item['display_label'] = listing_lates[0]
#                 item['information'] = listing_lates[1]
#                 item['gmt_create'] = str(datetime.now())
#                 item['user_create'] = 'xfc'
#                 yield item
#         except:
#             with open('unqie_code4.txt', 'a') as af:
#                 af.write((response.meta['customized_code'] + ', ' +response.meta['current_code']) + '\n')
#
#
#     def errback_scraping(self, failure):
#         req_url = failure.request.url
#         if failure.check(HttpError):
#             response = failure.value.response
#             self.logger.error('HttpError %s on %s', response.status, req_url)
#             with open('unique_code.txt', 'a') as wf:
#                 wf.write((response.meta['company_id'] + ', ' + response.meta['security_code']) + '\n')
#         elif failure.check(DNSLookupError):
#             self.logger.error('DNSLookupError on %s', req_url)
#         elif failure.check(ConnectionRefusedError):
#             self.logger.error('ConnectionRefusedError on %s', req_url)
#         elif failure.check(TimeoutError, TCPTimedOutError):
#             self.logger.error('TimeoutError on %s', req_url)
#         elif failure.check(ResponseNeverReceived):
#             self.logger.error('ResponseNeverReceived on %s', req_url)
#         else:
#             self.logger.error('UnpectedError on %s', req_url)
#             self.logger.error(repr(failure))