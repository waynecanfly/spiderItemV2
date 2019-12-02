#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/9/23 15:15
import hashlib

import pymysql

value_origin = hashlib.md5()

def MD5_VALUE(path_link):
    """ MD5值的生成 """
    try:
        with open(r'%s' % path_link, 'rb') as rf:
            while True:
                file_iter = rf.read(2048)
                if not file_iter:
                    break
                value_origin.update(file_iter)
        md_value = value_origin.hexdigest()
        return md_value
    # 判断出错的原因，
    except IOError:
        # PATH_ERROR：路径出错原因是找不到路径文件；
        return "PATH_ERROR"
    except:
        # UNKONOW_ERROR：可能是其他出错原因
        return "UNKNOW_ERROR"


def process():
    conn = pymysql.connect(host="10.100.4.99", port=3306, db="opd_common", user="root", passwd="OPDATA",
                                charset="utf8")
    cursor = conn.cursor()
    sql = "select report_id,doc_local_path from financial_origin_began_complete20191101_copy1_copy1 where country_code='HKG' " \
          "and doc_type='pdf'"

    cursor.execute(sql)
    result = cursor.fetchall()
    for res in result:
        report_id = res[0]
        doc_local_path = res[1]
        md5 = MD5_VALUE(doc_local_path)
        print(md5)
        sql02 = "update financial_origin_began_complete20191101_copy1_copy1 set md5='{md5}' where report_id='{report_id}'".format(
            md5=md5, report_id=report_id
        )
        cursor.execute(sql02)
        conn.commit()

if __name__ == '__main__':
    process()
