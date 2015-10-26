#!/usr/bin/env python
# encoding: utf-8

from bs4 import BeautifulSoup

soup = BeautifulSoup(
    """<strong>夹腿的动作通过给<a href="http://lovematters.cn/tags/238">阴蒂</a>间接的获得挤压和摩擦的刺激，"""
    """让女性获得性高潮，是一个非常普遍的女性自慰动作，本身没有任何不健康不卫生的因素。</strong>""")

t = soup.contents[0]

print t.get_text()
