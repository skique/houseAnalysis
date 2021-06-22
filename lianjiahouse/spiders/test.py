import scrapy
from scrapy import Request
import json

class TestRandomProxySpider(scrapy.Spider):
    name = "test_random_proxy"

    def start_requests(self):
        for _ in range(30):
            yield Request('http://httpbin.org/ip', dont_filter=True)
            yield Request('https://httpbin.org/ip', dont_filter=True)

    def parse(self, response):
        # print('ip代理设置成功')
        print('ip代理设置成功%s'%json.loads(response.text))