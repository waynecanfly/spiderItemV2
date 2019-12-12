# -*- coding: utf-8 -*-
import pymysql
import scrapy

from hongkong.items import HongKongHtmlFileItem


class DocumentFileDownloadSpiderSpider(scrapy.Spider):
    '''document type 类型文件的下载'''
    name = 'HKEX_document_file_download_spider'
    allowed_domains = ['hkex.com']
    start_urls = ['http://hkex.com/']

    def start_requests(self):
        conn = pymysql.connect(host="10.100.4.99", port=3306, db="opd_common", user="root", passwd="OPDATA",
                               charset="utf8")
        cursor = conn.cursor()
        sql = "select corresponding_link, report_id from financial_html_origin_began_complete where " \
              "source_category='document type' and is_downloaded='0' and country_code='HKG'"
        cursor.execute(sql)
        results = cursor.fetchall()
        # if results:
        for res in results:
            corresponding_link = res[0]
            report_id = res[1]
            item = HongKongHtmlFileItem()
            yield scrapy.FormRequest(method='GET', url=corresponding_link, callback=self.parse,
                                     errback=self.errback_scraping,
                                     meta={
                                         'corresponding_link': corresponding_link,
                                         'report_id': report_id,
                                         'item': item,
                                         # 'proxy': 'http://' + random.choice(self.ip_list)

                                     })

    def parse(self, response):
        report_id = response.meta['report_id']
        with open('W:/hkg/html/hongkong/' + report_id + '.pdf', 'wb') as wf:
            wf.write(response.body)
            wf.close()
        doc_local_path = 'X:/data/html/hongkong/' + str(report_id) + '.pdf'
        print('已成功下载' + report_id)
        item = HongKongHtmlFileItem()
        item['is_downloaded'] = '1'
        item['doc_local_path'] = doc_local_path
        item['report_id'] = report_id

        yield item

    def errback_scraping(self, failure):
        request = failure.request
        report_id = request.meta['report_id']
        self.logger.info('未成功下载 %s...', report_id)
        # print('未成功下载' + report_id)
