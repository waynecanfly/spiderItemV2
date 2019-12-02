# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HongkongItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class HongKongCompItem(scrapy.Item):
    company_short_name = scrapy.Field()
    company_code = scrapy.Field()
    country_code = scrapy.Field()
    # 香港的stock_code保存在security_code字段
    unique_code = scrapy.Field()
    security_code = scrapy.Field()
    company_list_url = scrapy.Field()
    exchange_market_code = scrapy.Field()
    security_type = scrapy.Field()
    market = scrapy.Field()
    spider_name = scrapy.Field()
    is_batch = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class HongkongOriginInfoItem(scrapy.Item):
    """ 公司基本信息 """
    country_code = scrapy.Field()
    exchange_market_code = scrapy.Field()
    security_code = scrapy.Field()
    company_code = scrapy.Field()
    display_label = scrapy.Field()
    information = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()


class HongKongMarketItem(scrapy.Item):
    country_code = scrapy.Field()
    company_code = scrapy.Field()
    display_label = scrapy.Field()
    information = scrapy.Field()
    data_type = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class HongKongPresetItem(scrapy.Item):
    country_code = scrapy.Field()
    company_code = scrapy.Field()
    display_label = scrapy.Field()
    information = scrapy.Field()
    data_type = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class HongKongSecurityItem(scrapy.Item):
    country_code = scrapy.Field()
    company_code = scrapy.Field()
    display_label = scrapy.Field()
    information = scrapy.Field()
    data_type = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class HongKongFileItem(scrapy.Item):
    exchange_market_code = scrapy.Field()
    country_code = scrapy.Field()
    company_code = scrapy.Field()
    report_id = scrapy.Field()
    disclosure_date = scrapy.Field()
    security_code = scrapy.Field()
    stock_short_name = scrapy.Field()
    headline = scrapy.Field()
    complete_doc_link = scrapy.Field()
    is_downloaded = scrapy.Field()
    quarterly_type = scrapy.Field()
    doc_type = scrapy.Field()
    doc_source_url = scrapy.Field()
    source_category = scrapy.Field()
    doc_local_path = scrapy.Field()
    file_original_title = scrapy.Field()
    gmt_create = scrapy.Field()
    md5 = scrapy.Field()
    user_create = scrapy.Field()
    fiscal_year = scrapy.Field()
    company_short_name = scrapy.Field()
    is_inflows_financial_html = scrapy.Field()

class HongKongHtmlFileItem(scrapy.Item):
    country_code = scrapy.Field()
    company_code = scrapy.Field()
    report_id = scrapy.Field()
    dictionary_field = scrapy.Field()
    corresponding_link = scrapy.Field()
    doc_local_path = scrapy.Field()
    is_downloaded = scrapy.Field()
    doc_source_url = scrapy.Field()
    source_category = scrapy.Field()
    user_create = scrapy.Field()
    gmt_create = scrapy.Field()
    user_updated = scrapy.Field()
    gmt_update = scrapy.Field()

class HongKongDelistedCompanyItem(scrapy.Item):
    country_code = scrapy.Field()
    exchange_market_code = scrapy.Field()
    security_code = scrapy.Field()
    issuer = scrapy.Field()
    market_type = scrapy.Field()
    delisting_date = scrapy.Field()
    first_trade = scrapy.Field()
    last_trade = scrapy.Field()
    trading_life_years = scrapy.Field()
    status = scrapy.Field()
    reason = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()
