# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import time

import pymysql

from samples.base_rule import toInsert, removeRepeatByComNm

from hongkong.items import HongKongCompItem, HongkongOriginInfoItem, HongKongFileItem, HongKongHtmlFileItem, \
    HongKongPresetItem, HongKongSecurityItem, HongKongMarketItem, HongKongDelistedCompanyItem

# from common.utils import get_table_name


class HongkongPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host="10.100.4.99", port=3306, db="opd_common", user="root", passwd="OPDATA",
                                    charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # if spider.name == 'HKEX_origin_info_update':
        #     if isinstance(item, HongkongOriginInfoItem):
        #         tablename = get_table_name()
        #         gmt_create = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        #         for vals in item:
        #             sql = "insert into {table} (" \
        #                   "country_code, exchange_market_code, security_code, company_code, display_label, information, gmt_create, user_create) values " \
        #                   "(%s,%s,%s,%s,%s,%s,%s,%s)".format(table=tablename)
        #             print('*' * 20, sql)
        #             self.cursor.execute(
        #                 sql,
        #                 [
        #                     'HKG',
        #                     'HKEX',
        #                     str(item['stock_code'][1]),
        #                     str(item['company_code'][1]),
        #                     str(item[vals][0]),
        #                     str(item[vals][1]),
        #                     str(gmt_create),
        #                     'cf'
        #                 ]
        #             )
        #             self.conn.commit()
        if spider.name == 'HKEX_data_source_list_insert':
            if isinstance(item, HongKongCompItem):

                toInsert(self.conn, self.cursor, 'company_data_source_complete20191010_copy1_copy1', item)
                # 不同的security_type列表中存在相同的公司，因此需要对公司列表去重
            # removeRepeatByComNm(self.cursor, 'company_data_source_complete20191010')
        # # 正式
        if spider.name == 'HKEX_origin_info_insert':
            if isinstance(item, HongKongPresetItem):
                toInsert(self.conn, self.cursor, 'company_origin_info_complete20191010_copy1', item)
            if isinstance(item, HongKongSecurityItem):
                toInsert(self.conn, self.cursor, 'company_origin_info_complete20191010_copy1', item)
            if isinstance(item, HongKongMarketItem):
                toInsert(self.conn, self.cursor, 'company_origin_info_complete20191010_copy1', item)
            if isinstance(item, HongkongOriginInfoItem):
                toInsert(self.conn, self.cursor, 'company_raw_info_20191126', item)
        if spider.name == 'HKEX_headline_origin_began_insert':
            if isinstance(item, HongKongFileItem):
                toInsert(self.conn, self.cursor, 'financial_origin_began_complete20191101_copy1_copy1', item)
        if spider.name == 'HKEX_document_origin_began_insert':
            if isinstance(item, HongKongFileItem):
                toInsert(self.conn, self.cursor, 'financial_origin_began_complete20191101_copy1_copy1', item)
        if spider.name == 'HKEX_headline_file_download_spider':
            if isinstance(item, HongKongFileItem):
                doc_local_path = item['doc_local_path']
                report_id = item['report_id']
                is_downloaded = item['is_downloaded']

                # print(doc_local_path)
                sql = "UPDATE financial_origin_began_complete20191101_copy1_copy1 SET is_downloaded='{is_downloaded}'," \
                      "doc_local_path='{doc_local_path}' where report_id='{report_id}'".format(
                    is_downloaded=is_downloaded,
                    doc_local_path=doc_local_path,
                    report_id=report_id)
                print('*' * 20, sql)
                self.cursor.execute(sql)
                self.conn.commit()
        if spider.name == 'HKEX_document_file_download_spider':
            if isinstance(item, HongKongHtmlFileItem):
                doc_local_path = item['doc_local_path']
                report_id = item['report_id']
                is_downloaded = item['is_downloaded']

                # print(doc_local_path)
                sql = "UPDATE financial_html_origin_began_complete SET is_downloaded='{is_downloaded}'," \
                      "doc_local_path='{doc_local_path}' where report_id='{report_id}'".format(
                    is_downloaded=is_downloaded,
                    doc_local_path=doc_local_path,
                    report_id=report_id)
                print('*' * 20, sql)
                self.cursor.execute(sql)
                self.conn.commit()

        if spider.name == 'HKEX_financial_html_origin_began_insert':
            if isinstance(item, HongKongHtmlFileItem):
                toInsert(self.conn, self.cursor, 'financial_html_origin_began_complete', item)

        if spider.name == 'HKEX_delisted_company_list':
            if isinstance(item, HongKongDelistedCompanyItem):
                toInsert(self.conn, self.cursor, 'company_listing_status_hkg', item)





