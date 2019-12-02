#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/9/23 15:15
import os


def FTP_PATH(doc_local_path, country_code, splicing):
    """ 文件上传 """
    count = 1
    number_documents = "ls -l | grep -c '^-'"
    try:
        path_list = 'sshpass -p originp123 scp {} root@10.100.4.102:/volume2/data/{}//{}'  # 携带登录密码
        push = path_list.format(doc_local_path, country_code, splicing)
        os.system(push)
        count += 1
        with open('file_number.txt', 'w') as wf:
            wf.write(count)
        if count == int(number_documents):
            return "上传成功!"
        return path_list.split(':')[-1]
    except:
        return "UPLOAD ERROR"