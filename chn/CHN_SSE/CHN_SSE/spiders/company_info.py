# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# # Author: xfc
# # @Time : 2019/10/21 14:12
# import scrapy
# import pymysql
# import json
# import random
#
# from datetime import datetime
#
# from scrapy import signals
#
#
# class CompanyInfoSpider(scrapy.Spider):
#     name = 'company_info'
#     allowed_domains = ['sse.com.cn']
#
#     info_url = 'http://query.sse.com.cn/commonQuery.do?'
#
#     data_form = {
#         'isPagination': 'false',
#         'sqlId': 'COMMON_SSE_ZQPZ_GP_GPLB_C',
#     }
#
#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         spider = super(CompanyInfoSpider, cls).from_crawler(
#             crawler, *args, **kwargs
#         )
#         crawler.signals.connect(spider.spider_opened, signals.spider_opened)
#         return spider
#
#     def spider_opened(self):
#         """ 查询当前所有存量公司 """
#         conn = pymysql.connect(**self.settings['DBARGS'])
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT company_id, security_code FROM `company_data_source_complete20191010_copy` "
#                            "WHERE country_code='chn' AND is_batch=0 ORDER BY security_code ASC ;")
#             feild_list = cursor.fetchall()
#
#             conn.close()
#             return feild_list
#
#     def start_requests(self):
#         for unqie_code in self.spider_opened():
#             self.data_form['productid'] = unqie_code['security_code']
#             yield scrapy.FormRequest(
#                 method="GET",
#                 callback=self.parse,
#                 url=self.info_url,
#                 formdata=self.data_form,
#                 meta={
#                     'company_code': unqie_code['company_id'],
#                     'security_code': unqie_code['security_code'],
#                     'proxy': 'http://58.218.200.253:9194'
#                 }
#             )
#
#     def parse(self, response):
#         if len(json.loads(response.text)['result']) != 0:
#
#             jres = json.loads(response.text)['result'][0]
#
#             unique_code = ('内部编码', response.meta['company_code'])
#             # 公司代码
#             company_code = ('公司代码', jres['COMPANY_CODE'])
#             # 股票代码
#             stock_code = ('股票代码', jres['SECURITY_CODE_A'] + '/' + jres['SECURITY_CODE_B'])
#             # 可转债简称
#             bond_short_name = ('可转债简称', jres['CHANGEABLE_BOND_ABBR'])
#             # 可转债代码
#             bond_code = ('可转债代码', jres['CHANGEABLE_BOND_CODE'])
#             # 公司简称中文
#             company_short_name_zh = ('公司简称中文', jres['COMPANY_ABBR'])
#             # 公司简称英文
#             company_short_name_en = ('公司简称英文', jres['ENGLISH_ABBR'])
#             # 公司全称中文
#             company_full_name_zh = ('公司全称中文', jres['FULLNAME'])
#             # 公司全称英文
#             company_full_name_en = ('公司全称英文', jres['FULL_NAME_IN_ENGLISH'])
#             # 注册地址
#             registered_address = ('注册地址', jres['COMPANY_ADDRESS'])
#             # 通讯地址
#             mailing_address = ('通讯地址', jres['OFFICE_ADDRESS'])
#             # 邮编
#             zip_code = ('邮编', jres['OFFICE_ZIP'])
#             # 法定代表人
#             legal_representative = ('法定代表人', jres['LEGAL_REPRESENTATIVE'])
#             # E-mail
#             email = ('E-mail', jres['E_MAIL_ADDRESS'])
#             # 联系电话
#             phone = ('联系电话', jres['REPR_PHONE'])
#             # 网址
#             web = ('网址', jres['WWW_ADDRESS'])
#             # CSRC行业(门类/大类/中类)
#             CSRC_industry = ('CSRC行业(门类/大类/中类)', jres['CSRC_CODE_DESC'] + '/' + \
#                              jres['CSRC_GREAT_CODE_DESC'] + '/' + \
#                              jres['CSRC_MIDDLE_CODE_DESC'])
#             # SSE行业
#             sse_industry = ('SSE行业', jres['SSE_CODE_DESC'])
#             # 所属省/直辖市
#             affiliation = ('所属省/直辖市', jres['AREA_NAME_DESC'])
#             # 状态
#             status = ('状态', jres['STATE_CODE_A_DESC'] + '/' + jres['STATE_CODE_B_DESC'])
#             # 是否上证180样本股
#             sample_stocks = ('是否上证180样本股', jres['SECURITY_30_DESC'])
#             # 是否境外上市
#             listed_abroad = ('是否境外上市', jres['FOREIGN_LISTING_DESC'])
#             # 境外上市地
#             listing_place = ('境外上市地', jres['FOREIGN_LISTING_ADDRESS'])
#             # 交易所
#             exchange_market_code = ('上市交易所', 'SSE')
#
#             yield InfoDetailItem(
#                 unique_code = unique_code,
#                 company_code = company_code,
#                 stock_code = stock_code,
#                 bond_short_name = bond_short_name,
#                 bond_code = bond_code,
#                 company_short_name_zh = company_short_name_zh,
#                 company_short_name_en = company_short_name_en,
#                 company_full_name_zh = company_full_name_zh,
#                 company_full_name_en = company_full_name_en,
#                 registered_address = registered_address,
#                 mailing_address = mailing_address,
#                 zip_code = zip_code,
#                 legal_representative = legal_representative,
#                 email = email,
#                 phone = phone,
#                 web = web,
#                 CSRC_industry = CSRC_industry,
#                 sse_industry = sse_industry,
#                 affiliation = affiliation,
#                 status = status,
#                 sample_stocks = sample_stocks,
#                 listed_abroad = listed_abroad,
#                 listing_place = listing_place,
#                 exchange_market_code = exchange_market_code,
#             )
#
#             # item = {}
#             # item['company_code'] = company_code
#             # item['stock_code'] = stock_code
#             # item['bond_short_name'] = bond_short_name
#             # item['bond_code'] = bond_code
#             # item['company_short_name_zh'] = company_short_name_zh
#             # item['company_short_name_en'] = company_short_name_en
#             # item['company_full_name_zh'] = company_full_name_zh
#             # item['company_full_name_en'] = company_full_name_en
#             # item['registered_address'] = registered_address
#             # item['mailing_address'] = mailing_address
#             # item['zip_code'] = zip_code
#             # item['legal_representative'] = legal_representative
#             # item['email'] = email
#             # item['phone'] = phone
#             # item['web'] = web
#             # item['CSRC_industry'] = CSRC_industry
#             # item['sse_industry'] = sse_industry
#             # item['affiliation'] = affiliation
#             # item['status'] = status
#             # item['sample_stocks'] = sample_stocks
#             # item['sample_stocks'] = sample_stocks
#             # item['listed_abroad'] = listed_abroad
#             # item['listing_place'] = listing_place
#             # item['exchange_market_code'] = exchange_market_code
