import json
import random
import requests

proxy_list_file = 'ip_list.json'

def generateProxy(file):
    proxies = []
    with open(file) as f:
        proxy_list = json.load(f)
        for proxy in proxy_list:
            scheme = proxy['proxy_scheme']
            url = proxy['proxy']
            proxies.append({scheme: url})

    return proxies
    
def getRandomProxy(proxies):
    http_list = list(filter(lambda d:list(d)[0] == 'http', proxies))
    https_list = list(filter(lambda d:list(d)[0] == 'https', proxies))
    proxy = {
        'http': random.choice(http_list)['http'] if len(http_list) else '',
        'https': random.choice(https_list)['https'] if len(https_list) else ''
    }
    return proxy

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