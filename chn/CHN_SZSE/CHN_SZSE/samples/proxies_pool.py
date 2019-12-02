#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/9/27 16:33

import requests
from bs4 import BeautifulSoup
import lxml
from multiprocessing import Process, Queue
import random
import json
import time
import requests


class Proxies:
    """docstring for Proxies"""

    def __init__(self):
        self.proxies = []
        self.verify_pro = []
        self.proxy_url = 'http://http.tiqu.alicdns.com/getip3?num=400&type=1&pro=&city=0&yys=0&' \
                         'port=1&pack=65959&ts=0&ys=0&cs=0&lb=4&sb=,&pb=45&mr=2&regions=110000,' \
                         '130000,140000,150000,210000,310000,320000,330000,340000,350000,360000,' \
                         '370000,410000,430000,440000,500000,510000,530000,610000,620000,640000'

        # self.get_proxy()

    def get_proxy(self):
        res = requests.get(self.proxy_url)

        ip_list = str(res.text).split('\n')
        # print(ip_list)
    #     self.detail_proxy(ip_list)
    #
    # def detail_proxy(self, proxy_list):
        ip_address = random.choice(ip_list)
        proxy = {
            'http': 'http://' + ip_address,
            'https': 'https://' + ip_address
        }

        respon = requests.get('https://www.baidu.com/', proxies=proxy)
        print(respon.status_code)
        if respon.status_code != 200:
            self.proxies.remove(ip_address)
            ip_proxy = random.choice(self.proxies)
        else:
            ip_proxy = ip_address
        print(ip_proxy)
        return ip_proxy


obj = Proxies()
obj.get_proxy()


# with open('ip_proxy.txt', 'a') as wf:
#     wf.write(obj.get_proxy() + '\n')


