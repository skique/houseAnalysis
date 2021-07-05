import scrapy
from scrapy import Request
import json

class TestRandomProxySpider(scrapy.Spider):
    name = "test_random_proxy"

    def start_requests(self):
        for _ in range(30):
            # yield Request('http://httpbin.org/ip', callback=self.httpParse, dont_filter=True)
            yield Request('https://httpbin.org/ip', callback=self.httpsParse, dont_filter=True)

    def httpParse(self, response):
        # print('ip代理设置成功')
        print('http代理设置成功%s'%json.loads(response.text))

    def httpsParse(self, response):
        # print('ip代理设置成功')
        print('https代理设置成功%s'%json.loads(response.text))