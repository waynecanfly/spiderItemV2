# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

class MyproxyMiddleware(object):
    """docstring for ProxyMiddleWare"""

    def __init__(self):
        self.ip_list = [
            "58.218.92.89:9660",
            "58.218.92.150:9972",
            "58.218.92.150:9810",
            "58.218.92.148:9889",
            "58.218.92.146:9730",
            "58.218.92.149:9746",
            "58.218.92.147:9772",
            "58.218.92.144:9568",
            "58.218.92.89:9327",
            "58.218.92.146:9826",
            "58.218.92.145:9631",
            "58.218.92.149:9511",
            "58.218.92.146:9910",
            "58.218.92.89:9536",
            "58.218.92.150:9901",
            "58.218.92.148:9964",
            "58.218.92.148:9868",
            "58.218.92.144:9802",
            "58.218.92.146:9839",
            "58.218.92.151:9577",
            "58.218.92.89:9642",
            "58.218.92.89:9028",
            "58.218.92.148:9958",
            "58.218.92.150:9685",
            "58.218.92.89:9595",
            "58.218.92.148:9988",
            "58.218.92.145:9951",
            "58.218.92.89:9705",
            "58.218.92.149:9614",
            "58.218.92.148:9900",
            "58.218.92.150:9742",
            "58.218.92.151:9582",
            "58.218.92.148:9881",
            "58.218.92.149:9918",
            "58.218.92.150:9996",
            "58.218.92.151:9751",
            "58.218.92.145:9537",
            "58.218.92.145:9551",
            "58.218.92.144:9749",
            "58.218.92.145:9503",
    ]

    def process_request(self, request, spider):
        '''对request对象加上proxy'''
        # proxy = self.get_random_proxy()
        # request.meta['User-Agent'] = ' Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'
        haha = random.randint(0,10)
        if haha >= 5:
            print('\n随机{}正在使用代理\n'.format(haha))
            request.meta['proxy'] = random.choice(self.ip_list)

    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            # print("this is response ip:" + proxy)
            # 对当前reque加上代理
            request.meta['proxy'] = random.choice(self.ip_list)
            return request
        return response

    def process_exception(self, request, exception, spider):
        # 出现异常时（超时）使用代理
        print("\n出现异常，正在使用代理重试....\n")
        request.meta['proxy'] = random.choice(self.ip_list)
        return request

class MyUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent):
        super().__init__()
        self.user_agent = user_agent
        self.user_list = [
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36'
        ]

    def process_request(self, request, spider):
        request.headers['User_Agent'] = random.choice(self.user_list)
