# -*- coding: utf-8 -*-
import json
import time

import pymysql
import requests
import scrapy

from samples.data_clear import HKEXGetToken, hongKongExtractData

from samples.base_rule import HKEXGetSymCode, HKEXGetCompcodeBySymCode

from hongkong.items import HongkongOriginInfoItem



class HkexOriginInfoUpdateSpider(scrapy.Spider):
    name = 'HKEX_origin_info_update'
    allowed_domains = ['hkex.com']
    start_urls = ['http://hkex.com/']
    url = 'https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities?sc_lang=en'
    url_origin = "https://www1.hkex.com.hk/hkexwidget/data/getequityquote?sym={sym}&token={token}&lang=eng&qid={qid}&callback={callback}"
    conn = pymysql.connect(host="10.100.4.99", port=3306, db="opd_common", user="root", passwd="OPDATA",
                           charset="utf8")
    cursor = conn.cursor()

    def start_requests(self):
        # get请求获取公司的json数据，url中的参数有token,callback,和时间戳

        # equity_type通过url中参数preset获取公司列表，以下是自己构建的preset和equity_type的字典，数据来源：
        # https://www1.hkex.com.hk/hkexwidget/data/getequityfilter?lang=eng&token=evLtsLsBNAUVTPxtGqVeG4rU%2fr5pezNPoyMv
        # 7bJb0tvw03NC6moq0yFjwNAM3blt&preset=1|&sort=5&order=0&all=1&qid=1571033378530&callback=jQuery31108811674289579774_1571033304451

        response = requests.get(self.url)
        res = response.text
        # 获取token值
        token = HKEXGetToken(res)
        qid = str(time.time()).replace('.', '')[:13]
        callback = 'callback=jQuery31108811674289579774_{qid}'.format(qid=qid)


        # 发送请求，获取公司信息的数据
        sym_list = HKEXGetSymCode(self.cursor, 'company_data_source_complete20191010_copy1')
        for sym in sym_list:
            url = self.url_origin.format(sym=sym, token=token, qid=qid, callback=callback)
            yield scrapy.Request(url=url, callback=self.parse_origin, meta={
                'callback': callback
            })


    def parse_origin(self, response):
        # 清洗json数据
        callback_key = response.meta['callback']
        response_text = hongKongExtractData(response, callback_key, -1)
        jsobj = json.loads(response_text)
        company_origin_list = jsobj['data']['quote']
        issued_shares = company_origin_list['amt_os']
        industry = str(company_origin_list['hsic_ind_classification']) + '-' + str(
            company_origin_list['hsic_sub_sector_classification'])
        listing_date = company_origin_list['listing_date']
        financial_year_ends = company_origin_list['fiscal_year_end']

        if financial_year_ends:
            financial_year_ends = financial_year_ends
        else:
            financial_year_ends = None

        chairman = company_origin_list['chairman']
        principal_office = company_origin_list['office_address']
        place_of_incorporation = company_origin_list['incorpin']
        listing_category = company_origin_list['listing_category']
        registrar = company_origin_list['registrar']
        isin = company_origin_list['isin']
        stock_code = company_origin_list['sym']
        company_name = company_origin_list['nm']
        company_short_name = company_origin_list['nm_s']
        res = HKEXGetCompcodeBySymCode(self.cursor, 'company_data_source_complete20191010_copy1', stock_code)
        if res:
            company_code = res[0]
            item = HongkongOriginInfoItem()
            item['company_code'] = ('custom_code', company_code)
            item['issued_shares'] = ('issued_shares', issued_shares)
            item['industry'] = ('industry', industry)
            item['listing_date'] = ('listing_date', listing_date)
            item['financial_year_ends'] = ('financial_year_ends', financial_year_ends)
            item['chairman'] = ('chairman', chairman)
            item['principal_office'] = ('principal_office', principal_office)
            item['place_of_incorporation'] = ('place_of_incorporation', place_of_incorporation)
            item['listing_category'] = ('listing_category', listing_category)
            item['registrar'] = ('registrar', registrar)
            item['isin'] = ('isin', isin)
            item['stock_code'] = ('stock_code', stock_code)
            item['company_name'] = ('company_name', company_name)
            item['company_short_name'] = ('company_short_name', company_short_name)

        yield item


    def parse(self, response):
        pass
