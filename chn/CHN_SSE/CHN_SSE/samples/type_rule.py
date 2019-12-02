#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/9/23 15:16

"""

规范后的财报年份：
Q1：end_date <= 03-31 的按end_date的年份，否则end_date的年份 +1；
Q2：end_date <= 06-30 的按end_date的年份，否则end_date的年份 +1；
Q3：end_date <= 09-30 的按end_date的年份，否则end_date的年份 +1；
这里的财年就是修正的截止日期的年份。

*************************************************************

规范后的截止日期:
每个月15日及15日以前的归类到上个月；
每个月15日之后的归类到下个月。

"""


import re
import time
import pymysql
from datetime import datetime


# class Stanard:
#
#     num_list = ['1','2','3','4','5','6','7','8','9','10','11','12']
#     dates_list = ['01-31', '02-28', '03-31', '04-30', '05-31', '06-30',
#                   '07-31', '08-31', '09-30', '10-31', '11-30', '12-31']
#
#     conn = pymysql.connect(host='10.100.4.99', user='root', password='OPDATA', db='opd_common')
#     cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
#
#     # def __init__(self, end_time):
#     #     self.end_time = end_time
#     #     self.conn = pymysql.connect(host='10.100.4.99', user='root', password='OPDATA', db='opd_common')
#     #     self.cursor = self.conn.cursor()
#
#
#     def read_mysql(self):
#         self.cursor.execute("SELECT report_id, end_date FROM financial_origin_began_backup20190910 "
#                             "where country_code='JPN' ORDER BY company_code ASC LIMIT 1000;")
#         feild_list = self.cursor.fetchall()
#         for feild_dict in feild_list:
#             self.fical_year_stanard(feild_dict['report_id'], feild_dict['end_date'])
#
#     def fical_year_stanard(self, report_id, end_date):
#         """ 规范后的年份 """
#         # end_str = self.end_time.strftime("%Y-%m-%d %H:%M:%S")
#         end_str = end_date.strftime("%Y-%m-%d %H:%M:%S")
#         print(end_str)
#         year_num = ''.join(end_str).split('-')[0]  # 年份
#         month_num = ''.join(end_str).split('-')[1]  # 月份
#         day_num = ''.join(end_str).split('-')[2]  # 日/天
#         date_day = day_num.split(' ')[0]
#         if month_num[0] == '0':
#             month_num = month_num[-1]
#         count_alone = int(month_num) - 1
#         count_done = int(month_num) - 2
#         month_alone = self.dates_list[count_alone]
#         if date_day <= '15':
#             month_alone = self.dates_list[count_done]
#         Revised_fiscal_year = ''.join(year_num) + '-' + month_alone + ' ' + '00:00:00'  # 修正后的财年日期
#         standard_date = datetime.strptime(Revised_fiscal_year, "%Y-%m-%d %H:%M:%S")
    #
    #
    # def end_date_stanard(self):
    #     """ 规范后的截止日期 """
    #     end_str = self.end_time.strftime("%Y-%m-%d %H:%M:%S")
    #     year_num = ''.join(end_str).split('-')[0]  # 年份
    #     month_num = ''.join(end_str).split('-')[1]  # 月份
    #     day_num = ''.join(end_str).split('-')[2]  # 日/天
    #     date_day = day_num.split(' ')[0]
    #     date_time = day_num.split(' ')[-1]
    #     # 个位数日期取一个数
    #     # if month_num[0] == '0':
    #     #     month_nums = month_num[-1]
    #     # else:
    #     #     month_nums = month_num
    #     count_alone = int(month_num) - 1
    #     count_done = int(month_num) - 2
    #
    #     # 截止日期小于15日的日期归为上个月
    #     if date_day <= '15':
    #         month_alone = self.dates_list[count_done]
    #     else:
    #         month_alone = self.dates_list[count_alone]
    #     Revised_fiscal_year = ''.join(year_num) + '-' + month_alone + ' ' + '00:00:00'  # 修正后的财年日期
    #     standard_date = datetime.strptime(Revised_fiscal_year, "%Y-%m-%d %H:%M:%S")
    #
    #
    # def quarter_type_stanard(self):
    #     """ 规范后的季度类型 """
    #     pass
