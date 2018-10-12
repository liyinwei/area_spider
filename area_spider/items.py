# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AreaSpiderItem(scrapy.Item):
    # 行政区划编码
    code = scrapy.Field()
    # 行政区划名称
    name = scrapy.Field()
    # 省、市、区/县、乡镇/街道、村
    level = scrapy.Field()
    # 城乡分类代码 仅村级别有
    cls = scrapy.Field()
