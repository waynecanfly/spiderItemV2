#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/10/11 10:25

from queue import Queue
from threading import Thread, RLock


import requests


def start_requests():
    ip = {
        'http' : 'http://58.218.200.227:4981',
        'https' : 'https://58.218.200.227:4981'
    }
    res = requests.get(url='http://www.baidu.com', proxies=ip)
    print(res.status_code)
    print(res.text)


start_requests()