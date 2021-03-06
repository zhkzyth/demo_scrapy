#!/usr/bin/env python
# encoding: utf-8

from scrapy.selector import Selector

try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle


from template.items import *
from misc.log import *
from misc.spider import CommonSpider


class templateSpider(CommonSpider):
    name = "template"
    allowed_domains = ["template.com"]
    start_urls = [
        "http://www.template.com/",
    ]
    rules = [
        Rule(sle(allow=("/topsites/category;?[0-9]*/Top/World/Chinese_Simplified_CN/.*$")), callback='parse', follow=True),
    ]

    def parse(self, response):
        info('Parse '+response.url)
        # self.parse_with_rules(response, self.css_rules, templateItem)
