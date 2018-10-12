# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd


class AreaSpiderPipeline(object):
    def __init__(self):
        self.data = []

    def process_item(self, item, spider):
        self.data.append(item)
        return item

    def close_spider(self, spider):
        print('datasize: %s' % len(self.data))
        pd.DataFrame(self.data).to_excel('./area.xlsx')
