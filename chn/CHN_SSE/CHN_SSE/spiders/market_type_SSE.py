# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# # Author: xfc
# # @Time : 2019/11/11 13:34
# import pymysql
#
# from datetime import datetime
#
# conn = pymysql.connect(host='10.100.4.99', user='root', passwd='OPDATA', db='opd_common', charset='utf8')
# cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
#
# def request():
#     cur.execute("SELECT company_code, security_code, market_type FROM `company_data_source_complete20191010_copy` "
#                 "WHERE exchange_market_code='SSE' ORDER BY company_code ASC ;")
#     feild_list = cur.fetchall()
#     for feild_dict in feild_list:
#         company_code = feild_dict['company_code']
#         security_code = feild_dict['security_code']
#         market_type = feild_dict['market_type']
#         detail(company_code, security_code, market_type)
#
# def detail(company_code, security_code, market_type):
#     item = {}
#     item['country_code'] = 'chn'
#     item['exchange_market_code'] = 'SSE'
#     item['security_code'] = security_code
#     item['company_code'] = company_code
#     item['display_label'] = '市场类型'
#     item['information'] = market_type
#     item['gmt_create'] = str(datetime.now())
#     item['user_create'] = 'xfc'
#     cols, values = zip(*item.items())
#     print(cols, '&' * 20)
#     print(values, '%' * 20)
#     sql = "INSERT INTO `{}` ({}) VALUES {}".format \
#             (
#             'company_origin_information_survey_1111',
#             ','.join(cols),
#             (str(values) + ',')[0:-1]
#         )
#     print('*' * 20, sql)
#     try:
#         cur.execute(sql)
#         conn.commit()
#     except Exception as e:
#         print('SQL ERROR !!!', e)
#
# request()