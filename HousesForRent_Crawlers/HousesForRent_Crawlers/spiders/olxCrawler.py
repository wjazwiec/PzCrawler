# -*- coding: utf-8 -*-
import scrapy

import sys
reload(sys)

sys.setdefaultencoding('utf-8')

import const

class OlxCrawlerSpider(scrapy.Spider):
    name = "olxCrawler"
    allowed_domains = ["olx.pl"]
    start_urls = [
        'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/wroclaw/?page=1'
    ]
    

    def parse(self, response):
        pass
