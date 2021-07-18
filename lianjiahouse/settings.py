# -*- coding: utf-8 -*-

# Scrapy settings for lianjiahouse project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'lianjiahouse'

SPIDER_MODULES = ['lianjiahouse.spiders']
NEWSPIDER_MODULE = 'lianjiahouse.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'lianjiahouse (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'lianjiahouse.middlewares.LianjiahouseSpiderMiddleware': 600,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#    'lianjiahouse.middlewares.LianjiahouseDownloaderMiddleware': 543,
    # 'lianjiahouse.middlewares.LianjiahouseRandomHttpProxyMiddleware': 543, 
    'lianjiahouse.middlewares.ProxyMiddleware': 543 # IP代理
    # 'lianjiahouse.middlewares.LianjiahouseSpiderMiddleware': 600, # 数据统计暂时没有生效，待调试
}

HTTPPROXY_PROXY_LIST_FILE = 'iplist.json'

PROXY_URL = 'http://127.0.0.1:5555/random'

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'lianjiahouse.pipelines.LianjiahouseDuplicatesPipeline': 200, # 去处重复项
    # 'lianjiahouse.pipelines.LianjiahousePipeline': 300, # mongodb数据存储
    # 'lianjiahouse.pipelines.LianjiaImagePipeline':400  # 图片下载
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# CLOSESPIDER_ITEMCOUNT = 1000
HTTPERROR_ALLOWED_CODES = [301]
# 图片存储配置
IMAGES_STORE = './images/'
IMAGES_URLS_FIELD = 'images_urls'
IMAGES_RESULT_FIELD = 'images'

# MongoDB配置信息
MONGO_URI = '1.15.237.241:27017'
MONGO_DATABASE = 'lianjia'

# FEED_URI = 'export_data/%(name)s.data' # 导出文件路径
# FEED_FORMAT = 'csv' # 导出文件格式
# FEED_EXPORTER_ENCODING = 'utf-8' # 导出文件编码（默认情况下json文件使用数字编码，其他使用utf-8编码）
# FEED_EXPORTERS = {
#     'excel': 'lianjiahouse.my_exporters.ExcelItemExporter'
# }
