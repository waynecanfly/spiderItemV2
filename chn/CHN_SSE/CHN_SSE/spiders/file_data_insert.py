#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/10/20 13:42
import scrapy
import pymysql
import json
import random

from datetime import datetime

from scrapy import signals
from ..samples import MD5_Value
from ..items import SseFileDataItem, SseFileData2Item


class FileDataSpider(scrapy.Spider):
    name = 'file_data_insert'
    allowed_domains = ['sse.com.cn']

    file_url = 'http://query.sse.com.cn/security/stock/queryCompanyBulletin.do?'

    # date_parameter = [
    #     ('2010-01-01', '2012-12-31'),
    #     ('2013-01-01', '2015-12-31'),
    #     ('2016-01-01', '2018-12-31'),
    #     ('2019-01-01', str(datetime.now()).split(' ')[0])
    # ]

    date_parameter = [
        ('2001-01-01', '2002-12-31'),
        ('2003-01-01', '2005-12-31'),
        ('2006-01-01', '2008-12-31'),
        ('2009-01-01', '2009-12-31'),
        ('2010-01-01', '2012-12-31'),
        ('2013-01-01', '2015-12-31'),
        ('2016-01-01', '2018-12-31'),
        ('2019-01-01', str(datetime.now()).split(' ')[0])
    ]

    report_type = {
        '年报摘要': 'FYD',
        '年报': 'FY',
        '第一季度季报': 'Q1',
        '半年报': 'Q2',
        '半年报摘要': 'Q2',
        '半年报补充公告': 'Q2',
        '第三季度季报': 'Q3',
        '年报补充公告': 'FY',
        '年报更正公告': 'FY'
    }

    data_form = {
        'isPagination': 'true',
        'securityType': '0101,120100,020100,020200,120200',
        'reportType2': 'DQBG',
        'pageHelp.pageSize': '100',
    }

    ip_list = [
        '58.218.92.157:9968',
        '58.218.92.90:9552',
        '58.218.92.137:9931'
    ]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(FileDataSpider, cls).from_crawler(
            crawler, *args, **kwargs
        )
        crawler.signals.connect(spider.spider_opened, signals.spider_opened)
        return spider

    def spider_opened(self):
        """ 查询当前所有存量公司 """
        conn = pymysql.connect(**self.settings['DBARGS'])
        with conn.cursor() as cursor:
            cursor.execute("SELECT company_code, security_code FROM `company_data_source_complete20191010_copy` WHERE "
                           "exchange_market_code='SSE' AND country_code='chn' ORDER BY security_code ASC ;")

            # cursor.execute("SELECT `company_data_source_complete20191010_copy`.`company_code`, "
            #             "`company_data_source_complete20191010_copy`.`security_code`, "
            #             "`company_data_source_complete20191010_copy`.`exchange_market_code` "
            #             "FROM `company_data_source_complete20191010_copy` WHERE "
            #             "`company_data_source_complete20191010_copy`.`exchange_market_code`='SSE' "
            #             "AND `company_data_source_complete20191010_copy`.`company_code` NOT IN "
            #             "(SELECT company_code FROM `financial_origin_began_complete20191104`)")
            feild_list = cursor.fetchall()

            conn.close()
            return feild_list


    def start_requests(self):
        try:
            count = 1
            for feild_dict in self.spider_opened():
                for date_before in self.date_parameter:
                    self.data_form['productId'] = feild_dict['security_code']
                    self.data_form['beginDate'] = date_before[0]
                    self.data_form['endDate'] = date_before[1]

                    yield scrapy.FormRequest(
                        method="GET",
                        callback=self.parse_first,
                        url=self.file_url,
                        formdata=self.data_form,
                        meta={
                            'company_code': feild_dict['company_code'],
                            'security_code': feild_dict['security_code'],
                            'file_num': feild_dict['file_num'],
                            'is_batch': feild_dict['is_batch']
                        }
                    )

                    count += 1
        except Exception as e:
            return "ERROR Wrroy %s" % e

    def parse_first(self, response):
        value_whole = json.loads(response.text)['result']
        if response.meta['is_batch'] == 1:
            for element in value_whole:
                # print(element['BULLETIN_TYPE'])
                # with open('index_value.txt', 'a') as wf:
                #     wf.write((response.meta['company_id'] + ', ' + response.meta['security_code'] + ', ' + element['BULLETIN_TYPE'] + ', ' + element['BULLETIN_YEAR']) + '\n')

                report_id = response.meta['company_code'] + self.uniqueIDMaker()
                # doc_name = '/data/OPDCMS/china/SSE_CHN/{file_name}.pdf'.format(
                #     file_name=report_id
                # )
                doc_name = 'E:\\Restructure\\sse_file\\{file_name}.pdf'.format(
                    file_name=report_id
                )
                with open(r'%s' % doc_name, 'wb') as wf:
                    wf.write(response.body)

                title_quarter = element['BULLETIN_TYPE']

                # 文件id
                report_id = report_id
                # 国家代码
                country_code = 'chn'
                # 交易所
                exchange_market_code = 'SSE'
                # 公司代码
                company_code = response.meta['company_code']
                # 原始标题
                file_original_title = element['TITLE']
                # 证券代码
                security_code = element['SECURITY_CODE']
                # 文件披露时间
                disclosure_date = element['SSEDATE']
                # 文件年份
                fiscal_year = element['BULLETIN_YEAR']
                # 文件季度类型
                quarterly_type = self.report_type[title_quarter]
                # 文件url
                doc_source_url = element['URL']
                # 文件路径
                doc_local_path = doc_name
                # 文件类型
                doc_type = 'pdf'
                # MD5值
                md5 = MD5_Value.MD5_VALUE(doc_name)
                # 创建时间
                gmt_create = str(datetime.now())
                # 创建用户
                user_create = 'xfc'
                yield SseFileDataItem(
                    report_id = report_id,
                    country_code = country_code,
                    exchange_market_code = exchange_market_code,
                    company_code = company_code,
                    file_original_title = file_original_title,
                    security_code = security_code,
                    disclosure_date = disclosure_date,
                    fiscal_year = fiscal_year,
                    quarterly_type = quarterly_type,
                    doc_source_url = doc_source_url,
                    doc_local_path = doc_local_path,
                    doc_type = doc_type,
                    md5 = md5,
                    gmt_create = gmt_create,
                    user_create = user_create
                )
        elif len(value_whole) > response.meta['file_num']:
            download_num = int(len(value_whole)) - int(response.meta['file_num'])
            value_whole.reverse()
            get_dates = value_whole[0:download_num]
            for element in value_whole:
                # print(element['BULLETIN_TYPE'])
                # with open('index_value.txt', 'a') as wf:
                #     wf.write((response.meta['company_id'] + ', ' + response.meta['security_code'] + ', ' + element['BULLETIN_TYPE'] + ', ' + element['BULLETIN_YEAR']) + '\n')

                report_id = response.meta['company_code'] + self.uniqueIDMaker()
                # doc_name = '/data/OPDCMS/china/SSE_CHN/{file_name}.pdf'.format(
                #     file_name=report_id
                # )
                doc_name = 'E:\\Restructure\\sse_file\\{file_name}.pdf'.format(
                    file_name=report_id
                )
                with open(r'%s' % doc_name, 'wb') as wf:
                    wf.write(response.body)

                title_quarter = element['BULLETIN_TYPE']

                # 文件id
                report_id = report_id
                # 国家代码
                country_code = 'chn'
                # 交易所
                exchange_market_code = 'SSE'
                # 公司代码
                company_code = response.meta['company_code']
                # 原始标题
                file_original_title = element['TITLE']
                # 证券代码
                security_code = element['SECURITY_CODE']
                # 文件披露时间
                disclosure_date = element['SSEDATE']
                # 文件年份
                fiscal_year = element['BULLETIN_YEAR']
                # 文件季度类型
                quarterly_type = self.report_type[title_quarter]
                # 文件url
                doc_source_url = element['URL']
                # 文件路径
                doc_local_path = doc_name
                # 文件类型
                doc_type = 'pdf'
                # MD5值
                md5 = MD5_Value.MD5_VALUE(doc_name)
                # 创建时间
                gmt_create = str(datetime.now())
                # 创建用户
                user_create = 'xfc'
                yield SseFileData2Item(
                    report_id = report_id,
                    country_code = country_code,
                    exchange_market_code = exchange_market_code,
                    company_code = company_code,
                    file_original_title = file_original_title,
                    security_code = security_code,
                    disclosure_date = disclosure_date,
                    fiscal_year = fiscal_year,
                    quarterly_type = quarterly_type,
                    doc_source_url = doc_source_url,
                    doc_local_path = doc_local_path,
                    doc_type = doc_type,
                    md5 = md5,
                    gmt_create = gmt_create,
                    user_create = user_create
                )



    def uniqueIDMaker(self):
        time_id = str(datetime.now()).split(".")[-1]
        random_id1 = str(random.randrange(0, 9))
        random_id2 = str(random.randrange(0, 9))
        unique_id = time_id + random_id1 + random_id2
        return unique_id

