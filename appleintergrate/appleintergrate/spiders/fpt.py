from os import name
import scrapy
from scrapy.http import HtmlResponse
from scrapy.item import Field
from appleintergrate.items import IpadItem
import json
import datetime
import re
import requests

class FptSpider(scrapy.Spider):
    name = 'fpt'
    allowed_domains = ['fptshop.com.vn']
    base_url = ['https://fptshop.com.vn/apple/ipad']
    start_url = 'https://fptshop.com.vn'
    def start_requests(self):
        for url in self.base_url:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, *args, **kwargs):
        product_paths = response.xpath('//div[contains(@class,"product-grid")]/div[contains(@class,"product product-grid__item product--absolute")]/div[contains(@class,"product_img")]/a/@href').getall()
        for product_path in product_paths:
            url = self.start_url + product_path
            yield scrapy.Request(url=url, callback=self.parse_product)
            
    def parse_product(self, response):
        features = response.xpath('//table[@class = "st-pd-table"]/tbody/tr/td/span/text()').getall()
        data = IpadItem()
        if features != []:
            try:
                data = IpadItem(
                        name = response.xpath('//h1[@class="st-name"]/text()').getall()[0],
                        screen = features[0],
                        panel = features[0],
                        CPU = features[5],
                        ROM = features[4],
                        RAM = features[3],
                        rear_cam = features[1],
                        front_cam = features[2],
                        SIM = features[8],
                        security = '',
                        weigth = '',
                        operatingsys = features[9],
                        warranty = features[11],
                        status = "new",
                        available = 1
                )
            except:
                pass
        if features == []:
            features = response.xpath('//ul[@class = "detail-rm9 active "]/li/span/text()').getall()
            for i in range(0,int(len(features)/2)):
                data.fields[features[2*i]] = Field()
                data[features[2*i]] = features[2*i+1]
            print(data)
        if data != []:
            yield data
        else:
            pass
        