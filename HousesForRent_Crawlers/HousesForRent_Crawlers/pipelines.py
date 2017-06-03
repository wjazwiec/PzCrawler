# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import logging


class HousesforrentCrawlersPipeline(object):
    def process_item(self, item, spider):
        return item

class MySQLStorePipeline(object):

    host = 'serwer1696876.home.pl'
    user = '22342754_0000001'
    password = 'pietraszko666'
    db = '22342754_0000001'

    def __init__(self):
        self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db )
        self.cursor = self.connection.cursor()
        self.connection.set_character_set('utf8')
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')

    def process_item(self, item, spider):   
        try:
            self.cursor.execute("""INSERT IGNORE  INTO 22342754_0000001.adverts(idOriginal, portal, title, city, link, province, subregion, price, surface, floor, numberOfBedrooms, propertyType, furnitured, advertsFrom, description, dateAdded )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                           (
                            item['internalId'],
                            item['portal'],
                            item['title'],
                            item['city'],
                            item['url'],
                            item['subregion'],
                            item['district'],
                            item['price'],
                           # item['attributes'].get('surface'),
                           # item['attributes'].get('Poziom',''),
                           # item['attributes'].get('Powierzchnia',''),
                           # item['attributes'].get('Rodzaj zabudowy',''),
                           # item['attributes'].get('Umeblowane',''),
                           # item['attributes'].get('Oferta od',''),
                            item['surface'],
                            item['floor'],
                            item['numberOfRooms'],
                            item['propertyType'],   
                            item['furnitured'],
                            item['advertsFrom'],
                            item['description'],
                            item['addedDate']

                              ))
            self.connection.commit()
            lastrow = self.cursor.lastrowid;
            
            for photo in item['photos']:
                 self.cursor.execute('''INSERT INTO 22342754_0000001.photos(idAdverts, portal, photoLink) VALUES (%s, %s, %s)''',(lastrow, 'olx', photo))
            self.connection.commit()    
            logging.warning("Succesfully added")
            
        except MySQLdb.Error, e:
            logging.warning(e)
            return item
