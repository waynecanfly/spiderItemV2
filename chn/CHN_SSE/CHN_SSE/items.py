# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class ChnSseItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass
#
#
# class CompanyDataSourceItem(scrapy.Item):
#
#     company_id = scrapy.Field()
#     company_abbreviation = scrapy.Field()
#     # exchange_market_code = scrapy.Field()
#     country_code = scrapy.Field()
#     security_code = scrapy.Field()
#     latest_url = scrapy.Field()
#     latest_date = scrapy.Field()
#     spider_name = scrapy.Field()
#     # market_type = scrapy.Field()
#     # mark = scrapy.Field()
#     gmt_create = scrapy.Field()
#     user_create = scrapy.Field()
#
# class CompanyInFoItem(scrapy.Item):
#
#     exchange_market_code = scrapy.Field()
#     type_market = scrapy.Field()
#     customized_code = scrapy.Field()
#     company_name = scrapy.Field()
#     short_name = scrapy.Field()
#     current_code = scrapy.Field()
#     before_code = scrapy.Field()
#     listing_date = scrapy.Field()
#     market_type = scrapy.Field()
#     company_code = scrapy.Field()
#     stock_code = scrapy.Field()
#     # date_listing = scrapy.Field()
#     bond_short_name = scrapy.Field()
#     bond_code = scrapy.Field()
#     company_short_name_zh = scrapy.Field()
#     company_short_name_en = scrapy.Field()
#     company_full_name_zh = scrapy.Field()
#     company_full_name_en = scrapy.Field()
#     registered_address = scrapy.Field()
#     mailing_address = scrapy.Field()
#     zip_code = scrapy.Field()
#     legal_representative = scrapy.Field()
#     # secretary_name = scrapy.Field()
#     email = scrapy.Field()
#     phone = scrapy.Field()
#     web = scrapy.Field()
#     CSRC_industry = scrapy.Field()
#     sse_industry = scrapy.Field()
#     affiliation = scrapy.Field()
#     status = scrapy.Field()
#     sample_stocks = scrapy.Field()
#     listed_abroad = scrapy.Field()
#     listing_place = scrapy.Field()
#     country_code = scrapy.Field()
#     gmt_create = scrapy.Field()
#     user_create = scrapy.Field()
#
# class SecretaryName(scrapy.Item):
#     country_code = scrapy.Field()
#     company_code = scrapy.Field()
#     display_label = scrapy.Field()
#     information = scrapy.Field()
#     gmt_create = scrapy.Field()
#     user_create = scrapy.Field()
#
# class ListingDateIndex(scrapy.Item):
#     country_code = scrapy.Field()
#     company_code = scrapy.Field()
#     display_label = scrapy.Field()
#     information = scrapy.Field()
#     gmt_create = scrapy.Field()
#     user_create = scrapy.Field()
#
# class ListingDateLast(scrapy.Item):
#     country_code = scrapy.Field()
#     company_code = scrapy.Field()
#     display_label = scrapy.Field()
#     information = scrapy.Field()
#     gmt_create = scrapy.Field()
#     user_create = scrapy.Field()
#
# class SeniorInfo(scrapy.Item):
#     company_code = scrapy.Field()
#     appointment_time = scrapy.Field()
#     fuction = scrapy.Field()
#     name = scrapy.Field()
#     gmt_create = scrapy.Field()
#     user_create = scrapy.Field()
#
# class SpcialItem(scrapy.Item):
#     company_code = scrapy.Field()
#     spcial_date = scrapy.Field()
#     spcial_listing = scrapy.Field()
#     curbonus = scrapy.Field()
#     openprice = scrapy.Field()
#     highprice = scrapy.Field()
#     lowprice = scrapy.Field()
#     closeprice = scrapy.Field()
#     tradingvol = scrapy.Field()
#     tradingamt = scrapy.Field()
#     exchangerate = scrapy.Field()
#
# class InitialItem(scrapy.Item):
#     company_code = scrapy.Field()
#     issued_number = scrapy.Field()
#     issued_price = scrapy.Field()
#     issued_date = scrapy.Field()
#     issued_total = scrapy.Field()
#     issued_weighting = scrapy.Field()
#     issued_diminish = scrapy.Field()
#     issued_way = scrapy.Field()
#     issued_underwriter = scrapy.Field()
#     get_rate = scrapy.Field()
#
# class SeoItem(scrapy.Item):
#     company_code = scrapy.Field()
#     seo_number = scrapy.Field()
#     seo_price = scrapy.Field()
#     seo_date = scrapy.Field()
#     distribution_price = scrapy.Field()
#     seo_mode = scrapy.Field()
#     seo_way = scrapy.Field()
#     seo_undderwrietr = scrapy.Field()
#     seo_recommender = scrapy.Field()
#     seo_contractor = scrapy.Field()
#     get_rate = scrapy.Field()
#     shareholder_rate = scrapy.Field()
#
# class AllocationItem(scrapy.Item):
#     company_code = scrapy.Field()
#     registration_date = scrapy.Field()
#     exclusive_trading = scrapy.Field()
#     allocation_price = scrapy.Field()
#     allocation_rate = scrapy.Field()
#     start_date_pay = scrapy.Field()
#     end_date_pay = scrapy.Field()
#     actual_allotment = scrapy.Field()
#     allocation_listing_date = scrapy.Field()
#
# class StructureCapItem(scrapy.Item):
#     company_code = scrapy.Field()
#     data_time = scrapy.Field()
#     limited_circulating_shares = scrapy.Field()
#     special_voting_unit = scrapy.Field()
#     unlimited_circulating_shares = scrapy.Field()
#     unlimited_circulating_shares_A = scrapy.Field()
#     domestic_listed_stock_B = scrapy.Field()
#     domestic_listed_stock_total = scrapy.Field()
#
# class StructureStrItem(scrapy.Item):
#     company_code = scrapy.Field()
#     change_date = scrapy.Field()
#     change_reason = scrapy.Field()
#     change_shares = scrapy.Field()
#
# class BonusItem(scrapy.Item):
#     company_code = scrapy.Field()
#     bonus_registration_date = scrapy.Field()
#     bonus_equity_total = scrapy.Field()
#     bonus_deduction_date = scrapy.Field()
#     bonus_close_price = scrapy.Field()
#     bonus_quotation = scrapy.Field()
#     bonus_per_share = scrapy.Field()
#
# class DeliveryItem(scrapy.Item):
#     company_code = scrapy.Field()
#     delivery_registration_date = scrapy.Field()
#     equity_total = scrapy.Field()
#     exclusion_date = scrapy.Field()
#     red_stock_listing_date = scrapy.Field()
#     announcement_date = scrapy.Field()
#     share_delivery_ratio = scrapy.Field()
#
#
class SseFileDataItem(scrapy.Item):
    report_id = scrapy.Field()
    country_code = scrapy.Field()
    exchange_market_code = scrapy.Field()
    company_code = scrapy.Field()
    security_code = scrapy.Field()
    fiscal_year = scrapy.Field()
    quarterly_type = scrapy.Field()
    disclosure_date = scrapy.Field()
    file_original_title = scrapy.Field()
    doc_source_url = scrapy.Field()
    doc_local_path = scrapy.Field()
    doc_type = scrapy.Field()
    md5 = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class SseFileData2Item(scrapy.Item):
    report_id = scrapy.Field()
    country_code = scrapy.Field()
    exchange_market_code = scrapy.Field()
    company_code = scrapy.Field()
    security_code = scrapy.Field()
    fiscal_year = scrapy.Field()
    quarterly_type = scrapy.Field()
    disclosure_date = scrapy.Field()
    file_original_title = scrapy.Field()
    doc_source_url = scrapy.Field()
    doc_local_path = scrapy.Field()
    doc_type = scrapy.Field()
    md5 = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class AddCompanyMarketItem(scrapy.Item):
    country_code = scrapy.Field()
    exchange_market_code = scrapy.Field()
    security_code = scrapy.Field()
    company_code = scrapy.Field()
    display_label = scrapy.Field()
    information = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

#
#
# class MarketTypeItem(scrapy.Item):
#     company_abbreviation_A = scrapy.Field()
#     company_abbreviation_B = scrapy.Field()
#     security_code = scrapy.Field()
#     abbreviation_code = scrapy.Field()
#     company_listing_date = scrapy.Field()
#     market_type = scrapy.Field()
#
#     company_code = scrapy.Field()
#     country_code = scrapy.Field()
#     gmt_create = scrapy.Field()
#     user_create = scrapy.Field()
#
#
# class InfoDetailItem(scrapy.Item):
#     unique_code = scrapy.Field()
#     company_code = scrapy.Field()
#     stock_code = scrapy.Field()
#     bond_short_name = scrapy.Field()
#     bond_code = scrapy.Field()
#     company_short_name_zh = scrapy.Field()
#     company_short_name_en = scrapy.Field()
#     company_full_name_zh = scrapy.Field()
#     company_full_name_en = scrapy.Field()
#     registered_address = scrapy.Field()
#     mailing_address = scrapy.Field()
#     zip_code = scrapy.Field()
#     legal_representative = scrapy.Field()
#     email = scrapy.Field()
#     phone = scrapy.Field()
#     web = scrapy.Field()
#     CSRC_industry = scrapy.Field()
#     sse_industry = scrapy.Field()
#     affiliation = scrapy.Field()
#     status = scrapy.Field()
#     sample_stocks = scrapy.Field()
#     listed_abroad = scrapy.Field()
#     listing_place = scrapy.Field()
#     exchange_market_code = scrapy.Field()
#
# class EquityStructure(scrapy.Item):
#     company_code = scrapy.Field()
#     classification_id = scrapy.Field()
#     # correlation_id = scrapy.Field()
#     # header_sort = scrapy.Field()
#     gmt_create = scrapy.Field()
#     user_create = scrapy.Field()
#     result = scrapy.Field()
#
# class EquityChange(scrapy.Item):
#     company_code = scrapy.Field()
#     classification_id = scrapy.Field()
#     # correlation_id = scrapy.Field()
#     # header_sort = scrapy.Field()
#     gmt_create = scrapy.Field()
#     user_create = scrapy.Field()
#     result = scrapy.Field()
#
# class Executive(scrapy.Item):
#     company_code = scrapy.Field()
#     classification_id = scrapy.Field()
#     gmt_create = scrapy.Field()
#     user_create = scrapy.Field()
#     result = scrapy.Field()
#
# class Bonus(scrapy.Item):
#     company_code = scrapy.Field()
#     classification_id = scrapy.Field()
#     gmt_create = scrapy.Field()
#     user_create = scrapy.Field()
#     result = scrapy.Field()
#
# class Delivery(scrapy.Item):
#     company_code = scrapy.Field()
#     classification_id = scrapy.Field()
#     gmt_create = scrapy.Field()
#     user_create = scrapy.Field()
#     result = scrapy.Field()

class CompanyListItem(scrapy.Item):
    company_code = scrapy.Field()
    company_short_name = scrapy.Field()
    abbreviation = scrapy.Field()
    country_code = scrapy.Field()
    exchange_market_code = scrapy.Field()
    market_type = scrapy.Field()
    security_code = scrapy.Field()
    company_list_url = scrapy.Field()
    ipo_date = scrapy.Field()
    is_batch = scrapy.Field()
    spider_name = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

""" 新表 """
class SampleInfoItem(scrapy.Item):
    """ 公司基本信息 """
    country_code = scrapy.Field()
    exchange_market_code = scrapy.Field()
    security_code = scrapy.Field()
    company_code = scrapy.Field()
    display_label = scrapy.Field()
    information = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class MSXXNameItem(scrapy.Item):
    """ 董事会秘书姓名 """
    country_code = scrapy.Field()
    exchange_market_code = scrapy.Field()
    security_code = scrapy.Field()
    company_code = scrapy.Field()
    display_label = scrapy.Field()
    information = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class AGSSRDateFirstItem(scrapy.Item):
    """ 上市日A """
    country_code = scrapy.Field()
    exchange_market_code = scrapy.Field()
    security_code = scrapy.Field()
    company_code = scrapy.Field()
    display_label = scrapy.Field()
    information = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class BGSSRDateLastItem(scrapy.Item):
    """ 上市日B """
    country_code = scrapy.Field()
    exchange_market_code = scrapy.Field()
    security_code = scrapy.Field()
    company_code = scrapy.Field()
    display_label = scrapy.Field()
    information = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class AGFHItem(scrapy.Item):
    """ 分红 A股 """
    country_code = scrapy.Field()
    exchange_market_code = scrapy.Field()
    security_code = scrapy.Field()
    company_code = scrapy.Field()
    classification_id = scrapy.Field()
    correlation_id = scrapy.Field()
    header = scrapy.Field()
    header_sort = scrapy.Field()
    content = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class BGFHItem(scrapy.Item):
    """ 分红 B股 """
    country_code = scrapy.Field()
    exchange_market_code = scrapy.Field()
    security_code = scrapy.Field()
    company_code = scrapy.Field()
    classification_id = scrapy.Field()
    correlation_id = scrapy.Field()
    header = scrapy.Field()
    header_sort = scrapy.Field()
    content = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class AGSGItem(scrapy.Item):
    """ 送股 A股 """
    country_code = scrapy.Field()
    exchange_market_code = scrapy.Field()
    security_code = scrapy.Field()
    company_code = scrapy.Field()
    classification_id = scrapy.Field()
    correlation_id = scrapy.Field()
    header = scrapy.Field()
    header_sort = scrapy.Field()
    content = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class BGSGItem(scrapy.Item):
    """ 送股 B股 """
    country_code = scrapy.Field()
    exchange_market_code = scrapy.Field()
    security_code = scrapy.Field()
    company_code = scrapy.Field()
    classification_id = scrapy.Field()
    correlation_id = scrapy.Field()
    header = scrapy.Field()
    header_sort = scrapy.Field()
    content = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class EquityChangeItem(scrapy.Item):
    """ 股本变动 """
    country_code = scrapy.Field()
    exchange_market_code = scrapy.Field()
    security_code = scrapy.Field()
    company_code = scrapy.Field()
    classification_id = scrapy.Field()
    correlation_id = scrapy.Field()
    header = scrapy.Field()
    header_sort = scrapy.Field()
    content = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class EquityStructureItem(scrapy.Item):
    """ 股本结构 """
    country_code = scrapy.Field()
    exchange_market_code = scrapy.Field()
    security_code = scrapy.Field()
    company_code = scrapy.Field()
    classification_id = scrapy.Field()
    correlation_id = scrapy.Field()
    header = scrapy.Field()
    header_sort = scrapy.Field()
    content = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()


class SeniorManagementItem(scrapy.Item):
    """ 高管人员 """
    country_code = scrapy.Field()
    exchange_market_code = scrapy.Field()
    security_code = scrapy.Field()
    company_code = scrapy.Field()
    classification_id = scrapy.Field()
    correlation_id = scrapy.Field()
    header = scrapy.Field()
    header_sort = scrapy.Field()
    content = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class FinancingSituationAFirst(scrapy.Item):
    """ 筹资情况 """
    country_code = scrapy.Field()
    exchange_market_code = scrapy.Field()
    security_code = scrapy.Field()
    company_code = scrapy.Field()
    classification_id = scrapy.Field()
    correlation_id = scrapy.Field()
    header = scrapy.Field()
    header_sort = scrapy.Field()
    content = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class FinancingSituationAad(scrapy.Item):
    """ 筹资情况 """
    country_code = scrapy.Field()
    exchange_market_code = scrapy.Field()
    security_code = scrapy.Field()
    company_code = scrapy.Field()
    classification_id = scrapy.Field()
    correlation_id = scrapy.Field()
    header = scrapy.Field()
    header_sort = scrapy.Field()
    content = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()

class FinancingSituationSpecial(scrapy.Item):
    """ 筹资情况 """
    country_code = scrapy.Field()
    exchange_market_code = scrapy.Field()
    security_code = scrapy.Field()
    company_code = scrapy.Field()
    classification_id = scrapy.Field()
    correlation_id = scrapy.Field()
    header = scrapy.Field()
    header_sort = scrapy.Field()
    content = scrapy.Field()
    gmt_create = scrapy.Field()
    user_create = scrapy.Field()
