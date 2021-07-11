# -*- coding: utf-8 -*-
import scrapy
import requests
import time
from lxml import etree
from lianjiahouse.items import ZufangItem

import json
from math import radians, cos, sin, asin, sqrt 
import requests


class LianjiaSpider(scrapy.Spider):
    name = 'lianjiazufang'
    start_urls = 'https://hz.lianjia.com/zufang/yuhang/'
    myPlace = '杭州市余杭区微洱大厦'

    def start_requests(self):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 \
                         Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': user_agent}
        yield scrapy.Request(url=self.start_urls, headers=headers, method='GET', callback=self.parse)

    def parse(self, response):
        container_area = ['未来科技城','闲林', '西溪', '临平', '翡翠城']
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 \
                                 Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': user_agent}
        lists = response.body.decode('utf-8')
        selector = etree.HTML(lists)
        area_list = selector.xpath('//div[@class="filter"]//ul[@data-target="area"][2]//li[@data-type="bizcircle"]//a')
        for area in area_list:
        # area = area_list[0]
            try:
                area_han = area.xpath('text()').pop()    # 地点
                if area_han in container_area: # 只解析想要的地区
                    area_pin = area.xpath('@href').pop().split('/')[2]   # 拼音
                    area_url = 'https://hz.lianjia.com/zufang/{}/'.format(area_pin)
                    print(area_url)
                    yield scrapy.Request(url=area_url, headers=headers, callback=self.detail_url, meta={"id1":area_han,"id2":area_pin} )
                else:
                    pass
            except Exception:
                pass


    def detail_url(self,response):
        lists = response.body.decode('utf-8')
        selector = etree.HTML(lists)
        total = selector.xpath('//*[@class="content__pg"]/@data-totalpage').pop()
        print(total)
        total = int(total)
        totalPages = total
        for i in range(1, totalPages):
            url = 'https://hz.lianjia.com/zufang/{}/pg{}/'.format(response.meta["id2"],str(i))
            time.sleep(2)
            try:
                contents = requests.get(url)
                contents = etree.HTML(contents.content.decode('utf-8'))
                container_xpath = '//*[@class="content__list"]//*[@class="content__list--item"]'
                houselist = contents.xpath(container_xpath)
                
                ak = 'fqIjTkn3QPOnfdqonGfcEBT7IalMd7Vn'

                for house in houselist:
                    try:
                        item = ZufangItem()
                        ad = house.xpath('a[2]/p[@class="content__list--item--ad"]')
                        isAd = 1 if len(ad) else 0
                        item['advertisement'] = isAd
                        item['title'] = ''.join(house.xpath('div[1]/p[1]/a//text()')).replace('\n', '').replace(' ', '')
                        
                        item['link'] = house.xpath('div[1]/p[1]/a/@href').pop()
                        item['city'] = response.meta["id1"]

                        item['url'] = url
                        
                        if isAd != 1:
                            item['community'] = ''.join(house.xpath('div[1]/p[2]/a/text()')).strip()
                            item['price'] = house.xpath('div[1]/span[1]/em/text()').pop()

                            info = house.xpath('div[1]/p[2]/text()')
                            item['houseInfo'] = ''.join(house.xpath('div[1]/p[2]/text()')).replace('\n', '').replace(' ', '')
                            item['area'] = info[4].replace('\n', '').replace(' ', '')
                            item['direction'] = info[5].replace('\n', '').replace(' ', '')
                            item['layout'] = info[6].replace('\n', '').replace(' ', '')
                            
                            item['time'] = ''.join(house.xpath('div[1]/p[4]/span/text()')).strip()
                        else:
                            item['community'] = house.xpath('div[1]/p[4]/span[1]/text()').pop().strip()
                            item['houseInfo'] = ''.join(house.xpath('div[1]/p[2]/text()')).replace('\n', '').replace(' ', '')
                            
                            item['time'] = house.xpath('div[1]/p[4]/span/text()').pop().strip()

                        

                        place1=item['community']
                        place2=self.myPlace
                        try:
                            lat,lng = self.getPosition(ak,place1)
                            item['lat'] = lat
                            item['lng'] = lng
                            item['distance'] = self.calDistance(ak,place1,place2)
                        except Exception as e:
                            item['distance'] = ''
                            print(e)
                    except Exception:
                        pass
                    yield item
            except Exception:
                pass

    #根据地址返回经纬度 
    def getPosition(self, ak, dw):
        url = 'http://api.map.baidu.com/geocoding/v3/?address={Address}&output=json&ak={Ak}'.format(Address=dw, Ak=ak)
        res = requests.get(url)
        json_data = json.loads(res.text)
        if json_data['status'] == 0:
            lat = json_data['result']['location']['lat']  # 纬度
            lng = json_data['result']['location']['lng']  # 经度
        else:
            print("Error output!")
            print(json_data)
            return json_data['status']
        return lat,lng

    # 根据经纬度计算距离
    def calDistance(self, ak,place1,place2):
        '''
        输入两个地点名，输出直线距离(千米)
        place1：地点1
        place2：地点2
        '''
        lat1,lng1 = self.getPosition(ak,place1)#经纬度1
        lat2,lng2 = self.getPosition(ak,place2)#经纬度2
        lng1, lat1, lng2, lat2 = map(radians, [float(lng1), float(lat1), float(lng2), float(lat2)]) # 经纬度转换成弧度
        dlon=lng2-lng1
        dlat=lat2-lat1
        a=sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        distances =2*asin(sqrt(a))*6371*1000 # 地球平均半径，6371km
        distance= round(distances/1000,3)
        return distance