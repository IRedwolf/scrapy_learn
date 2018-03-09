# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst


class ToscrapeItemload(ItemLoader):
    default_output_processor = TakeFirst()


def stock_num_re(value):
    return int(value[10:-10])


def rating_map(value):
    review_num = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5,
    }
    if value: return review_num.get(value)
    else: return 0


class ToscrapeBookItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    price = scrapy.Field()
    upc = scrapy.Field()
    review_num = scrapy.Field()
    stock = scrapy.Field(
        input_processor=MapCompose(stock_num_re)
    )

