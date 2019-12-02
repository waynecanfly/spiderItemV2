# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

class MyproxyMiddleware(object):
    """docstring for ProxyMiddleWare"""

    def __init__(self):
        self.ip_list = [
            "58.218.92.151:9825",
            "58.218.92.144:9714",
            "58.218.92.148:9631",
            "58.218.92.147:9997",
            "58.218.92.150:9800",
            "58.218.92.149:9881",
            "58.218.92.149:9650",
            "58.218.92.146:9756",
            "58.218.92.145:9662",
            "58.218.92.148:9651",
            "58.218.92.147:9825",
            "58.218.92.89:9011",
            "58.218.92.148:9799",
            "58.218.92.149:9600",
            "58.218.92.146:9565",
            "58.218.92.147:9934",
            "58.218.92.146:9741",
            "58.218.92.89:9541",
            "58.218.92.146:9839",
            "58.218.92.148:9863",
            "58.218.92.89:9158",
            "58.218.92.89:9798",
            "58.218.92.146:9657",
            "58.218.92.150:9630",
            "58.218.92.149:9545",
            "58.218.92.89:9333",
            "58.218.92.151:9518",
            "58.218.92.149:9999",
            "58.218.92.145:9875",
            "58.218.92.145:9859",
            "58.218.92.151:9672",
            "58.218.92.147:9808",
            "58.218.92.148:9771",
            "58.218.92.149:9639",
            "58.218.92.147:9719",
            "58.218.92.146:9799",
            "58.218.92.151:9594",
            "58.218.92.89:9807",
            "58.218.92.89:9747",
            "58.218.92.146:9762",
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
