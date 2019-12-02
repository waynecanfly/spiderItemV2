# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# # Author: xfc
# # @Time : 2019/10/9 16:58
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
# from ..items import BonusItem
# from ..items import DeliveryItem
# from ..items import Bonus
# from ..items import Delivery
#
#
# class SseProfitSpider(scrapy.Spider):
#     name = 'SSE_profit'
#     allowed_domains = ['sse.com.cn']
#
#     data_form = {
#         'isPagination': 'false',
#     }
#
#     get_request_url = 'http://query.sse.com.cn/commonQuery.do?'
#
#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         spider = super(SseProfitSpider, cls).from_crawler(
#             crawler, *args, **kwargs
#         )
#         crawler.signals.connect(spider.spider_opened, signals.spider_opened)
#         return spider
#
#     def spider_opened(self):
#         """ 查询当前所有存量公司 """
#         conn = pymysql.connect(**self.settings['DBARGS'])
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT company_code, security_code FROM `company_data_source_complete20191010_copy` "
#                            "WHERE country_code='chn' AND exchange_market_code='SSE' AND is_batch=0 ORDER BY security_code ASC ;")
#             feild_list = cursor.fetchall()
#             conn.close()
#
#             return feild_list
#
#     def start_requests(self):
#         for feild_data in self.spider_opened():
#             self.data_form['sqlId'] = 'COMMON_SSE_ZQPZ_GG_LYFP_AGFH_L'
#             self.data_form['productid'] = feild_data['security_code']
#
#             yield scrapy.FormRequest(
#                 method="GET",
#                 callback=self.parse_bonus,
#                 url=self.get_request_url,
#                 formdata=self.data_form,
#                 meta={
#                     'proxy' : 'http://58.218.200.247:9186',
#                     'company_code' : feild_data['company_code']
#                 }
#             )
#
#             self.data_form['sqlId'] = 'COMMON_SSE_ZQPZ_GG_LYFP_AGSG_L'
#             self.data_form['productid'] = feild_data['security_code']
#
#             yield scrapy.FormRequest(
#                 method="GET",
#                 callback=self.parse_delivery,
#                 url=self.get_request_url,
#                 formdata=self.data_form,
#                 meta={
#                     'proxy' : 'http://58.218.201.74:9166',
#                     'company_code': feild_data['company_code']
#                 }
#             )
#
#     def parse_bonus(self, response):
#         # item1 = Bonus()
#         # dict1 = {}
#         jres_bonus = json.loads(response.text)['result']
#         head_id = 0
#         for bonus_json in jres_bonus:
#             head_id += 1
#             # 股权登记日
#             bonus_registration_date = ('股权登记日', bonus_json['RECORD_DATE_A'], 1, head_id)
#             # 股权登记日总股本(万股)
#             bonus_equity_total = ('股权登记日总股本(万股)', bonus_json['ISS_VOL'], 2, head_id)
#             # 除息交易日
#             bonus_deduction_date = ('除息交易日', bonus_json['EX_DIVIDEND_DATE_A'], 3, head_id)
#             # 除息前日收盘价
#             bonus_close_price = ('除息前日收盘价', bonus_json['LAST_CLOSE_PRICE_A'], 4, head_id)
#             # 除息报价
#             bonus_quotation = ('除息报价', bonus_json['OPEN_PRICE_A'], 5, head_id)
#             # 每股红利
#             bonus_per_share  = ('每股红利', bonus_json['DIVIDEND_PER_SHARE2_A'], 6, head_id)
#             classification_id = 20
#             item1 = {}
#             dict1 = {}
#             dict1['bonus_registration_date'] = bonus_registration_date
#             dict1['bonus_equity_total'] = bonus_equity_total
#             dict1['bonus_deduction_date'] = bonus_deduction_date
#             dict1['bonus_close_price'] = bonus_close_price
#             dict1['bonus_quotation'] = bonus_quotation
#             dict1['bonus_per_share'] = bonus_per_share
#             item1['company_code'] = response.meta['company_code']
#             item1['classification_id'] = classification_id
#             item1['gmt_create'] = str(datetime.now())
#             item1['user_create'] = 'xfc'
#             item1['result'] = dict1
#             print(item1)
#
#             # yield BonusItem(
#             #     company_code = code,
#             #     bonus_registration_date = bonus_registration_date,
#             #     bonus_equity_total = bonus_equity_total,
#             #     bonus_deduction_date = bonus_deduction_date,
#             #     bonus_close_price = bonus_close_price,
#             #     bonus_quotation = bonus_quotation,
#             #     bonus_per_share = bonus_per_share
#             # )
#
#
#     def parse_delivery(self, response):
#         dict2 = {}
#         item2 = Delivery()
#         jres_delivery = json.loads(response.text)['result']
#         head_id = 0
#         for delivery_json in jres_delivery:
#             head_id += 1
#             # 股权登记日
#             delivery_registration_date = ('股权登记日', delivery_json['RECORD_DATE_A'], 1, head_id)
#             # 股权登记日总股本(万股)
#             equity_total = ('股权登记日总股本(万股)', delivery_json['ISS_VOL'], 2, head_id)
#             # 除权基准日
#             exclusion_date = ('除权基准日', delivery_json['EX_RIGHT_DATE_A'], 3, head_id)
#             # 红股上市日
#             red_stock_listing_date = ('红股上市日', delivery_json['TRADE_DATE_A'], 4, head_id)
#             # 公告刊登日
#             announcement_date = ('公告刊登日', delivery_json['ANNOUNCE_DATE'], 5, head_id)
#             # 送股比例
#             share_delivery_ratio = ('送股比例', delivery_json['BONUS_RATE'], 6, head_id)
#             # code = ('公司代码', response.meta['company_code'])
#             classification_id = 21
#
#             dict2['delivery_registration_date'] = delivery_registration_date
#             dict2['equity_total'] = equity_total
#             dict2['exclusion_date'] = exclusion_date
#             dict2['red_stock_listing_date'] = red_stock_listing_date
#             dict2['announcement_date'] = announcement_date
#             dict2['share_delivery_ratio'] = share_delivery_ratio
#             item2['company_code'] = response.meta['company_code']
#             item2['classification_id'] = classification_id
#             item2['gmt_create'] = str(datetime.now())
#             item2['user_create'] = 'xfc'
#             item2['result'] = dict2
#             yield item2
#
#             # yield DeliveryItem(
#             #     company_code = code,
#             #     delivery_registration_date = delivery_registration_date,
#             #     equity_total = equity_total,
#             #     exclusion_date = exclusion_date,
#             #     red_stock_listing_date = red_stock_listing_date,
#             #     announcement_date = announcement_date,
#             #     share_delivery_ratio = share_delivery_ratio
#             # )
#
