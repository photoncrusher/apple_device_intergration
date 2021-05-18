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
from bs4 import BeautifulSoup
class XtvSpider(scrapy.Spider):
    name = 'xtv'
    # allowed_domains = ["thegioididong.com"]
    start_urls = ["https://www.xtmobile.vn/apple"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(1))
                assert(splash:runjs('try{document.getElementsByClassName("pagination-more")[0].getElementsByClassName("fa fa-caret-down")[0].click();}catch(e){}'))
                assert(splash:wait(1))
                assert(splash:runjs('try{document.getElementsByClassName("pagination-more")[0].getElementsByClassName("fa fa-caret-down")[0].click();}catch(e){}'))
                assert(splash:wait(1))
                return {
                    html = splash:html(),
                    url = splash:url(),
                }
            end
            """

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield SplashRequest(
                url,
                endpoint="render.html",
                callback=self.parse,
                headers=headers,
                meta={
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
                },
            )

    def parse(self, response):
        items = response.css('div.product-base-grid')
        for item in items:
            price = item.css('div.price::text').get()
            price = price[0:len(price) - 1] + ' VNĐ'
            link = 'https://www.xtmobile.vn' + item.css('h3')[0].css('a').attrib['href']
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            colors = soup.find('ul', class_='color-list-show').find_all('li')
            mau = ''
            for c in colors:
                mau += c.find('p').text + ' '

            thongtin = soup.find('ul', class_='parametdesc').find_all('strong')

            yield {
                'Tên sản phẩm': item.css('h3 a::text')[0].get(),
                'Giá sản phẩm': price,
                'Màu': mau,
                'Màn hình': thongtin[0].text,
                'Camera trước': thongtin[1].text,
                'Camera sau': thongtin[2].text,
                'Chip': thongtin[3].text,
                'Ram': thongtin[4].text,
                'Bộ nhớ trong': thongtin[5].text,
                'Thẻ sim': thongtin[6].text,
                'Pin': thongtin[7].text,
                'Hệ điều hành': thongtin[8].text
            }