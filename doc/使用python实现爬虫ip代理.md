# 使用python实现爬虫ip代理

大家都知道我们可以去写爬虫去爬一些现成的网站，获取网站的数据据为已有，作为网站方，他们当然不必希望有人可以随意爬取他们的数据，但是不能不能直接把网站关停，让所有人都访问不了网站，所以网站会设定一些规则来判断这条访问请求是不是来自爬虫。<br />​

一个常用的命中是否是爬虫的策略是看一个ip下是否在大量并且有规律的访问网站页面。为了规避掉这条命中策略，编写爬虫程序的开发者，首先要做的就是做一个ip代理池，每次发送请求时就从ip代理迟里随机取一个。这样网站的所有者很难从一些不规律的访问记录来判断这条请求是不是来自爬虫。<br />​

要为我们的爬虫程序设置一个ip代理池主要分为两步

1. 获取大量有效的ip
1. 爬虫程序发起请求时需要从代理池中随机取一个ip代理

​<br />
<a name="G8OLk"></a>
## 获取ip代理
获取ip代理的方式主要有两种，如果想要可靠的稳定的ip，花点钱就可以了。有很多可以提供大量的ip代理的服务，有兴趣可以自己去了解下。<br />本文主要介绍的是第二种：爬取一些免费的代理ip。<br />以[小舒代理](http://www.xsdaili.cn/dayProxy/ip/2993.html)为例，这个网站每天都会提供一些可用的代理ip。但是大都不稳定，我们需要获取页面上所有的ip，然后遍历它们是否可用，如果可用的话就将它写入到文件。<br />​

新建get_ip.py文件，实现的代码如下：
```python
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


```
运行脚本
```python
python get_ip.py
```
这个脚本运行后可以看到我们项目下生成了ip_list.json文件，其中proxy字段是代理的ip，proxy_scheme字段是代理ip的类型。<br />![image.png](https://cdn.nlark.com/yuque/0/2021/png/638254/1625298249720-4a3305ca-b463-4483-9e83-5b5a33073e3b.png#clientId=u92e9f01c-3022-4&from=paste&height=393&id=ud3da22ef&margin=%5Bobject%20Object%5D&name=image.png&originHeight=786&originWidth=980&originalType=binary&ratio=1&size=106261&status=done&style=none&taskId=u52677de2-8e94-4d4d-a934-71a81c3345a&width=490)<br />

<a name="uiTgs"></a>
## 使用ip代理发起请求
使用ip代理发起请求时，需要区分发起的请求是http请求还是https的请求，我们构造一个proxy代理通常是一个数据字典，这个字段既有http对应的代理，又有https对应的代理。这个proxy代理通常如下：
```python
proxy = {
    'http': 'http://121.226.188.62:4264',
    'https': 'https://121.226.188.62:4264',
}
```
使用requests发起请求，只需要给请求设置proxies参数就可以了，将构造的proxy代理作为参数传给proxies发起请求，即设置了一个请求代理。<br />需要注意的是，如果proxy中没有设置对应的请求类型的ip的，这个请求还是会以本地的ip发起请求，即代理没有设置成功。所以有时候你看到请求发送成功也能正常相应，但是他可能代理没生效，依然使用本地的ip发起请求。这个时候检查下构造proxy中是否设置了对应的请求类型。<br />​

新建testproxy.py，具体的实现代码如下：
```python
import json
import random
import requests

proxy_list_file = 'iplist.json'

# 读取代理池中的文件，构造成[{'http':'http://121.226.188.62:4264'}]的形式
def generateProxy(file):
    proxies = []
    with open(file) as f:
        proxy_list = json.load(f)
        for proxy in proxy_list:
            scheme = proxy['proxy_scheme']
            url = proxy['proxy']
            proxies.append({scheme: url})

    return proxies
    
# 将代理ip列表分为http和https两部分，构造proxy。分别设置http代理和https代理（从对应的代理中随机取一个）
def getRandomProxy(proxies):
    http_list = list(filter(lambda d:list(d)[0] == 'http', proxies))
    https_list = list(filter(lambda d:list(d)[0] == 'https', proxies))
    proxy = {
        'http': random.choice(http_list)['http'] if len(http_list) else '',
        'https': random.choice(https_list)['https'] if len(https_list) else ''
    }
    return proxy

# 使用代理扽别发起http请求和https的请求，看看发起对应的请求时是否使用的对应的请求代理。
def validate(proxy):
    https_url = 'https://icanhazip.com/'
    http_url = 'http://icanhazip.com/'
    headers = {'User-Agent': 'curl/7.29.0'}
    print(f"当前使用代理：{proxy}")
    # print(f"当前使用代理：{proxy.values()}")
    try: 
        https_r = requests.get(https_url, headers=headers, proxies=proxy, timeout=30)
        print(f"访问https网站使用代理：{https_r.text}")
    except Exception:
        print('https请求失败')
    try: 
        http_r = requests.get(http_url, headers=headers, proxies=proxy, timeout=30)
        print(f"访问http网站使用代理：{http_r.text}")
    except Exception:
        print('http请求失败')

proxyList = generateProxy(proxy_list_file)
for i in range(10):
    proxy = getRandomProxy(proxyList)
    validate(proxy)
```
我们模拟发送请求10次，每一次都从ip代理池中随机取一个代理<br />运行这个文件
```python
python testproxy.py
```
从打印的信息中可以看出，发送http请求时使用的是proxy中的http代理，发送https请求时使用的是proxy中的https代理。代理设置成功！<br />![image.png](https://cdn.nlark.com/yuque/0/2021/png/638254/1625303149706-e732da11-0f71-4dd5-9f54-967e47bed3bb.png#clientId=ud66a6d49-9cf3-4&from=paste&height=459&id=u18b1694f&margin=%5Bobject%20Object%5D&name=image.png&originHeight=918&originWidth=2148&originalType=binary&ratio=1&size=335523&status=done&style=none&taskId=ua743c673-9368-4a38-9e12-af937880b08&width=1074)
