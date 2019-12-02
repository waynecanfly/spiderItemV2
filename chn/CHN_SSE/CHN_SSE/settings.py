# -*- coding: utf-8 -*-

# Scrapy settings for CHN_SSE project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import pymysql

BOT_NAME = 'CHN_SSE'

SPIDER_MODULES = ['CHN_SSE.spiders']
NEWSPIDER_MODULE = 'CHN_SSE.spiders'


DBARGS = {
    'host': '10.100.4.99',
    'user': 'fcxfc',
    'passwd': 'admin123',
    'db': 'opd_common',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
    'autocommit': True
}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'CHN_SSE (+http://www.yourdomain.com)'
# USER_AGENT_LIST = [
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
#     'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
#     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
# ]

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
  'Referer': 'http://www.sse.com.cn/disclosure/listedinfo/regular/',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    # 'CHN_SSE.middlewares.ChnSseSpiderMiddleware': 543,
#     'CHN_SSE.middlewares.MyproxyMiddleware': 543,
#     'CHN_SSE.middlewares.MyUserAgentMiddleware': 553
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'CHN_SSE.middlewares.ChnSseDownloaderMiddleware': 543,
    'CHN_SSE.middlewares.MyproxyMiddleware': 543,
    'CHN_SSE.middlewares.MyUserAgentMiddleware': 553
}

# 去重器
# DUPEFILTER_CLASS = 'scrapy.dupefilter.RFPDupeFilter'
# DUPEFILTER_DEBUG = False
# 保存反问记录的日志路径
# JOBDIR = ""


# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'CHN_SSE.pipelines.DeFaultValuePipeline': 310,
    'CHN_SSE.pipelines.ChnSsePipeline': 320,
    # 'CHN_SSE.pipelines.DuplicatesPipeline': 330,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# PROXY_URL = 'http://http.tiqu.alicdns.com/getip3?num=400&type=1&pro=0&city=0&yys=0&' \
#           'port=11&pack=65959&ts=0&ys=0&cs=0&lb=4&sb=0&pb=45&mr=2&regions='

PROXY_URL = 'http://http.tiqu.alicdns.com/getip3?num=1&type=2&pro=0&city=0&yys=0' \
            '&port=11&pack=65959&ts=0&ys=0&cs=0&lb=4&sb=0&pb=45&mr=2&regions='

IP_PATH = 'E:\Restructure\CHN_SSE\CHN_SSE\samples\ip_proxy.txt'
