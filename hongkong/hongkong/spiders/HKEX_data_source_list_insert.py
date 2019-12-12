# -*- coding: utf-8 -*-
import scrapy
import json
import requests
import time


from hongkong.items import HongKongCompItem

from samples.custom_code_util import read_file, alter_file

from samples.data_clear import hongKongExtractData, HKEXGetToken

from samples.base_rule import HKEXIsNewCompany


class HongkongallSpider(scrapy.Spider):
    '''公司列表爬取'''
    name = 'HKEX_data_source_list_insert'
    allowed_domains = ['hkex.com']
    start_urls = ['http://hkex.com/']
    url = 'https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities?sc_lang=en'
    url_dict = {
        'Equity': 'https://www1.hkex.com.hk/hkexwidget/data/getequityfilter?lang=eng&token={token}&sort=5&order=0&all=1&qid={qid}&callback={callback}',
        'REITs': 'https://www1.hkex.com.hk/hkexwidget/data/getreitfilter?lang=eng&token={token}&sort=5&order=0&all=1&qid={qid}&callback={callback}',
        'Etps': 'https://www1.hkex.com.hk/hkexwidget/data/getetpfilter?lang=eng&token={token}&sort=5&order=0&all=1&qid={qid}&callback={callback}',
        'DWs': 'https://www1.hkex.com.hk/hkexwidget/data/getdwfilter?lang=eng&token={token}&sort=5&order=0&all=1&qid={qid}&callback={callback}',
        'Inline Warrants': 'https://www1.hkex.com.hk/hkexwidget/data/getiwfilter?lang=eng&token={token}&sort=5&order=0&all=1&qid={qid}&callback={callback}',
        'CBBCs': 'https://www1.hkex.com.hk/hkexwidget/data/getcbbcfilter?lang=eng&token={token}&sort=5&order=0&all=1&qid={qid}&callback={callback}',
        'Debt Securities':'https://www1.hkex.com.hk/hkexwidget/data/getdebtfilter?lang=eng&token={token}&sort=5&order=0&all=1&qid={qid}&callback={callback}'
    }


    def start_requests(self):
        # get请求获取公司的json数据，url中的参数有token,callback,和时间戳
        response = requests.get(self.url)
        res = response.text
        token = HKEXGetToken(res)
        qid = str(time.time()).replace('.', '')[:13]
        callback = 'jQuery31105065240248734231_{qid}'.format(qid=qid)
        new_dict = {v: k for k, v in self.url_dict.items()}
        for url in self.url_dict.values():
            security_type = new_dict[url]
            url = url.format(token=token, qid=qid, callback=callback)
            yield scrapy.Request(url=url, callback=self.parse, meta={
                                                                        'callback': callback,
                                                                        'company_list_url': url,
                                                                        'security_type': security_type
                                                                        })
    def parse(self, response):
        # 清洗json数据
        callback_key = response.meta['callback']
        company_list_url = response.meta['company_list_url']
        security_type = response.meta['security_type']
        response_text = hongKongExtractData(response, callback_key, -1)
        jsobj = json.loads(response_text)
        comp_list = jsobj['data']['stocklist']

        for compinfo in comp_list:
            stock_code = compinfo['sym']
            # 判断是否为新公司，即判断stock_code在当前数据库中对应的security_type中是否存在
            result = HKEXIsNewCompany(stock_code, 'company_base_info', security_type)
            if not result:

                custom_code = read_file('D:/Collection_SpiderItem/spiderItemV2/hongkong/hongkong/custom_code.txt')
                new_custom_code = int(custom_code) + 1
                alter_file('D:/Collection_SpiderItem/spiderItemV2/hongkong/hongkong/custom_code.txt', custom_code, str(new_custom_code))
                company_short_name = compinfo['nm']
                company_code = 'HKG' + custom_code
                gmt_create = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                item = HongKongCompItem()
                item['company_short_name'] = company_short_name
                item['country_code'] = 'HKG'
                item['unique_code'] = 'HKGHKEX' + str(stock_code)
                item['security_type'] = security_type
                item['company_code'] = company_code
                item['security_code'] = stock_code
                item['exchange_market_code'] = 'HKEX'
                item['company_list_url'] = company_list_url
                item['spider_name'] = 'HKEX_data_source_list_insert'
                item['gmt_create'] = gmt_create
                item['user_create'] = 'cf'
                item['is_batch'] = 0
            
                yield item
        