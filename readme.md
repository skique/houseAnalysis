## 二手房源分析

##  数据抓取
    
### 获取有效ip

xsdaili_getIP.py脚本文件实现了获取小舒代理每日免费ip列表，并写入到ip_list.json文件   
### Spider: 
1. houseSpider: 规则爬虫二维爬取

定义两个Rule分别提取翻页的链接以及详情的链接，   
爬虫将根据这两个规则拿到的链接发起爬虫请求   

2. testSpider: 测试http代理中间件是否生效

### middlewaves

#### ip代理设置

在middleware中定义一个 LianjiahouseRandomHttpProxyMiddleware 的中间件用以设置请求代理   
具体代码见 LianjiahouseRandomHttpProxyMiddleware 类的实现

#### 添加统计信息

在middleware中定义一个 LianjiahouseSpiderMiddleware 的中间件用以对抓取的数据进行初步的统计，即对相同小区的数量进行统计。   
具体代码见 LianjiahouseSpiderMiddleware 类的实现   
利用Scrapy提供的统计数据收集功能，以key/value方式，可以方便地统计一些特殊信息，   
Scrapy提供的这种收集数据机制叫作Stats Collection。   
数据收集器对每个Spider保持一个状态表。当Spider启动时，该表自动打开；当Spider关闭时，该表自动关闭。   
> stats 属性有以下属性值可以配置。
```
stats.set_value('key', value) # 设置数据
stats.inc_value('key') # 增加数据值
stats.max_value('key', value) # 当新的值比原来大时设置值
stats.min_value('key', value) # 当新的值比原来小时设置值
stats.get_value('key') # 获取数据
stats.get_stats() # 获取所有数据
```

### pipelines

#### 过滤重复项

在pipelines文件中定义一个 LianjiahouseDuplicatesPipeline 的管道用以过滤重复的item。   
处理流程：   
init时初始化一个set集合   
在process_item的钩子函数中去处item的house_name字段，判断该字段是否在集合中，   
如果不在集合中， 则向集合插入该item，否则丢弃掉该item。        
具体代码见 LianjiahouseDuplicatesPipeline 类的实现   

#### images图片下载

在pipelines文件中定义一个 LianjiaImagePipeline 的管道用以处理下载图片到本地，   
需要注意的是， 要先在setting 中 添加图片存储配置   

```
# 图片存储配置
IMAGES_STORE = '/images'
IMAGES_URLS_FIELD = 'images_urls'
IMAGES_RESULT_FIELD = 'images'
```

具体代码见 LianjiaImagePipeline 类的实现
#### 数据存储

采用mongodb作为存储数据库。   
在pipelines文件中定义一个 LianjiahousePipeline 的管道用以处理数据库的连接，数据写入以及关闭，   
需要注意的是， 要先在setting 中添加数据库的设置   

```
# MongoDB配置信息
MONGO_URI = 'localhost:27017'
MONGO_DATABASE = 'lianjia'
```

具体代码见 LianjiahousePipeline 类的实现   

#### 文件写入


### scrapy爬虫设置

scrapy项目的setting配置文件中需要把对应的middlewaves和pipelines激活。配置以键值对的形式，键为对应的中间件或管道对应的类名，值为执行顺序，order小的先执行。

额外的setting设置：
```
CLOSESPIDER_ITEMCOUNT: 1000 # 最大爬取的数据为1000

```


## 数据分析