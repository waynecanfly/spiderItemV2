# -*- coding: UTF-8 -*-
import pymysql

db_config = {
    "pdfparser": {
      "name": "pdfparse_lib",
      "ip": "10.100.4.77",
      "user": "root",
      "password": "Origin123_"
    },
    "common": {
      "name": "opd_common",
      "ip": "10.100.4.99",
      "user": "originp",
      "password": "originp"
    },
    "opd_fdss": {
      "name": "opd_fdss",
      "ip": "10.100.4.88",
      "user": "u_opd_fdss",
      "password": "u_opd_fdss"
    },
    "opd_fdss_test": {
      "name": "opd_fdss_test",
      "ip": "10.100.4.88",
      "user": "u_opd_fdss",
      "password": "u_opd_fdss"
    },
    "base_info": {
      "name": "base_info",
      "ip": "10.100.4.99",
      "user": "originp",
      "password": "originp"
    }
}


def query_pdfparse(sql):
    pdf_lib_ip = db_config['pdfparser']['ip']
    pdf_lib_user = db_config['pdfparser']['user']
    pdf_lib_password = db_config['pdfparser']['password']
    pdf_lib_dbname = db_config['pdfparser']['name']
    db = pymysql.connect(host = pdf_lib_ip, user=pdf_lib_user, passwd=pdf_lib_password, db=pdf_lib_dbname, port = 3306,charset='utf8')
    try:
        cursor = db.cursor()
        result = cursor.execute(sql)
        data = cursor.fetchall()
        db.commit()
        db.close()
        return data
    except pymysql.IntegrityError:
        db.close()
        raise pymysql.IntegrityError
    except Exception:
        print('[SQL_ERROR]: ' + sql)
        db.close()
        raise Exception


def query_opd_fdss(sql):
    common_ip = db_config['opd_fdss']['ip']
    common_user = db_config['opd_fdss']['user']
    common_password = db_config['opd_fdss']['password']
    common_dbname = db_config['opd_fdss']['name']
    db = pymysql.connect(host=common_ip, user=common_user, passwd=common_password, db=common_dbname, port=3306, charset='utf8')
    try:
        cursor = db.cursor()
        result = cursor.execute(sql)
        data = cursor.fetchall()
        db.commit()
        db.close()
        return data
    except Exception:
        db.close()
        print(sql)
        raise Exception


def query_opd_fdss_test(sql):
    common_ip = db_config['opd_fdss_test']['ip']
    common_user = db_config['opd_fdss_test']['user']
    common_password = db_config['opd_fdss_test']['password']
    common_dbname = db_config['opd_fdss_test']['name']
    db = pymysql.connect(host=common_ip, user=common_user, passwd=common_password, db=common_dbname, port=3306, charset='utf8')
    try:
        cursor = db.cursor()
        result = cursor.execute(sql)
        data = cursor.fetchall()
        db.commit()
        db.close()
        return data
    except Exception:
        db.close()
        print(sql)
        raise Exception


def query_common(sql):
    common_ip = db_config['common']['ip']
    common_user = db_config['common']['user']
    common_password = db_config['common']['password']
    common_dbname = db_config['common']['name']

    db = pymysql.connect(host=common_ip, user=common_user, passwd=common_password, db=common_dbname, port=3306, charset='utf8')
    try:
        cursor = db.cursor()
        result = cursor.execute(sql)
        data = cursor.fetchall()
        db.commit()
        db.close()
        return data
    except Exception:
        print('Error Sql： ' + sql)
        db.close()

        raise Exception


def query_baseinfo(sql):
    common_ip = db_config['base_info']['ip']
    common_user = db_config['base_info']['user']
    common_password = db_config['base_info']['password']
    common_dbname = db_config['base_info']['name']

    db = pymysql.connect(host = common_ip, user = common_user, passwd = common_password, db = common_dbname, port = 3306,charset='utf8')
    try:
        cursor = db.cursor()
        result = cursor.execute(sql)
        data = cursor.fetchall()
        db.commit()
        db.close()
        return data
    except Exception:
        db.close()
        raise Exception


def deleteDataByReportID(tablename, reportid):
    pdf_lib_ip = db_config['pdfparser']['ip']
    pdf_lib_user = db_config['pdfparser']['user']
    pdf_lib_password = db_config['pdfparser']['password']
    pdf_lib_dbname = db_config['pdfparser']['name']

    sql = "delete from {tablename} where reportid='{reportid}'"
    sql = sql.format(tablename=tablename, reportid=reportid)

    db = pymysql.connect(host=pdf_lib_ip, user=pdf_lib_user, passwd=pdf_lib_password, db=pdf_lib_dbname, port=3306, charset='utf8')
    try:
        cursor = db.cursor()
        result = cursor.execute(sql)
        data = cursor.fetchall()
        db.commit()
        db.close()
        return data
    except Exception:
        db.close()
        raise Exception


def query_pdfparse_overlap_by_reportid(sql,tablename, reportid):
    pdf_lib_ip = db_config['pdfparser']['ip']
    pdf_lib_user = db_config['pdfparser']['user']
    pdf_lib_password = db_config['pdfparser']['password']
    pdf_lib_dbname = db_config['pdfparser']['name']


    db = pymysql.connect(host = pdf_lib_ip, user = pdf_lib_user, passwd = pdf_lib_password, db = pdf_lib_dbname, port = 3306,charset='utf8')
    try:
        cursor = db.cursor()
        # delete first
        deletesql = "delete from {tablename} where reportid = '{reportid}'"
        deletesql = deletesql.format(tablename=tablename, reportid=reportid)
        cursor.execute(deletesql)

        # query
        result = cursor.execute(sql)
        data = cursor.fetchall()
        db.commit()
        db.close()
        return data
    except Exception:
        db.close()
        raise Exception
