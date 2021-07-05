# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import scrapy
from scrapy import signals
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from collections import defaultdict
import json
import random
import time

from scrapy.exceptions import NotConfigured

class LianjiahouseDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class LianjiahouseRandomHttpProxyMiddleware(HttpProxyMiddleware):
    def __init__(self, auth_encoding='latin-1', proxy_list_file=None):
        if not proxy_list_file:
            raise NotConfigured

        self.auth_encoding = auth_encoding
        # 分别用两个列表维护http和https的代理
        self.proxies = defaultdict(list)

        # 从json文件中读取代理服务器配置信息，填入self.proxies
        with open(proxy_list_file) as f:
            proxy_list = json.load(f)
            for proxy in proxy_list:
                scheme = proxy['proxy_scheme']
                url = proxy['proxy']
                self.proxies[scheme].append(self._get_proxy(url,scheme))

    @classmethod
    def from_crawler(cls, crawler):
        # 从配置文件读取用户验证信息的编码
        settings = crawler.settings
        auth_encoding = settings.get('HHTPPROXY_AUTH_ENCODING', 'lantain-1')

        # 从配置文件中读取代理服务器列表文件（json的路径）
        proxy_list_file = settings.get('HTTPPROXY_PROXY_LIST_FILE')

        return cls(auth_encoding, proxy_list_file)


    def _set_proxy(self, request, scheme):
        creds, proxy = random.choice(self.proxies[scheme])
        request.meta['proxy'] = proxy
        if creds:
            request.headers['Proxy-Authorization'] = b'Basic' + creds

class LianjiahouseSpiderMiddleware(object):
    """
    利用Scrapy数据收集功能，记录相同小区的数量
    """
    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(stats=crawler.stats)

    def process_spider_output(self, response, result, spider):
        """
        从item中获取小区名称，在数据收集其中记录相同小区数量
        :param response:
        :param result:
        :param spider:
        :return:
        """
        for item in result:
            if isinstance(item,scrapy.Item):
                # 从result中的item获取小区名称
                community_name = item['community_name']
                # 在数据统计中为相同的小区增加数量值
                self.stats.inc_value(community_name)
            yield item



# class ProxyMiddleWare(object):  
#     """docstring for ProxyMiddleWare"""  
#     def process_request(self,request, spider):  
#         '''对request对象加上proxy'''  
#         proxy = self.get_random_proxy()  
#         print("this is request ip:"+proxy)  
#         request.meta['proxy'] = proxy   # 对当前reque加上代理

#     def get_random_proxy(self):  
#         '''随机从文件中读取proxy'''  
#         while 1:  
#             with open('iplist.txt', 'r') as f: 
#                 proxies = f.readlines()  
#             if proxies:  
#                 break  
#             else:  
#                 time.sleep(1)  
#         proxy = random.choice(proxies).strip()
#         return proxy