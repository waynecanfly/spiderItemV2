# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChnSzseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_id = scrapy.Field()
    security_code = scrapy.Field()
    company_abbreviation = scrapy.Field()
    company_name = scrapy.Field()
    country_code = scrapy.Field()
    latest_url = scrapy.Field()
    latest_date = scrapy.Field()
    spider_name = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class ChnSzseListItem(scrapy.Item):
    company_code = scrapy.Field()
    company_unique_code = scrapy.Field()
    company_abbreviation = scrapy.Field()
    company_name = scrapy.Field()
    country_code = scrapy.Field()
    industry = scrapy.Field()
    web_site = scrapy.Field()
    download_url = scrapy.Field()

class SzseCollectionItem1(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    company_code = scrapy.Field()
    company_name = scrapy.Field()
    company_short_name = scrapy.Field()
    country_code = scrapy.Field()
    exchange_market_code = scrapy.Field()
    market_type = scrapy.Field()
    security_code = scrapy.Field()
    company_list_url = scrapy.Field()
    spider_name = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class SzseCollectionItem2(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    company_code = scrapy.Field()
    company_name = scrapy.Field()
    company_short_name = scrapy.Field()
    country_code = scrapy.Field()
    exchange_market_code = scrapy.Field()
    market_type = scrapy.Field()
    security_code = scrapy.Field()
    company_list_url = scrapy.Field()
    spider_name = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class SzseCollectionItem3(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    company_code = scrapy.Field()
    company_name = scrapy.Field()
    company_short_name = scrapy.Field()
    country_code = scrapy.Field()
    exchange_market_code = scrapy.Field()
    market_type = scrapy.Field()
    security_code = scrapy.Field()
    company_list_url = scrapy.Field()
    spider_name = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

# class SzseSharesA(scrapy.Item):
#     company_code = scrapy.Field()
#     company_unique = scrapy.Field()
#     shrot_name = scrapy.Field()
#     unqie_code_B = scrapy.Field()
#     abbreviation_B = scrapy.Field()
#     listing_date_B = scrapy.Field()
#     total_stock_B = scrapy.Field()
#     circulating_stock_B = scrapy.Field()
#     industry = scrapy.Field()
#     info_url = scrapy.Field()
#
# class SzseSharesB(scrapy.Item):
#     company_code = scrapy.Field()
#     unique_code_A = scrapy.Field()
#     jumpstart_A = scrapy.Field()
#     unique_code_B = scrapy.Field()
#     jumpstart_B = scrapy.Field()
#     listing_date_B = scrapy.Field()
#     total_B = scrapy.Field()
#     lt_circulation_B = scrapy.Field()
#     sector = scrapy.Field()
#     details = scrapy.Field()
#
# class SzseSharesC(scrapy.Item):
#     company_code = scrapy.Field()
#     incorporation_code = scrapy.Field()
#     incorporation_name = scrapy.Field()
#     A_unique_code = scrapy.Field()
#     A_shares = scrapy.Field()
#     A_listing_date = scrapy.Field()
#     B_unique_code = scrapy.Field()
#     B_shares = scrapy.Field()
#     B_listing_date = scrapy.Field()
#     whole_details = scrapy.Field()


class SecretaryItem(scrapy.Item):
    country_code = scrapy.Field()
    company_code =scrapy.Field()
    classification_id = scrapy.Field()
    correlation_id = scrapy.Field()
    header = scrapy.Field()
    header_sort = scrapy.Field()
    content = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class SecretaryTwoItem(scrapy.Item):
    country_code = scrapy.Field()
    company_code =scrapy.Field()
    classification_id = scrapy.Field()
    correlation_id = scrapy.Field()
    header = scrapy.Field()
    header_sort = scrapy.Field()
    content = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class SecretaryThreeItem(scrapy.Item):
    country_code = scrapy.Field()
    company_code =scrapy.Field()
    classification_id = scrapy.Field()
    correlation_id = scrapy.Field()
    header = scrapy.Field()
    header_sort = scrapy.Field()
    content = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class RegItem(scrapy.Item):
    country_code = scrapy.Field()
    company_code = scrapy.Field()
    classification_id = scrapy.Field()
    correlation_id = scrapy.Field()
    header = scrapy.Field()
    header_sort = scrapy.Field()
    content = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class DisItem(scrapy.Item):
    country_code = scrapy.Field()
    company_code = scrapy.Field()
    classification_id = scrapy.Field()
    correlation_id = scrapy.Field()
    header = scrapy.Field()
    header_sort = scrapy.Field()
    content = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class StockItem(scrapy.Item):
    country_code = scrapy.Field()
    company_code = scrapy.Field()
    classification_id = scrapy.Field()
    correlation_id = scrapy.Field()
    header = scrapy.Field()
    header_sort = scrapy.Field()
    content = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class CompanyInfoItem(scrapy.Item):
    gsqc = scrapy.Field()
    ywqc = scrapy.Field()
    zcdz = scrapy.Field()
    agdm = scrapy.Field()
    agjc = scrapy.Field()
    agssrq = scrapy.Field()
    agzgb = scrapy.Field()
    agltgb = scrapy.Field()
    dldq = scrapy.Field()
    shi = scrapy.Field()
    http = scrapy.Field()
    bgdm = scrapy.Field()
    bgjc = scrapy.Field()
    bgssrq = scrapy.Field()
    bgzgb = scrapy.Field()
    bgltgb = scrapy.Field()
    sheng = scrapy.Field()
    sshymc = scrapy.Field()
    company_code = scrapy.Field()
    security_code = scrapy.Field()
