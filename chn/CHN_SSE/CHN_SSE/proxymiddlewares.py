#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: xfc
# @Time : 2019/10/11 11:35
import requests
import time
import random
import json

class GetProxyMiddleware(object):
    proxy_list = [

    ]

    test_url = 'http://query.sse.com.cn/security/stock/getStockListData2.do?'

    header_form = {
        'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }

    data_form = {
        'isPagination': 'true',
        'stockCode': '',
        'csrcCode': '',
        'areaName': '',
        'pageHelp.pageSize': '1000',
        'stockType': '1'
    }

    def process_request(self, request, spider):
        with open('E:\\Restructure\\CHN_SSE\\CHN_SSE\\samples\\custom_code.txt', 'r') as rf:
            proxy_str = rf.read()
        proxy_list = proxy_str.split('\n')
        # request.meta["proxy"] = "http://%s" % random.choice(proxy_list)
        request.meta["proxy"] = "http://" + self.get_random_proxy()



    def get_random_proxy(self):
        real_ip = random.choice(self.proxy_list)
        ip_chioce = {
            "http://": "http://" + real_ip,
            "https://": "https://" + real_ip,
        }
        try:
            res = requests.get(
                url=self.test_url,
                params=self.data_form,
                headers=self.header_form,
                proixes=ip_chioce
            )
            if res.text is not None:
                self.proxy_list.remove(real_ip)
                ip_address = real_ip
                return ip_address

        except:
            print('get ERROR')
            self.proxy_list.remove(real_ip)
            # ip_address = random.choice(self.proxy_list)
