# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# # Author: xfc
# # @Time : 2019/10/8 16:03
# """
#
# 筹资情况：
#     A首次发行
#     A增发
#     A配股
#
#     特殊事件首日表现
#
# """
#
# import scrapy
# import json
# import pymysql
# from scrapy import signals
#
# from datetime import datetime
# from ..items import SpcialItem
# from ..items import InitialItem
# from ..items import SeoItem
# from ..items import AllocationItem
#
#
# class FinancingSpider(scrapy.Spider):
#
#     name = 'SSE_financing'
#     allowed_domains = ['sse.com.cn']
#
#     request_url = 'http://query.sse.com.cn/commonQuery.do?'
#     form_data = {
#         'isPagination': 'false'
#     }
#
#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         spider = super(FinancingSpider, cls).from_crawler(
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
#
#             return feild_list
#
#     def start_requests(self):
#         """ 发起请求 """
#
#         for security_item in self.spider_opened():
#             special_url = 'http://query.sse.com.cn/marketdata/tradedata/queryStockSpecialQuat.do?'
#
#             special_form = {
#                 'isPagination': 'true'
#             }
#             special_form['product'] = security_item['security_code']
#
#             #   特殊事件首日表现
#             yield scrapy.FormRequest(
#                 method = "GET",
#                 callback = self.parse_spcial,
#                 url = special_url,
#                 formdata = special_form,
#                 meta = {
#                     'proxy' : 'http://58.218.201.74:9198',
#                     'security_code' : special_form['product'],
#                     'company_code' : security_item['company_id']
#                 }
#             )
#
#             #   筹资情况
#             #       A首次发行
#             self.form_data['sqlId'] = 'COMMON_SSE_ZQPZ_GPLB_CZQK_AGSCFX_S'
#             self.form_data['productid'] = security_item['security_code']
#
#             yield scrapy.FormRequest(
#                 method = "GET",
#                 callback = self.parse_initial,
#                 url = self.request_url,
#                 formdata = self.form_data,
#                 meta = {
#                     'proxy' : 'http://58.218.200.249:8758',
#                     'security_code' : special_form['product'],
#                     'company_code' : security_item['company_id']
#                 }
#             )
#
#             #       A增发
#             self.form_data['sqlId'] = 'COMMON_SSE_ZQPZ_GPLB_CZQK_AGZF_S'
#             self.form_data['productid'] = security_item['security_code']
#
#             yield scrapy.FormRequest(
#                 method = "GET",
#                 callback = self.parse_seo,
#                 url = self.request_url,
#                 formdata = self.form_data,
#                 meta = {
#                     'proxy' : 'http://58.218.200.248:8779',
#                     'security_code' : special_form['product'],
#                     'company_code' : security_item['company_id']
#                 }
#             )
#
#             #       A配股
#             self.form_data['sqlId'] = 'COMMON_SSE_ZQPZ_GPLB_CZQK_AGPG_S'
#             self.form_data['productid'] = security_item['security_code']
#
#             yield scrapy.FormRequest(
#                 method = "GET",
#                 callback = self.parse_allocation,
#                 url = self.request_url,
#                 formdata = self.form_data,
#                 meta = {
#                     'proxy' : 'http://58.218.200.248:8785',
#                     'security_code' : special_form['product'],
#                     'company_code' : security_item['company_id']
#                 }
#             )
#
#
#     def parse_spcial(self, response):
#         """ 特殊事件首日表现 """
#
#         json_list = json.loads(response.text)['result']
#         for spcial_json in json_list:
#             # 日期
#             spcial_date = ('日期', spcial_json['listingDate'])
#             # 事件
#             spcial_listing = ('事件', spcial_json['listingMark'])
#             # 当日流通股本(万股)
#             curbonus = ('当日流通股本(万股)', spcial_json['curBonus'])
#             # 开盘价(元)
#             openprice = ('开盘价(元)', spcial_json['openprice'])
#             # 最高价(元)
#             highprice = ('最高价(元)', spcial_json['highprice'])
#             # 最低价(元)
#             lowprice = ('最低价(元)', spcial_json['lowprice'])
#             # 收盘价(元)
#             closeprice = ('收盘价(元)', spcial_json['closeprice'])
#             # 成交量(万股)
#             tradingvol = ('成交量(万股)', spcial_json['tradingvol'])
#             # 成交额(万元)
#             tradingamt = ('成交额(万元)', spcial_json['tradingamt'])
#             # 换手率
#             exchangerate = ('换手率', spcial_json['exchangerate'])
#             code = ('公司代码', response.meta['company_code'])
#
#             yield SpcialItem(
#                 company_code = code,
#                 spcial_date = spcial_date,
#                 spcial_listing = spcial_listing,
#                 curbonus = curbonus,
#                 openprice = openprice,
#                 highprice = highprice,
#                 lowprice = lowprice,
#                 closeprice = closeprice,
#                 tradingvol = tradingvol,
#                 tradingamt = tradingamt,
#                 exchangerate = exchangerate
#             )
#
#
#     def parse_initial(self, response):
#         """ A首发 """
#
#         json_list = json.loads(response.text)['result']
#         for initial_json in json_list:
#             # 发行数量(万股)
#             issued_number = ('发行数量(万股)', initial_json['ISSUED_VOLUME_A'])
#             # 发行价格
#             issued_price = ('发行价格', initial_json['ISSUED_PRICE_A'])
#             # 发行日期
#             issued_date = ('发行日期', initial_json['ISSUED_BEGIN_DATE_A'])
#             # 募集资金总额(万元)
#             issued_total = ('募集资金总额(万元)', initial_json['RAISED_MONEY_A'])
#             # 加权法
#             issued_weighting = ('加权法', initial_json['ISSUED_PROFIT_RATE_A1'])
#             # 摊薄法
#             issued_diminish = ('摊薄法', initial_json['ISSUED_PROFIT_RATE_A2'])
#             # 发行方式
#             issued_way = ('发行方式', initial_json['ISSUED_MODE_CODE_A'])
#             # 主承销商
#             issued_underwriter = ('主承销商', initial_json['MAIN_UNDERWRITER_NAME_A'])
#             # 中签率
#             get_rate = ('中签率', initial_json['GOT_RATE_A'])
#             code = ('公司代码', response.meta['company_code'])
#             yield InitialItem(
#                 company_code = code,
#                 issued_number = issued_number,
#                 issued_price = issued_price,
#                 issued_date = issued_date,
#                 issued_total = issued_total,
#                 issued_weighting = issued_weighting,
#                 issued_diminish = issued_diminish,
#                 issued_way = issued_way,
#                 issued_underwriter = issued_underwriter,
#                 get_rate = get_rate
#             )
#
#
#     def parse_seo(self,  response):
#         """ A增发 """
#
#         json_list = json.loads(response.text)['result']
#         for seo_json in json_list:
#             # 发行数量(万股)
#             seo_number = ('发行数量(万股)', seo_json['ISSUED_VOLUME_A'])
#             # 发行价格
#             seo_price = ('发行价格', seo_json['ISSUED_PRICE_A'])
#             # 发行日期
#             seo_date = ('发行日期', seo_json['ISSUED_BEGIN_DATE_A'])
#             # 配售价格
#             distribution_price = ('配售价格', seo_json['ISSUED_PRICE_A'])
#             # 发行方式
#             seo_mode = ('发行方式', seo_json['ISSUED_MODE_CODE_A'])
#             # 加权法
#             seo_way = ('加权法', seo_json['ISSUED_PROFIT_RATE_A1'])
#             # 摊薄法
#             seo_undderwrietr = ('摊薄法', seo_json['ISSUED_PROFIT_RATE_A2'])
#             # 上市推荐人
#             seo_recommender = ('上市推荐人', seo_json['RECOMMEND_NAME_A'])
#             # 主承办商
#             seo_contractor = ('主承办商', seo_json['MAIN_UNDERWRITER_NAME_A'])
#             # 中签率
#             get_rate = ('中签率', seo_json['GOT_RATE_A'])
#             # 老股东配售比例
#             shareholder_rate = ('老股东配售比例', seo_json['RIGHT_ISSUE_PRICE_A'])
#             code = ('公司代码', response.meta['company_code'])
#             yield SeoItem(
#                 company_code = code,
#                 seo_number = seo_number,
#                 seo_price = seo_price,
#                 seo_date = seo_date,
#                 distribution_price = distribution_price,
#                 seo_mode = seo_mode,
#                 seo_way = seo_way,
#                 seo_undderwrietr = seo_undderwrietr,
#                 seo_recommender = seo_recommender,
#                 seo_contractor = seo_contractor,
#                 get_rate = get_rate,
#                 shareholder_rate = shareholder_rate
#             )
#
#
#     def parse_allocation(self, response):
#         """ A配股 """
#
#         json_list = json.loads(response.text)['result']
#         for allocation_json in json_list:
#             # 股权登记日
#             registration_date = ('股权登记日', allocation_json['RECORD_DATE_A'])
#             # 除权交易日
#             exclusive_trading = ('除权交易日', allocation_json['EX_RIGHTS_DATE_A'])
#             # 配股价格
#             allocation_price = ('配股价格', allocation_json['PRICE_OF_RIGHTS_ISSUE_A'])
#             # 配股比例
#             allocation_rate = ('配股比例', allocation_json['RATIO_OF_RIGHTS_ISSUE_A'])
#             # 配股缴款起始日
#             start_date_pay = ('配股缴款起始日', allocation_json['START_DATE_OF_REMITTANCE_A'])
#             # 配股缴款截止日
#             end_date_pay = ('配股缴款截止日', allocation_json['END_DATE_OF_REMITTANCE_A'])
#             # 实际配股量(万股)
#             actual_allotment = ('实际配股量(万股)', allocation_json['TRUE_COLUME_A'])
#             # 配股上市日
#             allocation_listing_date = ('配股上市日', allocation_json['LISTING_DATE_A'])
#             code = ('公司代码', response.meta['company_code'])
#             yield AllocationItem(
#                 company_code = code,
#                 registration_date = registration_date,
#                 exclusive_trading = exclusive_trading,
#                 allocation_price = allocation_price,
#                 allocation_rate = allocation_rate,
#                 start_date_pay = start_date_pay,
#                 end_date_pay = end_date_pay,
#                 actual_allotment = actual_allotment,
#                 allocation_listing_date = allocation_listing_date
#             )
#
