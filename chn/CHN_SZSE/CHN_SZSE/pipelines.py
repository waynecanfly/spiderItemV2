# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from twisted.enterprise import adbapi

from .items import ChnSzseItem, SzseCollectionItem1, SzseCollectionItem2, SzseCollectionItem3
from .items import ChnSzseListItem
from .items import SecretaryItem
from .items import RegItem
from .items import DisItem
from .items import StockItem
from .items import CompanyInfoItem
from .items import SecretaryTwoItem
from .items import SecretaryThreeItem

from datetime import datetime
from .samples.base_rule import toInsert
from common.utils import get_table_name

class ChnSzsePipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        dbargs = settings['DBARGS']
        dbpool = adbapi.ConnectionPool('pymysql', **dbargs)
        return cls(dbpool)

    def __init__(self, dbpool):
        self.dbpool = dbpool

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item, spider)
        query.addCallback(self.handle_error)

    def do_insert(self, cursor, item, spider):
        # if spider.name == 'SZ_list_insert':
        #     if isinstance(item, ChnSzseItem):
        #         cursor.execute(toInsert('company_data_source_complete20191022_copy', item))
        #     elif isinstance(item, ChnSzseListItem):
        #         for vals in item:
        #             sql = "INSERT INTO `company_origin_info_complete20191022` (" \
        #                   "country_code, company_code, display_label, information, gmt_create, user_create" \
        #                   ") VALUES (%s, %s, %s, %s, %s, %s);"
        #             print('$' * 20, sql)
        #             cursor.execute(
        #                 sql,
        #                 ['chn',
        #                  str(item['company_code'][1]),
        #                  str(item[vals][0]),
        #                  str(item[vals][1]),
        #                  str(datetime.now()),
        #                  'xfc'])
        #
        #     elif isinstance(item, ChnSzseItem):
        #         cursor.execute(toInsert('company_data_source_complete20191022_copy', item))
        #     elif isinstance(item, ChnSzseListItem):
        #         for vals in item:
        #             sql = "INSERT INTO `company_origin_info_complete20191022` (" \
        #                   "country_code, company_code, display_label, information, gmt_create, user_create" \
        #                   ") VALUES (%s, %s, %s, %s, %s, %s);"
        #             print('$' * 20, sql)
        #             cursor.execute(
        #                 sql,
        #                 ['chn',
        #                  str(item['company_code'][1]),
        #                  str(item[vals][0]),
        #                  str(item[vals][1]),
        #                  str(datetime.now()),
        #                  'xfc'])
        #
        #     elif isinstance(item, ChnSzseItem):
        #         cursor.execute(toInsert('company_data_source_complete20191022_copy', item))
        #     elif isinstance(item, ChnSzseListItem):
        #         for vals in item:
        #             sql = "INSERT INTO `company_origin_info_complete20191022` (" \
        #                   "country_code, company_code, display_label, information, gmt_create, user_create" \
        #                   ") VALUES (%s, %s, %s, %s, %s, %s);"
        #             print('$' * 20, sql)
        #             cursor.execute(
        #                 sql,
        #                 ['chn',
        #                  str(item['company_code'][1]),
        #                  str(item[vals][0]),
        #                  str(item[vals][1]),
        #                  str(datetime.now()),
        #                  'xfc'])
        # if spider.name == 'secretary_seniority':
        #     if isinstance(item, SecretaryItem):
        #         # cursor.execute(toInsert('company_original_information_detail_c20191104', item))
        #         pass
        #     elif isinstance(item, SecretaryTwoItem):
        #         cursor.execute(toInsert('company_original_information_detail_c20191104', item))
        #     elif isinstance(item, SecretaryThreeItem):
        #         cursor.execute(toInsert('company_original_information_detail_c20191104', item))
        #
        # elif spider.name == 'Regulatory_discipline':
        #     if isinstance(item, RegItem):
        #         cursor.execute(toInsert('company_original_information_detail_c20191104', item))
        #     elif isinstance(item, DisItem):
        #         cursor.execute(toInsert('company_original_information_detail_c20191104', item))
        #
        # elif spider.name == 'stock_change':
        #     if isinstance(item, StockItem):
        #         cursor.execute(toInsert('company_original_information_detail_c20191104', item))

        if spider.name == 'SZSE_company_list':
            pass
            if isinstance(item, SzseCollectionItem1):
                cursor.execute(toInsert('company_base_info', item))

            elif isinstance(item, SzseCollectionItem2):
                cursor.execute(toInsert('company_base_info', item))

            elif isinstance(item, SzseCollectionItem3):
                cursor.execute(toInsert('company_base_info', item))

        elif spider.name == 'company_info':
            tablename = get_table_name()
            # tablename = 'company_raw_info_20191120'
            if isinstance(item, CompanyInfoItem):
                for vals in item:
                    sql = "INSERT INTO `%s` (" \
                          "country_code, exchange_market_code, security_code, company_code, display_label, information, " \
                          "gmt_create, user_create) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(
                        sql,
                        [
                            tablename,
                            'chn',
                            'SZSE',
                            str(item['security_code'][1]),
                            str(item['company_code'][1]),
                            str(item[vals][0]),
                            str(item[vals][1]),
                            str(datetime.now()),
                            'xfc'
                        ]
                    )

    def handle_error(self, failure):
        if failure:
            print(failure)