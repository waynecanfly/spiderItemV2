# -*- coding: utf-8 -*-
import time

import scrapy

from hongkong.items import HongKongDelistedCompanyItem

from samples.base_rule import HKEXIsNewDelistedSec


class HkexDelistedCompanyListSpider(scrapy.Spider):
    '''获取退上市公司列表'''
    name = 'HKEX_delisted_company_list'
    allowed_domains = ['webb-site.com']
    start_urls = ['http://webb-site.com/']
    market_url_dict = {
        'main': 'https://webb-site.com/dbpub/delisted.asp?s=nameup&t=s&e=m',
        'gem': 'https://webb-site.com/dbpub/delisted.asp?s=nameup&t=s&e=g'
    }

    def start_requests(self):
        new_market_url_dict = {v: k for k, v in self.market_url_dict.items()}
        for url in self.market_url_dict.values():
            bond_info = new_market_url_dict[url]
            yield scrapy.Request(url=url, callback=self.parse, meta={
                'bond_info': bond_info,
            })
        # print(new_market_url_dict)

    def parse(self, response):
        market_type = response.meta['bond_info']
        infos = response.xpath("//body/div[@class='mainbody']/table[@class='numtable']")
        info_list = infos.xpath("//tr")
        info_list.pop(0)
        for info in info_list:
            stock_code = info.xpath("./td[2]/a/text()").extract()
            issuer = info.xpath("./td[4]/a/text()").extract()
            first_trade = info.xpath("./td[5]/text()").extract()
            last_trade = info.xpath("./td[6]/text()").extract()
            delisted_date = info.xpath("./td[7]/text()").extract()
            trading_life_years = info.xpath("./td[8]/text()").extract()
            reason = info.xpath("./td[9]/text()").extract()
            # 以下代码重复严重，可以重写
            if len(stock_code) == 0:
                stock_code = 'Null'
            else:
                stock_code = stock_code[0]
            if len(issuer) == 0:
                issuer = 'Null'
            else:
                issuer = issuer[0]
            if len(first_trade) == 0:
                first_trade = 'Null'
            else:
                first_trade = first_trade[0]
            if len(last_trade) == 0:
                last_trade = 'Null'
            else:
                last_trade = last_trade[0]
            if len(delisted_date) == 0:
                delisted_date = 'Null'
            else:
                delisted_date = delisted_date[0]
            if len(trading_life_years) == 0:
                trading_life_years = 'Null'
            else:
                trading_life_years = trading_life_years[0]
            if len(reason) == 0:
                reason = 'Null'
            else:
                reason = reason[0]
            gmt_create = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if not HKEXIsNewDelistedSec(stock_code):
                item = HongKongDelistedCompanyItem()
                item['country_code'] = 'HKG'
                item['exchange_market_code'] = 'HKEX'
                item['security_code'] = stock_code
                item['issuer'] = issuer
                item['first_trade'] = first_trade
                item['market_type'] = market_type
                item['last_trade'] = last_trade
                item['delisting_date'] = delisted_date
                item['trading_life_years'] = trading_life_years
                item['status'] = -2
                item['reason'] = reason
                item['gmt_create'] = gmt_create
                item['user_create'] = 'cf'

                yield item