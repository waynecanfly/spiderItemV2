# -*- coding: utf-8 -*-
import random

import pymysql

import scrapy

from hongkong.items import HongKongFileItem


class HkexFileDownloadSpiderSpider(scrapy.Spider):
    name = 'HKEX_headline_file_download_spider'
    allowed_domains = ['hkex.com']
    start_urls = ['http://hkex.com/']
    # ip_list = [
    #     '58.218.200.253:9579',
    #     '58.218.200.253:4827',
    #     '58.218.201.74:7303',
    #     '58.218.200.214:3890',
    #     '58.218.200.214:3578',
    #     '58.218.201.74:8261',
    #     '58.218.200.253:8936',
    #     '58.218.201.122:9160',
    #     '58.218.201.74:8957',
    #     '58.218.201.74:8634',
    #     '58.218.201.114:4735',
    #     '58.218.201.74:4923',
    #     '58.218.201.114:8106',
    #     '58.218.201.74:6901',
    #     '58.218.200.253:8758',
    #     '58.218.201.114:8706',
    #     '58.218.200.253:2330',
    #     '58.218.201.114:8879',
    #     '58.218.201.74:6196',
    #     '58.218.200.214:8754',
    #     '58.218.201.74:7762',
    #     '58.218.200.253:2288',
    #     '58.218.201.74:6456'
    # ]


    def start_requests(self):
        '''下载香港文件表中为pdf类型的文件'''
        conn = pymysql.connect(host="10.100.4.99", port=3306, db="opd_common", user="root", passwd="OPDATA",
                               charset="utf8")
        cursor = conn.cursor()
        sql = "select doc_source_url, report_id, doc_type, disclosure_date from financial_origin_began_complete_hkg2019124_copy1 " \
              "where is_downloaded='0' and source_category='headline category' and country_code='HKG'"
        cursor.execute(sql)
        results = cursor.fetchall()
        # if results:
        for res in results:
            doc_source_url = res[0]
            report_id = res[1]
            doc_type = res[2]
            disclosure_date = res[3]
            item = HongKongFileItem()
            yield scrapy.FormRequest(method='GET', url=doc_source_url, callback=self.parse, errback=self.errback_scraping,
                meta={
                'doc_source_url': doc_source_url,
                'report_id': report_id,
                'doc_type': doc_type,
                'item': item,
                'disclosure_date': disclosure_date
                # 'proxy': 'http://' + random.choice(self.ip_list)

            })

    def parse(self, response):
        report_id = response.meta['report_id']
        doc_source_url = response.meta['doc_source_url']
        doc_type = response.meta['doc_type']
        disclosure_date = response.meta['disclosure_date']
        file_name = report_id + '.' + doc_type
        year = disclosure_date.year
        with open('W:/hkg/' + str(year) + '/' + file_name, 'wb') as wf:
            wf.write(response.body)
            wf.close()
        doc_local_path = '/nas2_volume3/hkg/' + str(year) + '/' + file_name
        print('已成功下载' + report_id)
        self.logger.info('已成功下载 %s...', report_id)
        item = HongKongFileItem()
        item['is_downloaded'] = '1'
        item['doc_local_path'] = doc_local_path
        item['report_id'] = report_id

        yield item

    def errback_scraping(self, failure):
        request = failure.request
        report_id = request.meta['report_id']
        print('未成功下载' + report_id)
        self.logger.info('未成功下载 %s...', report_id)
        # if 'item' in request.meta:  # 未正确处理的报表
        #     item = request.meta['item']
        #     item['is_downloaded'] = False
        #     self.total_failed += 1
        #     yield item
        # item = request.meta['item']
        # item['is_downloaded'] = 0
        # item['report_id'] = report_id

