# -*- coding: utf-8 -*-
import scrapy

import sys
import re
reload(sys)

sys.setdefaultencoding('utf-8')

from ..items import *

class QuotesSpider(scrapy.Spider):
    allowed_domains = ['otodom.pl']
    name = "otodom"
    start_urls = [
        'https://www.otodom.pl/wynajem/mieszkanie/wroclaw/?search%5Bdist%5D=0&search%5Bcity_id%5D=39'
    ]

    PATH_DISTRICT = '''//div[@class='article-offer']/section[@class='section-offer-title']/div[@class='container-fluid container-fluid-sm container-fluid-sm-inset']/div[@class='row']/header[@class='col-md-offer-content']/address/p[@class='address-links']/a[3]/text()''' #np. stare miasto
    PATH_STREET = '''//div[@class='article-offer']/section[@class='section-offer-title']/div[@class='container-fluid container-fluid-sm container-fluid-sm-inset']/div[@class='row']/header[@class='col-md-offer-content']/address/p[@class='address-links']/a[4]/text()'''  #np. Podwale 82
    PATH_CITY = '''//div[@class='article-offer']/section[@class='section-offer-title']/div[@class='container-fluid container-fluid-sm container-fluid-sm-inset']/div[@class='row']/header[@class='col-md-offer-content']/address/p[@class='address-links']/a[2]/text()''' #Wroclaw

    PATH_SURFACE = '''//div[@class='col-md-offer-content']/ul[@class='params-list']/li[1]/ul[@class='main-list']/li[@class='param_m']/span/strong/text()'''
    PATH_DESCRIPTION = ''' //div[@class='row']/div[@class='col-md-offer-content']/div[@class='text-container hidden-text']/div[@class='text-contents']/div[@itemprop='description']''' #done
    PATH_PHOTHOS = '''//div[@class='gallery-box-thumbs hidden-print']/a/@href'''
    PATH_PRICE = '''//div[@class='box-price']/strong[@class='box-price-value no-estimates']/text()''' #done
    PATH_ADDED_DATE = '''//div[@class='row']/div[@class='col-md-offer-content']/div[@class='text-details clearfix']/div[@class='right']/p[1]/text()'''

    PATH_EQUIPMENT = '''//div[@class='article-offer']/section[@class='section-offer-params']/div[@class='container']/div[@class='row']/div[@class='col-md-offer-content']/ul[@class='params-list']/li[2]/ul[@class='dotted-list']'''
    PATH_ROOMS = '''//div[@class='row']/div[@class='col-md-offer-content']/ul[@class='params-list']/li[1]/ul[@class='main-list']/li[3]/span/strong/text()'''
    def parse(self, response):
        for href in response.xpath('//header[@class="offer-item-header"]/h3/a/@href').extract() :
            yield scrapy.Request(response.urljoin(href), callback=self.parseOffert)

#
 #       nextPage = response.xpath("//div[@class='after-offers clearfix']/nav[@class='pull-left']/form[@id='pagerForm']/ul[@class='pager']/li[2]/a/@href").extract_first()
#
 #       if nextPage is None:
  #          nextPage = response.xpath("//div[@class='after-offers clearfix']/nav[@class='pull-left']/form[@id='pagerForm']/ul[@class='pager']/li[3]/a/@href").extract_first()

        
#        print("nastepna sytona->>>>>>>>>>>>>>" + nextPage)
 #       if nextPage is not None:
  #          yield scrapy.Request(nextPage, callback=self.parse)
   #     else:
    #        print("strona nieprawidlowa ->>>>>>>>>>>>>>>>>>>>> " + nextPage)

    def parseOffert(self, response):

        def removeWhiteSpaces(string):
            return " ".join(string.split())

        def parseDate(oldData):
            splited = oldData.split();
            month = splited[1]
            if (month[:2] == "st"):
                monthId = "01"
            elif (month[:2] == "lu"):
                monthId = "02"
            elif (month[:2] == "ma"):
                monthId = "03"
            elif (month[:2] == "kw"):
                monthId = "04"
            elif (month[:2] == "ma"):
                monthId = "05"
            elif (month[:2] == "cz"):
                monthId = "06"
            elif (month[:2] == "li"):
                monthId = "07"
            elif (month[:2] == "si"):
                monthId = "08"
            elif (month[:2] == "wr"):
                monthId = "09"
            elif (month[:2] == "pa"):
                monthId = "10"
            elif (month[:2] == "li"):
                monthId = "11"
            elif (month[:2] == "gr"):
                monthId = "12"
            newDate = splited[2] + "-" + monthId + "-" + splited[0]
            return newDate;

        singleOffert = Offert()

        description = re.sub('<[^<]+?>', '', response.xpath(self.PATH_DESCRIPTION).extract_first()) #done
        equipment_from_path = response.xpath(self.PATH_EQUIPMENT).extract_first()
        if equipment_from_path != None:
            #equipment_list_with_spaces = re.sub('<[^<]+?>', '', response.xpath(self.PATH_EQUIPMENT).extract_first()) #almost done
            #equipment_list = removeWhiteSpaces(equipment_list_with_spaces) #and done - list like "zmywarka lodowka bla bla"
            furnitured = "tak" 
	else:
	    furnitured = "nie"


        price = response.xpath(self.PATH_PRICE).extract_first()
        number_of_rooms = response.xpath(self.PATH_ROOMS).extract_first()
        date_added_with_words = response.xpath(self.PATH_ADDED_DATE).extract_first()
        date_added = date_added_with_words[14:]  #data DD.MM.YYYY
        price = response.xpath(self.PATH_PRICE).extract_first()
        price_exactly = (price.split(':')[0])[:-3].replace(' ', '')
        photos = response.xpath(self.PATH_PHOTHOS).extract()
        city = response.xpath(self.PATH_CITY).extract_first()
        street = response.xpath(self.PATH_STREET).extract_first()
        district = response.xpath(self.PATH_DISTRICT).extract_first()
        surface = response.xpath(self.PATH_SURFACE).extract_first()


        singleOffert['internalId'] = "000000"
        singleOffert['portal'] = 'otodom'
        singleOffert['title'] = "tytu" #TODO
        singleOffert['city'] = city.encode('utf-8')
        singleOffert['url'] = response.url.encode('utf-8')
        singleOffert['subregion'] = "Dolnośląskie"
        singleOffert['district'] = district.encode('utf-8')
        singleOffert['price'] = price_exactly.encode('utf-8')
        singleOffert['surface'] = surface.encode('utf-8')
        singleOffert['floor'] = "2"; #TODO
        singleOffert['numberOfRooms'] = number_of_rooms.encode('utf-8')
        singleOffert['propertyType'] = "blok" #TODO
        singleOffert['furnitured'] = furnitured.encode('utf-8')
        singleOffert['advertsFrom'] = "Osoby prywatnej" #TODO
        singleOffert['description'] = description.encode('utf-8')
        singleOffert['addedDate'] = date_added.encode('utf-8') #GDY STARSZE NIZ 14 DNI TO POMIN ( NIE ZWRACAJ singleOffert )
        singleOffert['photos'] = photos

        print(singleOffert)
