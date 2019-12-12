#! /usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':
    setting = get_project_settings()
    process = CrawlerProcess(setting)
    WorkSpider = ['HKEX_origin_info_update']

    for spider_name in process.spiders.list():
        if spider_name not in WorkSpider:
            continue
        print("Running spider %s" % (spider_name))
        process.crawl(spider_name)
    process.start()