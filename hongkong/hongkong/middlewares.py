# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import random

import requests
from twisted.internet.error import TimeoutError

from hongkong.settings import USER_AGENT_LIST


class RandomUserAgentMiddleware(object):
    # def __init__(self, user_agents):
    #     self.user_agents = user_agents
    #
    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(crawler.settings['USER_AGENT_LIST'])

    def process_request(self, request, spider):
        # request.headers.setdefault(
        #     'User-Agent', random.choice(self.user_agents)
        # )
        ua = random.choice(USER_AGENT_LIST)
        if ua:
            request.headers.setdefault('User-Agent', ua)

class ProxyMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings['API_URL'])

    def __init__(self, api_url):
        self.api_url = api_url
        self.proxy_ip = None
        self.total_urls = 0

    def process_request(self, request, spider):
        if self.total_urls % 10 == 0:
            self.proxy_ip = self.get_proxy_ip()

        if self.proxy_ip:
            request.meta['proxy'] = 'http://' + str(self.proxy_ip)
            request.meta['ip'] = self.proxy_ip
        else:
            request.meta['ip'] = 'localhost'

    def get_proxy_ip(self):
        try:
            response = requests.get(self.api_url, timeout=5)
            # print(type(response.text))
            return str(response.text)
        except requests.exceptions.Timeout:
            pass


class ExceptionMiddleware(object):
    def process_exception(self, request, exception, spider):
        if isinstance(exception, TimeoutError):
            return request


if __name__ == '__main__':
    rm = RandomUserAgentMiddleware()

