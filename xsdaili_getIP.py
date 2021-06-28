import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import json

class Proxies(object):

    """docstring for Proxies"""
    def __init__(self):
        self.proxies = []
        self.verify_pro = []
        self.headers = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }
        self.get_proxies()

    #获取IP
    def get_proxies(self):
        url = 'http://www.xsdaili.cn/dayProxy/ip/2983.html'#可以更改网页最新链接抓取
        html = requests.get(url, headers=self.headers).content
        soup = BeautifulSoup(html, 'lxml')
        br = str(soup.find(attrs={'class':'cont'}))
        ip = re.findall('(\d*\d\.\d*\.\d*\.\d*\:\d*@[A-Z]*)',br)
        for odd in ip:
            # ip_dict = {}
            # ip_dict[str(odd.split('@')[1]).lower()] = odd.split('@')[0]
            # self.proxies.append(ip_dict)
            proxy_scheme = str(odd.split('@')[1]).lower()
            proxy = str(odd.split('@')[1]).lower() + '://' + odd.split('@')[0]
            self.proxies.append({'proxy_scheme': proxy_scheme, "proxy": proxy})

    #验证IP
    def verify_proxies(self):
        # url = 'http://ip.42.pl/raw'
        for item in self.proxies:
            proxy = item['proxy']
            scheme = item['proxy_scheme']
            url = '%s://ip.42.pl/raw' % scheme
            # proxy_str = re.search('https*',str(proxy)).group() + '://' + re.search('\d*\d\.\d*\.\d*\.\d*\:\d*',str(proxy)).group()
            proxy_handler = urllib.request.ProxyHandler({scheme: proxy})
            openner = urllib.request.build_opener(proxy_handler)

            try:
                openner.open(url,timeout=2)
                request = urllib.request.Request(url,headers=self.headers)
                response = openner.open(request)
                if response.getcode() == 200:#判断响应码是否为200，成功请求
                    # print(response.read().decode('gbk'))
                    print(response.read().decode())
                    self.verify_pro.append({'proxy':proxy, 'proxy_scheme': scheme})
            except Exception as e:
                print(e)


    def write_proxies(self):
        self.verify_proxies()
        proxie = self.verify_pro
        with open('ip_list.json', 'w') as f:
                json.dump(proxie, f)
        print(self.verify_pro)

Proxies().write_proxies()


'''
#urllib库

from urllib import request

res = resquest.urlopen(url,headers)#发起请求，获取响应对象

html = res.read().decode()#响应对象方法read() --> bytes字节串

url = res.geturl()#响应对象方法geturl() -> 返回实际数据的url地址

code = res.getcode()#响应对象方法getcode() -> 返回HTTP响应码

# http://httpbin.org/get 获取请求头网站

# http://pv.sohu.com/cityjson 返回本机IP地址网站

# http://ip.42.pl/raw 返回本机IP地址网站

# http://icanhazip.com/ 返回本机ip地址
# https://icanhazip.com/ 返回本机ip地址

'''