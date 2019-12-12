#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
import traceback

from cleaning.chn_company import dbtools
from cleaning.hkg_company.container import Company, Security
from cleaning.hkg_company.raw_info_label import marked_info_label


def get_base_info():
    splider_company_box = []

    base_info_sql = "SELECT company_code, unique_code, company_short_name, country_code, exchange_market_code, security_code, security_type from company_base_info_hkg where country_code='hkg' and security_type in ('Equity', 'REITs')"
    base_info_list = dbtools.query_common(base_info_sql)

    for b in base_info_list:
        splider_company_box.append(Company(b[0], b[1], b[2], b[3], b[4], b[5], b[6]))

    return splider_company_box


def get_security_info():
    splider_security_box = []

    security_info_sql = "select company_code, unique_code, company_short_name, country_code, exchange_market_code, security_code, security_type from company_base_info_hkg where country_code='hkg' and security_type in ('Equity', 'REITs')"
    security_info_list = dbtools.query_common(security_info_sql)
    for s in security_info_list:
        splider_security_box.append(Security(s[0], s[1], s[2], s[5], s[6], s[3], s[4]))

    return splider_security_box


def get_db_raw_info():
    raw_info_map = {}
    aim_label_box = []
    for aim_label_list in marked_info_label.values():
        aim_label_box += aim_label_list
    condition = " where display_label in ('{}')".format("','".join(aim_label_box))

    raw_info_sql = 'select unique_code, display_label, information, gmt_create from company_raw_info_20191126' + condition
    # print(raw_info_sql)
    raw_info = dbtools.query_common(raw_info_sql)
    for info in raw_info:
        unique_code = info[0]
        label = info[1]
        value = info[2]
        create_time = info[3]
        if unique_code not in raw_info_map:
            raw_info_map[unique_code] = {}
        if label not in raw_info_map[unique_code]:
            raw_info_map[unique_code][label] = {}
        raw_info_map[unique_code][label][create_time] = value

    return raw_info_map


def clear_label(label):
    if label is None:
        return ''
    return re.sub('\s|-|/|,', '', label)


def get_unlisted_status():
    delist_info = {}
    delist_list_sql = "SELECT security_code, status, delisting_date FROM `company_listing_status_hkg`"
    result = dbtools.query_common(delist_list_sql)
    for r in result:
        delist_info[r[0]] = [int(r[1]), r[2]]
    return delist_info


def get_stander_industry_map():
    stander_industry_map = {}
    map_sql = "SELECT sector_industry_key,opd_sector_code,opd_industry_code,gics_sector_code,gics_industry_group_code FROM opd_sector_relationship WHERE country_code = 'hkg'"
    result = dbtools.query_common(map_sql)
    for r in result:
        original_describe = clear_label(r[0])
        stander_industry_map[original_describe] = [r[1], r[2], r[3], r[4]]

    return stander_industry_map


def gen_other_company_info(base_info_company_box):
    raw_info_map = get_db_raw_info()
    stander_industry_map = get_stander_industry_map()

    for company in base_info_company_box:
        try:
            # 英文名称、网址、行业信息
            for label in raw_info_map[company.company_code].keys():
                if label in marked_info_label['name_en']:
                    date_list = raw_info_map[company.company_code][label].keys()
                    company.name_en = raw_info_map[company.company_code][label][max(date_list)]
                elif label in marked_info_label['website_url']:
                    date_list = raw_info_map[company.company_code][label].keys()
                    company.website_url = raw_info_map[company.company_code][label][max(date_list)]
                elif label in marked_info_label['market_type']:
                    date_list = raw_info_map[company.company_code][label].keys()
                    company.market_type = raw_info_map[company.company_code][label][max(date_list)]
                elif label in marked_info_label['isin']:
                    date_list = raw_info_map[company.company_code][label].keys()
                    company.isin = raw_info_map[company.company_code][label][max(date_list)]
                elif label in marked_info_label['place_of_incorporation']:
                    date_list = raw_info_map[company.company_code][label].keys()
                    company.registered_address = raw_info_map[company.company_code][label][max(date_list)]
                elif label in marked_info_label['principal_office']:
                    date_list = raw_info_map[company.company_code][label].keys()
                    company.office_address = raw_info_map[company.company_code][label][max(date_list)]
                elif label in marked_info_label['industry']:
                    date_list = raw_info_map[company.company_code][label].keys()
                    original_industry = raw_info_map[company.company_code][label][max(date_list)]
                    company.original_industry_describe = original_industry
                    stander_industry = stander_industry_map.get(clear_label(original_industry), None)
                    if stander_industry is not None:
                        company.opd_sector_code = stander_industry[0]
                        company.opd_industry_code = stander_industry[1]
                        company.gics_sector_code = stander_industry[2]
                        company.gics_industry_group_code = stander_industry[3]
        except:
            excepttext = traceback.format_exc()
            print(excepttext)
            print('---------------------------------------- ' + company.unique_code)

    return base_info_company_box


def gen_other_security_info(base_info_security_box):
    raw_info_map = get_db_raw_info()
    unlisted_status_info = get_unlisted_status()

    for security in base_info_security_box:
        try:
            if security.security_code in unlisted_status_info.keys():
                security.status = unlisted_status_info[security.security_code][0]
                security.delist_date = unlisted_status_info[security.security_code][1]
            for label in raw_info_map[security.company_code].keys():
                if label in marked_info_label['listing_date']:
                    date_list = raw_info_map[security.company_code][label].keys()
                    security.listing_date = raw_info_map[security.company_code][label][max(date_list)]
                elif label in marked_info_label['market_type']:
                    date_list = raw_info_map[security.company_code][label].keys()
                    security.market_type = raw_info_map[security.company_code][label][max(date_list)]
        except:
            excepttext = traceback.format_exc()
            print(excepttext)
            print('---------------------------------------- ' + security.unique_code)

    return base_info_security_box


def get_exist_company_and_security():
    exist_company_map = {}
    exist_security_map = {}
    company_sql = """select company_code, unique_code, name_origin, company_short_name, security_code, country_code_listed, ipo_date, info_disclosure_id, download_link, market_type, exchange_market_code,
          name_en, opd_sector_code, opd_industry_code, gics_sector_code, gics_industry_group_code, status, delist_date, website_url from company"""
    result = dbtools.query_common(company_sql)
    for r in result:
        company = Company(r[0], r[1], r[3], r[5], r[10], r[4])
        company.name_en = r[11]
        company.opd_sector_code = r[12]
        company.opd_industry_code = r[13]
        company.gics_sector_code = r[14]
        company.gics_industry_group_code = r[15]
        # company.status = r[16]
        # company.delist_date = r[17]
        company.website_url = r[18]
        exist_company_map[company.company_code] = company

    # 获取证券表信息
    security_sql = "select company_code, unique_code, name_origin, market_type, security_code, security_type, country_code_listed, exchange_market_code, listing_date, STATUS, delisting_date from security_hkg where country_code='HKG'"
    result = dbtools.query_common(security_sql)
    for s in result:
        security = Security(s[0], s[1], s[2], s[4], s[5], s[6], s[7])
        security.market_type = s[3]
        security.listing_date = s[8]
        security.delist_date = s[10]
        security.status = s[9]
        exist_security_map[security.company_code] = security

    return exist_company_map, exist_security_map


def compare(new_download_company_box, exist_company_map, new_download_security_box, exist_security_map):
    new_company_box = []
    modify_company_box = []
    modify_security_box = []
    new_security_box = []
    for new_company in new_download_company_box:
        exist_company = exist_company_map.get(new_company.company_code, None)
        if exist_company is not None:
            j2 = exist_company.company_short_name != new_company.company_short_name
            j6 = exist_company.name_en != new_company.name_en
            j7 = exist_company.opd_sector_code != new_company.opd_sector_code
            j8 = exist_company.opd_industry_code != new_company.opd_industry_code
            j9 = exist_company.gics_sector_code != new_company.gics_sector_code
            j10 = exist_company.gics_industry_group_code != new_company.gics_industry_group_code
            j11 = exist_company.market_type != new_company.market_type
            j13 = exist_company.website_url != new_company.website_url
            if j2 or j6 or j7 or j8 or j9 or j10 or j11 or j13:
                modify_company_box.append(new_company)
        else:
            new_company_box.append(new_company)

    for new_security in new_download_security_box:
        exist_security = exist_security_map.get(new_security.company_code, None)
        if exist_security is not None:
            j1 = exist_security.name_origin != new_security.name_origin
            j2 = exist_security.market_type != new_security.market_type
            j3 = exist_security.security_type != new_security.security_type
            if j1 or j2 or j3:
                modify_security_box.append(new_security)
        else:
            new_security_box.append(new_security)

    return new_company_box, modify_company_box, new_security_box, modify_security_box


def gen_insert_value_box(new_company_box, new_security_box):
    company_values_box = []
    security_value_box = []
    for new_c in new_company_box:
        company_value = """("{company_code}", "{unique_code}", "{name_en}", "{company_short_name}", "{security_code}", "{original_industry_describe}", "{opd_sector_code}", "{opd_industry_code}", "{gics_sector_code}", "{gics_industry_group_code}",
        "{country_code_listed}", "{country_code_origin}", "{isin}", "{exchange_market_code}","{website_url}","{registered_address}", "{office_address}", {gmt_create}, "{user_create}")""".format(
            company_code=new_c.company_code,
            unique_code=new_c.unique_code,
            name_en=new_c.name_en,
            company_short_name=new_c.company_short_name,
            security_code=new_c.security_code,
            original_industry_describe=new_c.original_industry_describe,
            opd_sector_code=new_c.opd_sector_code,
            opd_industry_code=new_c.opd_industry_code,
            gics_sector_code=new_c.gics_sector_code,
            gics_industry_group_code=new_c.gics_industry_group_code,
            country_code_listed=new_c.country_code,
            country_code_origin=new_c.country_code,
            isin=new_c.isin,
            exchange_market_code=new_c.exchange_market_code,
            website_url=new_c.website_url,
            registered_address=new_c.registered_address,
            office_address=new_c.office_address,
            gmt_create='now()',
            user_create='program_auto'
        )

        company_values_box.append(company_value)

    for security in new_security_box:
        security_value = """("{company_code}", "{unique_code}", "{name_origin}", "{market_type}", "{security_code}", "{security_type}", "{country_code_listed}", "{exchange_market_code}", "{listing_date}", {status}, "{delist_date}", 
        "{user_create}", {gmt_create})""".format(
            unique_code=security.unique_code,
            company_code=security.company_code,
            name_origin=security.name_origin,
            market_type=security.market_type,
            security_code=security.security_code,
            security_type=security.security_type,
            country_code_listed=security.country_code_listed,
            exchange_market_code=security.exchange_market_code,
            listing_date=security.listing_date,
            status=security.status,
            delist_date=security.delist_date,
            gmt_create='now()',
            user_create='program_auto'
        )
        security_value_box.append(security_value)

    return company_values_box, security_value_box


def insert_new_to_db(new_company_box, new_security_box):
    if len(new_company_box) == 0:
        return True

    company_values_box, security_values_box = gen_insert_value_box(new_company_box, new_security_box)

    company_insert_sql = "INSERT INTO company_hkg(company_code, unique_code, name_en, company_short_name, security_code, original_industry_describe, opd_sector_code, opd_industry_code, gics_sector_code, gics_industry_group_code, country_code_listed, country_code_origin, isin,exchange_market_code, website_url,registered_address, office_address, gmt_create, user_create) VALUES {values}"
    company_insert_sql = company_insert_sql.format(values=', '.join(company_values_box))
    print(company_insert_sql)
    dbtools.query_common(company_insert_sql)

    # security_insert_sql = "INSERT INTO security_hkg(company_code, unique_code, name_origin, market_type, security_code, security_type, country_code_listed, exchange_market_code, listing_date, status, delist_date, user_create, gmt_create) VALUES {values}"
    # security_insert_sql = security_insert_sql.format(values=', '.join(security_values_box))
    # print(security_insert_sql)
    # dbtools.query_common(security_insert_sql)


def process():
    # 在baseinfo中获取公司信息，生成采集公司对象列表
    new_download_company_box = get_base_info()
    # 生成采集证券对象列表
    new_download_security_box = get_security_info()

    # 通过rawinfo表清洗出公司其它详细信息
    new_download_company_box = gen_other_company_info(new_download_company_box)
    # 通过rawinfo表清洗出证券其它详细信息
    new_download_security_box = gen_other_security_info(new_download_security_box)

    # # 入库
    insert_new_to_db(new_download_company_box, new_download_security_box)


if __name__ == '__main__':
    process()

