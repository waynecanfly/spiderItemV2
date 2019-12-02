import re
import traceback

import pymysql

from cleaning.chn_company import dbtools
from cleaning.chn_company.container import Company, Security
from cleaning.chn_company.industry_pdf_parser import get_industry_dict
from cleaning.chn_company.raw_info_lable import marked_info_label


def get_base_info():
    splider_company_box = []
    exist_company = []

    base_info_sql = "SELECT company_code, unique_code, market_company_code, company_name, company_short_name, country_code, info_disclosure_id, download_link, exchange_market_code, market_type FROM company_base_info WHERE country_code='chn'"
    base_info_list = dbtools.query_common(base_info_sql)

    for b in base_info_list:
        c = Company(b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[7], b[8], b[9])
        if c.unique_code not in exist_company:
            splider_company_box.append(c)
            exist_company.append(c.unique_code)

    return splider_company_box

def get_db_raw_info():
    raw_info_map = {}
    aim_label_box = []
    for aim_label_list in marked_info_label.values():
        aim_label_box += aim_label_list
    condition = " where display_label in ('{}')".format("','".join(aim_label_box))

    raw_info_sql = 'select unique_code, display_label, information, gmt_create from company_raw_info' + condition
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

def get_unlisted_status():
    delist_info = {}
    delist_list_sql = "SELECT security_code, status, delisting_date FROM `company_listing_status`"
    result = dbtools.query_common(delist_list_sql)
    for r in result:
        delist_info [r[0]] = [int(r[1]), r[2]]
    return delist_info

def clear_label(label):
    if label is None:
        return ''
    return re.sub('、|/|\s|-|\d|[A-Za-z]', '', label)

def get_stander_industry_map():
    stander_industry_map = {}
    map_sql = "SELECT sector_industry_key,opd_sector_code,opd_industry_code,gics_sector_code,gics_industry_group_code FROM opd_sector_relationship WHERE country_code = 'chn'"
    result = dbtools.query_common(map_sql)
    for r in result:
        original_describe = clear_label(r[0])
        # print(original_describe)
        stander_industry_map[original_describe] = [r[1], r[2], r[3], r[4]]
    return stander_industry_map


def gen_other_and_security_info(new_download_company_box):

    raw_info_map = get_db_raw_info()
    unlisted_status_info = get_unlisted_status()
    csrc_industry_dict = get_industry_dict()
    # csrc_industry_dict = {}
    stander_industry_map = get_stander_industry_map()


    for company in new_download_company_box:
        if company.unique_code == 'CHNSSE601077':
            print('d')
            pass
        try:
            # 通过网站披露的信息获取公司行业信息
            csrc_industry = csrc_industry_dict.get(company.market_company_code, None)
            spider_industry = None

            # 中文全称、英文名称、网址、行业信息、获取采集行业信息
            for label in raw_info_map[company.unique_code].keys():
                # 中文全称、英文名称、网址、行业信息:
                if label in marked_info_label['name_zh']:
                    date_list = raw_info_map[company.unique_code][label].keys()
                    company.company_name = raw_info_map[company.unique_code][label][max(date_list)]
                if label in marked_info_label['name_en']:
                    date_list = raw_info_map[company.unique_code][label].keys()
                    company.name_en = raw_info_map[company.unique_code][label][max(date_list)]
                elif label in marked_info_label['website_url']:
                    date_list = raw_info_map[company.unique_code][label].keys()
                    company.website_url = raw_info_map[company.unique_code][label][max(date_list)]
                elif label in marked_info_label['industry']:
                    date_list = raw_info_map[company.unique_code][label].keys()
                    spider_industry = raw_info_map[company.unique_code][label][max(date_list)]


            # 确定最终行业信息
            company.original_industry_describe = csrc_industry if csrc_industry is not None else spider_industry
            stander_industry = stander_industry_map.get(clear_label(company.original_industry_describe), None)
            if stander_industry is not None:
                company.opd_sector_code = stander_industry[0]
                company.opd_industry_code = stander_industry[1]
                company.gics_sector_code = stander_industry[2]
                company.gics_industry_group_code = stander_industry[3]


            # a股， b 股， 科创版  一下代码过于难懂，要重写
            plate = [['a_code', 'a_ipo', 'A股'], ['b_code', 'b_ipo', 'B股'],  ['kechuang_code', 'kechuang_ipo', 'A股']]
            for p in plate:
                for l1 in marked_info_label[p[0]]:
                    is_ok = False
                    security_code_idc = raw_info_map[company.unique_code].get(l1, None)
                    if security_code_idc is not None:
                        security_code = list(security_code_idc.values())[0]

                        if security_code == '':
                            break
                        for l2 in marked_info_label[p[1]]:
                            security_ipo_dic = raw_info_map[company.unique_code].get(l2, None)
                            if security_ipo_dic is not None:
                                security_ipo = list(security_ipo_dic.values())[0]
                                # 退上市信息。 深交所没有退市日期？  有， 也在退市表中
                                status = 1
                                delist_date = ''

                                if security_code in unlisted_status_info.keys():
                                    info = unlisted_status_info[security_code]
                                    status = info[0]
                                    delist_date = info[1]
                                market_type = '主板' if '主板' in company.market_type else company.market_type
                                equity_type = p[2]
                                company.security_box.append(Security(company.unique_code, company.company_code, company.company_name,  market_type, security_code, 'Equity', equity_type, company.country_code, company.exchange_market_code, security_ipo, status, delist_date))
                                break
                    if is_ok:
                        break

            # 根据证券状态确定公司状态
            if len(company.security_box) == 0:
                raise Exception('NO SECURITY  ' + company.unique_code)
            company.status = max([x.status for x in company.security_box])

        except:
            excepttext = traceback.format_exc()
            print(excepttext)
            print('---------------------------------------- ' + company.unique_code)

    return new_download_company_box


def get_exist_company_with_security():
    # 获取公司表信息
    exist_company_map = {}
    # company_code, unique_code, security_code, company_name, company_short_name, country_code, info_disclosure_id, download_link, exchange_market_code

    sql = """SELECT company_code, unique_code, '', name_origin, company_short_name, country_code_listed, info_disclosure_id, download_link, exchange_market_code,
          name_en, opd_sector_code, opd_industry_code, gics_sector_code, gics_industry_group_code, STATUS, website_url FROM company WHERE country_code_listed='CHN'"""
    result = dbtools.query_common(sql)
    for r in result:
        company = Company(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8])
        if company.company_code == 'CHN75976':
            print('d')
            pass
        company.name_en = r[9]
        company.opd_sector_code = r[10]
        company.opd_industry_code = r[11]
        company.gics_sector_code = r[12]
        company.gics_industry_group_code = r[13]
        company.status = r[14]
        company.website_url = r[15]
        exist_company_map[company.unique_code] = company

    # 获取证券表信息
    security_sql  = "SELECT unique_code, company_code, name_origin, market_type, security_code, security_type, equity_type, country_code_listed, exchange_market_code, ipo_date, STATUS, delist_date FROM security WHERE country_code_listed = 'CHN' "
    security_result = dbtools.query_common(security_sql)
    for sr in security_result:
        s = Security(sr[0], sr[1], sr[2], sr[3], sr[4], sr[5], sr[6], sr[7], sr[8], sr[9], sr[10], sr[11])
        if s.unique_code == 'CHNSSE603489':
            print('d')
        exist_company_map[s.unique_code].security_box.append(s)

    return exist_company_map



def compare(new_download_company_box, exist_company_map):
    new_company_box = []
    new_security_box = []

    modify_company_box = []
    modify_security_box = []

    # 以下两个集合用于比较而临时建的
    new_download_security_box =[]
    exist_security_dict ={}

    for new_company in new_download_company_box:
        exist_company = exist_company_map.get(new_company.unique_code, None)
        if exist_company is not None:

            new_download_security_box += new_company.security_box
            for s in exist_company.security_box:
                exist_security_dict[s.security_code] = s

            j1 = exist_company.company_name != new_company.company_name
            j2 = exist_company.company_short_name != new_company.company_short_name
            j3 = exist_company.name_en != new_company.name_en
            j4 = exist_company.original_industry_describe != new_company.original_industry_describe
            j5 = exist_company.opd_sector_code != new_company.opd_sector_code
            j6 = exist_company.opd_industry_code != new_company.opd_industry_code
            j7 = exist_company.gics_sector_code != new_company.gics_sector_code
            j8 = exist_company.gics_industry_group_code != new_company.gics_industry_group_code
            j9 = exist_company.csrc_code != new_company.csrc_code
            j10 = exist_company.download_link != new_company.download_link
            j11 = exist_company.status != new_company.status
            j12 = exist_company.established_date != new_company.established_date
            j13 = exist_company.website_url != new_company.website_url


            if j1 or j2 or j3 or j4 or j5 or j6 or j7 or j8 or j9 or j10 or j11 or j12 or j13:
                modify_company_box.append(new_company)
        else:
            new_company_box.append(new_company)
            for new_s in new_company.security_box:
                new_security_box.append(new_s)

    # compare security
    for new_security in new_download_security_box:
        exist_security = exist_security_dict.get(new_security.security_code, None)
        if exist_security is not None:
            j1 = exist_security.delist_date != new_security.delist_date
            j2 = exist_security.ipo_date != new_security.ipo_date
            j3 = exist_security.equity_type != new_security.equity_type
            j4 = exist_security.name_origin != new_security.name_origin
            j5 = exist_security.status != new_security.status
            if j1 or j2 or j3 or j4 or j5:
                modify_security_box.append(exist_security)
        else:
            new_security_box.append(new_security)

    return new_company_box, new_security_box, modify_company_box, modify_security_box


def gen_insert_value_box(new_company_box, new_security_box):
    company_values_box = []
    security_values_box = []

    for new_c in new_company_box:
        company_value = """("{company_code}", "{unique_code}", "{name_en}", "{company_short_name}", "{original_industry_describe}", "{opd_sector_code}", "{opd_industry_code}", "{gics_sector_code}", "{gics_industry_group_code}",
                "{csrc_code}", "{country_code_listed}", "{country_code_origin}", {established_date}, "{info_disclosure_id}", "{isin}", "{exchange_market_code}",  {status}, "{website_url}", "{download_link}", {gmt_create}, "{user_create}")""".format(
            company_code=new_c.company_code,
            unique_code=new_c.unique_code,
            name_origin=new_c.company_name.replace("\"", "\\\"") if new_c.company_name is not None else new_c.company_name,
            # name_en=pymysql.escape_string(new_c.name_en),
            name_en=new_c.name_en.replace("\"", "\\\"") if new_c.company_name is not None else new_c.name_en,
            company_short_name=new_c.company_short_name,
            original_industry_describe=new_c.original_industry_describe if new_c.original_industry_describe is not None else '',
            opd_sector_code=new_c.opd_sector_code,
            opd_industry_code=new_c.opd_industry_code,
            gics_sector_code=new_c.gics_sector_code,
            gics_industry_group_code=new_c.gics_industry_group_code,
            csrc_code=new_c.csrc_code,
            country_code_listed=new_c.country_code,
            country_code_origin=new_c.country_code,
            established_date="\"{}\"".format(new_c.established_date) if new_c.established_date != '' else "null",
            info_disclosure_id=new_c.info_disclosure_id,
            isin=new_c.isin,
            status=new_c.status,
            exchange_market_code=new_c.exchange_market_code,
            website_url=new_c.website_url,
            download_link=new_c.download_link if new_c.download_link is not None else '',
            gmt_create='now()',
            user_create='program_auto'
        )
        company_values_box.append(company_value)

    for security in new_security_box:
        security_value = """("{unique_code}", "{company_code}", "{name_origin}", "{market_type}", "{security_code}", "{security_type}", "{equity_type}", "{country_code_listed}", "{exchange_market_code}", {ipo_date}, {status}, {delist_date})""".format(
            unique_code=security.unique_code,
            company_code=security.company_code,
            name_origin=security.name_origin.replace("\"", "\\\"") if security.name_origin is not None else security.name_origin,
            market_type=security.market_type,
            security_code=security.security_code,
            security_type=security.security_type,
            equity_type=security.equity_type,
            country_code_listed=security.country_code_listed,
            exchange_market_code=security.exchange_market_code,
            ipo_date="\"{}\"".format(security.ipo_date) if security.ipo_date != '' else "null",
            status=security.status,
            delist_date="\"{}\"".format(security.delist_date) if security.delist_date != '' else "null",
            gmt_create='now()',
            user_create='program_auto'
        )
        security_values_box.append(security_value)
    return company_values_box, security_values_box


def insert_new_to_db(new_company_box, new_security_box):
    if len(new_company_box)==0:
        return True

    company_values_box, security_values_box = gen_insert_value_box(new_company_box, new_security_box)

    company_insert_sql = "INSERT INTO company(company_code, unique_code, name_origin, name_en, company_short_name, original_industry_describe, opd_sector_code, opd_industry_code, gics_sector_code, gics_industry_group_code, csrc_code, country_code_listed, country_code_origin, established_date, info_disclosure_id, isin, exchange_market_code, STATUS, website_url, download_link, gmt_create, user_create) VALUES {values}"
    company_insert_sql = company_insert_sql.format(values=', '.join(company_values_box))
    print(company_insert_sql)
    dbtools.query_common(company_insert_sql)

    security_insert_sql = "INSERT INTO security(unique_code, company_code, name_origin, market_type, security_code, security_type, equity_type, country_code_listed, exchange_market_code, ipo_date, status, delist_date) VALUES {values}"
    security_insert_sql = security_insert_sql.format(values=', '.join(security_values_box))
    print(security_insert_sql)
    dbtools.query_common(security_insert_sql)



def modify_exist_info(modify_company_box, modify_security_box):
    for modify_c in modify_company_box:
        update_sql = """UPDATE company SET 
                        name_origin="{name_origin}", 
                        name_en="{name_en}", 
                        company_short_name="{company_short_name}", 
                        original_industry_describe="{original_industry_describe}",
                        opd_sector_code="{opd_sector_code}", 
                        opd_industry_code="{opd_industry_code}", 
                        gics_sector_code="{gics_sector_code}", 
                        gics_industry_group_code="{gics_industry_group_code}", 
                        csrc_code="{csrc_code}", 
                        established_date="{established_date}", 
                        status={status}, 
                        website_url="{website_url}", 
                        download_link="{download_link}", 
                        gmt_update=now(), 
                        user_update="{user_update}"
                        WHERE unique_code="{unique_code}"
                        """.format(
            name_origin=modify_c.company_name,
            name_en=modify_c.name_en,
            company_short_name=modify_c.company_short_name,
            original_industry_describe=modify_c.original_industry_describe,
            opd_sector_code=modify_c.opd_sector_code,
            opd_industry_code=modify_c.opd_industry_code,
            gics_sector_code=modify_c.gics_sector_code,
            gics_industry_group_code=modify_c.gics_industry_group_code,
            csrc_code=modify_c.csrc_code,
            established_date=modify_c.established_date,
            status=modify_c.status,
            delist_date=modify_c.delist_date,
            website_url=modify_c.website_url,
            download_link=modify_c.download_link,
            gmt_update = 'now()',
            user_update='program_auto',
            unique_code=modify_c.unique_code
        )
        print(update_sql)

        dbtools.query_common(update_sql)

    for modify_s in modify_security_box:
        update_sql = """UPDATE security SET 
                        delist_date="{delist_date}", 
                        ipo_date="{ipo_date}", 
                        equity_type="{equity_type}", 
                        name_origin="{name_origin}",
                        status="{status}"
                        gmt_update=now(), 
                        user_update="{user_update}"
                        WHERE security_code="{security_code}
                        """.format(
            delist_date=modify_s.company_name,
            ipo_date=modify_s.name_en,
            equity_type=modify_s.company_short_name,
            name_origin=modify_s.original_industry_describe,
            status=modify_s.opd_sector_code,
            gmt_update='now()',
            user_update='program_auto',
            security_code=modify_s.security_code
        )
        print(update_sql)

        dbtools.query_common(update_sql)

    return True

def process():
    # 在baseinfo中获取公司信息，生成采集公司对象列表
    new_download_company_box = get_base_info()

    # 通过rawinfo表清洗出公司其它详细信息以及公司所包含的证券信息
    new_download_company_box = gen_other_and_security_info(new_download_company_box)


    # 获取company中存量的公司信息，生成存量公司对象列表
    exist_company_map = get_exist_company_with_security()

    # 比较采集列表和存量列表。生成新增公司列表及信息更改公司列表
    new_company_box, new_security_box, modify_company_box, modify_security_box = compare(new_download_company_box, exist_company_map)

    # 入库
    insert_new_to_db(new_company_box, new_security_box)
    modify_exist_info(modify_company_box, modify_security_box)


def temp():
    sql = "SELECT source_report_id, statusid FROM fs_process_index WHERE country_code = 'CHN'"
    result = dbtools.query_opd_fdss(sql)

    id_map = {}
    for r in result:
        if r[0] not in id_map:
            id_map[r[0]] = [r[1]]
        else:
            id_map[r[0]].append(r[1])

    for id in id_map:
        update_sql = "update financial_origin_began set error_code = {} where report_id='{}'".format(max(id_map[id]), id)
        print(update_sql)
        dbtools.query_common(update_sql)




if __name__ == '__main__':
    # table_name = get_table_date()
    # print(table_name)
    # print(clear_label('A农、林、牧、渔   业/05农、林、  牧、渔服务业'))
    # temp()

    process()
