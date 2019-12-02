# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# # Author: xfc
# # @Time : 2019/10/11 18:21
# import scrapy
# import pymysql
# import json
# import random
#
# from datetime import datetime
#
# from scrapy import signals
# from ..items import SseFileDataItem
# from ..samples import MD5_Value
#
#
# class SseFileSpider(scrapy.Spider):
#     name = 'SSE_file_insert'
#     allowed_domains = ['sse.com.cn']
#
#     file_url = 'http://query.sse.com.cn/security/stock/queryCompanyBulletin.do'
#
#     date_parameter = [
#         ('2010-01-01', '2012-12-31'),
#         ('2013-01-01', '2015-12-31'),
#         ('2016-01-01', '2018-12-31'),
#         ('2019-01-01', str(datetime.now()).split(' ')[0])
#     ]
#
#     form_data = {
#         'isPagination': 'true',
#         'pageHelp.pageCount': '100',
#         'reportType2': 'DQBG',
#         'securityType': '0101,120100,020100,020200,120200'
#     }
#
#     report_type = {
#         '年报摘要':'FYD',
#         '年报':'FY',
#         '第一季度季报':'Q1',
#         '半年报': 'Q2',
#         '半年报摘要':'Q2',
#         '第三季度季报':'Q3',
#     }
#
#     ip_list = [
#         "58.218.200.247:8766",
#         "58.218.200.247:8776",
#         "58.218.200.248:8761",
#         "58.218.200.229:8763",
#         "58.218.200.229:8759",
#         "58.218.200.229:8772",
#         "58.218.200.247:8795",
#         "58.218.200.247:8797",
#         "58.218.200.237:5181",
#         "58.218.200.249:8750",
#         "58.218.200.247:8777",
#         "58.218.200.247:8761",
#     ]
#
#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         spider = super(SseFileSpider, cls).from_crawler(
#             crawler, *args, **kwargs
#         )
#         crawler.signals.connect(spider.spider_opened, signals.spider_opened)
#         return spider
#
#     def spider_opened(self):
#         """ 查询当前所有存量公司 """
#         conn = pymysql.connect(**self.settings['DBARGS'])
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT company_id, security_code FROM `company_data_source_complete20191010` "
#                            "WHERE country_code='chn' AND is_batch=0 ORDER BY security_code ASC ;")
#             feild_list = cursor.fetchall()
#
#             conn.close()
#             return feild_list
#
#
#     def start_requests(self):
#         for feild_dict in self.spider_opened():
#             unique_datas = [feild_dict['company_id'], feild_dict['security_code']]
#
#             for date_feild in self.date_parameter:
#                 # print(date_feild, unique_datas, '*'*30)
#
#                 self.form_data['productId'] = unique_datas[1]
#                 self.form_data['beginDate'] = date_feild[0]
#                 self.form_data['endDate'] = date_feild[1]
#
#                 yield scrapy.FormRequest(
#                     method="GET",
#                     callback=self.parse,
#                     url=self.file_url,
#                     formdata=self.form_data,
#                     meta={
#                         "company_code" : unique_datas[0],
#                         "security_code" : unique_datas[1],
#                         "proxy" : "http://" + random.choice(self.ip_list)
#                     }
#                 )
#
#
#     def parse(self, response):
#
#         build_jres = json.loads(response.text)
#         if build_jres['result']:
#             for feild_datas in build_jres['result']:
#
#                 # 报表类型
#                 report_origin = feild_datas['BULLETIN_TYPE']
#                 quarterly_type = self.report_type[report_origin]
#                 # 披露时间
#                 disclosure_date = feild_datas['SSEDATE']
#                 # 原始标题
#                 file_original_title = feild_datas['TITLE']
#                 # 证券代码
#                 security_code = feild_datas['SECURITY_CODE']
#                 # 文件链接
#                 doc_source_url = "http://www.sse.com.cn" + feild_datas['URL']
#
#                 yield scrapy.FormRequest(
#                     method="GET",
#                     callback=self.parse_download,
#                     url=doc_source_url,
#                     meta={
#                         "company_code" : response.meta['company_code'],
#                         "security_code" : response.meta['security_code'],
#                         "quarterly_type" : quarterly_type,
#                         "disclosure_date" : disclosure_date,
#                         "file_original_title" : file_original_title,
#                         "doc_source_url" : doc_source_url,
#                         "proxy" : 'http://' + random.choice(self.ip_list)
#                     }
#                 )
#
#     def uniqueIDMaker(self):
#         time_id = str(datetime.now()).split(".")[-1]
#         random_id1 = str(random.randrange(0, 9))
#         random_id2 = str(random.randrange(0, 9))
#         unique_id = time_id + random_id1 + random_id2
#         return unique_id
#
#     def parse_download(self, response):
#         try:
#             report_id = response.meta['company_code'] + self.uniqueIDMaker()
#             doc_name = '/data/OPDCMS/china/SSE_CHN/{file_name}.pdf'.format(
#                 file_name= report_id
#             )
#             with open(r'%s' % doc_name, 'wb') as wf:
#                 wf.write(response.body)
#
#             item = SseFileDataItem()
#             item['report_id'] = report_id
#             item['country_code'] = 'chn'
#             item['exchange_market_code'] = 'SSE'
#             item['company_code'] = response.meta['company_code']
#             item['security_code'] = response.meta['security_code']
#             item['fiscal_year'] = ''.join(response.meta['disclosure_date']).split('-')[0]
#             item['quarterly_type'] = response.meta['quarterly_type']
#             item['disclosure_date'] = response.meta['disclosure_date']
#             item['file_original_title'] = response.meta['file_original_title']
#             item['doc_source_url'] = response.meta['doc_source_url']
#             item['doc_local_path'] = doc_name
#             item['doc_type'] = 'pdf'
#             item['md5'] = MD5_Value.MD5_VALUE(doc_name)
#             item['gmt_create'] = str(datetime.now())
#             item['user_create'] = 'xfc'
#             yield item
#
#
#         except:
#             yield scrapy.FormRequest(
#                 method="GET",
#                 callback=self.agan_parse,
#                 url= response.meta['doc_source_url'],
#                 meta={
#                     "company_code": response.meta['company_code'],
#                     "security_code": response.meta['security_code'],
#                     "quarterly_type": response.meta['quarterly_type'],
#                     "disclosure_date": response.meta['disclosure_date'],
#                     "file_original_title": response.meta['file_original_title'],
#                     "doc_source_url": response.meta['doc_source_url'],
#                     "proxy": 'http://' + random.choice(self.ip_list)
#                 }
#             )
#
#     def agan_parse(self, response):
#
#         report_id = response.meta['company_code'] + self.uniqueIDMaker()
#         doc_name = '/data/OPDCMS/china/SSE_CHN/{file_name}.pdf'.format(
#             file_name=report_id
#         )
#         with open(r'%s' % doc_name, 'wb') as wf:
#             wf.write(response.body)
#
#         item = SseFileDataItem()
#         item['report_id'] = report_id
#         item['country_code'] = 'chn'
#         item['exchange_market_code'] = 'SSE'
#         item['company_code'] = response.meta['company_code']
#         item['security_code'] = response.meta['security_code']
#         item['fiscal_year'] = ''.join(response.meta['disclosure_date']).split('-')[0]
#         item['quarterly_type'] = response.meta['quarterly_type']
#         item['disclosure_date'] = response.meta['disclosure_date']
#         item['file_original_title'] = response.meta['file_original_title']
#         item['doc_source_url'] = response.meta['doc_source_url']
#         item['doc_local_path'] = doc_name
#         item['doc_type'] = 'pdf'
#         item['md5'] = MD5_Value.MD5_VALUE(doc_name)
#         item['gmt_create'] = str(datetime.now())
#         item['user_create'] = 'xfc'
#         yield item
#
#
