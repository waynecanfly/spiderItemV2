#! /usr/bin/env python
# -*- coding: utf-8 -*-

class Company:
    def __init__(self, company_code, unique_code, company_short_name, country_code, exchange_market_code, security_code, security_type):
        self.company_code = company_code
        self.unique_code = unique_code
        self.company_short_name = company_short_name
        self.security_code = security_code
        self.country_code = country_code
        self.exchange_market_code = exchange_market_code
        self.security_type = security_type
        self.name_origin = '' # 没有
        self.name_en = ''

        # 市场类型 MAIN GEM
        self.market_type = ''
        self.original_industry_describe = ''
        # 所属OPD行业一级分类
        self.opd_sector_code = ''
        # 所属OPD行业二级分类
        self.opd_industry_code = '' # 没有
        # 所属GICS一级行业
        self.gics_sector_code = ''
        # 所属GICS二级行业
        self.gics_industry_group_code = ''
        self.csrc_code = ''  # 暂时没有
        self.country_code_listed = 'HKG'
        self.country_code_origin = ''  # 未找到，暂时留空
        # 公司成立日期
        self.established_date = ''
        # 电子信息披露标识
        self.info_disclosure_id = ''
        # 国际证券识别编号体系
        self.isin = ''
        # 公司状态
        self.status = ''
        # 退市日期
        self.delisted_date = ''
        # 公司官网
        self.website_url = ''
        # 公司信息下载地址
        self.download_link = ''
        # 证券列表
        # self.security_box = []


class Security:
    def __init__(self, company_code, unique_code, name_origin, security_code, security_type, country_code_listed, exchange_market_code):
        self.company_code = company_code
        self.unique_code = unique_code
        self.name_origin = name_origin
        self.market_type = ''
        self.security_code = security_code
        self.security_type = security_type
        self.country_code_listed = country_code_listed
        self.listing_date = ''
        self.exchange_market_code = exchange_market_code
        self.status = 1
        self.delist_date = ''
