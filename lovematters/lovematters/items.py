#!/usr/bin/env python
# encoding: utf-8
import scrapy


class LoveMattersItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    comment = scrapy.Field()
    author = scrapy.Field()
    source_url = scrapy.Field()
    base_url = scrapy.Field()
    source_type = scrapy.Field()
    source_created = scrapy.Field()
    view_num = scrapy.Field()
    like_num = scrapy.Field()
    forward_num = scrapy.Field()
    play_num = scrapy.Field()
    comment_num = scrapy.Field()
    created = scrapy.Field()
    updated = scrapy.Field()
