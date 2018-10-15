#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author: liyinwei
@E-mail: coridc@foxmail.com
@Time: 2018/10/11 下午21:27
@Description: 国家统计局五级行政区划爬取
"""
from scrapy import Spider
from area_spider.items import AreaSpiderItem


class AreaSpider(Spider):
    name = "area_spider"

    allowed_domains = ['stats.gov.cn']

    start_urls = [
        'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html'
    ]

    def parse(self, response):
        """
        处理省份页面
        :param response:
        :return:
        """
        for sel in response.xpath('//tr[@class="provincetr"]/td/a'):
            item = AreaSpiderItem()
            item['code'] = sel.xpath('@href').extract()[0].split('.')[0] + '0000000000'
            item['name'] = sel.xpath('text()').extract()[0].strip()
            item['level'] = 'province'
            item['cls'] = ''
            yield item

        for href in response.xpath('//tr[@class="provincetr"]/td/a/@href'):
            yield response.follow(href, self.parse_city)

    def parse_city(self, response):
        """
        处理市级页面
        :param response:
        :return:
        """
        for sel in response.xpath('//tr[@class="citytr"]'):
            item = AreaSpiderItem()
            item['code'] = sel.xpath('td[1]/a/text()').extract()[0].strip()
            item['name'] = sel.xpath('td[2]/a/text()').extract()[0].strip()
            item['level'] = 'city'
            item['cls'] = ''
            yield item

        for href in response.xpath('//tr[@class="citytr"]/td[1]/a/@href'):
            yield response.follow(href, self.parse_county)

    def parse_county(self, response):
        """
        处理区县级页面
        :param response:
        :return:
        """
        for sel in response.xpath('//tr[@class="countytr"]'):
            item = AreaSpiderItem()

            code = sel.xpath('td[1]/a/text()').extract()
            name = sel.xpath('td[2]/a/text()').extract()
            if code:
                item['code'] = code[0].strip()
            else:
                continue

            if name:
                item['name'] = name[0].strip()
            else:
                continue

            item['level'] = 'county'
            item['cls'] = ''
            yield item

        for href in response.xpath('//tr[@class="countytr"]/td/a/@href'):
            yield response.follow(href, self.parse_town)

    def parse_town(self, response):
        """
        处理乡镇/街道级页面
        :param response:
        :return:
        """
        for sel in response.xpath('//tr[@class="towntr"]'):
            item = AreaSpiderItem()
            item['code'] = sel.xpath('td[1]/a/text()').extract()[0].strip()
            item['name'] = sel.xpath('td[2]/a/text()').extract()[0].strip()
            item['level'] = 'town'
            item['cls'] = ''
            yield item

        for href in response.xpath('//tr[@class="towntr"]/td/a/@href'):
            yield response.follow(href, self.parse_village)

    def parse_village(self, response):
        """
        处理村/居委会级页面
        :param response:
        :return:
        """
        for sel in response.xpath('//tr[@class="villagetr"]'):
            item = AreaSpiderItem()
            item['code'] = sel.xpath('td[1]/text()').extract()[0].strip()
            item['name'] = sel.xpath('td[3]/text()').extract()[0].strip()
            item['level'] = 'village'
            item['cls'] = sel.xpath('td[2]/text()').extract()[0].strip()
            yield item
