#!/usr/bin/env python
# encoding: utf-8

import re
import json

from scrapy.contrib.spiders import CrawlSpider
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from scrapy.selector import Selector

from bs4 import BeautifulSoup

from lovematters.items import LoveMattersItem
from misc.log import (
    warn, info
)
from misc.utils import (
    iso_time_to_utc_timestamp
)


class LoveMattersSpider(CrawlSpider):

    name = "lovematters"
    allowed_domains = ["lovematters.cn"]
    start_urls = [
        "http://lovematters.cn/",         #
        # "http://lovematters.cn/category/5",
        # "http://lovematters.cn/news/4431"
        # "http://lovematters.cn/news/3176"
        # "http://lovematters.cn/tags/342"
    ]

    rules = [
        # Rule(sle(allow=("/news/\d+/?$")), callback='parse_blog_detail'),
        Rule(sle(allow=("/news/\d+/?$")), callback='parse_blog_detail', follow=True),
        Rule(sle(allow=("/resource/\d+/?$")), callback='parse_blog_detail', follow=True),
        Rule(sle(allow=("/term/\d+/?$")), callback='parse_blog_detail', follow=True),
        Rule(sle(allow=("/category/\d+\?page=\d+$", )), callback='parse_blog_list', follow=True),
        Rule(sle(allow=("/tags/\d+\?$", )), callback='parse_blog_list', follow=True),
    ]

    http_prefix = re.compile('^(http|https)')

    base_url = 'http://lovematters.cn'

    def is_p_type(self, raw_item):

        pattern = re.compile(r'<p>')

        if pattern.match(raw_item.extract()):

            return True

        return False

    def is_img_type(self, raw_item):
        pattern = re.compile(r'^<img')

        if pattern.match(raw_item.extract()):
            return True

        return False

    def prepare_content(self, response):

        result = []

        soup = BeautifulSoup(response.body_as_unicode())

        post_content = soup.select('#main-content article div.content div.field-type-text-with-summary')[0]

        for item in post_content.findChildren(recursive=False):
            content = ""

            for node in item.contents:

                if node.name == 'br':
                    if content:
                        result.append(self._prepare_text_content(content))
                    content = ""
                    continue

                if node.name == 'img':
                    url = node['src']
                    result.append(self._prepare_img_content(url))
                    content = ""
                    continue

                if node.name == 'div':
                    img_list = node.find_all('img')
                    if len(img_list) > 0:
                        img_node = img_list[0]
                        url = img_node['src']
                        result.append(self._prepare_img_content(url))
                        content = ""
                        continue

                try:
                    concat_str = node.string
                    if not concat_str:
                        concat_str = node.get_text()
                except:
                    warn('failed to parse node %s' % node)

                content = content + concat_str

            if content:
                result.append(self._prepare_text_content(content))

        for item in result:
            print item['content']

        return result

    # TODO mark down what we have visit
    def parse_blog_list(self, response):
        info('process blog list response' + str(response.url))

    def parse_blog_detail(self, response):
        info('process blog list response' + str(response.url))
        sel = Selector(response)

        header = sel.css('#main-content article header')
        desc_img = self._prepare_desc_img(header)
        source_created, author, raw_description = self._prepare_copy_right(header)
        description = self._prepare_description(raw_description)

        # content = sel.css('#main-content article div.content div.field-type-text-with-summary')
        title = "".join(sel.css('#main-content h1.page-title').xpath('./text()').extract()).strip()

        item = LoveMattersItem()
        # prepare basic info
        item['base_url'] = self.base_url
        item['source_url'] = response.url
        item['title'] = title

        # prepare content
        result = self.prepare_content(response)
        result.insert(0, desc_img)
        result.insert(0, description)
        item['content'] = json.dumps(result)

        item['author'] = author
        item['source_created'] = source_created

        # prepare comment
        item['comment'] = self.prepare_comment(sel)

        # get comment num
        item['comment_num'] = 0

        # get view num
        item['view_num'] = 0

        # get like num
        item['like_num'] = 0

        # get like num
        item['forward_num'] = 0

        # get play num
        item['play_num'] = 0

        yield item

    # TIPS no comment, so stop to write more code
    def prepare_comment(self, sel):
        result = []

        return json.dumps(result)

    def _prepare_copy_right(self, header):

        author = ''.join(header.css('p.copyright').xpath('./a[1]//text()').extract()).strip()
        description = ''.join(header.xpath('//div[@class="node-description"]/text()').extract()).strip()
        source_created = ''.join(header.css('p.copyright').xpath('./time/@datetime').extract())

        source_created = iso_time_to_utc_timestamp(source_created)

        return source_created, author, description

    def _prepare_desc_img(self, header):

        img_url = ''.join(header.css('div.node-image img').xpath('./@src').extract()).strip()

        if not self.http_prefix.match(img_url):
            desc_img = self.base_url + img_url
        else:
            desc_img = img_url

        return {
            "content": {
                "url": desc_img,
                "height": 0,
                "width": 0,
            },
            "type": "image"
        }

    def _prepare_description(self, raw_description):

        return {"content": raw_description, "type": "text"}

    def _prepare_text_content(self, content):
        return {
            "content": content,
            "type": "text"
        }

    def _prepare_img_content(self, url):

        if not self.http_prefix.match(url):
            real_url = self.base_url + url
        else:
            real_url = url

        return {
            "type": "image",
            "content": {
                "url": real_url,
                "width": 0,
                "height": 0
                }
            }
