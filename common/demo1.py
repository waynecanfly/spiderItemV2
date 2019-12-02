#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/11/14 18:21
import json

def detail():
    with open('D:/Colletion_SpiderItem/spiderItemV2/common/updatefields.json', 'r', encoding='utf-8') as rf:
        valaues = json.load(rf)
    print(valaues)

detail()