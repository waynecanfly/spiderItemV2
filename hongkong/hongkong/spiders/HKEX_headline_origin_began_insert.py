# -*- coding: utf-8 -*-
import json
import time

import pymysql
import requests
import scrapy
from lxml import etree, html

from samples.data_clear import hongKongExtractDataTest, getReleaseYear, hongKongExtractFnYear, judgeFiscalYear, \
    disclosureTimeFormat, get_stockId

from hongkong.items import HongKongFileItem
from scrapy.utils.project import get_project_settings

from samples.base_rule import HKEXGetStockCode, HKEXGetStockCode1, HKEXGetStockCodeHeadlineType

from samples.custom_code_util import uniqueIDMaker

from samples.base_rule import HKEXIsNewFile


class FinancialOriginBeganCompleteInsertSpider(scrapy.Spider):
    '''
    文件列表页面是post请求，传递的参数包括:
        'lang':' EN',
                'category':' 0',
                'market':' SEHK',
                'searchType':' 1',
                'documentType':' -1',
                't1code':' 40000',
                't2Gcode':' -2',
                't2code':' 40100',
                'stockId':' 10148',
                'from':' 20070625',
                'to':' 20191021',
                'MB - Daterange':' 0',
                # 'title':''
        stockId是网站内部使用的值，获取方式是请求stockId_url得到json数据解析出来该字段，type代表Current Security:
        type=A:Current Security
        type=I:Delisted Security,详情查看业务提供的网址

        业务给的财报类型FY:40100
        Q2:40200
        quarterly_report:40300
    '''
    conn = pymysql.connect(host="10.100.4.99", port=3306, db="opd_common", user="root", passwd="OPDATA",
                           charset="utf8")
    cursor = conn.cursor()
    FILES_STORE = get_project_settings().get("FILES_STORE")
    name = 'HKEX_headline_origin_began_insert'
    allowed_domains = ['hkex.com']
    start_urls = ['http://hkex.com/']
    stockId_url = 'https://www1.hkexnews.hk/search/prefix.do?&callback=callback&lang=EN&type=A&name={stock_code}'
    company_file_url = 'https://www1.hkexnews.hk/search/titlesearch.xhtml?lang=en'
    doc_addr = 'https://www1.hkexnews.hk'

    quarterly_type_dict = {
        'FY': 40100,
        'Q2': 40200,
        'quarterly_report': 40300
    }

    def start_requests(self):
        # res_list = HKEXGetStockCode(self.cursor, 'company_data_source_complete20191010_copy1')
        res_list = HKEXGetStockCodeHeadlineType(self.cursor)
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
        # print(str(stock_code) + ':' + str(stockId))
        # with open('companyCodeStockId.csv', 'a+') as wf:
        #     print('写入：'+ company_code)
        #     wf.write(str(stock_code) + ':' + str(stockId) + '\n')
        #     wf.close()

        headers = {
            'Connection': 'keep-alive',
            'Content-Length': '158',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'www1.hkexnews.hk',
            'Origin': 'https://www1.hkexnews.hk',
            'Referer': 'https://www1.hkexnews.hk/search/titlesearch.xhtml?lang=en',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
        # # # for t2code in self.quarterly_type_dict.values():
        # #     # print(t2code)
        new_quarterly_type_dict = {v:k for k,v in self.quarterly_type_dict.items()}
        for quarterly_type_code in self.quarterly_type_dict.values():
            quarterly_type = new_quarterly_type_dict[quarterly_type_code]
            form_data = {
                'lang': 'EN',
                'category': '0',
                'market': 'SEHK',
                'searchType': '1',
                'documentType': '-1',
                't1code': '40000',
                't2Gcode': '-2',
                't2code': quarterly_type,
                'stockId': stockId,
                'from': '20070625',
                'to': '20191021',
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
            for tr in table_list:
                release_time = tr.xpath("./td[@class='text-right release-time']/text()")[1]
                stock_code = tr.xpath("./td[@class='text-right stock-short-code']/text()")[0]
                stock_short_name = tr.xpath("./td[@class='stock-short-name']/text()")[0]
                headline = tr.xpath("./td[4]/div[@class='headline']/text()")[0]
                title = tr.xpath("./td[4]/div[@class='doc-link']/a/text()")[0].replace(' ', '').replace('\r', '').replace('\t', '').replace('\n', '')
                doc_link = tr.xpath("./td[4]/div[@class='doc-link']/a/@href")[0]
                complete_doc_link = self.doc_addr + doc_link
                result = HKEXIsNewFile('financial_origin_began_complete20191101_copy1_copy1', 'headline category', complete_doc_link, company_code)
                if not result:
                    disclosure_date = disclosureTimeFormat(release_time)
                    fiscal_year = hongKongExtractFnYear(title)
                    if '/' in fiscal_year:
                        fiscal_year = judgeFiscalYear(fiscal_year)
                    else:
                        fiscal_year = fiscal_year

                    uniqueID = uniqueIDMaker()
                    report_id = company_code + uniqueID
                    gmt_create = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    item = HongKongFileItem()
                    item['company_code'] = company_code
                    item['disclosure_date'] = disclosure_date
                    item['security_code'] = stock_code
                    item['company_short_name'] = stock_short_name
                    item['headline'] = headline
                    item['file_original_title'] = title
                    item['doc_source_url'] = complete_doc_link
                    item['exchange_market_code'] = 'HKEX'
                    item['country_code'] = 'HKG'
                    item['user_create'] = 'cf'
                    item['report_id'] = report_id
                    item['fiscal_year'] = fiscal_year
                    item['quarterly_type'] = quarterly_type
                    item['gmt_create'] = gmt_create
                    item['source_category'] = 'Headline Category'
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
        # print(response.text)
        pass



