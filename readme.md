## 二手房源分析

##  数据抓取
    
### 获取有效ip

xsdaili_getIP.py脚本文件实现了获取小舒代理每日免费ip列表，并写入到ip_list.json文件   

### scrapy爬虫

scrapy项目的setting配置：
```
CLOSESPIDER_ITEMCOUNT: 1000 # 最大爬取的数据为1000

```

### ip代理设置

在middleware中定义一个LianjiahouseRandomHttpProxyMiddleware的中间件用以设置请求代理  

### Spider: 
1. houseSpider: 规则爬虫二维爬取

定义两个Rule分别提取翻页的链接以及详情的链接，   
爬虫将根据这两个规则拿到的链接发起爬虫请求   

2. testSpider: 测试http代理中间件是否生效

### images图片下载

在pipelines文件中定义一个LianjiaImagePipeline的管道用以处理下载图片到本地，   
需要注意的是， 要先在setting 中 添加图片存储配置

```
# 图片存储配置
IMAGES_STORE = '/images'
IMAGES_URLS_FIELD = 'images_urls'
IMAGES_RESULT_FIELD = 'images'
```
### 数据存储

采用mongodb作为存储数据库。   
在pipelines文件中定义一个LianjiahousePipeline的管道用以处理数据库的连接，数据写入以及关闭，   
需要注意的是， 要先在setting 中添加数据库的设置   

```
# MongoDB配置信息
MONGO_URI = 'localhost:27017'
MONGO_DATABASE = 'lianjia'
```

- 数据分析