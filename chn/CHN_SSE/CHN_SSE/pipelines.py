# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi

# from common.utils import get_table_name
from .items import SampleInfoItem, MSXXNameItem, AGSSRDateFirstItem, BGSSRDateLastItem, AGFHItem, \
    BGFHItem, AGSGItem, BGSGItem, EquityChangeItem, EquityStructureItem, SeniorManagementItem, FinancingSituationAFirst, \
    FinancingSituationAad, FinancingSituationSpecial, CompanyListItem, AddCompanyMarketItem

from .samples.base_rule import toInsert
from .samples.base_rule import toUpdate
from .samples.base_rule import saveOriginInsert

from datetime import datetime

# class DeFaultValuePipeline(object):
#
#     def process_item(self, item, spider):
#         if spider.name == 'SSE_list':
#             if isinstance(item, CompanyInFoItem):
#                 item.setdefault('country_code', 'chn')
#                 item.setdefault('gmt_create', str(datetime.now()))
#                 item.setdefault('user_create', 'xfc')
            # elif isinstance(item, ListingDateIndex):
            #     item.setdefault('country_code', 'chn')
            #     item.setdefault('gmt_create', str(datetime.now()))
            #     item.setdefault('user_create', 'xfc')
            # elif isinstance(item, ListingDateLast):
            #     item.setdefault('country_code', 'chn')
            #     item.setdefault('gmt_create', str(datetime.now()))
            #     item.setdefault('user_create', 'xfc')
            # elif isinstance(item, SecretaryName):
            #     item.setdefault('country_code', 'chn')
            #     item.setdefault('gmt_create', str(datetime.now()))
            #     item.setdefault('user_create', 'xfc')

# class DuplicatesPipeline(object):
#     def __init__(self):
#         self.book_set = set()
#
#     def process_item(self, item, spider):
#         name = item['name']
#         if name in self.book_set:
#             raise EquityChange("Dupliacte book found: %s" % item)
#
#         self.book_set.add(name)
#         return item

class ChnSsePipeline(object):

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
        # tablename = get_table_name()
        if spider.name == 'SSE_list_insert':
            pass
            if isinstance(item, CompanyListItem):
                cursor.execute(toInsert('company_base_info_20191122', item))

            elif isinstance(item, AddCompanyMarketItem):
                # cursor.execute(toInsert(tablename, item))
                cursor.execute(toInsert('comany_raw_info_20191121', item))
        # elif spider.name == 'SSE_company_sample_info':
        #     if isinstance(item, SampleInfoItem):
        #         # tablename = 'company_raw_info_20191120'
        #         cursor.execute(toInsert(tablename, item))
        # elif spider.name == 'SSE_listing_date_name':
        #     if isinstance(item, MSXXNameItem):
        #         cursor.execute(toInsert(tablename, item))
        #
        #     elif isinstance(item, AGSSRDateFirstItem):
        #         cursor.execute(toInsert(tablename, item))
        #
        #     elif isinstance(item, BGSSRDateLastItem):
        #         cursor.execute(toInsert(tablename, item))
        # elif spider.name == 'LiRunFenPei':
        #     if isinstance(item, AGFHItem):
        #         cursor.execute(toInsert('company_original_information_detail_20191114', item))
        # elif spider.name == 'LiRunFenPei':
        #     if isinstance(item, BGFHItem):
        #         cursor.execute(toInsert('company_original_information_detail_20191114', item))
        # elif spider.name == 'LiRunFenPei':
        #     if isinstance(item, AGSGItem):
        #         cursor.execute(toInsert('company_original_information_detail_20191114', item))
        # elif spider.name == 'LiRunFenPei':
        #     if isinstance(item, BGSGItem):
        #         cursor.execute(toInsert('company_original_information_detail_20191114', item))
        # elif spider.name == 'gubenjieogu':
        #     if isinstance(item, EquityChangeItem):
        #         cursor.execute(toInsert('company_original_information_detail_20191114', item))
        # elif spider.name == 'gubenjieogu':
        #     if isinstance(item, EquityStructureItem):
        #         cursor.execute(toInsert('company_original_information_detail_20191114', item))
        # elif spider.name == 'gaoguanrenyuan':
        #     if isinstance(item, SeniorManagementItem):
        #         cursor.execute(toInsert('company_original_information_detail_20191114', item))
        # elif spider.name == 'couzhiqingkaung':
        #     if isinstance(item, FinancingSituationAFirst):
        #         cursor.execute(toInsert('company_original_information_detail_20191114', item))
        # elif spider.name == 'couzhiqingkaung':
        #     if isinstance(item, FinancingSituationAad):
        #         cursor.execute(toInsert('company_original_information_detail_20191114', item))
        # elif spider.name == 'couzhiqingkaung':
        #     if isinstance(item, FinancingSituationSpecial):
        #         cursor.execute(toInsert('company_original_information_detail_20191114', item))zz
        else:
            return "None Values !"

    def handle_error(self, failure):
        if failure:
            print(failure)
