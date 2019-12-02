# -*- coding: utf-8 -*-
import json
import re
import time

import pymysql
import requests
import scrapy

from hongkong.items import HongkongOriginInfoItem,  HongKongMarketItem, HongKongPresetItem, HongKongSecurityItem

from samples.base_rule import HKEXqueryCompanyCode, HKEXGetSymCode, HKEXGetCompcodeBySymCode

from samples.data_clear import hongKongExtractData,HKEXGetToken



class HkexOriginInfoInsertSpider(scrapy.Spider):
    '''爬取公司原始信息并入库'''
    conn = pymysql.connect(host="10.100.4.99", port=3306, db="opd_common", user="root", passwd="OPDATA",
                                charset="utf8")
    cursor = conn.cursor()
    gmt_create = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    name = 'HKEX_origin_info_insert'
    allowed_domains = ['hkex.com']
    start_urls = ['http://hkex.com/']
    url = 'https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities?sc_lang=en'
    security_type_dict = {
        'Equity': 'https://www1.hkex.com.hk/hkexwidget/data/getequityfilter?lang=eng&token={token}&sort=5&order=0&all=1&qid={qid}&callback={callback}',
        'REITs': 'https://www1.hkex.com.hk/hkexwidget/data/getreitfilter?lang=eng&token={token}&sort=5&order=0&all=1&qid={qid}&callback={callback}',
        'Etps': 'https://www1.hkex.com.hk/hkexwidget/data/getetpfilter?lang=eng&token={token}&sort=5&order=0&all=1&qid={qid}&callback={callback}',
        'DWs': 'https://www1.hkex.com.hk/hkexwidget/data/getdwfilter?lang=eng&token={token}&sort=5&order=0&all=1&qid={qid}&callback={callback}',
        'Inline Warrants': 'https://www1.hkex.com.hk/hkexwidget/data/getiwfilter?lang=eng&token={token}&sort=5&order=0&all=1&qid={qid}&callback={callback}',
        'CBBCs': 'https://www1.hkex.com.hk/hkexwidget/data/getcbbcfilter?lang=eng&token={token}&sort=5&order=0&all=1&qid={qid}&callback={callback}',
        'Debt Securities': 'https://www1.hkex.com.hk/hkexwidget/data/getdebtfilter?lang=eng&token={token}&sort=5&order=0&all=1&qid={qid}&callback={callback}'
    }
    # 市场类型链接
    market_dict = {
        'MAIN': 'https://www1.hkex.com.hk/hkexwidget/data/getequityfilter?lang=eng&token={token}&market=MAIN&sort=5&order=0&all=1&qid={qid}&callback={callback}',
        'GEM': 'https://www1.hkex.com.hk/hkexwidget/data/getequityfilter?lang=eng&token={token}&market=GEM&sort=5&order=0&all=1&qid={qid}&callback={callback}'
    }
    # 公司预设类型
    url_preset = 'https://www1.hkex.com.hk/hkexwidget/data/getequityfilter?lang=eng&token={token}&preset={preset}|&sort=5' \
                 '&order=0&all=1&qid={qid}&callback={callback}'

    preset_field_dict = {
        '1': 'Is Shortsell Eligible Securities',
        '9': 'Is CAS Securities',
        '3': 'Is VCM Eligible Securities',
        '4': 'Is A/H Companies',
        '6': 'Is Secondary Listings',
        '8': 'Is Stapled Securities'
    }
    # 公司详细信息链接
    url_origin = "https://www1.hkex.com.hk/hkexwidget/data/getequityquote?sym={sym}&token={token}&lang=eng&qid={qid}&callback={callback}"

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

        # 发送请求获取预设属性信息
        new_preset_field_dict = {v: k for k, v in self.preset_field_dict.items()}
        # for pre in self.preset_field_dict.keys():
        #     preset_field = self.preset_field_dict[pre]
        #     url = self.url_preset.format(token=token, preset=pre, qid=qid, callback=callback)
        #     yield scrapy.Request(url=url, callback=self.parse_preset, meta={
        #         'preset_field': preset_field,
        #         'callback': callback
        #     })

        # 发送请求，获取security_type的数据
        new_security_type_dict = {v: k for k, v in self.security_type_dict.items()}
        for url in self.security_type_dict.values():
            security_type = new_security_type_dict[url]
            url = url.format(token=token, qid=qid, callback=callback)
            yield scrapy.Request(url=url, callback=self.parse_security, meta={
                'security_type': security_type,
                'callback': callback
            })

        # # 发送请求，获取公司信息的数据
        # sym_list = HKEXGetSymCode(self.cursor, 'company_data_source_complete20191010_copy1')
        # for sym in sym_list:
        #     # if sym == '8053':
        #         url = self.url_origin.format(sym=sym, token=token, qid=qid, callback=callback)
        #         # print(url)
        #         yield scrapy.Request(url=url, callback=self.parse_origin, meta={
        #             'callback': callback
        #         })

        # 发送请求，获取市场类型信息
        # new_market_dict = {v: k for k, v in self.market_dict.items()}
        # for url in self.market_dict.values():
        #     market = new_market_dict[url]
        #     url = url.format(token=token, qid=qid, callback=callback)
        #     yield scrapy.Request(url=url, callback=self.parse_market, meta={
        #         'market': market,
        #         'callback': callback
        #     })

    # def parse_preset(self, response):
    #     callback_key = response.meta['callback']
    #     preset_field = response.meta['preset_field']
    #     # 数据清洗
    #     response_text = hongKongExtractData(response, callback_key, -1)
    #     jsobj = json.loads(response_text)
    #     company_code_list = jsobj['data']['stocklist']
    #     for company_info in company_code_list:
    #         stock_code = company_info['sym']
    #         res = HKEXGetCompcodeBySymCode(self.cursor, 'company_data_source_complete20191010_copy1', stock_code)
    #         if res:
    #             company_code = res[0]
    #             item = HongKongPresetItem()
    #             item['country_code'] = 'HKG'
    #             item['company_code'] = company_code
    #             item['display_label'] = preset_field
    #             item['information'] = '1'
    #             item['data_type'] = 'string'
    #             item['gmt_create'] = self.gmt_create
    #             item['user_create'] = 'cf'
    #
    #             yield item


    def parse_origin(self,response):
        # 清洗json数据
        callback_key = response.meta['callback']
        response_text = hongKongExtractData(response, callback_key, -1)
        jsobj = json.loads(response_text)
        company_origin_list = jsobj['data']['quote']
        gmt_create = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        issued_shares = company_origin_list['amt_os']
        industry = str(company_origin_list['hsic_ind_classification']) + '-' + str(company_origin_list['hsic_sub_sector_classification'])
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
        data_list = [
            ('issued_shares',issued_shares),
            ('industry', industry),
            ('listing_date', listing_date),
            ('financial_year_ends', financial_year_ends),
            ('chairman', chairman),
            ('principal_office', principal_office),
            ('place_of_incorporation', place_of_incorporation),
            ('listing_category',listing_category),
            ('registrar', registrar),
            ('isin', isin),
            ('stock_code', stock_code),
            ('company_name', company_name),
            ('company_short_name', company_short_name)
        ]
        res = HKEXGetCompcodeBySymCode(self.cursor, 'company_data_source_complete20191010_copy1', stock_code)

        if res:
            company_code = res[0]
            security_code = stock_code
            for data in data_list:
                item = HongkongOriginInfoItem()
                item['country_code'] = 'HKG'
                item['exchange_market_code'] = 'HKEX'
                item['security_code'] = security_code
                item['company_code'] = company_code
                item['display_label'] = data[0]
                item['information'] = data[1]
                item['gmt_create'] = gmt_create
                item['user_create'] = 'cf'

                yield item

    def parse_market(self, response):
        # 清洗json数据
        market = response.meta['market']
        callback_key = response.meta['callback']

        response_text = hongKongExtractData(response, callback_key, -1)
        jsobj = json.loads(response_text)
        comp_list = jsobj['data']['stocklist']
        for compinfo in comp_list:
            company_short_name = compinfo['nm']
            stock_code = compinfo['sym']
            res = HKEXGetCompcodeBySymCode(self.cursor, 'company_data_source_complete20191010_copy1', stock_code)
            if res:
                company_code = res[0]
                item = HongKongMarketItem()
                item['country_code'] = 'HKG'
                item['company_code'] = company_code
                item['display_label'] = 'market'
                item['information'] = market
                item['data_type'] = 'string'
                item['gmt_create'] = self.gmt_create
                item['user_create'] = 'cf'

                yield item


    def parse_security(self, response):
        # 清洗json数据
        callback_key = response.meta['callback']
        security_type = response.meta['security_type']
        response_text = hongKongExtractData(response, callback_key, -1)
        jsobj = json.loads(response_text)
        comp_list = jsobj['data']['stocklist']
        for comp_info in comp_list:
            stock_code = comp_info['sym']
            res = HKEXGetCompcodeBySymCode(self.cursor, 'company_data_source_complete20191010_copy1', stock_code)
            if res:
                company_code = res[0]
                item = HongKongSecurityItem()
                item['country_code'] = 'HKG'
                item['company_code'] = company_code
                item['display_label'] = 'security_type'
                item['information'] = security_type
                item['data_type'] = 'string'
                item['gmt_create'] = self.gmt_create
                item['user_create'] = 'cf'

                yield item
















