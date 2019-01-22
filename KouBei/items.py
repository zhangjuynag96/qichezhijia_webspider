# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field

class AutohomeKoubeiViewItem(Item):
    collection = table =  'detail'

    actual_battery_consumption = Field()  #百公里耗电
    actual_oil_consumption = Field()   #百公里耗油
    apperance = Field()    #车辆外观评分
    boughtcityname = Field()    #车辆购买城市
    bought_city = Field()
    bought_date = Field()        #购买时间
    bought_place = Field()
    bought_province = Field()
    carownerlevels = Field()
    comfortableness = Field()     #舒适度评分
    commentcount = Field()
    consumption = Field()     #车辆油耗评分
    cost_efficient = Field()   #车辆性价比评分
    created = Field()    #创建评论时间
    driven_kilometers = Field()        #行驶公里数
    feeling = Field()     #评价内容
    feeling_summary = Field()    #评价总结
    helpfulcount = Field()
    interior = Field()    #内饰评分
    last_edit = Field()     #最后一次评论时间
    maneuverability = Field()    #车辆操作评分
    nickname = Field()     #评论人昵称
    power = Field()     #动力评分
    price = Field()     #购买价格
    seriesid = Field()    #车辆型号id
    showid = Field()    #此条评论id
    space = Field()     #空间评分
    specname = Field()    #车辆配置
    specid = Field()
    userid = Field()    #评论人id
    visitcount = Field()     #此评论访问数
    brandname = Field()    #汽车归属公司
    seriesname = Field()    #汽车型号
