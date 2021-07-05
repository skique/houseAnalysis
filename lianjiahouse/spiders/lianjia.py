# -*- coding: utf-8 -*-
import scrapy
import requests
import re
import time
import math
from lxml import etree
from lianjiahouse.items import LianjiaItem
# from scrapy_redis.spiders import RedisSpider

class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    # redis_key = 'lianjiaspider:urls'
    start_urls = 'https://hz.lianjia.com/ershoufang/'

    def start_requests(self):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 \
                         Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': user_agent}
        yield scrapy.Request(url=self.start_urls, headers=headers, method='GET', callback=self.parse)

    def parse(self, response):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 \
                                 Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': user_agent}
        lists = response.body.decode('utf-8')
        selector = etree.HTML(lists)
        area_list = selector.xpath('//div[@class="m-filter"]//div[@data-role="ershoufang"]//a')
        for area in area_list:
        # area = area_list[0]
            try:
                area_han = area.xpath('text()').pop()    # 地点

                area_pin = area.xpath('@href').pop().split('/')[2]   # 拼音
                area_url = 'https://hz.lianjia.com/ershoufang/{}/'.format(area_pin)
                print(area_url)
                yield scrapy.Request(url=area_url, headers=headers, callback=self.detail_url, meta={"id1":area_han,"id2":area_pin} )
            except Exception:
                pass

    def findTrueScript(self, scripts):
        for str in scripts:
            if 'resblockPosition' in str:
                return str


    def get_latitude(self,url):  # 进入每个房源链接抓经纬度
        p = requests.get(url)
        contents = etree.HTML(p.content.decode('utf-8'))
        scripts = contents.xpath('/html/body/script/text()')
        latitude = self.findTrueScript(scripts)
        time.sleep(3)
        regex = '''resblockPosition(.+)'''
        items = re.search(regex, latitude)
        content = items.group()[:-1]  # 经纬度
        longitude_latitude = content.split(':')[1]
        return longitude_latitude[1:-1]

    def detail_url(self,response):
        # 'https://hz.lianjia.com/ershoufang/dongcheng/pg2/'
        lists = response.body.decode('utf-8')
        selector = etree.HTML(lists)
        total = selector.xpath('//*[@id="content"]/div[1]/div[2]/h2/span/text()').pop().strip()
        print(total)
        total = int(total)
        # 页码大于100时，取100
        totalPages = math.ceil(total/30) if math.ceil(total/30) < 100 else 100
        for i in range(1, totalPages):
            url = 'https://hz.lianjia.com/ershoufang/{}/pg{}/'.format(response.meta["id2"],str(i))
            time.sleep(2)
            try:
                contents = requests.get(url)
                contents = etree.HTML(contents.content.decode('utf-8'))
                houselist = contents.xpath('//*[@id="content"]//div[@class="leftContent"]//ul[@class="sellListContent"]/li')
                for house in houselist:
                    try:
                        item = LianjiaItem()
                        item['title'] = house.xpath('div[1]/div[1]/a/text()').pop()
                        item['community'] = house.xpath('div[1]/div[2]/div/a[1]/text()').pop()
                        item['houseInfo'] = house.xpath('div[1]//div[@class="houseInfo"]//text()').pop()
                        item['model'] = house.xpath('div[1]//div[@class="houseInfo"]//text()').pop().split('|')[0]
                        item['area'] = house.xpath('div[1]//div[@class="houseInfo"]//text()').pop().split('|')[1]
                        item['focus_num'] = house.xpath('div[1]/div[4]/text()').pop().split('/')[0]
                        # item['watch_num'] = house.xpath('div[1]/div[4]/text()').pop().split('/')[1]
                        item['time'] = house.xpath('div[1]/div[4]/text()').pop().split('/')[1]
                        item['price'] = house.xpath('div[1]/div[6]/div[1]/span/text()').pop()
                        item['average_price'] = house.xpath('div[1]/div[6]/div[2]/span/text()').pop()
                        item['link'] = house.xpath('div[1]/div[1]/a/@href').pop()
                        item['city'] = response.meta["id1"]
                        self.url_detail = house.xpath('div[1]/div[1]/a/@href').pop()
                        item['Latitude'] = self.get_latitude(self.url_detail)
                    except Exception:
                        pass
                    yield item
            except Exception:
                pass