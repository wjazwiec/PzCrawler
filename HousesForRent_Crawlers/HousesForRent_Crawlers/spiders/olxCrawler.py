# -*- coding: utf-8 -*-
import scrapy

import sys
import re
reload(sys)

sys.setdefaultencoding('utf-8')

from ..items import *

import const

class OlxCrawlerSpider(scrapy.Spider):
    name = "olxCrawler"
    allowed_domains = ["olx.pl"]
    start_urls = [
        'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/wroclaw/?page=2'
    ]
    
    def parse(self, response):
        
        for href in response.xpath(const.OLX_PATH_TO_OFFERT_LINK).extract():
            if re.match( ".*olx.*", href):
                yield scrapy.Request(response.urljoin(href), callback=self.parseOffert)
           
        nextPage = response.xpath(const.OLX_NEXT_PAGE_PATH).extract_first()
        
        if nextPage is not None:
            yield scrapy.Request(nextPage, callback=self.parse)



    
    def parseOffert(self, response):

        def removeWhiteSpaces(string):
            return " ".join(string.split()) 
        

        def parseDate(oldData):
            splited = oldData.split(' ');
            month = splited[1]
            monthId="";
            
            if(month[:2] == "st"):
                monthId = "01"
            elif(month[:2] == "lu"):
                monthId = "02"
            elif(month[:3] == "mar"):
                monthId = "03"
            elif(month[:2] == "kw"):
                monthId = "04"
            elif(month[:3] == "maj"):
                monthId = "05"
            elif(month[:2] == "cz"):
                monthId = "06"
            elif(month[:2] == "li"):
                monthId = "07"
            elif(month[:2] == "si"):
                monthId = "08"
            elif(month[:2] == "wr"):
                monthId = "09"
            elif(month[:2] == "pa"):
                monthId = "10"
            elif(month[:2] == "li"):
                monthId = "11"
            elif(month[:2] == "gr"):
                monthId = "12"
            newDate = splited[2]+"-"+monthId+"-"+splited[0]
            return newDate;

        
        singleOffert = Offert()
        
        location = response.xpath(const.OLX_PATH_LOCATION).extract_first().split(',')
        added = response.xpath(const.OLX_DATETIME_NEW_PATH).extract()

        reg = re.compile(".*(\d{2}:\d{2}), (.*),.*");
        for elem in added:
            date_search = reg.search(elem)
            if(date_search):
                time = date_search.group(1)
                date = date_search.group(2)
        
        
        description = response.xpath(const.OLX_PATH_DESCRIPTION).extract()
        addedDescription = ' '.join(description)
        photos = response.xpath(const.OLX_PATH_PHOTHOS).extract();
        price = response.xpath(const.OLX_PATH_PRICE).extract_first();
        price_exactly = (price.split(':')[0])[:-3].replace(' ','')
        internalId = response.xpath(const.OLX_PATH_INTERNAL_ID).extract_first()    
        attributes = response.xpath(const.OLX_PATH_ATTRIBUTES)
        a =attributes.xpath('//table/tr/th/text()').extract()
        b =attributes.xpath('//table/tr/td/strong/a/text()').extract()
        dictAttributes = {}
        for i in range(0,len(a)-1):
            dictAttributes[a[i].encode('utf-8')] = removeWhiteSpaces(b[i]).encode('utf-8')
        surface = removeWhiteSpaces(response.xpath(const.OLX_SURFACE_NEW_PATH).extract_first())[:-2]
        
        singleOffert['title'] = response.css('title::text').extract_first().encode('utf-8')[:-10]
        singleOffert['url'] = response.url.encode('utf-8')
        singleOffert['city'] = location[0].encode('utf-8')
        singleOffert['subregion'] = removeWhiteSpaces(location[1]).encode('utf-8')
        singleOffert['district'] = removeWhiteSpaces(location[2]).encode('utf-8')
        singleOffert['portal'] = 'olx'
        singleOffert['addedTime'] = time.encode('utf-8')
        singleOffert['addedDate'] = parseDate(date).encode('utf-8')
        singleOffert['internalId'] = removeWhiteSpaces(internalId)[15:].encode('utf-8')
        singleOffert['description'] = removeWhiteSpaces(addedDescription).encode('utf-8')
        singleOffert['photos'] = photos
        singleOffert['price'] = price_exactly.encode('utf-8')
        singleOffert['surface'] = surface.encode('utf-8')
        singleOffert['floor'] = dictAttributes.get('Poziom','')
        singleOffert['numberOfRooms'] = dictAttributes['Powierzchnia']
        singleOffert['propertyType'] = dictAttributes['Rodzaj zabudowy']
        singleOffert['furnitured'] = dictAttributes['Umeblowane']
        singleOffert['advertsFrom'] = dictAttributes['Oferta od']
        return singleOffert

    
