# -*- coding: utf-8 -*-
import time

import pymysql
import scrapy

from samples.base_rule import HKEXGetHtmlTypeFileInfo

from hongkong.items import HongKongHtmlFileItem

from samples.custom_code_util import uniqueIDMaker


class HkexDocumentFileDownloadSpiderSpider(scrapy.Spider):
    name = 'HKEX_financial_html_origin_began_insert'
    allowed_domains = ['hkex.com']
    start_urls = ['http://hkex.com/']
    conn = pymysql.connect(host="10.100.4.99", port=3306, db="opd_common", user="root", passwd="OPDATA",
                           charset="utf8")
    cursor = conn.cursor()
    def start_requests(self):
        '''用于处理香港htm文件，解析标题-链接格式的公告文件链接'''
        results = HKEXGetHtmlTypeFileInfo(self.cursor)
        for res in results:
            company_code = res[0]
            doc_source_url = res[1]
            source_category = res[2]
            link_head = 'https://www1.hkexnews.hk/listedco/listconews/' + doc_source_url.split('/')[-4] + '/' + \
                        doc_source_url.split('/')[-3] + '/' + doc_source_url.split('/')[-2]
            yield scrapy.Request(url=doc_source_url, callback=self.parse, meta={
                    'link_head': link_head,
                    'company_code': company_code,
                    'doc_source_url': doc_source_url,
                    'source_category': source_category
                })

    def parse(self, response):
        source_category = response.meta['source_category']
        doc_source_url = response.meta['doc_source_url']
        company_code = response.meta['company_code']
        link_head = response.meta['link_head']
        gmt_create = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        complete_href_lists = []
        title_lists = []
        href_list = response.xpath("//a")
        title_list = response.xpath("//a")
        for titles in title_list:
            title = titles.xpath("./text()").extract_first()
            if not title:
                title = titles.xpath("./font/text()").extract_first()
            title_lists.append(title)

        for hrefs in href_list:
            href = hrefs.xpath("./@href").extract_first()
            link_end = href.split('/')[-2] + '/' + href.split('/')[-1]
            complete_href = link_head + '/' + link_end
            # complete_href_list.append(complete_href)
            complete_href_lists.append(complete_href)
        title_link_dict = dict(zip(title_lists, complete_href_lists))
        for title, link in title_link_dict.items():
            uniqueID = uniqueIDMaker()
            report_id = company_code + uniqueID
            item = HongKongHtmlFileItem()
            item['country_code'] = 'HKG'
            item['company_code'] = company_code
            item['report_id'] = report_id
            item['dictionary_field'] = title
            item['corresponding_link'] = link
            item['is_downloaded'] = 0
            item['doc_source_url'] = doc_source_url
            item['source_category'] = source_category
            item['user_create'] = 'cf'
            item['gmt_create'] = gmt_create

            yield item

