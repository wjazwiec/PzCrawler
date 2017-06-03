# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HousesforrentCrawlersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Offert(scrapy.Item):
     url = scrapy.Field()
     title = scrapy.Field()
     city = scrapy.Field()
     subregion = scrapy.Field()
     district = scrapy.Field()
     portal = scrapy.Field()
     addedTime = scrapy.Field()
     addedDate = scrapy.Field()
     internalId = scrapy.Field()
     description = scrapy.Field()
     photos = scrapy.Field()
     price = scrapy.Field()
     surface = scrapy.Field()
     floor = scrapy.Field()
     numberOfRooms = scrapy.Field()
     propertyType = scrapy.Field()
     furnitured = scrapy.Field()
     advertsFrom = scrapy.Field()
