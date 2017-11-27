# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CmicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    image_urls = scrapy.Field()
    # images = scrapy.Field()
    image_paths = scrapy.Field()
    comic_name = scrapy.Field()
    comic_hui = scrapy.Field()
    img_order = scrapy.Field()
    file_hash = scrapy.Field()
    web_path_sha1 = scrapy.Field()
    web_path = scrapy.Field()
    local_path = scrapy.Field()
    create_date = scrapy.Field()
    pass




