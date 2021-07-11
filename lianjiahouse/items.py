# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ZufangItem(scrapy.Item):
    # 标签  小区  户型   面积   关注人数  观看人数  发布时间  价格   均价  详情链接  经纬度 城区
    # 标签
    title = scrapy.Field()
    # 小区
    community = scrapy.Field()
    # 房间信息
    houseInfo = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 户型
    layout = scrapy.Field()
    # 朝向
    direction = scrapy.Field()
    # 发布时间
    time = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 详情链接
    link = scrapy.Field()
    # 城区
    city = scrapy.Field()
    # 经度
    lat = scrapy.Field()
    # 纬度
    lng = scrapy.Field()
    # 距离
    distance = scrapy.Field()
    # 是否是广告
    advertisement = scrapy.Field()
    # 爬取的url
    url = scrapy.Field()

class LianjiaItem(scrapy.Item):
    # 标签  小区  户型   面积   关注人数  观看人数  发布时间  价格   均价  详情链接  经纬度 城区
    # 标签
    title = scrapy.Field()
    # 小区
    community = scrapy.Field()
    # 房间信息
    houseInfo = scrapy.Field()
    # 户型
    model = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 关注人数
    focus_num = scrapy.Field()
    # 观看人数
    watch_num = scrapy.Field()
    # 发布时间
    time = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 均价
    average_price = scrapy.Field()
    # 详情链接
    link = scrapy.Field()
    # 城区
    city = scrapy.Field() 
    # 经纬度
    Latitude = scrapy.Field() 
class LianjiahouseItem(LianjiaItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 发布信息名称
    house_name = scrapy.Field()
    # 小区名称
    community_name = scrapy.Field()
    # 所在区域
    location = scrapy.Field()
    # 链家编号
    house_record = scrapy.Field()
    # 总售价
    total_amount = scrapy.Field()
    # 单价
    unit_price = scrapy.Field()
    # 房屋基本信息
    # 建筑面积
    area_total = scrapy.Field()
    # 套内面积
    area_use = scrapy.Field()
    # 厅室户型
    house_type = scrapy.Field()
    # 朝向
    direction = scrapy.Field()
    # 装修情况
    sub_info = scrapy.Field()
    # 供暖方式
    # heating_method = scrapy.Field()
    # 产权
    # house_property = scrapy.Field()
    # 楼层
    floor = scrapy.Field()
    # 总层高
    total_floors = scrapy.Field()
    # 电梯
    is_left = scrapy.Field()
    # 户梯比例
    left_rate = scrapy.Field()
    # 户型结构
    structure = scrapy.Field()
    # 房屋交易信息
    # 挂牌时间
    release_date = scrapy.Field()
    # 上次交易时间
    last_trade_time = scrapy.Field()
    # 房屋使用年限
    house_years = scrapy.Field()
    # 房屋抵押信息
    pawn = scrapy.Field()
    # 交易权属
    trade_property = scrapy.Field()
    # 房屋用途
    house_usage = scrapy.Field()
    # 产权所有
    property_own = scrapy.Field()
    # 图片地址
    images_urls = scrapy.Field()
    # 保存图片
    # images = scrapy.Field()
