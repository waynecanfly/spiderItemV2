

class Company:
    # def __init__(self, company_code, unique_code, company_name, company_short_name, security_code, country_code, ipo_date, info_disclosure_id, download_link, market_type, exchange_market_code):
    def __init__(self,  company_code, unique_code, market_company_code, company_name, company_short_name, country_code, info_disclosure_id, download_link, exchange_market_code, market_type=''):
        self.company_code = company_code
        self.unique_code = unique_code
        self.market_company_code = market_company_code
        self.company_name = company_name
        self.company_short_name = company_short_name
        self.country_code = country_code
        self.market_type = market_type


        self.download_link = download_link if download_link is not None else '' \
                                                                             ''
        self.exchange_market_code = exchange_market_code

        self.info_disclosure_id = '' # 中国的把交易所上的公司码作为信息披露码


        # 默认为空 无值的

        self.name_en = ''

        self.original_industry_describe = ''
        self.opd_sector_code = ''
        self.opd_industry_code = ''
        self.gics_sector_code = ''
        self.gics_industry_group_code = ''
        self.csrc_code = ''  # 暂时没有

        self.country_code_origin = ''  # 没有
        self.established_date = ''  # 没有
        self.isin = ''    # 没有
        self.status = ''
        # self.delist_date = ''  # 移到证券
        self.website_url = ''


        self.security_box = []


class Security:
    def __init__(self, unique_code, company_code, name_origin, market_type, security_code, security_type, equity_type, country_code_listed, exchange_market_code, ipo_date, status, delist_date):
        self.unique_code = unique_code
        self.company_code = company_code
        self.name_origin = name_origin
        self.market_type = market_type
        self.security_code = security_code
        self.security_type = security_type
        self.equity_type = equity_type
        self.country_code_listed = country_code_listed
        self.exchange_market_code = exchange_market_code
        self.ipo_date = ipo_date
        self.status = status
        self.delist_date = delist_date
