#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/9/23 15:15
import hashlib


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


