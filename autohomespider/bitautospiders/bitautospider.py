# -*- coding: utf-8 -*-
import json
import scrapy
import re
from scrapy.selector import Selector
from  myproject.items import  MyprojectItem
try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as sle
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request
from  myproject.spiders.DecodeScript import DecodeScript
from myproject.spiders.DecodeFontFile import DecodeFontFile
from scrapy_splash import SplashRequest
class bitautospider(CrawlSpider):
    name = 'bitautospider'
    # 评论的个数
    count = 0
    allowed_domains = ['bitauto.com']
    # start_urls = ['https://k.autohome.com.cn/314']
    start_urls = ['http://car.bitauto.com/kaimeirui/koubei/gengduo/1991-0-0-0-0-0-0-0-0-0-0--1-10.html']

    def start_requests(self):  # 重新定义起始爬取点
        for url in self.start_urls:
          yield SplashRequest(url, args={'timeout': 8, 'images': 0},magic_response=True)

    def parse(self, response):
        print(response.text)



if __name__ == '__main__':
    from scrapy import cmdline
    args = "scrapy crawl bitautospider".split()
    cmdline.execute(args)
