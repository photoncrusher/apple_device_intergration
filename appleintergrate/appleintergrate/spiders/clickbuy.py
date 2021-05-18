from os import name
import scrapy
from scrapy.http import HtmlResponse
from scrapy.item import Field
from appleintergrate.items import IpadItem
from scrapy_splash import SplashRequest
import json
import datetime
import re
import requests

class ClickbuySpider(scrapy.Spider):
    name = 'clickbuy'
    start_urls = ["https://clickbuy.com.vn/?s=apple&post_type=product"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(1))
                assert(splash:runjs('for(var i = 0 ; i < 10 ; i ++){document.getElementById("sb-infinite-scroll-load-more-1").getElementsByTagName("a")[0].click();}'))
                assert(splash:wait(1))
                return {
                    html = splash:html(),
                    url = splash:url(),
                }
            end
            """

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url,
                callback=self.parse,
                meta={
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
                },
            )

    def parse(self, response):
        product_paths = response.xpath('//*[@class="style-flex-colum col-6 col-sm-4 col-lg-4 ex_p2"]/a/@href').getall()
        for product_path in product_paths:
            url = product_path
            yield scrapy.Request(url=url, callback=self.parse_product)
            
    def parse_product(self, response):
        features_label = response.xpath('//*[@class="woocommerce-product-attributes shop_attributes"]/tbody/tr/th/text()').getall()
        storage = response.xpath('//*[@class="woocommerce-product-attributes shop_attributes"]/tbody/tr/td/p/a/text()').getall()
        features = response.xpath('//*[@class="woocommerce-product-attributes shop_attributes"]/tbody/tr/td/p/text()').getall()
        data = IpadItem()
        for i in range(1,int(len(features)/2)):
            data.fields[features[i]] = Field()
            data[features[i]] = features[i-1]
        for j in storage:
            data.fields[features[0]] = Field()
            data[features[0]] = j
        print(data)
        yield data
