#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json



def alter_file(file, old_str, new_str):
    """
    替换文件中的字符串
    :param file:文件名
    :param old_str:旧字符串
    :param new_str:新字符串
    :return:
    """
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str, new_str)
            file_data += line
    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)


def read_file(file):
    """
    读取文件中的字符串
    file:文件名
    return:custom_code
    """
    with open(file) as f:
        file_data = f.readline()

    return file_data

def get_file_path():
    root_path = os.path.abspath(os.path.dirname(__file__)).split('spiderItemV2')[0]
    file_path = root_path + '/spiderItemV2/common/tablename.txt'

    return file_path

def get_hongkong_spider_path():
    root_path = os.path.abspath(os.path.dirname(__file__)).split('spiderItemV2')[0]
    hk_path = root_path + '/spiderItemV2/hongkong'

    return hk_path

def get_table_name():
    file_path = get_file_path()
    msg = read_file(file_path)
    table_name = msg.split(':')[1]
    return table_name

def get_table_date():
    file_path = get_file_path()
    msg = read_file(file_path)
    table_date = msg.split(':')[0]
    return table_date

def get_china_sse_spider_path():
    root_path = os.path.abspath(os.path.dirname(__file__)).split('spiderItemV2')[0]
    sse_path = root_path + '/spiderItemV2/chn/CHN_SSE'

    return sse_path

def get_china_szse_spider_path():
    root_path = os.path.abspath(os.path.dirname(__file__)).split('spiderItemV2')[0]
    szse_path = root_path + '/spiderItemV2/chn/CHN_SZSE'


    return szse_path



# if __name__ == '__main__':
    # table_name = get_table_date()
    # print(table_name)
