#! /usr/bin/env python
# -*- coding: utf-8 -*-

import random
from datetime import datetime


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


def uniqueIDMaker():
    time_id = str(datetime.now()).split(".")[-1]
    random_id1 = str(random.randrange(0, 9))
    random_id2 = str(random.randrange(0, 9))
    unique_id = time_id + random_id1 + random_id2
    return unique_id


if __name__ == '__main__':
    uniqueIDMaker = uniqueIDMaker()
    print(uniqueIDMaker)