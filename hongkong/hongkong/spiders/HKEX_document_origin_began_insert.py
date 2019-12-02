# -*- coding: utf-8 -*-
import json
import time

import pymysql
import requests
import scrapy
from lxml import etree

from samples.base_rule import HKEXGetStockCode, HKEXGetStockCodeDocumentType, HKEXIsNewFile

from samples.data_clear import disclosureTimeFormat, hongKongExtractFnYear, hongKongExtractDataTest, getReleaseYear, get_stockId

from samples.custom_code_util import uniqueIDMaker

from hongkong.items import HongKongFileItem



class HkexDocumentOriginBeganInsertSpider(scrapy.Spider):
    '''爬取document type类型的公司公告 包括html和pdf文件信息'''
    name = 'HKEX_document_origin_began_insert'
    allowed_domains = ['hkex.com']
    start_urls = ['http://hkex.com/']
    stockId_url = 'https://www1.hkexnews.hk/search/prefix.do?&callback=callback&lang=EN&type=A&name={stock_code}'
    company_file_url = 'https://www1.hkexnews.hk/search/titlesearch.xhtml?lang=en'
    doc_addr = 'https://www1.hkexnews.hk'
    conn = pymysql.connect(host="10.100.4.99", port=3306, db="opd_common", user="root", passwd="OPDATA",
                           charset="utf8")
    cursor = conn.cursor()
    # 获取HKEX交易所网站中公司的编码stockId
    def start_requests(self):
        res_list = HKEXGetStockCodeDocumentType(self.cursor)
        for res in res_list:
            stock_code = res[0]
            company_short_name = res[1]
            company_code = res[2]
            callback = 'callback'
            url = self.stockId_url.format(stock_code=stock_code)
            yield scrapy.Request(url=url, callback=self.get_stockId_parse, meta={
                'stock_code': stock_code,
                'callback': callback,
                'company_short_name': company_short_name,
                'company_code': company_code
            })

        # # 测试部分
        # stock_code = '00001'
        # company_short_name = 'CKH HOLDINGS'
        # callback = 'callback'
        # company_code = 'HKG104948'
        # url = self.stockId_url.format(stock_code=stock_code)
        # yield scrapy.Request(url=url, callback=self.get_stockId_parse, meta={
        #     'stock_code': stock_code,
        #     'company_short_name': company_short_name,
        #     'callback': callback,
        #     'company_code': company_code
        # })

    def get_stockId_parse(self, response):
        stock_code = response.meta['stock_code']
        uselessData = response.meta['callback']
        company_short_name = response.meta['company_short_name']
        company_code = response.meta['company_code']
        response_text = response.text
        res_text = hongKongExtractDataTest(response_text, uselessData, -3)
        jsobj = json.loads(res_text)
        stockInfo_list = jsobj['stockInfo']
        stockId = get_stockId(stockInfo_list, company_short_name)

        if stockId:
            headers = {
                'Connection': 'keep-alive',
                'Content-Length': '158',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'www1.hkexnews.hk',
                'Origin': 'https://www1.hkexnews.hk',
                'Referer': 'https://www1.hkexnews.hk/search/titlesearch.xhtml?lang=en',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
            }
            form_data = {
                'lang': 'EN',
                'category': '0',
                'market': 'SEHK',
                'searchType': '2',
                'documentType': '11500',
                't1code': '-2',
                't2Gcode': '-2',
                't2code': '-2',
                'stockId': stockId,
                'from': '19990401',
                'to': '20070624',
                'MB - Daterange': '0',
                'title': ''
            }
            print('开始请求文件列表')
            res = requests.post(self.company_file_url, data=form_data, headers=headers)
            print('请求成功，开始解析文件链接')
            html_str = res.text
            content = etree.HTML(html_str)
            table_list = content.xpath("//main[@class='title-search']/div[@id='titleSearchResultPanel']/div[@class='title-search-content']/"
                                    "div[@class='title-search-result search-page-container']/table[@class='table sticky-header-table table-scroll table-mobile-list']/tbody//tr")
            # print(table_list)
            for tr in table_list:
                release_time = tr.xpath("./td[@class='text-right release-time']/text()")[1]
                stock_code = tr.xpath("./td[@class='text-right stock-short-code']/text()")[0]
                stock_short_name = tr.xpath("./td[@class='stock-short-name']/text()")[0]
                # headline = tr.xpath("./td[4]/div[@class='headline']/text()")[0]
                title = tr.xpath("./td[4]/div[@class='doc-link']/a/u/text()")[0].replace(' ', '').replace('\r', '').replace('\t', '').replace('\n', '')
                doc_link = tr.xpath("./td[4]/div[@class='doc-link']/a/@href")[0]
                complete_doc_link = self.doc_addr + doc_link
                result = HKEXIsNewFile('financial_origin_began_complete20191101_copy1_copy1', 'document type',
                                       complete_doc_link, company_code)
                if not result:
                    release_year = getReleaseYear(release_time)
                    disclosure_date = disclosureTimeFormat(release_time)
                    uniqueID = uniqueIDMaker()
                    report_id = company_code + uniqueID
                    gmt_create = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    item = HongKongFileItem()
                    item['company_code'] = company_code
                    item['disclosure_date'] = disclosure_date
                    item['security_code'] = stock_code
                    item['company_short_name'] = stock_short_name
                    item['file_original_title'] = title
                    item['doc_source_url'] = complete_doc_link
                    item['exchange_market_code'] = 'HKEX'
                    item['country_code'] = 'HKG'
                    item['user_create'] = 'cf'
                    item['report_id'] = report_id
                    item['fiscal_year'] = release_year
                    item['gmt_create'] = gmt_create
                    item['source_category'] = 'document type'
                    item['is_inflows_financial_html'] = 0
                    doc_name = doc_link.split('/')[-1]
                    # 对文件类型进行判断
                    doc_type = doc_name[-3:]
                    if doc_type == 'htm':
                        item['doc_type'] = 'htm'
                    else:
                        item['doc_type'] = 'pdf'
                    item['is_downloaded'] = 0

                    yield item


    def parse(self, response):
        pass
